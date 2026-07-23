"""
Comprehensive unit & integration test suite for Milestone 22 — Performance, Scalability & Distributed Infrastructure.

Tests cover:
- Cache abstraction, MemoryCache TTL, compression, namespaces, tags
- RedisAdapter fallback mechanism
- Event-driven cache invalidation via EventBus
- ConnectionPoolMonitor & ReadReplicaRouter
- Performance optimizations (payload compression, cursor paginator, streaming optimizer)
- Rate limiting (SlidingWindowRateLimiter & TokenBucket)
- BenchmarkRunner scenarios & metrics
- AutoscalingEngine replica recommendations
- CapacityPlanner resource estimations
- PerformanceService coordinator
- FastAPI REST endpoints (/cache, /cache/invalidate, /performance, /benchmark, /capacity)
"""

from __future__ import annotations

import time
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies.dependencies import get_performance_service
from app.main import app
from app.performance import (
    AutoscalingEngine,
    BenchmarkRunner,
    CachePolicy,
    CapacityPlanner,
    ConnectionPoolMonitor,
    CursorPaginator,
    MemoryCache,
    PerformanceService,
    RateLimitExceeded,
    ReadReplicaRouter,
    RedisAdapter,
    SlidingWindowRateLimiter,
    StreamingResultOptimizer,
    TokenBucket,
    compress_payload,
    decompress_payload,
)
from app.performance.schemas import (
    BenchmarkResultSchema,
    CacheStatsSchema,
    CapacityReportSchema,
    InvalidateCacheResponseSchema,
    PerformanceMetricsSchema,
)
from app.realtime.eventbus import global_event_bus
from app.realtime.events import create_result_published_event

LATENCY_P95_10MS = 10.0
CAPACITY_USERS_10K = 10000
EXPECTED_2 = 2
EXPECTED_3 = 3
EXPECTED_4 = 4


# ─────────────────────────────────────────────────────────────────────────────
# 1. Caching & Invalidation Tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestCaching:
    async def test_memory_cache_get_set(self) -> None:
        cache = MemoryCache()
        pol = CachePolicy(ttl_seconds=3600, namespace="test", tags=["tag1"], compress=True)
        await cache.set("k1", {"foo": "bar"}, policy=pol)

        val = await cache.get("k1", namespace="test")
        assert val == {"foo": "bar"}

        stats = cache.get_stats()
        assert stats.hit_count == 1

    async def test_memory_cache_ttl_expiration(self) -> None:
        cache = MemoryCache()
        pol = CachePolicy(ttl_seconds=0, namespace="test")
        await cache.set("k_exp", "val", policy=pol)
        time.sleep(0.01)
        val = await cache.get("k_exp", namespace="test")
        assert val is None

    async def test_invalidate_pattern_and_tags(self) -> None:
        cache = MemoryCache()
        pol = CachePolicy(tags=["candidates"])
        await cache.set("cand_1", "meta", policy=pol)
        await cache.set("cand_2", "meta", policy=pol)

        count = await cache.invalidate_tags(["candidates"])
        assert count == EXPECTED_2

    async def test_redis_adapter_fallback(self) -> None:
        redis = RedisAdapter()
        await redis.set("rk", "rval")
        val = await redis.get("rk")
        assert val == "rval"
        assert redis.get_stats().provider == "redis (fallback)"


@pytest.mark.asyncio
class TestEventDrivenCacheInvalidation:
    async def test_event_bus_triggers_invalidation(self) -> None:
        cache_service = PerformanceService()
        await cache_service.cache_service.set("res_key", "data", policy=CachePolicy(tags=["results"]))

        # Publish result published event over EventBus
        evt = create_result_published_event(result_id="r1", election_id="e1", candidate_id="c1", votes=500)
        await global_event_bus.publish("results", evt)

        # Cache entry for tag "results" should be invalidated
        val = await cache_service.cache_service.get("res_key")
        assert val is None

        # Clean up event store for topic results
        if "results" in global_event_bus._event_store:
            global_event_bus._event_store["results"].clear()


# ─────────────────────────────────────────────────────────────────────────────
# 2. Connection Pooling & Optimizations Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestPoolingAndOptimizations:
    def test_connection_pool_monitor(self) -> None:
        monitor = ConnectionPoolMonitor()
        status = monitor.get_pool_status()
        assert "pool_size" in status

    def test_read_replica_router(self) -> None:
        router = ReadReplicaRouter()
        assert router.get_read_engine() is not None
        assert router.get_write_engine() is not None

    def test_compression_and_paginator(self) -> None:
        compressed = compress_payload("hello world")
        assert len(compressed) > 0
        decompressed = decompress_payload(compressed)
        assert decompressed == "hello world"

        cursor = CursorPaginator.encode_cursor("id_123", "2026-01-01")
        item_id, created = CursorPaginator.decode_cursor(cursor)
        assert item_id == "id_123"
        assert created == "2026-01-01"

    def test_streaming_optimizer(self) -> None:
        items = list(range(250))
        chunks = StreamingResultOptimizer.chunk_generator(items, chunk_size=100)
        assert len(chunks) == EXPECTED_3


# ─────────────────────────────────────────────────────────────────────────────
# 3. Rate Limiting Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestRateLimiting:
    def test_sliding_window_limiter(self) -> None:
        limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=60.0)
        assert limiter.check_rate_limit("user_1") is True
        assert limiter.check_rate_limit("user_1") is True
        assert limiter.check_rate_limit("user_1") is False

        with pytest.raises(RateLimitExceeded):
            limiter.enforce_rate_limit("user_1")

    def test_token_bucket(self) -> None:
        bucket = TokenBucket(capacity=2, refill_rate_per_sec=10.0)
        assert bucket.consume(1) is True
        assert bucket.consume(1) is True
        assert bucket.consume(1) is False


# ─────────────────────────────────────────────────────────────────────────────
# 4. Benchmark, Autoscaling & Capacity Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestBenchmarkAndCapacity:
    def test_benchmark_runner(self) -> None:
        res = BenchmarkRunner.run_benchmark("test_scenario", iterations=50)
        assert res.scenario == "test_scenario"
        assert res.throughput_ops_per_sec >= 0.0

    def test_autoscaling_engine(self) -> None:
        rec = AutoscalingEngine.evaluate_component("workers", current_replicas=2, cpu_pct=90.0, memory_pct=80.0)
        assert rec.recommended_replicas == EXPECTED_4

    def test_capacity_planner(self) -> None:
        report = CapacityPlanner.estimate_capacity(target_concurrent_users=CAPACITY_USERS_10K)
        assert report.max_concurrent_users == CAPACITY_USERS_10K
        assert report.estimated_max_rps > 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 5. PerformanceService & Router Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestPerformanceAPIRouter:
    def setup_method(self) -> None:
        mock_service = AsyncMock()
        mock_service.get_cache_stats = MagicMock(
            return_value=CacheStatsSchema(
                provider="memory",
                keys_count=10,
                hit_count=50,
                miss_count=5,
                hit_ratio=0.909,
                memory_used_bytes=1024,
            )
        )
        mock_service.invalidate_cache = AsyncMock(
            return_value=InvalidateCacheResponseSchema(keys_invalidated=3, status="success")
        )
        mock_service.get_performance_summary = MagicMock(
            return_value=PerformanceMetricsSchema(
                cache=CacheStatsSchema(
                    provider="memory",
                    keys_count=10,
                    hit_count=50,
                    miss_count=5,
                    hit_ratio=0.909,
                    memory_used_bytes=1024,
                ),
                db_pool_active=2,
                db_pool_size=20,
                compression_enabled=True,
                rate_limit_policy="sliding_window",
            )
        )
        mock_service.run_benchmark = MagicMock(
            return_value=BenchmarkResultSchema(
                scenario="rest_api",
                operations_count=100,
                total_duration_sec=0.5,
                throughput_ops_per_sec=200.0,
                avg_latency_ms=2.5,
                p95_latency_ms=5.0,
                p99_latency_ms=LATENCY_P95_10MS,
            )
        )
        mock_service.get_capacity_report = MagicMock(
            return_value=CapacityReportSchema(
                max_concurrent_users=CAPACITY_USERS_10K,
                estimated_max_rps=2000.0,
                recommended_db_connections=50,
                recommended_redis_memory_mb=1024,
                projected_storage_gb_per_month=150.0,
            )
        )

        app.dependency_overrides[get_performance_service] = lambda: mock_service

    def teardown_method(self) -> None:
        app.dependency_overrides.clear()

    def test_cache_stats_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/cache")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["provider"] == "memory"

    def test_cache_invalidate_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.post("/api/v1/cache/invalidate", json={"tags": ["results"]})
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["keys_invalidated"] == EXPECTED_3

    def test_performance_metrics_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/performance")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["compression_enabled"] is True

    def test_benchmark_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/benchmark?scenario=rest_api")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["scenario"] == "rest_api"

    def test_capacity_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/capacity?target_users=10000")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["max_concurrent_users"] == CAPACITY_USERS_10K
