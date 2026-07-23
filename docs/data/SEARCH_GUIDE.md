# Search Platform Guide

## 1. Search Abstraction Layer (SAL)
The `backend/app/search/` subsystem uses a Search Abstraction Layer (SAL).
- **Purpose:** Decouples the application logic from the underlying search engine.
- **Backends:** Currently implemented using PostgreSQL Full-Text Search, but designed to allow swapping to Elasticsearch or Typesense in the future.

## 2. PostgreSQL Full-Text Search
- **Implementation:** Utilizes `tsvector` for document representation and `tsquery` for parsing user inputs.
- **Indexing:** Heavily relies on GIN (Generalized Inverted Index) indexes on searchable text columns to guarantee sub-millisecond query performance on large datasets.

## 3. BM25 Ranking Algorithm
- **Mechanism:** PostgreSQL's native ranking (`ts_rank_cd`) is augmented with custom logic to approximate BM25, prioritizing term frequency and inverse document frequency.
- **Recency Decay:** For certain queries (like news or recent elections), a time-decay function slightly boosts more recent records.

## 4. Search Query Parsing
- **Capabilities:** Supports simple term searches, phrase matching (using quotes), prefix matching (using `:*`), and boolean operators (AND, OR, NOT).

## 5. Filters
Search results can be narrowed using structured filters.
- **Fields:** Available by entity type (e.g., State, Election Type, Year, Party).
- **Date Ranges:** Supported for election events.

## 6. Highlighting
- **Extraction:** Returns the context around the matched terms using `ts_headline`.
- **Formatting:** Wraps matching keywords in specific HTML tags (e.g., `<b>` or `<mark>`) for frontend rendering.

## 7. Autocomplete
- **Engine:** Uses a specialized prefix-matching engine and trigram indexes (`pg_trgm`) for fast typeahead suggestions.
- **Sources:** Aggregates top candidate names, party names, and constituencies.
- **Ranking:** Prioritizes exact prefix matches and historically popular queries.

## 8. Geospatial Search
- **Implementation:** PostGIS integration for spatial queries.
- **Queries:** Supports bounding box queries (finding polling booths within a map view), polygon containment (checking if a point is within a constituency), and haversine distance calculations.

## 9. Faceted Search
Provides aggregate counts for filter categories alongside search results, allowing the frontend to build dynamic filter sidebars (e.g., "Show me results (BJP: 40, INC: 30)").

## 10. Search Analytics
- **Tracking:** Logs anonymized search queries, click-through rates, and zero-result queries.
- **Access:** Analytics data is available to admins to identify missing content or tune synonyms.

## 11. Index Management
- **Commands:** Admin tools to trigger reindexing operations.
- **When to Reindex:** Necessary after bulk ETL loads or schema changes affecting searchable columns.
- **Health:** Scripts monitor GIN index bloat and recommend `REINDEX` operations.

## 12. Performance Tuning
- **Caching:** Common searches are cached via Redis.
- **Maintenance:** Routine vacuuming and index rebuilding. Connection pool sizing is tuned for high-read search workloads.

## 13. Debugging Search Results
- **Missing Results:** Check if the document is properly indexed in the `tsvector` column or if the query parser rejected a term.
- **Unexpected Results:** Inspect the `ts_rank` score to see why a document was matched (often due to stemming resolving unexpected roots).

## 14. API Endpoints
- `/api/v1/search`: Main search interface.
- `/api/v1/search/autocomplete`: Fast typeahead suggestions.
- `/api/v1/search/geospatial`: Map-based spatial queries.
- `/api/v1/search/analytics`: Admin endpoint for search metrics.
- `/api/v1/search/reindex`: Admin endpoint for triggering index rebuilds.
