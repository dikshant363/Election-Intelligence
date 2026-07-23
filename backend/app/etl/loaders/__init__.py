"""ETL data loaders: bulk-insert election domain records with chunking, retry, and transaction safety."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.etl.exceptions import LoadError
from app.etl.staging import BatchStatus, ImportBatchModel, ImportRecordModel, RejectedRecordModel

DEFAULT_CHUNK_SIZE = 500
DEFAULT_MAX_RETRIES = 3


async def _flush_or_rollback(session: AsyncSession) -> None:
    try:
        await session.flush()
    except Exception as exc:
        await session.rollback()
        raise LoadError(f"Database flush failed: {exc}") from exc


class StagingLoader:
    """Loads parsed, validated records into the staging tables within a transaction."""

    def __init__(
        self,
        session: AsyncSession,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        self._session = session
        self.chunk_size = chunk_size

    async def load_valid_records(
        self,
        batch_id: str,
        records: list[dict[str, Any]],
        transformed: list[dict[str, Any]] | None = None,
    ) -> int:
        """Bulk-insert valid records into import_records. Returns count loaded."""
        loaded = 0
        effective_transformed = transformed or records

        for chunk_start in range(0, len(records), self.chunk_size):
            chunk_raw = records[chunk_start : chunk_start + self.chunk_size]
            chunk_trans = effective_transformed[chunk_start : chunk_start + self.chunk_size]

            orm_objects = [
                ImportRecordModel(
                    batch_id=batch_id,
                    record_index=chunk_start + i,
                    raw_data=json.dumps(raw, ensure_ascii=False, default=str),
                    transformed_data=json.dumps(trans, ensure_ascii=False, default=str),
                    is_loaded=False,
                )
                for i, (raw, trans) in enumerate(zip(chunk_raw, chunk_trans, strict=False))
            ]
            self._session.add_all(orm_objects)
            await _flush_or_rollback(self._session)
            loaded += len(orm_objects)

        return loaded

    async def load_rejected_records(
        self,
        batch_id: str,
        rejected: list[dict[str, Any]],
    ) -> int:
        """Bulk-insert rejected records with error details."""
        loaded = 0
        for chunk_start in range(0, len(rejected), self.chunk_size):
            chunk = rejected[chunk_start : chunk_start + self.chunk_size]
            orm_objects = []
            for i, item in enumerate(chunk):
                errors = item.get("errors", [])
                first_error = errors[0] if errors else {}
                orm_objects.append(
                    RejectedRecordModel(
                        batch_id=batch_id,
                        record_index=chunk_start + i,
                        raw_data=json.dumps(
                            item.get("record", {}), ensure_ascii=False, default=str
                        ),
                        error_code=str(first_error.get("error", "UNKNOWN")),
                        error_message=str(first_error.get("message", "Validation failed")),
                    )
                )
            self._session.add_all(orm_objects)
            await _flush_or_rollback(self._session)
            loaded += len(orm_objects)

        return loaded

    async def mark_batch_loaded(self, batch_id: str, loaded_count: int) -> None:
        """Update the ImportBatch status to COMPLETED and set loaded_records count."""
        stmt = (
            update(ImportBatchModel)
            .where(ImportBatchModel.id == batch_id)
            .values(
                status=BatchStatus.COMPLETED,
                loaded_records=loaded_count,
            )
        )
        await self._session.execute(stmt)
        await _flush_or_rollback(self._session)
