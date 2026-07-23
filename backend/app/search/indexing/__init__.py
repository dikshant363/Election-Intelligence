"""Search index management: PostgreSQL FTS, OpenSearch adapter stub, incremental/full reindexing."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models import CandidateModel, ElectionModel

logger = logging.getLogger("app.search.indexing")

INDEX_VERSION = "v1"


@dataclass
class IndexStats:
    """Statistics for an indexed entity dataset."""

    index_name: str
    version: str = INDEX_VERSION
    total_documents: int = 0
    last_indexed_at: datetime | None = None
    is_active: bool = True


class SearchIndex(ABC):
    """Abstract interface for all search engine index backends."""

    @abstractmethod
    async def initialize(self) -> None:
        """Create or initialize required database indexes/tables."""

    @abstractmethod
    async def index_document(self, entity_type: str, document_id: str, data: dict[str, Any]) -> None:
        """Index a single document."""

    @abstractmethod
    async def delete_document(self, entity_type: str, document_id: str) -> None:
        """Remove a document from index (handles soft delete)."""

    @abstractmethod
    async def reindex_all(self) -> IndexStats:
        """Perform full reindex of all supported entities."""


class PostgresFTSIndex(SearchIndex):
    """PostgreSQL Full-Text Search index manager using tsvector GIN indexes."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.stats = IndexStats(index_name="postgres_fts")

    async def initialize(self) -> None:
        """Create GIN full-text indexes concurrently if not existing."""
        ddl_statements = [
            "CREATE EXTENSION IF NOT EXISTS pg_trgm;",
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_elections_fts_title
            ON elections USING GIN (to_tsvector('english', title || ' ' || election_type));
            """,
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_candidates_fts_name
            ON candidates USING GIN (to_tsvector('english', name));
            """,
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_parties_fts_name
            ON political_parties USING GIN (to_tsvector('english', name || ' ' || code));
            """,
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_constituencies_fts_name
            ON constituencies USING GIN (to_tsvector('english', name || ' ' || code));
            """,
        ]
        for stmt in ddl_statements:
            try:
                await self._session.execute(text(stmt))
            except Exception as exc:
                logger.warning("FTS index setup notice: %s", exc)

    async def index_document(
        self, entity_type: str, document_id: str, data: dict[str, Any]
    ) -> None:
        """Incremental indexing step — PostgreSQL auto-updates tsvector on write."""

    async def delete_document(self, entity_type: str, document_id: str) -> None:
        """Soft deletes automatically excluded via deleted_at IS NULL queries."""

    async def reindex_all(self) -> IndexStats:
        """Re-verify document counts across all search models."""
        count_elections = (
            await self._session.execute(
                select(ElectionModel).where(ElectionModel.deleted_at.is_(None))
            )
        ).scalars().all()
        count_candidates = (
            await self._session.execute(
                select(CandidateModel).where(CandidateModel.deleted_at.is_(None))
            )
        ).scalars().all()

        total = len(count_elections) + len(count_candidates)
        self.stats.total_documents = total
        self.stats.last_indexed_at = datetime.now(UTC)
        return self.stats


class OpenSearchAdapter(SearchIndex):
    """Extensible OpenSearch index adapter stub for future cluster deployment."""

    def __init__(self, endpoint: str = "http://localhost:9200") -> None:
        self.endpoint = endpoint
        self.stats = IndexStats(index_name="opensearch_cluster")

    async def initialize(self) -> None:
        logger.info("OpenSearchAdapter initialized stub for endpoint: %s", self.endpoint)

    async def index_document(
        self, entity_type: str, document_id: str, data: dict[str, Any]
    ) -> None:
        pass

    async def delete_document(self, entity_type: str, document_id: str) -> None:
        pass

    async def reindex_all(self) -> IndexStats:
        self.stats.last_indexed_at = datetime.now(UTC)
        return self.stats
