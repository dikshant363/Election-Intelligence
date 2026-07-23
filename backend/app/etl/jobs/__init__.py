"""ETL job definitions: pre-configured pipeline jobs for election data types."""

from __future__ import annotations

from dataclasses import dataclass

from app.etl.connectors import FileConnector, HttpConnector
from app.etl.parsers import CsvParser, ExcelParser, GeoJsonParser, JsonParser
from app.etl.pipeline import PipelineConfig
from app.etl.transformers import (
    CANDIDATE_DATASET_TRANSFORMER,
    ELECTION_DATASET_TRANSFORMER,
)
from app.etl.validators import BatchValidator, FieldRule


def _election_result_rules() -> list[FieldRule]:
    return [
        FieldRule(name="election_id", required=True, field_type=str, max_length=50),
        FieldRule(name="constituency_code", required=True, field_type=str, max_length=10),
        FieldRule(name="candidate_name", required=True, field_type=str, max_length=200),
        FieldRule(name="party_code", required=True, field_type=str, max_length=20),
        FieldRule(name="votes_cast", required=True, field_type=int, min_value=0),
    ]


def _candidate_rules() -> list[FieldRule]:
    return [
        FieldRule(name="candidate_id", required=True, field_type=str, max_length=50),
        FieldRule(name="full_name", required=True, field_type=str, max_length=200),
        FieldRule(name="party_code", required=True, field_type=str, max_length=20),
        FieldRule(name="constituency_code", required=True, field_type=str, max_length=10),
        FieldRule(name="state", required=True, field_type=str, max_length=60),
    ]


def _polling_booth_rules() -> list[FieldRule]:
    return [
        FieldRule(name="booth_id", required=True, field_type=str, max_length=50),
        FieldRule(name="booth_name", required=True, field_type=str, max_length=200),
        FieldRule(name="constituency_code", required=True, field_type=str, max_length=10),
        FieldRule(name="state", required=True, field_type=str, max_length=60),
    ]


@dataclass
class HttpJobConfig:
    """Parameters for the HttpJsonJob factory."""

    url: str
    rules: list[FieldRule]
    job_name: str = "http_json_import"
    headers: dict[str, str] | None = None
    initiated_by: str | None = None
    chunk_size: int = 1000


class ElectionResultCSVJob:
    """Pre-configured job to import election results from a CSV file."""

    @staticmethod
    def make_config(
        file_path: str,
        initiated_by: str | None = None,
        chunk_size: int = 1000,
    ) -> PipelineConfig:
        return PipelineConfig(
            job_name="election_results_csv",
            source_uri=file_path,
            connector=FileConnector(file_path),
            parser=CsvParser(),
            validator=BatchValidator(
                rules=_election_result_rules(),
                duplicate_key_fields=["election_id", "constituency_code", "candidate_name"],
            ),
            transformer=ELECTION_DATASET_TRANSFORMER,
            chunk_size=chunk_size,
            initiated_by=initiated_by,
        )


class CandidateExcelJob:
    """Pre-configured job to import candidates from an Excel file."""

    @staticmethod
    def make_config(
        file_path: str,
        sheet_name: str | int = 0,
        initiated_by: str | None = None,
        chunk_size: int = 1000,
    ) -> PipelineConfig:
        return PipelineConfig(
            job_name="candidates_excel",
            source_uri=file_path,
            connector=FileConnector(file_path),
            parser=ExcelParser(sheet_name=sheet_name),
            validator=BatchValidator(
                rules=_candidate_rules(),
                duplicate_key_fields=["candidate_id"],
            ),
            transformer=CANDIDATE_DATASET_TRANSFORMER,
            chunk_size=chunk_size,
            initiated_by=initiated_by,
        )


class PollingBoothGeoJsonJob:
    """Pre-configured job to import polling booth locations from GeoJSON."""

    @staticmethod
    def make_config(
        file_path: str,
        initiated_by: str | None = None,
        chunk_size: int = 500,
    ) -> PipelineConfig:
        return PipelineConfig(
            job_name="polling_booths_geojson",
            source_uri=file_path,
            connector=FileConnector(file_path),
            parser=GeoJsonParser(),
            validator=BatchValidator(
                rules=_polling_booth_rules(),
                duplicate_key_fields=["booth_id"],
                geo_config=("latitude", "longitude"),
            ),
            transformer=ELECTION_DATASET_TRANSFORMER,
            chunk_size=chunk_size,
            initiated_by=initiated_by,
        )


class HttpJsonJob:
    """Generic job to import JSON data from an HTTP endpoint."""

    @staticmethod
    def make_config(cfg: HttpJobConfig) -> PipelineConfig:
        return PipelineConfig(
            job_name=cfg.job_name,
            source_uri=cfg.url,
            connector=HttpConnector(cfg.url, headers=cfg.headers),
            parser=JsonParser(),
            validator=BatchValidator(rules=cfg.rules),
            transformer=ELECTION_DATASET_TRANSFORMER,
            chunk_size=cfg.chunk_size,
            initiated_by=cfg.initiated_by,
        )
