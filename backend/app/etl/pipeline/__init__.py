"""ETL Pipeline: orchestrates Connector → Parser → Validator → Transformer → Loader."""

from __future__ import annotations

import contextlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.etl.connectors import SourceConnector
from app.etl.exceptions import ETLException
from app.etl.loaders import StagingLoader
from app.etl.parsers import DataParser
from app.etl.staging import BatchStatus, ImportBatchModel, TransformationLogModel
from app.etl.tracking import JobProgress, JobRegistry, job_registry
from app.etl.transformers import RecordTransformer
from app.etl.validators import BatchValidator


@dataclass
class PipelineConfig:
    """Configuration for a single ETL pipeline run."""

    job_name: str
    source_uri: str
    connector: SourceConnector
    parser: DataParser
    validator: BatchValidator
    transformer: RecordTransformer | None = None
    chunk_size: int = 1000
    initiated_by: str | None = None


class ETLPipeline:
    """
    Orchestrates the full ETL lifecycle:
    Fetch → Parse → Validate → Transform → Stage → Load
    """

    def __init__(
        self,
        session: AsyncSession,
        config: PipelineConfig,
        registry: JobRegistry | None = None,
    ) -> None:
        self._session = session
        self.config = config
        self._registry = registry or job_registry
        self._loader = StagingLoader(session, chunk_size=config.chunk_size)

    async def _fetch_phase(
        self, progress: JobProgress, batch: ImportBatchModel
    ) -> bytes:
        """Phase 1: Fetch raw bytes from source and record checksum."""
        progress.log("Fetching data from source connector...")
        raw_bytes = await self.config.connector.fetch()
        checksum = self.config.connector.checksum(raw_bytes)
        batch.source_checksum = checksum
        await self._session.flush()
        progress.log(f"Fetched {len(raw_bytes):,} bytes (sha256={checksum[:16]}...)")
        return raw_bytes

    async def _parse_phase(
        self, progress: JobProgress, batch: ImportBatchModel, raw_bytes: bytes
    ) -> list[dict[str, Any]]:
        """Phase 2: Parse raw bytes into structured records (streaming chunked)."""
        progress.log("Parsing records...")
        all_records: list[dict[str, Any]] = []
        for chunk in self.config.parser.parse_chunked(raw_bytes, self.config.chunk_size):
            all_records.extend(chunk)
            progress.parsed_records += len(chunk)
        progress.total_records = len(all_records)
        batch.total_records = len(all_records)
        await self._session.flush()
        progress.log(f"Parsed {len(all_records):,} records")
        return all_records

    async def _validate_phase(
        self,
        progress: JobProgress,
        batch: ImportBatchModel,
        all_records: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Phase 3: Validate records and separate valid from rejected."""
        progress.log("Validating records...")
        batch.status = BatchStatus.VALIDATING
        await self._session.flush()
        valid, rejected, report = self.config.validator.validate_batch(all_records)
        progress.valid_records = report.valid_records
        progress.rejected_records = report.invalid_records
        batch.valid_records = report.valid_records
        batch.rejected_records = report.invalid_records
        await self._session.flush()
        progress.log(
            f"Validation: {report.valid_records} valid, "
            f"{report.invalid_records} rejected ({report.error_rate:.1%} error rate)"
        )
        return valid, rejected

    async def _transform_phase(
        self,
        progress: JobProgress,
        batch: ImportBatchModel,
        valid: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Phase 4: Apply optional field-level transformations."""
        if not self.config.transformer:
            return valid
        progress.log("Applying transformations...")
        batch.status = BatchStatus.TRANSFORMING
        await self._session.flush()
        transformed = self.config.transformer.transform_batch(valid)
        log_entry = TransformationLogModel(
            batch_id=batch.id,
            transformer_name=self.config.transformer.__class__.__name__,
            fields_transformed=json.dumps(
                list(self.config.transformer.field_transforms.keys())
            ),
            records_affected=len(transformed),
        )
        self._session.add(log_entry)
        await self._session.flush()
        progress.log(f"Transformed {len(transformed):,} records")
        return transformed

    async def _load_phase(
        self,
        progress: JobProgress,
        batch: ImportBatchModel,
        valid: list[dict[str, Any]],
        transformed: list[dict[str, Any]],
        rejected: list[dict[str, Any]],
    ) -> None:
        """Phase 5: Bulk-insert valid and rejected records into staging tables."""
        progress.log("Loading to staging tables...")
        batch.status = BatchStatus.LOADING
        await self._session.flush()
        batch_id = str(batch.id)
        loaded = await self._loader.load_valid_records(batch_id, valid, transformed)
        if rejected:
            await self._loader.load_rejected_records(batch_id, rejected)
        progress.loaded_records = loaded
        await self._loader.mark_batch_loaded(batch_id, loaded)
        await self._session.commit()
        progress.log(f"Loaded {loaded:,} records to staging")

    async def run(self) -> JobProgress:
        """Execute the full ETL pipeline. Returns final JobProgress."""
        progress = self._registry.register(self.config.job_name)
        progress.start()
        progress.log(f"Starting pipeline '{self.config.job_name}'")

        batch = ImportBatchModel(
            job_name=self.config.job_name,
            source_uri=self.config.source_uri,
            format="auto",
            status=BatchStatus.RUNNING,
            initiated_by=self.config.initiated_by,
            started_at=datetime.now(UTC),
        )
        self._session.add(batch)
        await self._session.flush()

        try:
            raw_bytes = await self._fetch_phase(progress, batch)
            all_records = await self._parse_phase(progress, batch, raw_bytes)
            valid, rejected = await self._validate_phase(progress, batch, all_records)
            transformed = await self._transform_phase(progress, batch, valid)
            await self._load_phase(progress, batch, valid, transformed, rejected)
            progress.complete()
            progress.log("Pipeline completed successfully")

        except ETLException as exc:
            await self._session.rollback()
            batch.status = BatchStatus.FAILED
            batch.error_message = exc.message
            with contextlib.suppress(Exception):
                await self._session.commit()
            progress.fail(exc.message)
            progress.log(f"Pipeline FAILED: {exc.message}")

        except Exception as exc:
            await self._session.rollback()
            progress.fail(str(exc))
            progress.log(f"Pipeline FAILED with unexpected error: {exc}")

        return progress
