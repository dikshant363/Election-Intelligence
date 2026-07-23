"""Pydantic v2 schemas for Performance & Scalability APIs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CacheStatsSchema(BaseModel):
    """Cache engine statistics."""

    model_config = ConfigDict(frozen=True)

    provider: str = Field(..., description="memory, redis, dragonfly, keydb")
    keys_count: int
    hit_count: int
    miss_count: int
    hit_ratio: float
    memory_used_bytes: int


class InvalidateCacheRequestSchema(BaseModel):
    """Cache invalidation request."""

    model_config = ConfigDict(frozen=True)

    pattern: str | None = None
    namespace: str | None = None
    tags: list[str] = Field(default_factory=list)


class InvalidateCacheResponseSchema(BaseModel):
    """Cache invalidation output response."""

    model_config = ConfigDict(frozen=True)

    keys_invalidated: int
    status: str = "success"


class PerformanceMetricsSchema(BaseModel):
    """Overall system performance summary."""

    model_config = ConfigDict(frozen=True)

    cache: CacheStatsSchema
    db_pool_active: int
    db_pool_size: int
    compression_enabled: bool
    rate_limit_policy: str


class BenchmarkResultSchema(BaseModel):
    """Benchmark test result summary."""

    model_config = ConfigDict(frozen=True)

    scenario: str
    operations_count: int
    total_duration_sec: float
    throughput_ops_per_sec: float
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float


class AutoscalingRecommendationSchema(BaseModel):
    """Autoscaling metrics and node recommendations."""

    model_config = ConfigDict(frozen=True)

    component: str
    current_replicas: int
    recommended_replicas: int
    cpu_utilization_pct: float
    memory_utilization_pct: float
    scaling_reason: str


class CapacityReportSchema(BaseModel):
    """Capacity planning and growth projections."""

    model_config = ConfigDict(frozen=True)

    max_concurrent_users: int
    estimated_max_rps: float
    recommended_db_connections: int
    recommended_redis_memory_mb: int
    projected_storage_gb_per_month: float
