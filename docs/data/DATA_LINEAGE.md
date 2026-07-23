# Data Lineage and Provenance

This document outlines the architecture, tracking mechanisms, and compliance requirements for data lineage within the Election Intelligence Platform v1.0.0.

## 1. What is Data Lineage?

In the context of election intelligence, data lineage is the comprehensive tracking of data origins, transformations, and movements over time. Because election data dictates public policy insights and political analysis, ensuring its authenticity, immutability, and traceability is non-negotiable. If a user questions why a specific candidate's vote count is listed as *X*, the platform must immediately surface the exact ECI PDF or API endpoint, extraction timestamp, and transformation logic that produced *X*.

## 2. Provenance Tracking Architecture

Lineage is handled centrally by the `backend/app/etl/provenance/` module.
The architecture utilizes an Event Sourcing pattern combined with a specialized lineage tracking database table (`data_lineage_events`).

- **Connectors & Parsers** (`backend/app/etl/connectors/`): Stamp incoming raw data with a `SourceRecordID`.
- **Transformers**: Append transformation logic versions to the record payload.
- **Loaders**: Commit the final aggregate to the database while synchronously writing the lineage graph to the provenance table.

## 3. Data Lineage Metadata

Every domain entity record in the system contains a `provenance_id` foreign key. This links to a `LineageMetadata` object tracking:

```json
{
  "provenance_id": "uuid-v4",
  "source_system": "ECI_RESULTS_PORTAL",
  "source_uri": "https://results.eci.gov.in/...",
  "ingestion_time": "2024-06-04T12:00:00Z",
  "batch_id": "batch-20240604-001",
  "pipeline_version": "v1.2.4",
  "operator_id": "auto-cron-worker",
  "validation_hash": "sha256-hash-of-raw-payload"
}
```

## 4. Lineage Tracking for Entities

- **Election**: Tracks official gazette notifications and master schedule source URLs.
- **Candidate**: Tracks affidavit (Form 26) PDF hashes, OCR extraction confidence scores, and ECI nomination IDs.
- **Party**: Tracks ECI recognized party list updates and symbol allocation documents.
- **Constituency**: Tracks delimitation commission report IDs and boundary shapefile versions.
- **PollingBooth**: Tracks booth list PDFs published by District Election Officers (DEO).
- **Result**: Highly volatile; tracks continuous round-wise API polling timestamps, discrepancies, and ECI finalizing signatures.

## 5. Querying Lineage Data

Lineage can be queried via the internal API provided by `backend/app/api/v1/routers/provenance.py`.

```http
GET /api/v1/provenance/candidate/{candidate_id}
```
**Response**: Returns the directed acyclic graph (DAG) of how the candidate record was constructed, from raw PDF ingestion to current state.

## 6. Data Quality Scoring

The ETL validators (`backend/app/etl/validators/`) assign a `quality_score` (0.0 to 1.0) to every parsed record.
- Exact matches from JSON APIs: `1.0`
- Clean OCR extraction: `0.9`
- Missing optional fields / fuzzy matches: `0.7`
This score is embedded in the lineage metadata and allows downstream AI contexts to warn users if data is of low confidence.

## 7. Change Tracking

The persistence layer (`backend/app/persistence/`) uses SQLAlchemy event listeners to intercept `UPDATE` and `DELETE` operations. All mutations trigger an `EntityUpdated` domain event (`backend/app/domain/events/`), which is routed to the event bus (`backend/app/realtime/eventbus/`) and permanently appended to the provenance log.

## 8. Audit Trail for Data Modifications

Manual data overrides (e.g., by a data steward correcting a typo in a candidate name) require an authenticated session (`backend/app/identity/`).
The audit trail strictly records:
- `user_id` making the change.
- `previous_state` (JSON diff).
- `new_state` (JSON diff).
- `justification_reason` (Mandatory text field).

## 9. Lineage for AI Training Data

When data is exported from the platform to fine-tune AI models or build vector embeddings, the `batch_id` and timestamp are embedded in the export manifest. 
If downstream hallucinations occur, engineers can cross-reference the exact dataset state at the time of embedding generation using the exported provenance manifest.

## 10. Regulatory Compliance

Election data handling complies with Indian IT Act requirements and standard data immutability practices.
- **Non-repudiation**: Raw payloads are hashed at the point of ingestion (`validation_hash`).
- **Traceability**: Every data point surfaced on the UI can be mapped to an external, publicly verifiable source.

## 11. Lineage Visualization

The platform provides a graphical representation of data flow for administrators. Using the `backend/app/search/` module, lineage events are indexed in Elasticsearch, allowing UI clients to render interactive node-based graphs of data transformations.

## 12. Data Retention Policy

| Data Type | Retention Period | Storage Tier |
|-----------|------------------|--------------|
| **Raw Ingests (PDFs, HTML)** | Indefinite | Cold Storage (S3 Glacier) |
| **Lineage Metadata (Active)** | 5 Years | Primary DB (PostgreSQL) |
| **Audit Trails (Mutations)** | 10 Years | Write-Once-Read-Many (WORM) Store |
| **Vector Embeddings** | Ephemeral (Recomputed) | Vector DB |
