# ETL Guide

## 1. Architecture Overview
The ETL (Extract, Transform, Load) subsystem (`backend/app/etl/`) orchestrates the ingestion of election data.
**Pipeline Stages:** `Connectors` → `Parsers` → `Validators` → `Transformers` → `Staging` → `Loaders` → `Provenance/Tracking`.

## 2. Supported Data Formats and Sources
- **Formats:** CSV and JSON files, primarily provided by the Election Commission or trusted civic tech partners.
- **Connectors:** Abstracted connectors fetch data from local filesystems, AWS S3 buckets, or direct database connections.

## 3. Data Entities and Ingestion Rules
The system handles 6 domain entities:
1. **Elections:** Metadata about the election event (year, type, state).
2. **Constituencies:** Geographic and administrative boundaries.
3. **Parties:** Political party metadata and symbols.
4. **Candidates:** Profiles of individuals running for office.
5. **Polling Booths:** Specific voting locations.
6. **Results:** Vote counts and margins linking candidates, parties, and constituencies.
*Ingestion must generally follow this order to satisfy foreign key constraints.*

## 4. Validation Rules
The `validators/` submodule ensures data integrity before loading.
- **Checks:** Data type enforcement, required field checks, uniqueness constraints, and referential integrity (e.g., a candidate must belong to a valid party).
- **Behavior:** Invalid rows are flagged and segregated, preventing corruption of the main database.

## 5. Transformation Rules
The `transformers/` submodule maps raw source data to internal domain models (`backend/app/domain/`).
- **Standardization:** Normalizes text (e.g., title casing names), handles date parsing, and resolves entity aliases (e.g., mapping variant party acronyms to a canonical ID).

## 6. Staging Process
Data is first loaded into staging tables (`staging/`).
- **Purpose:** Allows for bulk operations, complex validations, and manual inspection before committing to production tables. Prevents dirty reads during long ingestion jobs.

## 7. Loading Process
The `loaders/` submodule moves data from staging to the persistence layer.
- **UnitOfWork:** SQLAlchemy 2 models (`backend/app/persistence/models/`) are managed within a UnitOfWork pattern, ensuring atomic commits. If a load fails midway, the transaction rolls back.

## 8. Provenance Tracking
The `provenance/` submodule records data lineage.
- **Lineage:** Every record in the database is tagged with a batch ID indicating its source file, ingestion timestamp, and the ETL job that created it.

## 9. Job Scheduling and Tracking
The `jobs/` and `tracking/` submodules manage execution.
- **State Management:** Jobs transition through states (PENDING, RUNNING, COMPLETED, FAILED). Metrics (rows processed, time taken) are recorded.

## 10. Error Handling
- **Partial Loads:** Configurable thresholds determine if a job fails entirely upon hitting validation errors or if it proceeds with valid rows while dumping errors to a dead-letter queue.
- **Recovery:** Failed jobs can be restarted from the last successful checkpoint.

## 11. Export Capabilities
The `exports/` submodule allows exporting clean data.
- **Formats:** Authorized users can export entity data back out as CSV or JSON for offline analysis.

## 12. Running an ETL Job
- **CLI Commands:** Internal admin commands can trigger jobs via terminal.
- **API Endpoints:** Webhooks and authenticated API routes can initiate specific ingestion pipelines.

## 13. Monitoring ETL Runs
- **Metrics/Logs:** Check job tracking tables and application logs for throughput metrics, validation error rates, and connection issues.
