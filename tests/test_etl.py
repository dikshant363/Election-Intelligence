"""
Comprehensive test suite for Milestone 17 — ETL Data Ingestion Platform.

Coverage:
- Parsers: CSV, Excel, JSON, GeoJSON, Parquet
- Connectors: File, HTTP stub, ZIP
- Validators: field rules, duplicate detection, geographic, batch
- Transformers: state, date, party code, constituency code, coordinates
- Tracking: JobProgress, JobRegistry
- Exports: CSV, JSON, Parquet, GeoJSON
- Exceptions hierarchy
- Pipeline: end-to-end integration (mocked DB)
"""

from __future__ import annotations

import csv
import io
import json
import uuid
import zipfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from app.etl.connectors import FileConnector, ZipConnector
from app.etl.exceptions import (
    ConnectorError,
    ETLException,
    LoadError,
    ParseError,
    ValidationError,
)
from app.etl.exports import (
    CsvExporter,
    GeoJsonExporter,
    JsonExporter,
    ParquetExporter,
    export_records,
)
from app.etl.parsers import (
    CsvParser,
    ExcelParser,
    GeoJsonParser,
    JsonParser,
    ParquetParser,
    ZipParser,
    get_parser_for_extension,
)
from app.etl.pipeline import ETLPipeline, PipelineConfig
from app.etl.tracking import JobProgress, JobRegistry, JobStatus
from app.etl.transformers import (
    CANDIDATE_DATASET_TRANSFORMER,
    ELECTION_DATASET_TRANSFORMER,
    RecordTransformer,
    normalize_constituency_code,
    normalize_coordinates,
    normalize_date,
    normalize_election_type,
    normalize_party_code,
    normalize_state,
)
from app.etl.validators import (
    BatchValidator,
    DuplicateDetector,
    FieldRule,
    GeographicValidator,
    RecordValidator,
    ValidationReport,
)

# Constants for comparison (to satisfy PLR2004)
EXPECTED_ROWS_SMALL = 2
EXPECTED_ROWS_MEDIUM = 3
EXPECTED_ROWS_FIFTY = 50
EXPECTED_ROWS_CHUNKED_A = 100
EXPECTED_ROWS_CHUNKED_B = 50
EXPECTED_ROWS_PARQUET = 3
CHECKSUM_HEX_LENGTH = 64
EXPECTED_CHUNK_COUNT = 3
PIPELINE_TOTAL = 3
PIPELINE_VALID_ALL = 3
PIPELINE_VALID_TWO = 2
PIPELINE_REJECTED_ONE = 1
PROGRESS_PCT_HALF = 50.0


# ─────────────────────────────────────────────────────────────────────────────
# EXCEPTION HIERARCHY
# ─────────────────────────────────────────────────────────────────────────────


class TestExceptions:
    def test_base_exception(self) -> None:
        exc = ETLException("base error", code="BASE")
        assert exc.message == "base error"
        assert exc.code == "BASE"
        assert str(exc) == "base error"

    def test_connector_error(self) -> None:
        exc = ConnectorError("timeout")
        assert exc.code == "CONNECTOR_ERROR"
        assert isinstance(exc, ETLException)

    def test_parse_error(self) -> None:
        exc = ParseError("bad csv")
        assert exc.code == "PARSE_ERROR"

    def test_validation_error(self) -> None:
        exc = ValidationError("field missing")
        assert exc.code == "VALIDATION_ERROR"

    def test_load_error(self) -> None:
        exc = LoadError("db down")
        assert exc.code == "LOAD_ERROR"


# ─────────────────────────────────────────────────────────────────────────────
# CONNECTORS
# ─────────────────────────────────────────────────────────────────────────────


class TestFileConnector:
    @pytest.mark.asyncio
    async def test_fetch_existing_file(self, tmp_path: Path) -> None:
        f = tmp_path / "data.csv"
        f.write_bytes(b"a,b\n1,2\n")
        connector = FileConnector(f)
        data = await connector.fetch()
        assert data == b"a,b\n1,2\n"

    @pytest.mark.asyncio
    async def test_fetch_missing_file_raises(self, tmp_path: Path) -> None:
        connector = FileConnector(tmp_path / "missing.csv")
        with pytest.raises(ConnectorError, match="File not found"):
            await connector.fetch()

    def test_checksum_consistent(self) -> None:
        connector = FileConnector("/dev/null")
        assert connector.checksum(b"hello") == connector.checksum(b"hello")
        assert len(connector.checksum(b"hello")) == CHECKSUM_HEX_LENGTH


class TestZipConnector:
    @pytest.mark.asyncio
    async def test_fetch_member_from_zip(self, tmp_path: Path) -> None:
        zf_path = tmp_path / "archive.zip"
        with zipfile.ZipFile(zf_path, "w") as zf:
            zf.writestr("data.csv", "col1,col2\nval1,val2\n")
        connector = ZipConnector(zf_path, "data.csv")
        data = await connector.fetch()
        assert b"col1" in data

    @pytest.mark.asyncio
    async def test_missing_member_raises(self, tmp_path: Path) -> None:
        zf_path = tmp_path / "archive.zip"
        with zipfile.ZipFile(zf_path, "w") as zf:
            zf.writestr("other.csv", "x,y\n")
        connector = ZipConnector(zf_path, "data.csv")
        with pytest.raises(ConnectorError, match="not found in ZIP"):
            await connector.fetch()


# ─────────────────────────────────────────────────────────────────────────────
# PARSERS
# ─────────────────────────────────────────────────────────────────────────────


def _make_csv_bytes(rows: list[dict]) -> bytes:
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
    return out.getvalue().encode()


class TestCsvParser:
    def test_parses_basic_csv(self) -> None:
        data = _make_csv_bytes([{"name": "Alice", "votes": "100"}])
        records = CsvParser().parse(data)
        assert len(records) == 1
        assert records[0]["name"] == "Alice"

    def test_parses_multiple_rows(self) -> None:
        rows = [{"a": str(i), "b": str(i * 2)} for i in range(EXPECTED_ROWS_FIFTY)]
        data = _make_csv_bytes(rows)
        records = CsvParser().parse(data)
        assert len(records) == EXPECTED_ROWS_FIFTY

    def test_chunked_parsing(self) -> None:
        rows = [{"x": str(i)} for i in range(250)]
        data = _make_csv_bytes(rows)
        chunks = list(CsvParser().parse_chunked(data, chunk_size=EXPECTED_ROWS_CHUNKED_A))
        assert len(chunks) == EXPECTED_CHUNK_COUNT
        assert len(chunks[0]) == EXPECTED_ROWS_CHUNKED_A
        assert len(chunks[2]) == EXPECTED_ROWS_CHUNKED_B

    def test_empty_csv_returns_empty_list(self) -> None:
        records = CsvParser().parse(b"name,votes\n")
        assert records == []

    def test_tab_delimited_csv(self) -> None:
        data = b"col1\tcol2\nval1\tval2\n"
        records = CsvParser(delimiter="\t").parse(data)
        assert records[0]["col1"] == "val1"


class TestJsonParser:
    def test_parses_array(self) -> None:
        data = json.dumps([{"a": 1}, {"a": 2}]).encode()
        records = JsonParser().parse(data)
        assert len(records) == EXPECTED_ROWS_SMALL

    def test_parses_envelope_dict(self) -> None:
        data = json.dumps({"data": [{"x": 1}]}).encode()
        records = JsonParser().parse(data)
        assert records[0]["x"] == 1

    def test_parses_json_lines(self) -> None:
        data = b'{"id": 1}\n{"id": 2}\n{"id": 3}\n'
        records = JsonParser(json_lines=True).parse(data)
        assert len(records) == EXPECTED_ROWS_MEDIUM

    def test_invalid_json_raises(self) -> None:
        with pytest.raises(ParseError, match="JSON parse failure"):
            JsonParser().parse(b"not json")


class TestGeoJsonParser:
    def test_parses_feature_collection(self) -> None:
        geo = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [77.5, 12.9]},
                    "properties": {"booth_id": "B001", "name": "Booth 1"},
                }
            ],
        }
        records = GeoJsonParser().parse(json.dumps(geo).encode())
        assert len(records) == 1
        assert records[0]["booth_id"] == "B001"
        assert records[0]["_geometry_type"] == "Point"

    def test_non_feature_collection_raises(self) -> None:
        with pytest.raises(ParseError, match="FeatureCollection"):
            GeoJsonParser().parse(json.dumps({"type": "Feature"}).encode())


class TestParquetParser:
    def test_parses_parquet_bytes(self) -> None:
        table = pa.Table.from_pydict({"id": [1, 2, 3], "name": ["a", "b", "c"]})
        buf = io.BytesIO()
        pq.write_table(table, buf)
        records = ParquetParser().parse(buf.getvalue())
        assert len(records) == EXPECTED_ROWS_PARQUET
        assert records[0]["id"] == 1

    def test_invalid_parquet_raises(self) -> None:
        with pytest.raises(ParseError, match="Parquet parse failure"):
            ParquetParser().parse(b"not parquet data")


class TestZipParser:
    def test_parses_csv_from_zip(self) -> None:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("data.csv", "a,b\n1,2\n3,4\n")
        records = ZipParser().parse(buf.getvalue())
        assert len(records) == EXPECTED_ROWS_SMALL

    def test_no_supported_member_raises(self) -> None:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("data.txt", "hello")
        with pytest.raises(ParseError, match="No supported file"):
            ZipParser().parse(buf.getvalue())


class TestGetParserForExtension:
    def test_csv(self) -> None:
        assert isinstance(get_parser_for_extension("data.csv"), CsvParser)

    def test_json(self) -> None:
        assert isinstance(get_parser_for_extension("records.json"), JsonParser)

    def test_geojson(self) -> None:
        assert isinstance(get_parser_for_extension("booths.geojson"), GeoJsonParser)

    def test_parquet(self) -> None:
        assert isinstance(get_parser_for_extension("results.parquet"), ParquetParser)

    def test_xlsx(self) -> None:
        assert isinstance(get_parser_for_extension("sheet.xlsx"), ExcelParser)

    def test_zip(self) -> None:
        assert isinstance(get_parser_for_extension("archive.zip"), ZipParser)

    def test_unknown_extension_raises(self) -> None:
        with pytest.raises(ParseError, match="Unsupported file extension"):
            get_parser_for_extension("data.pdf")


# ─────────────────────────────────────────────────────────────────────────────
# TRANSFORMERS
# ─────────────────────────────────────────────────────────────────────────────


class TestNormalizeFunctions:
    def test_normalize_state_alias(self) -> None:
        assert normalize_state("ap") == "Andhra Pradesh"
        assert normalize_state("Andhra Pradesh") == "Andhra Pradesh"
        assert normalize_state("Orissa") == "Odisha"
        assert normalize_state("wb") == "West Bengal"

    def test_normalize_state_unknown(self) -> None:
        result = normalize_state("unknown state")
        assert result == "Unknown State"

    def test_normalize_election_type(self) -> None:
        assert normalize_election_type("ls") == "Lok Sabha"
        assert normalize_election_type("bypolls") == "By-Election"
        assert normalize_election_type("vidhan sabha") == "State Assembly"

    def test_normalize_date_iso(self) -> None:
        assert normalize_date("2024-05-01") == "2024-05-01"

    def test_normalize_date_indian_format(self) -> None:
        assert normalize_date("15/11/2024") == "2024-11-15"

    def test_normalize_date_invalid(self) -> None:
        assert normalize_date("not-a-date") is None

    def test_normalize_date_empty(self) -> None:
        assert normalize_date("") is None

    def test_normalize_party_code(self) -> None:
        assert normalize_party_code("  bjp ") == "BJP"
        assert normalize_party_code("Indian National Congress") == "INDIANNATIONALCONGRESS"

    def test_normalize_constituency_code_numeric(self) -> None:
        assert normalize_constituency_code("7") == "007"
        assert normalize_constituency_code("42") == "042"
        assert normalize_constituency_code("100") == "100"

    def test_normalize_constituency_code_alpha(self) -> None:
        assert normalize_constituency_code("AC-01") == "AC01"

    def test_normalize_coordinates_valid(self) -> None:
        assert normalize_coordinates("12.9716") == pytest.approx(12.9716)

    def test_normalize_coordinates_invalid(self) -> None:
        assert normalize_coordinates("not-a-float") is None


class TestRecordTransformer:
    def test_transforms_fields(self) -> None:
        transformer = RecordTransformer(
            field_transforms={"state": normalize_state, "party_code": normalize_party_code}
        )
        record = {"state": "ap", "party_code": "  bjp  ", "votes": "100"}
        result = transformer.transform(record)
        assert result["state"] == "Andhra Pradesh"
        assert result["party_code"] == "BJP"
        assert result["votes"] == "100"  # unchanged

    def test_transform_batch(self) -> None:
        transformer = RecordTransformer({"state": normalize_state})
        records = [{"state": "ap"}, {"state": "goa"}, {"state": "wb"}]
        results = transformer.transform_batch(records)
        assert results[0]["state"] == "Andhra Pradesh"
        assert results[1]["state"] == "Goa"
        assert results[2]["state"] == "West Bengal"

    def test_transform_preserves_on_error(self) -> None:
        def bad_fn(x: str) -> str:
            raise ValueError("boom")

        transformer = RecordTransformer({"field": bad_fn})
        record = {"field": "original"}
        result = transformer.transform(record)
        assert result["field"] == "original"  # preserved

    def test_election_dataset_transformer(self) -> None:
        record = {"state": "up", "party_code": "sp", "constituency_code": "5"}
        result = ELECTION_DATASET_TRANSFORMER.transform(record)
        assert result["state"] == "Uttar Pradesh"
        assert result["party_code"] == "SP"
        assert result["constituency_code"] == "005"

    def test_candidate_dataset_transformer(self) -> None:
        record = {
            "state": "tn",
            "party_code": " dmk ",
            "constituency_code": "12",
            "dob": "01/01/1980",
        }
        result = CANDIDATE_DATASET_TRANSFORMER.transform(record)
        assert result["state"] == "Tamil Nadu"
        assert result["party_code"] == "DMK"
        assert result["dob"] == "1980-01-01"


# ─────────────────────────────────────────────────────────────────────────────
# VALIDATORS
# ─────────────────────────────────────────────────────────────────────────────


class TestFieldRule:
    def test_required_field_present(self) -> None:
        rules = [FieldRule(name="name", required=True)]
        validator = RecordValidator(rules)
        errors = validator.validate_record({"name": "Alice"}, 0)
        assert errors == []

    def test_required_field_missing(self) -> None:
        rules = [FieldRule(name="name", required=True)]
        validator = RecordValidator(rules)
        errors = validator.validate_record({}, 0)
        assert any(e["error"] == "REQUIRED_FIELD_MISSING" for e in errors)

    def test_type_mismatch(self) -> None:
        rules = [FieldRule(name="votes", required=True, field_type=int)]
        validator = RecordValidator(rules)
        errors = validator.validate_record({"votes": "abc"}, 0)
        assert any(e["error"] == "TYPE_MISMATCH" for e in errors)

    def test_range_min_violation(self) -> None:
        rules = [FieldRule(name="votes", required=True, min_value=0)]
        validator = RecordValidator(rules)
        errors = validator.validate_record({"votes": "-5"}, 0)
        assert any(e["error"] == "RANGE_BELOW_MIN" for e in errors)

    def test_range_max_violation(self) -> None:
        rules = [FieldRule(name="pct", required=True, max_value=100)]
        validator = RecordValidator(rules)
        errors = validator.validate_record({"pct": "150"}, 0)
        assert any(e["error"] == "RANGE_ABOVE_MAX" for e in errors)

    def test_allowed_values_violation(self) -> None:
        rules = [FieldRule(name="status", allowed_values={"active", "inactive"})]
        validator = RecordValidator(rules)
        errors = validator.validate_record({"status": "deleted"}, 0)
        assert any(e["error"] == "INVALID_VALUE" for e in errors)

    def test_max_length_violation(self) -> None:
        rules = [FieldRule(name="name", max_length=5)]
        validator = RecordValidator(rules)
        errors = validator.validate_record({"name": "toolongname"}, 0)
        assert any(e["error"] == "VALUE_TOO_LONG" for e in errors)


class TestDuplicateDetector:
    def test_no_duplicate(self) -> None:
        detector = DuplicateDetector(["id"])
        assert not detector.is_duplicate({"id": "1"})
        assert not detector.is_duplicate({"id": "2"})

    def test_detects_duplicate(self) -> None:
        detector = DuplicateDetector(["id"])
        detector.is_duplicate({"id": "1"})
        assert detector.is_duplicate({"id": "1"})

    def test_composite_key_duplicate(self) -> None:
        detector = DuplicateDetector(["election_id", "candidate_id"])
        detector.is_duplicate({"election_id": "E1", "candidate_id": "C1"})
        assert detector.is_duplicate({"election_id": "E1", "candidate_id": "C1"})
        assert not detector.is_duplicate({"election_id": "E1", "candidate_id": "C2"})

    def test_reset_clears_state(self) -> None:
        detector = DuplicateDetector(["id"])
        detector.is_duplicate({"id": "1"})
        detector.reset()
        assert not detector.is_duplicate({"id": "1"})


class TestGeographicValidator:
    def test_valid_coordinates(self) -> None:
        errors = GeographicValidator.validate_lat_lon(
            {"latitude": "12.9716", "longitude": "77.5946"}, "latitude", "longitude", 0
        )
        assert errors == []

    def test_invalid_latitude_range(self) -> None:
        errors = GeographicValidator.validate_lat_lon(
            {"latitude": "100", "longitude": "77"}, "latitude", "longitude", 0
        )
        assert any(e["error"] == "INVALID_LATITUDE" for e in errors)

    def test_invalid_longitude_range(self) -> None:
        errors = GeographicValidator.validate_lat_lon(
            {"latitude": "12", "longitude": "200"}, "latitude", "longitude", 0
        )
        assert any(e["error"] == "INVALID_LONGITUDE" for e in errors)

    def test_invalid_format(self) -> None:
        errors = GeographicValidator.validate_lat_lon(
            {"latitude": "abc", "longitude": "77"}, "latitude", "longitude", 0
        )
        assert any(e["error"] == "INVALID_LATITUDE_FORMAT" for e in errors)


class TestBatchValidator:
    def _make_validator(self) -> BatchValidator:
        return BatchValidator(
            rules=[
                FieldRule(name="id", required=True),
                FieldRule(name="votes", required=True, field_type=int, min_value=0),
            ],
            duplicate_key_fields=["id"],
        )

    def test_all_valid(self) -> None:
        validator = self._make_validator()
        records = [{"id": "1", "votes": "100"}, {"id": "2", "votes": "200"}]
        valid, rejected, report = validator.validate_batch(records)
        assert len(valid) == EXPECTED_ROWS_SMALL
        assert len(rejected) == 0
        assert report.is_valid
        assert report.total_records == EXPECTED_ROWS_SMALL

    def test_rejects_invalid(self) -> None:
        validator = self._make_validator()
        records = [{"id": "1", "votes": "-5"}]
        valid, rejected, report = validator.validate_batch(records)
        assert len(valid) == 0
        assert len(rejected) == 1
        assert report.invalid_records == 1

    def test_rejects_duplicates(self) -> None:
        validator = self._make_validator()
        records = [{"id": "1", "votes": "100"}, {"id": "1", "votes": "200"}]
        valid, rejected, report = validator.validate_batch(records)
        assert len(rejected) == 1  # second occurrence rejected

    def test_error_rate_calculation(self) -> None:
        report = ValidationReport(total_records=10, valid_records=7, invalid_records=3)
        assert report.error_rate == pytest.approx(0.3)


# ─────────────────────────────────────────────────────────────────────────────
# TRACKING
# ─────────────────────────────────────────────────────────────────────────────


class TestJobProgress:
    def test_initial_state(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test_job")
        assert job.status == JobStatus.PENDING
        assert job.total_records == 0
        assert job.started_at is None

    def test_start_sets_running(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test")
        job.start()
        assert job.status == JobStatus.RUNNING
        assert job.started_at is not None

    def test_complete(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test")
        job.start()
        job.complete()
        assert job.status == JobStatus.COMPLETED
        assert job.completed_at is not None

    def test_fail(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test")
        job.start()
        job.fail("db error")
        assert job.status == JobStatus.FAILED
        assert job.error_message == "db error"

    def test_cancel(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test")
        job.start()
        job.cancel()
        assert job.status == JobStatus.CANCELLED

    def test_progress_pct_calculation(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test")
        job.total_records = 100
        job.loaded_records = 50
        assert job.progress_pct == PROGRESS_PCT_HALF

    def test_progress_pct_zero_total(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test")
        assert job.progress_pct == 0.0

    def test_to_dict(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test")
        job.start()
        d = job.to_dict()
        assert "job_id" in d
        assert d["status"] == "running"
        assert d["job_name"] == "test"

    def test_log_appends_entries(self) -> None:
        job = JobProgress(job_id=uuid.uuid4(), job_name="test")
        job.log("started")
        job.log("parsing")
        assert len(job.log_entries) == EXPECTED_ROWS_SMALL


class TestJobRegistry:
    def test_register_creates_job(self) -> None:
        registry = JobRegistry()
        job = registry.register("test_job")
        assert job.job_name == "test_job"
        assert job.status == JobStatus.PENDING

    def test_get_returns_job(self) -> None:
        registry = JobRegistry()
        job = registry.register("job1")
        retrieved = registry.get(job.job_id)
        assert retrieved is job

    def test_get_unknown_returns_none(self) -> None:
        registry = JobRegistry()
        assert registry.get(uuid.uuid4()) is None

    def test_cancel_running_job(self) -> None:
        registry = JobRegistry()
        job = registry.register("job1")
        job.start()
        result = registry.cancel(job.job_id)
        assert result is True
        assert job.status == JobStatus.CANCELLED

    def test_cancel_pending_job_returns_false(self) -> None:
        registry = JobRegistry()
        job = registry.register("job1")
        result = registry.cancel(job.job_id)
        assert result is False

    def test_all_jobs(self) -> None:
        registry = JobRegistry()
        registry.register("job1")
        registry.register("job2")
        jobs = registry.all_jobs()
        assert len(jobs) == EXPECTED_ROWS_SMALL


# ─────────────────────────────────────────────────────────────────────────────
# EXPORTS
# ─────────────────────────────────────────────────────────────────────────────


SAMPLE_RECORDS = [
    {"id": "1", "state": "Goa", "votes": "100"},
    {"id": "2", "state": "Bihar", "votes": "200"},
]


class TestCsvExporter:
    def test_export_returns_bytes(self) -> None:
        data = CsvExporter().export(SAMPLE_RECORDS)
        assert isinstance(data, bytes)
        assert b"state" in data
        assert b"Goa" in data

    def test_empty_records(self) -> None:
        data = CsvExporter().export([])
        assert data == b""


class TestJsonExporter:
    def test_export_returns_bytes(self) -> None:
        data = JsonExporter().export(SAMPLE_RECORDS)
        parsed = json.loads(data)
        assert len(parsed) == EXPECTED_ROWS_SMALL
        assert parsed[0]["state"] == "Goa"

    def test_empty_records(self) -> None:
        data = JsonExporter().export([])
        assert json.loads(data) == []


class TestParquetExporter:
    def test_export_roundtrip(self) -> None:
        records = [{"id": "1", "votes": 100}, {"id": "2", "votes": 200}]
        data = ParquetExporter().export(records)
        assert len(data) > 0
        table = pq.read_table(io.BytesIO(data))
        assert table.num_rows == EXPECTED_ROWS_SMALL

    def test_empty_records_returns_empty(self) -> None:
        data = ParquetExporter().export([])
        assert data == b""


class TestGeoJsonExporter:
    def test_export_feature_collection(self) -> None:
        records = [
            {"id": "B001", "name": "Booth 1", "latitude": "12.97", "longitude": "77.59"},
        ]
        data = GeoJsonExporter().export(records)
        geo = json.loads(data)
        assert geo["type"] == "FeatureCollection"
        assert len(geo["features"]) == 1
        assert geo["features"][0]["geometry"]["type"] == "Point"

    def test_missing_coordinates_still_exports(self) -> None:
        records = [{"id": "B001", "name": "Booth 1"}]
        data = GeoJsonExporter().export(records)
        geo = json.loads(data)
        assert geo["features"][0]["geometry"] is None


class TestExportRecords:
    def test_csv_format(self) -> None:
        data = export_records(SAMPLE_RECORDS, "csv")
        assert b"state" in data

    def test_json_format(self) -> None:
        data = export_records(SAMPLE_RECORDS, "json")
        assert json.loads(data)[0]["state"] == "Goa"

    def test_unknown_format_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported export format"):
            export_records(SAMPLE_RECORDS, "pdf")


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE INTEGRATION (end-to-end with mocked session)
# ─────────────────────────────────────────────────────────────────────────────


class TestETLPipelineIntegration:
    """Integration tests for the ETL pipeline using mocked DB sessions."""

    @pytest.fixture
    def mock_session(self) -> AsyncMock:
        session = AsyncMock()
        session.flush = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        session.add = MagicMock()
        session.add_all = MagicMock()
        session.execute = AsyncMock()
        return session

    @pytest.mark.asyncio
    async def test_pipeline_successful_run(self, tmp_path: Path, mock_session: AsyncMock) -> None:
        csv_file = tmp_path / "results.csv"
        csv_file.write_bytes(b"id,votes\n1,100\n2,200\n3,300\n")

        config = PipelineConfig(
            job_name="test_pipeline",
            source_uri=str(csv_file),
            connector=FileConnector(csv_file),
            parser=CsvParser(),
            validator=BatchValidator(
                rules=[FieldRule(name="id", required=True), FieldRule(name="votes", required=True)]
            ),
            transformer=RecordTransformer({}),
            chunk_size=10,
            initiated_by="test_user",
        )

        mock_batch = MagicMock()
        mock_batch.id = uuid.uuid4()

        with patch("app.etl.pipeline.ImportBatchModel", return_value=mock_batch):
            registry = JobRegistry()
            pipeline = ETLPipeline(session=mock_session, config=config, registry=registry)
            progress = await pipeline.run()

        assert progress.status == JobStatus.COMPLETED
        assert progress.total_records == PIPELINE_TOTAL
        assert progress.valid_records == PIPELINE_VALID_ALL
        assert progress.rejected_records == 0

    @pytest.mark.asyncio
    async def test_pipeline_with_validation_errors(
        self, tmp_path: Path, mock_session: AsyncMock
    ) -> None:
        csv_file = tmp_path / "bad.csv"
        csv_file.write_bytes(b"id,votes\n1,100\n2,bad_value\n3,300\n")

        config = PipelineConfig(
            job_name="test_validation",
            source_uri=str(csv_file),
            connector=FileConnector(csv_file),
            parser=CsvParser(),
            validator=BatchValidator(
                rules=[
                    FieldRule(name="id", required=True),
                    FieldRule(name="votes", required=True, field_type=int),
                ]
            ),
            chunk_size=100,
        )

        mock_batch = MagicMock()
        mock_batch.id = uuid.uuid4()

        with patch("app.etl.pipeline.ImportBatchModel", return_value=mock_batch):
            registry = JobRegistry()
            pipeline = ETLPipeline(session=mock_session, config=config, registry=registry)
            progress = await pipeline.run()

        assert progress.total_records == PIPELINE_TOTAL
        assert progress.rejected_records == PIPELINE_REJECTED_ONE
        assert progress.valid_records == PIPELINE_VALID_TWO
