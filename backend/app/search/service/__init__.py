"""
Search service: high-level coordinator for all search operations.

This is the single entry point for the API layer and application handlers
to invoke search. It delegates to the engine and facets modules.
No direct SQL here — all SQL lives in engine/ and facets/.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.search.engine import (
    autocomplete,
    geo_search_polling_booths,
    search_candidates,
    search_constituencies,
    search_elections,
    search_parties,
)
from app.search.exceptions import SavedSearchError
from app.search.facets import (
    aggregate_candidates_by_party,
    aggregate_constituencies_by_state,
    compute_data_quality_metrics,
    get_candidate_facets,
    get_constituency_facets,
    get_election_facets,
)
from app.search.queries import (
    AutocompleteQuery,
    CandidateSearchQuery,
    ConstituencySearchQuery,
    ElectionSearchQuery,
    GeoSearchQuery,
    PartySearchQuery,
)
from app.search.results import (
    AggregationResult,
    AutocompleteResult,
    CandidateSearchResult,
    ConstituencySearchResult,
    ElectionSearchResult,
    FacetResult,
    PartySearchResult,
    SearchPage,
)
from app.search.saved import SavedSearchModel


class SearchService:
    """
    Unified search service.
    Coordinates full-text search, facets, aggregations, autocomplete, geo-search,
    and saved search management through a single coherent interface.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── Full-text search ──────────────────────────────────────────────────────

    async def search_elections(
        self, query: ElectionSearchQuery
    ) -> tuple[SearchPage, list[ElectionSearchResult]]:
        return await search_elections(self._session, query)

    async def search_candidates(
        self, query: CandidateSearchQuery
    ) -> tuple[SearchPage, list[CandidateSearchResult]]:
        return await search_candidates(self._session, query)

    async def search_parties(
        self, query: PartySearchQuery
    ) -> tuple[SearchPage, list[PartySearchResult]]:
        return await search_parties(self._session, query)

    async def search_constituencies(
        self, query: ConstituencySearchQuery
    ) -> tuple[SearchPage, list[ConstituencySearchResult]]:
        return await search_constituencies(self._session, query)

    # ── Autocomplete ──────────────────────────────────────────────────────────

    async def autocomplete(self, query: AutocompleteQuery) -> list[AutocompleteResult]:
        return await autocomplete(self._session, query)

    # ── Geo search ────────────────────────────────────────────────────────────

    async def geo_search(
        self, query: GeoSearchQuery
    ) -> tuple[SearchPage, list[dict[str, Any]]]:
        return await geo_search_polling_booths(self._session, query)

    # ── Facets ────────────────────────────────────────────────────────────────

    async def election_facets(self) -> list[FacetResult]:
        return await get_election_facets(self._session)

    async def constituency_facets(self) -> list[FacetResult]:
        return await get_constituency_facets(self._session)

    async def candidate_facets(self) -> list[FacetResult]:
        return await get_candidate_facets(self._session)

    # ── Aggregations ──────────────────────────────────────────────────────────

    async def candidates_by_party(self) -> AggregationResult:
        return await aggregate_candidates_by_party(self._session)

    async def constituencies_by_state(self) -> AggregationResult:
        return await aggregate_constituencies_by_state(self._session)

    # ── Data quality metrics ──────────────────────────────────────────────────

    async def data_quality_metrics(self, entity: str) -> dict[str, Any]:
        return await compute_data_quality_metrics(self._session, entity)

    # ── Saved searches ────────────────────────────────────────────────────────

    async def save_search(
        self,
        name: str,
        entity_type: str,
        query_params: dict[str, Any],
        created_by: str | None = None,
        description: str | None = None,
    ) -> SavedSearchModel:
        """Persist a named search query for future re-execution."""
        try:
            saved = SavedSearchModel(
                name=name,
                entity_type=entity_type,
                query_params=json.dumps(query_params, ensure_ascii=False),
                created_by=created_by,
                description=description,
                run_count=0,
            )
            self._session.add(saved)
            await self._session.flush()
            return saved
        except Exception as exc:
            raise SavedSearchError(f"Failed to save search '{name}': {exc}") from exc

    async def get_saved_searches(
        self, created_by: str | None = None
    ) -> list[SavedSearchModel]:
        """Retrieve saved searches, optionally filtered by user."""
        stmt = select(SavedSearchModel).order_by(SavedSearchModel.created_at.desc())
        if created_by:
            stmt = stmt.where(SavedSearchModel.created_by == created_by)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def record_search_run(self, saved_search_id: str) -> None:
        """Increment run_count and update last_run_at for a saved search."""
        try:
            uid = uuid.UUID(saved_search_id)
        except ValueError as exc:
            raise SavedSearchError(f"Invalid saved search ID: {saved_search_id}") from exc

        stmt = (
            update(SavedSearchModel)
            .where(SavedSearchModel.id == uid)
            .values(
                run_count=SavedSearchModel.run_count + 1,
                last_run_at=datetime.now(UTC),
            )
        )
        await self._session.execute(stmt)
        await self._session.flush()
