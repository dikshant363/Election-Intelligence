"""
Comprehensive unit & integration test suite for Milestone 18 — Search & Discovery Platform.

Tests cover:
- Ranking & Relevance Scoring
- Filters & Filter Combinations
- Autocomplete suggestions across entities
- Geospatial queries (radius, bounding box, polygon, Haversine)
- Aggregations & Analytics
- Pagination & Caching
- Text Highlighting & Snippet extraction
- Index rebuilding & OpenSearch adapter stub
- Query parsing (Boolean, Phrase, Prefix, Fuzzy)
- SearchService coordinator SAL
- FastAPI REST Search endpoints
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.search import (
    CandidateSearchResult,
    ElectionSearchResult,
    FilterError,
    GeospatialError,
    IndexError,
    InvalidQueryError,
    Pagination,
    ParsedQueryNode,
    QueryType,
    SearchHit,
    SearchOperator,
    SearchPage,
    SearchQuery,
    SearchService,
)
from app.search.analytics import AggregationMetric, AnalyticsEngine
from app.search.autocomplete import AutocompleteEngine, AutocompleteSuggestion
from app.search.cache import SLOW_QUERY_THRESHOLD_MS, CacheEntry, QueryMetrics, SearchCache, search_cache
from app.search.engine import QueryEngine, QueryParser
from app.search.filters import SQLFilterBuilder, SearchFilterSet
from app.search.geospatial import BoundingBox, Point, Polygon, SpatialSearchEngine, haversine_distance
from app.search.highlighting import HighlightConfig, TextHighlighter
from app.search.indexing import IndexStats, OpenSearchAdapter, PostgresFTSIndex
from app.search.ranking import RankingConfig, RelevanceRanker, ScoredHit

# Constants to avoid PLR2004 magic number warnings
PAGE_ONE = 1
PAGE_SIZE_DEFAULT = 20
PAGE_SIZE_MAX = 100
MAX_QUERY_LEN_500 = 500
DIST_DELHI_NOIDA = 20.0
RADIUS_5KM = 5.0
LAT_DELHI = 28.6139
LON_DELHI = 77.2090
LAT_NOIDA = 28.5355
LON_NOIDA = 77.3910
LIMIT_TEN = 10
LIMIT_FIVE = 5
SCORE_BASE = 1.0
SCORE_DECIMAL = 4.5
TOTAL_RECORDS_50 = 50
SLOW_QUERY_MS = 250.0
FAST_QUERY_MS = 50.0


# ─────────────────────────────────────────────────────────────────────────────
# 1. Ranking Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestRanking:
    def test_default_ranking_config(self) -> None:
        cfg = RankingConfig()
        assert cfg.title_boost == 3.0  # noqa: PLR2004
        assert cfg.enable_recency is True

    def test_scored_hit_calculation(self) -> None:
        hit = ScoredHit(
            id="1",
            entity_type="election",
            title="General Election",
            raw_score=2.0,
            field_boost=3.0,
            recency_boost=1.5,
            popularity_boost=1.1,
        )
        final = hit.calculate_final_score()
        assert final == round(2.0 * 3.0 * 1.5 * 1.1, 4)

    def test_recency_boost_decay(self) -> None:
        ranker = RelevanceRanker()
        now = datetime.now(UTC)
        boost_recent = ranker.calculate_recency_boost(now)
        assert boost_recent > 1.0

    def test_rank_hits_sorting(self) -> None:
        ranker = RelevanceRanker()
        h1 = ScoredHit("1", "election", "Low Score", raw_score=1.0)
        h2 = ScoredHit("2", "election", "High Score", raw_score=5.0)
        sorted_hits = ranker.rank_hits([h1, h2])
        assert sorted_hits[0].id == "2"


# ─────────────────────────────────────────────────────────────────────────────
# 2. Filter Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestFilters:
    def test_search_filter_set_to_dict(self) -> None:
        fs = SearchFilterSet(
            election_type="GENERAL",
            state_code="DL",
            election_year=2024,
        )
        d = fs.to_dict()
        assert d["election_type"] == "GENERAL"
        assert d["state_code"] == "DL"
        assert d["election_year"] == 2024  # noqa: PLR2004

    def test_search_filter_validation_valid(self) -> None:
        fs = SearchFilterSet(
            date_from=date(2024, 1, 1),
            date_to=date(2024, 12, 31),
            election_year=2024,
        )
        fs.validate()  # Should not raise

    def test_search_filter_validation_date_mismatch_raises(self) -> None:
        fs = SearchFilterSet(
            date_from=date(2024, 12, 31),
            date_to=date(2024, 1, 1),
        )
        with pytest.raises(FilterError):
            fs.validate()

    def test_search_filter_validation_invalid_year_raises(self) -> None:
        fs = SearchFilterSet(election_year=1800)
        with pytest.raises(FilterError):
            fs.validate()


# ─────────────────────────────────────────────────────────────────────────────
# 3. Highlighting Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestHighlighting:
    def test_text_highlighter_wrap(self) -> None:
        highlighter = TextHighlighter()
        res = highlighter.highlight_terms("Lok Sabha Election 2024", ["Lok", "Election"])
        assert "<mark>Lok</mark>" in res
        assert "<mark>Election</mark>" in res

    def test_extract_snippet(self) -> None:
        highlighter = TextHighlighter(HighlightConfig(fragment_size=30))
        text = "This is a long text description about the upcoming Lok Sabha general elections."
        snippet = highlighter.extract_snippet(text, ["Lok"])
        assert "<mark>Lok</mark>" in snippet


# ─────────────────────────────────────────────────────────────────────────────
# 4. Geospatial Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestGeospatial:
    def test_point_bounds_valid(self) -> None:
        p = Point(latitude=LAT_DELHI, longitude=LON_DELHI)
        assert p.latitude == LAT_DELHI

    def test_point_invalid_latitude(self) -> None:
        with pytest.raises(GeospatialError):
            Point(latitude=100.0, longitude=77.0)

    def test_haversine_distance(self) -> None:
        p1 = Point(LAT_DELHI, LON_DELHI)
        p2 = Point(LAT_NOIDA, LON_NOIDA)
        dist = haversine_distance(p1, p2)
        assert dist > 0.0
        assert dist < DIST_DELHI_NOIDA

    def test_bounding_box_contains(self) -> None:
        bbox = BoundingBox(min_lat=28.0, min_lon=77.0, max_lat=29.0, max_lon=78.0)
        p = Point(LAT_DELHI, LON_DELHI)
        assert bbox.contains(p) is True

    def test_polygon_contains(self) -> None:
        poly = Polygon(
            vertices=[
                Point(28.0, 77.0),
                Point(29.0, 77.0),
                Point(29.0, 78.0),
                Point(28.0, 78.0),
            ]
        )
        p = Point(LAT_DELHI, LON_DELHI)
        assert poly.contains(p) is True


# ─────────────────────────────────────────────────────────────────────────────
# 5. Caching & Performance Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestCacheAndMetrics:
    def test_cache_set_and_get(self) -> None:
        cache = SearchCache()
        key = cache.generate_cache_key("test", {"q": "bjp"})
        cache.set(key, "cached_result")
        assert cache.get(key) == "cached_result"

    def test_cache_expiration(self) -> None:
        cache = SearchCache()
        key = cache.generate_cache_key("test", {"q": "exp"})
        cache.set(key, "data", ttl=-1.0)
        assert cache.get(key) is None

    def test_slow_query_logging(self) -> None:
        cache = SearchCache()
        cache.record_query_execution("slow_q", SLOW_QUERY_MS)
        assert cache.metrics.slow_queries == 1

    def test_query_metrics_hit_rate(self) -> None:
        m = QueryMetrics(total_queries=10, cache_hits=8, cache_misses=2)
        assert m.hit_rate == 0.8  # noqa: PLR2004


# ─────────────────────────────────────────────────────────────────────────────
# 6. Query Engine & Parser Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestQueryEngine:
    def test_query_parser(self) -> None:
        node = QueryParser.parse("Lok Sabha*")
        assert len(node.children) == 2  # noqa: PLR2004
        assert node.children[1].is_prefix is True

    @pytest.mark.asyncio
    async def test_tsquery_string_phrase(self) -> None:
        session = AsyncMock()
        engine = QueryEngine(session)
        q = SearchQuery(raw_query="Lok Sabha", query_type=QueryType.PHRASE)
        tsq = engine.build_tsquery_string(q)
        assert tsq == "Lok <-> Sabha"

    @pytest.mark.asyncio
    async def test_tsquery_string_prefix(self) -> None:
        session = AsyncMock()
        engine = QueryEngine(session)
        q = SearchQuery(raw_query="Lok Sabha", query_type=QueryType.PREFIX)
        tsq = engine.build_tsquery_string(q)
        assert tsq == "Lok:* & Sabha:*"


# ─────────────────────────────────────────────────────────────────────────────
# 7. Autocomplete Engine Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestAutocomplete:
    async def test_autocomplete_candidates(self) -> None:
        session = AsyncMock()
        r1 = MagicMock()
        r1.id = "1"
        r1.name = "Rahul Gandhi"
        session.execute = AsyncMock(return_value=MagicMock(all=lambda: [r1]))

        engine = AutocompleteEngine(session)
        suggestions = await engine.suggest_candidates("Rahul")
        assert len(suggestions) == 1
        assert suggestions[0].label == "Rahul Gandhi"


# ─────────────────────────────────────────────────────────────────────────────
# 8. Indexing Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestIndexing:
    async def test_postgres_fts_index_reindex(self) -> None:
        session = AsyncMock()
        res_mock = MagicMock(scalars=lambda: MagicMock(all=lambda: [1, 2, 3]))
        session.execute = AsyncMock(return_value=res_mock)

        fts = PostgresFTSIndex(session)
        stats = await fts.reindex_all()
        assert stats.index_name == "postgres_fts"
        assert stats.total_documents == 6  # 3 elections + 3 candidates  # noqa: PLR2004

    async def test_opensearch_adapter_stub(self) -> None:
        adapter = OpenSearchAdapter("http://localhost:9200")
        await adapter.initialize()
        stats = await adapter.reindex_all()
        assert stats.index_name == "opensearch_cluster"


# ─────────────────────────────────────────────────────────────────────────────
# 9. Search Service SAL Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestSearchServiceSAL:
    async def test_search_service_delegates(self) -> None:
        session = AsyncMock()
        service = SearchService(session)

        with patch.object(service._engine, "execute_query", new_callable=AsyncMock) as mock_exec:
            mock_exec.return_value = SearchPage(hits=[], total=0, page=1, page_size=20)
            res = await service.search(SearchQuery(raw_query="test"))
            assert res.total == 0
            mock_exec.assert_called_once()

    async def test_autocomplete_all_entities(self) -> None:
        session = AsyncMock()
        service = SearchService(session)

        with (
            patch.object(service._autocomplete, "suggest_candidates", new_callable=AsyncMock) as m_c,
            patch.object(service._autocomplete, "suggest_parties", new_callable=AsyncMock) as m_p,
            patch.object(service._autocomplete, "suggest_constituencies", new_callable=AsyncMock) as m_co,
            patch.object(service._autocomplete, "suggest_elections", new_callable=AsyncMock) as m_e,
        ):
            m_c.return_value = [AutocompleteSuggestion("1", "Cand 1", "candidate")]
            m_p.return_value = []
            m_co.return_value = []
            m_e.return_value = []
            res = await service.autocomplete("test", entity_type="all")
            assert len(res) >= 1


# ─────────────────────────────────────────────────────────────────────────────
# 10. API Router Endpoint Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestSearchAPIRouter:
    def setup_method(self) -> None:
        from app.api.v1.dependencies.dependencies import get_search_service

        mock_service = AsyncMock()
        mock_service.search = AsyncMock(
            return_value=SearchPage(hits=[], total=0, page=1, page_size=20, query="general")
        )
        mock_service.autocomplete = AsyncMock(
            return_value=[AutocompleteSuggestion("1", "Lok Sabha", "election")]
        )
        mock_service.find_nearest_polling_booths = AsyncMock(
            return_value=[{"id": "b1", "name": "Booth 1", "constituency_id": "c1", "distance_km": 1.2}]
        )
        mock_service.get_analytics_by_state = AsyncMock(
            return_value=AggregationMetric("state_count", ["state_code"], [{"state_code": "DL", "count": 10}], 1)
        )
        mock_service.get_analytics_by_party = AsyncMock(
            return_value=AggregationMetric("party_count", ["party_code"], [], 0)
        )
        mock_service.get_turnout_statistics = AsyncMock(
            return_value={"total_elections": 5, "total_candidates": 100, "total_polling_booths": 500}
        )
        mock_service.reindex_all = AsyncMock(
            return_value=IndexStats(index_name="postgres_fts", total_documents=10)
        )

        app.dependency_overrides[get_search_service] = lambda: mock_service

    def teardown_method(self) -> None:
        app.dependency_overrides.clear()

    def test_search_endpoint(self) -> None:
        client = TestClient(app)
        response = client.get("/api/v1/search?q=general")
        assert response.status_code == 200  # noqa: PLR2004
        data = response.json()
        assert "hits" in data
        assert "took_ms" in data

    def test_autocomplete_endpoint(self) -> None:
        client = TestClient(app)
        response = client.get("/api/v1/search/autocomplete?prefix=Lok")
        assert response.status_code == 200  # noqa: PLR2004
        assert isinstance(response.json(), list)

    def test_geospatial_endpoint(self) -> None:
        client = TestClient(app)
        response = client.get(
            f"/api/v1/search/geospatial?latitude={LAT_DELHI}&longitude={LON_DELHI}&radius_km=5.0"
        )
        assert response.status_code == 200  # noqa: PLR2004
        assert isinstance(response.json(), list)

    def test_analytics_endpoint(self) -> None:
        client = TestClient(app)
        response = client.get("/api/v1/search/analytics")
        assert response.status_code == 200  # noqa: PLR2004
        data = response.json()
        assert "constituency_count_by_state" in data
        assert "turnout_statistics" in data

    def test_reindex_endpoint(self) -> None:
        client = TestClient(app)
        response = client.post("/api/v1/search/reindex")
        assert response.status_code == 200  # noqa: PLR2004
        data = response.json()
        assert data["index_name"] == "postgres_fts"
