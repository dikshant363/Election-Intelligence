"""FastAPI router for caching, benchmark execution, performance metrics, and capacity planning."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.dependencies import get_performance_service
from app.performance.schemas import (
    BenchmarkResultSchema,
    CacheStatsSchema,
    CapacityReportSchema,
    InvalidateCacheRequestSchema,
    InvalidateCacheResponseSchema,
    PerformanceMetricsSchema,
)
from app.performance.services import PerformanceService

router = APIRouter(tags=["Performance & Scalability"])


@router.get(
    "/cache",
    response_model=CacheStatsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get cache engine status and hit ratio statistics",
)
async def cache_stats(
    perf_service: Annotated[PerformanceService, Depends(get_performance_service)],
) -> CacheStatsSchema:
    """Return cache stats including hit count, miss count, and memory usage."""
    return perf_service.get_cache_stats()


@router.post(
    "/cache/invalidate",
    response_model=InvalidateCacheResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Invalidate cache entries matching pattern or tags",
)
async def invalidate_cache(
    req: InvalidateCacheRequestSchema,
    perf_service: Annotated[PerformanceService, Depends(get_performance_service)],
) -> InvalidateCacheResponseSchema:
    """Invalidate cache entries by key pattern or tags."""
    return await perf_service.invalidate_cache(req)


@router.get(
    "/performance",
    response_model=PerformanceMetricsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get overall system performance metrics and pool status",
)
async def performance_metrics(
    perf_service: Annotated[PerformanceService, Depends(get_performance_service)],
) -> PerformanceMetricsSchema:
    """Return performance metrics across cache, database connection pool, and rate limiting."""
    return perf_service.get_performance_summary()


@router.get(
    "/benchmark",
    response_model=BenchmarkResultSchema,
    status_code=status.HTTP_200_OK,
    summary="Execute synthetic performance benchmark scenario",
)
async def run_benchmark(
    scenario: Annotated[str, Query(description="Scenario name: rest_api, search, ai, etl")] = "rest_api",
    iterations: Annotated[int, Query(ge=1, le=1000)] = 100,
    perf_service: PerformanceService = Depends(get_performance_service),
) -> BenchmarkResultSchema:
    """Execute synthetic benchmark scenario measuring ops/sec and P95/P99 latencies."""
    return perf_service.run_benchmark(scenario=scenario, iterations=iterations)


@router.get(
    "/capacity",
    response_model=CapacityReportSchema,
    status_code=status.HTTP_200_OK,
    summary="Get capacity planning report and infrastructure growth projections",
)
async def capacity_report(
    target_users: Annotated[int, Query(ge=100, le=1000000)] = 10000,
    perf_service: PerformanceService = Depends(get_performance_service),
) -> CapacityReportSchema:
    """Return capacity estimations for concurrent users, RPS, memory, and database connections."""
    return perf_service.get_capacity_report(target_users=target_users)
