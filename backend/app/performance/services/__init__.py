"""Performance Layer Application Service coordinator."""

from __future__ import annotations

from app.performance.autoscaling import AutoscalingEngine
from app.performance.benchmark import BenchmarkRunner
from app.performance.cache import CacheService, global_cache_service
from app.performance.capacity import CapacityPlanner
from app.performance.pooling import ConnectionPoolMonitor
from app.performance.ratelimit import SlidingWindowRateLimiter
from app.performance.schemas import (
    AutoscalingRecommendationSchema,
    BenchmarkResultSchema,
    CacheStatsSchema,
    CapacityReportSchema,
    InvalidateCacheRequestSchema,
    InvalidateCacheResponseSchema,
    PerformanceMetricsSchema,
)


class PerformanceService:
    """
    Performance Application Service.
    Coordinates distributed caching, database pool monitoring, load benchmarks,
    rate limiting, autoscaling, and capacity planning.
    """

    def __init__(
        self,
        cache_service: CacheService | None = None,
        pool_monitor: ConnectionPoolMonitor | None = None,
        rate_limiter: SlidingWindowRateLimiter | None = None,
    ) -> None:
        self.cache_service = cache_service or global_cache_service
        self.pool_monitor = pool_monitor or ConnectionPoolMonitor()
        self.rate_limiter = rate_limiter or SlidingWindowRateLimiter()

    def get_cache_stats(self) -> CacheStatsSchema:
        """Get cache engine statistics and hit ratio."""
        return self.cache_service.get_stats()

    async def invalidate_cache(
        self, req: InvalidateCacheRequestSchema
    ) -> InvalidateCacheResponseSchema:
        """Invalidate cache keys matching pattern or tags."""
        count = 0
        if req.pattern:
            count += await self.cache_service.invalidate_pattern(req.pattern)
        if req.tags:
            count += await self.cache_service.invalidate_tags(req.tags)

        return InvalidateCacheResponseSchema(keys_invalidated=count, status="success")

    def get_performance_summary(self) -> PerformanceMetricsSchema:
        """Get overall system performance metrics summary."""
        pool_status = self.pool_monitor.get_pool_status()
        return PerformanceMetricsSchema(
            cache=self.cache_service.get_stats(),
            db_pool_active=pool_status["checkedout"],
            db_pool_size=pool_status["pool_size"],
            compression_enabled=True,
            rate_limit_policy="sliding_window",
        )

    def run_benchmark(self, scenario: str = "rest_api", iterations: int = 100) -> BenchmarkResultSchema:
        """Execute performance benchmark scenario."""
        return BenchmarkRunner.run_benchmark(scenario_name=scenario, iterations=iterations)

    def get_capacity_report(self, target_users: int = 10000) -> CapacityReportSchema:
        """Get capacity estimation report and growth projections."""
        return CapacityPlanner.estimate_capacity(target_concurrent_users=target_users)

    def get_autoscaling_recommendations(self) -> list[AutoscalingRecommendationSchema]:
        """Get component horizontal scaling recommendations."""
        return [
            AutoscalingEngine.evaluate_component("api_workers", current_replicas=3, cpu_pct=45.0, memory_pct=50.0),
            AutoscalingEngine.evaluate_component("background_workers", current_replicas=2, cpu_pct=85.0, memory_pct=70.0, queue_depth=60),
            AutoscalingEngine.evaluate_component("search_indexers", current_replicas=2, cpu_pct=15.0, memory_pct=25.0),
        ]
