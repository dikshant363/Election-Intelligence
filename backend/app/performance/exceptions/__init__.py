"""Performance Layer exception hierarchy."""

from __future__ import annotations


class PerformanceException(Exception):
    """Base exception for all performance and scaling operations."""

    def __init__(self, message: str, code: str = "PERFORMANCE_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class CacheError(PerformanceException):
    """Raised when a cache operation (get/set/invalidate) fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CACHE_ERROR")


class RateLimitExceeded(PerformanceException):
    """Raised when rate limits are exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message, code="RATE_LIMIT_EXCEEDED")


class BenchmarkError(PerformanceException):
    """Raised when benchmark runner encounters an error."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="BENCHMARK_ERROR")
