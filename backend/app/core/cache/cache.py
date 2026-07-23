"""Cache abstraction contracts and placeholder implementations."""

from abc import ABC, abstractmethod
from typing import Any


class Cache[T](ABC):
    """Abstract cache service interface."""

    @abstractmethod
    async def get(self, key: str) -> T | None:
        """Retrieve a cached value by key."""
        pass

    @abstractmethod
    async def set(
        self,
        key: str,
        value: T,
        ttl_seconds: int | None = None,
    ) -> None:
        """Set a cached key-value pair with optional TTL."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a cached key."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cached keys."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a cached key exists."""
        pass


class MemoryCache(Cache[Any]):
    """In-memory dictionary cache implementation placeholder."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    async def get(self, key: str) -> Any | None:
        """Retrieve a value from the in-memory cache."""
        return self._store.get(key)

    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int | None = None,
    ) -> None:
        """Store a value in the in-memory cache."""
        _ = ttl_seconds
        self._store[key] = value

    async def delete(self, key: str) -> bool:
        """Remove a value from the in-memory cache."""
        if key in self._store:
            del self._store[key]
            return True
        return False

    async def clear(self) -> None:
        """Clear all keys in the in-memory cache."""
        self._store.clear()

    async def exists(self, key: str) -> bool:
        """Check if a key exists in the in-memory cache."""
        return key in self._store


class RedisCache[T](Cache[T], ABC):
    """Abstract placeholder contract for future Redis cache integration."""

    pass
