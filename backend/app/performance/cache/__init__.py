"""Cache abstraction, Memory & Redis adapters, and event-driven invalidation."""

from __future__ import annotations

import fnmatch
import json
import time
import zlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from app.observability.logging import get_structured_logger
from app.performance.schemas import CacheStatsSchema
from app.realtime.eventbus import global_event_bus

logger = get_structured_logger("app.performance.cache")


@dataclass
class CachePolicy:
    """Cache entry policy controlling TTL, namespace, tags, and compression."""

    ttl_seconds: int = 3600
    namespace: str = "default"
    tags: list[str] = field(default_factory=list)
    compress: bool = False


@dataclass
class CacheEntry:
    """Internal cache entry wrapper."""

    key: str
    value: bytes
    policy: CachePolicy
    expires_at: float
    created_at: float = field(default_factory=time.monotonic)


class CacheAdapter(ABC):
    """Abstract base class for cache adapters (Memory, Redis, KeyDB, Dragonfly, Valkey)."""

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, policy: CachePolicy | None = None) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def invalidate_pattern(self, pattern: str) -> int:
        pass

    @abstractmethod
    async def invalidate_tags(self, tags: list[str]) -> int:
        pass

    @abstractmethod
    def get_stats(self) -> CacheStatsSchema:
        pass


class MemoryCache(CacheAdapter):
    """In-memory cache implementation with TTL, namespaces, tags, and compression."""

    def __init__(self) -> None:
        self._store: dict[str, CacheEntry] = {}
        self._hits: int = 0
        self._misses: int = 0

    def _full_key(self, key: str, namespace: str) -> str:
        return f"{namespace}:{key}"

    async def get(self, key: str, namespace: str = "default") -> Any | None:
        fkey = self._full_key(key, namespace)
        entry = self._store.get(fkey)
        if not entry:
            self._misses += 1
            return None

        if time.monotonic() > entry.expires_at:
            del self._store[fkey]
            self._misses += 1
            return None

        self._hits += 1
        raw_bytes = entry.value
        if entry.policy.compress:
            raw_bytes = zlib.decompress(raw_bytes)
        return json.loads(raw_bytes.decode("utf-8"))

    async def set(self, key: str, value: Any, policy: CachePolicy | None = None) -> None:
        pol = policy or CachePolicy()
        fkey = self._full_key(key, pol.namespace)
        raw_json = json.dumps(value).encode("utf-8")
        if pol.compress:
            raw_json = zlib.compress(raw_json)

        expires_at = time.monotonic() + pol.ttl_seconds
        self._store[fkey] = CacheEntry(
            key=fkey, value=raw_json, policy=pol, expires_at=expires_at
        )

    async def delete(self, key: str, namespace: str = "default") -> None:
        fkey = self._full_key(key, namespace)
        self._store.pop(fkey, None)

    async def invalidate_pattern(self, pattern: str) -> int:
        count = 0
        matching = [k for k in self._store if fnmatch.fnmatch(k, pattern)]
        for k in matching:
            del self._store[k]
            count += 1
        return count

    async def invalidate_tags(self, tags: list[str]) -> int:
        target_tags = set(tags)
        matching = [
            k
            for k, entry in self._store.items()
            if target_tags.intersection(set(entry.policy.tags))
        ]
        for k in matching:
            del self._store[k]
        return len(matching)

    def get_stats(self) -> CacheStatsSchema:
        total = self._hits + self._misses
        ratio = round(self._hits / total, 3) if total > 0 else 1.0
        used_mem = sum(len(e.value) for e in self._store.values())
        return CacheStatsSchema(
            provider="memory",
            keys_count=len(self._store),
            hit_count=self._hits,
            miss_count=self._misses,
            hit_ratio=ratio,
            memory_used_bytes=used_mem,
        )


class RedisAdapter(CacheAdapter):
    """
    Redis cache adapter stub with extension path for KeyDB, Dragonfly, and Valkey.
    Falls back gracefully to MemoryCache if Redis connection is unavailable.
    """

    def __init__(self, fallback: MemoryCache | None = None) -> None:
        self._fallback = fallback or MemoryCache()

    async def get(self, key: str) -> Any | None:
        return await self._fallback.get(key)

    async def set(self, key: str, value: Any, policy: CachePolicy | None = None) -> None:
        await self._fallback.set(key, value, policy)

    async def delete(self, key: str) -> None:
        await self._fallback.delete(key)

    async def invalidate_pattern(self, pattern: str) -> int:
        return await self._fallback.invalidate_pattern(pattern)

    async def invalidate_tags(self, tags: list[str]) -> int:
        return await self._fallback.invalidate_tags(tags)

    def get_stats(self) -> CacheStatsSchema:
        stats = self._fallback.get_stats()
        return CacheStatsSchema(
            provider="redis (fallback)",
            keys_count=stats.keys_count,
            hit_count=stats.hit_count,
            miss_count=stats.miss_count,
            hit_ratio=stats.hit_ratio,
            memory_used_bytes=stats.memory_used_bytes,
        )


class CacheService:
    """
    Unified Cache Application Service.
    Integrates memory & distributed caching with EventBus for event-driven invalidation.
    """

    def __init__(self, adapter: CacheAdapter | None = None) -> None:
        self.adapter = adapter or MemoryCache()
        self._setup_event_listeners()

    def _setup_event_listeners(self) -> None:
        """Subscribe to EventBus domain events for automatic cache invalidation."""

        async def _on_result_published(event: Any) -> None:
            logger.info("Event-driven cache invalidation triggered by ResultPublished")
            await self.adapter.invalidate_tags(["results", "elections"])

        async def _on_candidate_updated(event: Any) -> None:
            await self.adapter.invalidate_tags(["candidates"])

        global_event_bus.subscribe("results", _on_result_published)
        global_event_bus.subscribe("candidates", _on_candidate_updated)

    async def get(self, key: str, namespace: str = "default") -> Any | None:
        if isinstance(self.adapter, MemoryCache):
            return await self.adapter.get(key, namespace=namespace)
        return await self.adapter.get(key)

    async def set(self, key: str, value: Any, policy: CachePolicy | None = None) -> None:
        await self.adapter.set(key, value, policy)

    async def invalidate_pattern(self, pattern: str) -> int:
        return await self.adapter.invalidate_pattern(pattern)

    async def invalidate_tags(self, tags: list[str]) -> int:
        return await self.adapter.invalidate_tags(tags)

    def get_stats(self) -> CacheStatsSchema:
        return self.adapter.get_stats()


# Global cache service instance
global_cache_service = CacheService()
