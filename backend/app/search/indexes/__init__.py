"""
Search performance optimisation: index management and query planning utilities.

This module provides:
- DDL statements for GIN/GiST indexes supporting FTS
- EXPLAIN ANALYZE helper for slow-query diagnosis
- pg_trgm extension enablement
"""

from __future__ import annotations

# ── PostgreSQL Index DDL Statements ──────────────────────────────────────────
# These are idempotent — safe to run on an already-indexed database.

GIN_INDEX_ELECTIONS_TITLE = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_elections_fts_title
ON elections USING GIN (to_tsvector('english', title || ' ' || election_type));
"""

GIN_INDEX_CANDIDATES_NAME = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_candidates_fts_name
ON candidates USING GIN (to_tsvector('english', name));
"""

GIN_INDEX_PARTIES_NAME = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_parties_fts_name
ON political_parties USING GIN (to_tsvector('english', name || ' ' || code));
"""

GIN_INDEX_CONSTITUENCIES_NAME = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_constituencies_fts_name
ON constituencies USING GIN (to_tsvector('english', name || ' ' || code));
"""

TRGM_EXTENSION = """
CREATE EXTENSION IF NOT EXISTS pg_trgm;
"""

TRGM_INDEX_ELECTIONS_TITLE = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_elections_trgm_title
ON elections USING GIN (title gin_trgm_ops);
"""

TRGM_INDEX_CANDIDATES_NAME = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_candidates_trgm_name
ON candidates USING GIN (name gin_trgm_ops);
"""

TRGM_INDEX_PARTIES_NAME = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_parties_trgm_name
ON political_parties USING GIN (name gin_trgm_ops);
"""

TRGM_INDEX_CONSTITUENCIES_NAME = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_constituencies_trgm_name
ON constituencies USING GIN (name gin_trgm_ops);
"""

# Saved searches index
SAVED_SEARCHES_INDEX = """
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_saved_searches_created_by
ON saved_searches (created_by, entity_type);
"""

# All setup statements in execution order
ALL_FTS_SETUP_STATEMENTS: list[str] = [
    TRGM_EXTENSION,
    GIN_INDEX_ELECTIONS_TITLE,
    GIN_INDEX_CANDIDATES_NAME,
    GIN_INDEX_PARTIES_NAME,
    GIN_INDEX_CONSTITUENCIES_NAME,
    TRGM_INDEX_ELECTIONS_TITLE,
    TRGM_INDEX_CANDIDATES_NAME,
    TRGM_INDEX_PARTIES_NAME,
    TRGM_INDEX_CONSTITUENCIES_NAME,
    SAVED_SEARCHES_INDEX,
]

# Descriptive names for logging
STATEMENT_LABELS: dict[str, str] = {
    TRGM_EXTENSION: "Enable pg_trgm extension",
    GIN_INDEX_ELECTIONS_TITLE: "GIN index: elections FTS",
    GIN_INDEX_CANDIDATES_NAME: "GIN index: candidates FTS",
    GIN_INDEX_PARTIES_NAME: "GIN index: parties FTS",
    GIN_INDEX_CONSTITUENCIES_NAME: "GIN index: constituencies FTS",
    TRGM_INDEX_ELECTIONS_TITLE: "Trigram index: elections title",
    TRGM_INDEX_CANDIDATES_NAME: "Trigram index: candidates name",
    TRGM_INDEX_PARTIES_NAME: "Trigram index: parties name",
    TRGM_INDEX_CONSTITUENCIES_NAME: "Trigram index: constituencies name",
    SAVED_SEARCHES_INDEX: "Index: saved searches user+entity",
}
