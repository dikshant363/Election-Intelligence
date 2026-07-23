# ETL Platform Guide

## Overview

The Election Intelligence Platform ETL layer (`backend/app/etl/`) is a production-grade,
AI-free data ingestion and transformation system. It ingests official election datasets from
multiple sources, validates and normalises them, stages all imports before production, and
maintains full provenance and lineage for every record.

---

## Architecture

```
External Sources (Files, HTTP, S3, ZIP)
        ↓
Connectors (etl/connectors/)
        ↓
Parsers (etl/parsers/)
        ↓
Validators (etl/validators/)
        ↓
Transformers (etl/transformers/)
        ↓
Staging (etl/staging/  → import_batches, import_records, rejected_records, transformation_logs)
        ↓
Loaders (etl/loaders/)
        ↓
Provenance (etl/provenance/ → provenance_records)
        ↓
Production Database (PostgreSQL)
```

---

## Package Structure

```
backend/app/etl/
├── __init__.py
├── connectors/         # Source adapters: File, HTTP, S3, ZIP
├── parsers/            # Format parsers: CSV, Excel, JSON, GeoJSON, Parquet, ZIP
├── validators/         # Schema, type, range, duplicate, geographic validation
├── transformers/       # Field-level normalisation (states, dates, party codes, etc.)
├── staging/            # SQLAlchemy ORM models for staging tables
├── loaders/            # Chunked bulk-insert to staging
├── pipeline/           # Full ETL orchestrator: Fetch→Parse→Validate→Transform→Load
├── jobs/               # Pre-configured job factories for election data types
├── tracking/           # In-memory job progress registry (JobProgress, JobRegistry)
├── provenance/         # Provenance/lineage ORM model
├── exports/            # Export modules: CSV, JSON, Parquet, GeoJSON
└── exceptions/         # ETL-specific exception hierarchy
```

---

## Connectors

| Class | Description |
|-------|-------------|
| `FileConnector` | Reads data from a local filesystem path (async via aiofiles) |
| `HttpConnector` | Fetches data from HTTP/HTTPS URL (synchronous stdlib fallback) |
| `S3Connector` | Production stub for AWS S3 — requires boto3 |
| `ZipConnector` | Extracts a named member from a ZIP archive |

All connectors inherit `BaseConnector.checksum()` which returns a SHA-256 hex digest.

---

## Parsers

| Class | Formats |
|-------|---------|
| `CsvParser` | `.csv` — supports chunked streaming, custom delimiter, encoding |
| `ExcelParser` | `.xlsx` — reads via openpyxl, configurable sheet |
| `JsonParser` | `.json`, `.jsonl` — supports array root and `{"data": [...]}` envelope |
| `GeoJsonParser` | `.geojson` — flattens FeatureCollection properties |
| `ParquetParser` | `.parquet` — reads via pyarrow |
| `ZipParser` | `.zip` — extracts first supported member and delegates |

`get_parser_for_extension(filename)` returns the correct parser for a given filename.

---

## Validators

### FieldRule

```python
FieldRule(
    name="votes_cast",
    required=True,
    field_type=int,
    min_value=0,
    max_value=1_000_000,
    allowed_values=None,
    max_length=None,
)
```

### BatchValidator

Orchestrates field validation, duplicate detection, and geographic coordinate validation
for an entire batch in one pass.

```python
validator = BatchValidator(
    rules=[...],
    duplicate_key_fields=["election_id", "candidate_id"],
    geo_config=("latitude", "longitude"),
)
valid, rejected, report = validator.validate_batch(records)
```

---

## Transformers

Pre-built transformers normalise common Indian election data patterns:

- `normalize_state("ap")` → `"Andhra Pradesh"`
- `normalize_election_type("ls")` → `"Lok Sabha"`
- `normalize_date("15/11/2024")` → `"2024-11-15"`
- `normalize_party_code("bjp")` → `"BJP"`
- `normalize_constituency_code("7")` → `"007"`
- `normalize_coordinates("12.97")` → `12.97`

Two pre-built instances are available:

```python
from app.etl.transformers import ELECTION_DATASET_TRANSFORMER, CANDIDATE_DATASET_TRANSFORMER
```

---

## Staging Tables

| Table | Purpose |
|-------|---------|
| `import_batches` | Tracks lifecycle (status, counts, errors) of each import job |
| `import_records` | Stores raw + transformed data for each valid staged record |
| `rejected_records` | Stores records that failed validation with error codes |
| `transformation_logs` | Immutable audit of transformations applied to each batch |
| `provenance_records` | Lineage linking each production record back to its import |

> **Critical invariant**: Nothing enters production directly. All imports go through staging.
> Every production record MUST have a corresponding `provenance_records` entry.

---

## Pipeline Orchestration

```python
from app.etl.pipeline import ETLPipeline, PipelineConfig
from app.etl.connectors import FileConnector
from app.etl.parsers import CsvParser
from app.etl.validators import BatchValidator, FieldRule
from app.etl.transformers import ELECTION_DATASET_TRANSFORMER

config = PipelineConfig(
    job_name="election_results_csv",
    source_uri="/data/results_2024.csv",
    connector=FileConnector("/data/results_2024.csv"),
    parser=CsvParser(),
    validator=BatchValidator(rules=[...]),
    transformer=ELECTION_DATASET_TRANSFORMER,
    chunk_size=1000,
    initiated_by="admin@example.com",
)

pipeline = ETLPipeline(session=db_session, config=config)
progress = await pipeline.run()
print(progress.to_dict())
```

### Pipeline Phases

1. **Fetch** — Download raw bytes, compute SHA-256 checksum
2. **Parse** — Streaming chunked parse into structured records
3. **Validate** — Field rules, duplicate detection, geographic checks
4. **Transform** — Normalise fields (state names, dates, codes)
5. **Load** — Bulk-insert to staging tables; commit

---

## Pre-configured Jobs

```python
from app.etl.jobs import ElectionResultCSVJob, CandidateExcelJob, PollingBoothGeoJsonJob

config = ElectionResultCSVJob.make_config("/data/ls2024.csv", initiated_by="admin")
```

---

## Export

```python
from app.etl.exports import export_records

csv_bytes = export_records(records, "csv")
json_bytes = export_records(records, "json")
parquet_bytes = export_records(records, "parquet")
geojson_bytes = export_records(records, "geojson")
```

---

## Job Tracking

```python
from app.etl.tracking import job_registry

jobs = job_registry.all_jobs()
job_registry.cancel(job_id)
```

---

## Operations Reference

```bash
# Run ETL tests
.venv/bin/pytest tests/test_etl.py -v

# Lint check
.venv/bin/ruff check backend/app/etl/ tests/test_etl.py
```
