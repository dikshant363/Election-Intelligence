"""In-memory LRU search cache with TTL, query metrics, and slow query logging."""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger("app.search.cache")

SLOW_QUERY_THRESHOLD_MS = 200.0


@dataclass
class CacheEntry:
    """Cached search query result entry."""

    key: str
    value: Any
    created_at: float = field(default_factory=time.monotonic)
    ttl_seconds: float = 300.0

    @property
    def is_expired(self) -> bool:
        return (time.monotonic() - self.created_at) > self.ttl_seconds


@dataclass
class QueryMetrics:
    """Performance metrics counter for search operations."""

    total_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    slow_queries: int = 0
    total_execution_time_ms: float = 0.0

    @property
    def hit_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return round(self.cache_hits / self.total_queries, 4)

    @property
    def avg_execution_time_ms(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return round(self.total_execution_time_ms / self.total_queries, 2)


class SearchCache:
    """In-memory search cache with key hashing and query metric tracking."""

    def __init__(self, default_ttl: float = 300.0, max_entries: int = 1000) -> None:
        self.default_ttl = default_ttl
        self.max_entries = max_entries
        self._cache: dict[str, CacheEntry] = {}
        self.metrics = QueryMetrics()

    @staticmethod
    def generate_cache_key(prefix: str, params: dict[str, Any]) -> str:
        """Generate a deterministic SHA-256 cache key from query parameters."""
        param_str = json.dumps(params, sort_keys=True, default=str)
        hashed = hashlib.sha256(param_str.encode("utf-8")).hexdigest()[:16]
        return f"{prefix}:{hashed}"

    def get(self, key: str) -> Any | None:
        """Retrieve cached result if present and not expired."""
        self.metrics.total_queries += 1
        entry = self._cache.get(key)
        if entry is None or entry.is_expired:
            if entry:
                del self._cache[key]
            self.metrics.cache_misses += 1
            return None
        self.metrics.cache_hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Store result in cache, evicting oldest if max_entries reached."""
        if len(self._cache) >= self.max_entries:
            # Simple eviction of first key
            first_key = next(iter(self._cache))
            del self._cache[first_key]

        effective_ttl = ttl if ttl is not None else self.default_ttl
        self._cache[key] = CacheEntry(key=key, value=value, ttl_seconds=effective_ttl)

    def invalidate_all(self) -> None:
        """Clear all entries in cache."""
        self._cache.clear()

    def record_query_execution(self, query_name: str, duration_ms: float) -> None:
        """Record query execution time and log slow queries."""
        self.metrics.total_execution_time_ms += duration_ms
        if duration_ms >= SLOW_QUERY_THRESHOLD_MS:
            self.metrics.slow_queries += 1
            logger.warning(
                "SLOW QUERY LOG: '%s' took %.2f ms (threshold: %.0f ms)",
                query_name,
                duration_ms,
                SLOW_QUERY_THRESHOLD_MS,
            )


# Global singleton instance
search_cache = SearchCache()
