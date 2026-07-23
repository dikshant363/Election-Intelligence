"""Search repository data access layer."""

from __future__ import annotations

import time

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.models import CandidateModel, ElectionModel
from app.search.queries import SearchQuery


class SearchRepository:
    """Provides standard repository abstraction for search queries against PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def execute_fts_election_query(
        self, query: SearchQuery
    ) -> tuple[list[ElectionModel], int, float]:
        """Execute full-text search against elections table."""
        t0 = time.monotonic()
        stmt = select(ElectionModel).where(ElectionModel.deleted_at.is_(None))

        if query.raw_query:
            tsq = " & ".join(f"{t}:*" for t in query.raw_query.split() if t)
            if tsq:
                tsvector = func.to_tsvector("english", ElectionModel.title)
                stmt = stmt.where(tsvector.op("@@")(func.to_tsquery("english", tsq)))

        # Count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self._session.execute(count_stmt)).scalar_one()

        # Paginate
        stmt = stmt.offset(query.pagination.offset).limit(query.pagination.page_size)
        results = (await self._session.execute(stmt)).scalars().all()
        took_ms = (time.monotonic() - t0) * 1000.0

        return list(results), total, took_ms

    async def execute_fts_candidate_query(
        self, query: SearchQuery
    ) -> tuple[list[CandidateModel], int, float]:
        """Execute full-text search against candidates table."""
        t0 = time.monotonic()
        stmt = select(CandidateModel).where(CandidateModel.deleted_at.is_(None))

        if query.raw_query:
            tsq = " & ".join(f"{t}:*" for t in query.raw_query.split() if t)
            if tsq:
                tsvector = func.to_tsvector("english", CandidateModel.name)
                stmt = stmt.where(tsvector.op("@@")(func.to_tsquery("english", tsq)))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self._session.execute(count_stmt)).scalar_one()

        stmt = stmt.offset(query.pagination.offset).limit(query.pagination.page_size)
        results = (await self._session.execute(stmt)).scalars().all()
        took_ms = (time.monotonic() - t0) * 1000.0

        return list(results), total, took_ms
