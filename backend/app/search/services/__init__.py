"""Search Application Service coordinating the Search Abstraction Layer (SAL)."""

from __future__ import annotations

import time
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.search.analytics import AggregationMetric, AnalyticsEngine
from app.search.autocomplete import AutocompleteEngine, AutocompleteSuggestion
from app.search.cache import search_cache
from app.search.engine import QueryEngine
from app.search.geospatial import BoundingBox, Point, SpatialSearchEngine
from app.search.indexing import IndexStats, PostgresFTSIndex
from app.search.queries import SearchQuery
from app.search.results import SearchPage


class SearchService:
    """
    Search Abstraction Layer (SAL) coordinator service.
    Exposes unified search, autocomplete, geospatial, analytics, and index management
    operations to the Application and API layers.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._engine = QueryEngine(session)
        self._autocomplete = AutocompleteEngine(session)
        self._spatial = SpatialSearchEngine(session)
        self._analytics = AnalyticsEngine(session)
        self._indexer = PostgresFTSIndex(session)
        self._cache = search_cache

    async def search(self, query: SearchQuery) -> SearchPage:
        """Execute search with caching, metrics, and slow query logging."""
        cache_key = self._cache.generate_cache_key(
            "search",
            {"q": query.raw_query, "type": query.query_type, "page": query.pagination.page},
        )

        if query.enable_cache:
            cached_page = self._cache.get(cache_key)
            if cached_page is not None:
                return cached_page

        t0 = time.monotonic()
        page = await self._engine.execute_query(query)
        duration_ms = (time.monotonic() - t0) * 1000.0

        self._cache.record_query_execution("search_query", duration_ms)

        if query.enable_cache:
            self._cache.set(cache_key, page)

        return page

    async def autocomplete(
        self, prefix: str, entity_type: str = "all", limit: int = 10
    ) -> list[AutocompleteSuggestion]:
        """Fetch prefix autocomplete suggestions across domain entities."""
        if entity_type == "candidate":
            return await self._autocomplete.suggest_candidates(prefix, limit)
        if entity_type == "party":
            return await self._autocomplete.suggest_parties(prefix, limit)
        if entity_type == "constituency":
            return await self._autocomplete.suggest_constituencies(prefix, limit)
        if entity_type == "election":
            return await self._autocomplete.suggest_elections(prefix, limit)

        # "all" - aggregate top items from each entity
        per_entity_limit = max(1, limit // 4)
        results: list[AutocompleteSuggestion] = []

        cand = await self._autocomplete.suggest_candidates(prefix, per_entity_limit)
        party = await self._autocomplete.suggest_parties(prefix, per_entity_limit)
        const = await self._autocomplete.suggest_constituencies(prefix, per_entity_limit)
        elec = await self._autocomplete.suggest_elections(prefix, per_entity_limit)

        results.extend(cand)
        results.extend(party)
        results.extend(const)
        results.extend(elec)

        return results[:limit]

    async def find_nearest_polling_booths(
        self, latitude: float, longitude: float, radius_km: float = 5.0, limit: int = 10
    ) -> list[dict[str, Any]]:
        """Geospatial proximity search for polling booths."""
        center = Point(latitude=latitude, longitude=longitude)
        return await self._spatial.find_nearest_polling_booths(center, radius_km, limit)

    async def search_bounding_box(
        self, min_lat: float, min_lon: float, max_lat: float, max_lon: float, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Geospatial bounding box search."""
        bbox = BoundingBox(min_lat=min_lat, min_lon=min_lon, max_lat=max_lat, max_lon=max_lon)
        return await self._spatial.search_bounding_box(bbox, limit)

    async def get_analytics_by_state(self) -> AggregationMetric:
        """Get constituency count by state."""
        return await self._analytics.count_by_state()

    async def get_analytics_by_party(self) -> AggregationMetric:
        """Get candidate count by party."""
        return await self._analytics.count_by_party()

    async def get_turnout_statistics(self) -> dict[str, Any]:
        """Get turnout and totals statistics."""
        return await self._analytics.get_turnout_statistics()

    async def reindex_all(self) -> IndexStats:
        """Perform full reindex of search indices."""
        return await self._indexer.reindex_all()
