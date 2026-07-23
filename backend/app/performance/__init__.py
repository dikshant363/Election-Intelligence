"""Performance, Scalability & Distributed Infrastructure package root."""

from app.performance.autoscaling import AutoscalingEngine
from app.performance.benchmark import BenchmarkRunner
from app.performance.cache import (
    CacheAdapter,
    CachePolicy,
    CacheService,
    MemoryCache,
    RedisAdapter,
    global_cache_service,
)
from app.performance.capacity import CapacityPlanner
from app.performance.exceptions import (
    BenchmarkError,
    CacheError,
    PerformanceException,
    RateLimitExceeded,
)
from app.performance.optimization import (
    CursorPaginator,
    StreamingResultOptimizer,
    compress_payload,
    decompress_payload,
)
from app.performance.pooling import ConnectionPoolMonitor, ReadReplicaRouter
from app.performance.ratelimit import SlidingWindowRateLimiter, TokenBucket
from app.performance.services import PerformanceService

__all__ = [
    "CacheService",
    "CacheAdapter",
    "MemoryCache",
    "RedisAdapter",
    "CachePolicy",
    "global_cache_service",
    "ConnectionPoolMonitor",
    "ReadReplicaRouter",
    "compress_payload",
    "decompress_payload",
    "CursorPaginator",
    "StreamingResultOptimizer",
    "SlidingWindowRateLimiter",
    "TokenBucket",
    "BenchmarkRunner",
    "AutoscalingEngine",
    "CapacityPlanner",
    "PerformanceService",
    "PerformanceException",
    "CacheError",
    "RateLimitExceeded",
    "BenchmarkError",
]
