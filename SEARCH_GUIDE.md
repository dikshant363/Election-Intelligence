# Search Platform Guide

## Overview

The Search & Discovery Platform (`backend/app/search/`) is a production-grade, AI-free retrieval system designed for the Election Intelligence Platform. It provides full-text search, multi-field filtering, relevance ranking, text highlighting, entity autocomplete, geospatial proximity queries, statistical aggregations, and in-memory query caching.

---

## Architecture & Search Abstraction Layer (SAL)

The Application Layer interacts with search engines via a Search Abstraction Layer (SAL):

```
Client / REST API Routers (/api/v1/search)
                  │
                  ▼
   [Search Application Service (SAL)]  (app/search/services/)
                  │
 ┌────────────────┼────────────────┬──────────────┐
 ▼                ▼                ▼              ▼
[QueryEngine] [Autocomplete]  [Geospatial]  [Analytics]
 (FTS & AST)  (Prefix Top-N)  (Haversine)   (Aggregations)
```

By programming against `SearchService` (the SAL) rather than raw database calls, future AI vector search and OpenSearch clusters can be added without modifying application logic.

---

## Component Architecture

| Sub-package | Role |
| :--- | :--- |
| `search.exceptions` | Hierarchy of search exceptions (`SearchException`, `FilterError`, `GeospatialError`, etc.) |
| `search.queries` | Query domain AST (`SearchQuery`, `QueryType`, `SearchOperator`, `Pagination`) |
| `search.filters` | Reusable filter builders for elections, dates, parties, and geographies |
| `search.ranking` | Relevance scoring algorithm (`RelevanceRanker`, `ScoredHit`) |
| `search.highlighting` | Snippet generator (`TextHighlighter`) using configurable HTML tags |
| `search.autocomplete` | Entity typeahead (`AutocompleteEngine`) for elections, candidates, parties, and constituencies |
| `search.geospatial` | Haversine distance, bounding box, and polygon spatial engine (`SpatialSearchEngine`) |
| `search.analytics` | Reusable statistical aggregation engine (`AnalyticsEngine`) |
| `search.cache` | In-memory LRU cache (`SearchCache`), query metrics, and slow-query logger |
| `search.indexing` | FTS GIN index manager (`PostgresFTSIndex`) and OpenSearch cluster adapter stub |
| `search.services` | High-level `SearchService` (SAL) coordinator |

---

## API Endpoints

- `GET /api/v1/search` — Multi-field full-text search with pagination & highlighting
- `GET /api/v1/search/autocomplete` — Fast entity prefix autocomplete suggestions
- `GET /api/v1/search/geospatial` — Proximity search for nearest polling booths
- `GET /api/v1/search/analytics` — Constituency, party, and turnout statistical aggregations
- `POST /api/v1/search/reindex` — Trigger full reindex of search indices

---

## Verification & Testing

```bash
# Run search unit & integration test suite
.venv/bin/pytest tests/test_search.py -v

# Run full project test suite
.venv/bin/pytest
```
