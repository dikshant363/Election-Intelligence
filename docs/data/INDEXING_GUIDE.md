# Search Indexing & Extensibility Guide

## Overview

The Indexing module (`backend/app/search/indexing/`) manages full-text search indexes, incremental updates, full reindexing operations, and provides a pluggable engine adapter interface.

---

## Indexing Abstraction (`SearchIndex`)

All search backends inherit from the abstract `SearchIndex` base class:

```python
class SearchIndex(ABC):
    @abstractmethod
    async def initialize(self) -> None: ...

    @abstractmethod
    async def index_document(self, entity_type: str, document_id: str, data: dict) -> None: ...

    @abstractmethod
    async def delete_document(self, entity_type: str, document_id: str) -> None: ...

    @abstractmethod
    async def reindex_all(self) -> IndexStats: ...
```

---

## PostgreSQL Full-Text Search (`PostgresFTSIndex`)

The primary search index utilizes PostgreSQL `tsvector` generated columns and GIN indexes:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_elections_fts_title
ON elections USING GIN (to_tsvector('english', title || ' ' || election_type));

CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_candidates_fts_name
ON candidates USING GIN (to_tsvector('english', name));
```

---

## OpenSearch Adapter Stub (`OpenSearchAdapter`)

An extensible OpenSearch cluster adapter stub is provided for future multi-node horizontal scaling.

```python
adapter = OpenSearchAdapter(endpoint="http://localhost:9200")
await adapter.initialize()
```

---

## Soft Delete & Incremental Handling

- **Soft Delete**: `deleted_at IS NULL` conditions are automatically enforced across all search queries.
- **Incremental Updates**: PostgreSQL GIN indexes update automatically on row mutations.
- **Full Reindex**: Triggered via `POST /api/v1/search/reindex` or `SearchService.reindex_all()`.
