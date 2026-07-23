"""Unit tests for cache abstraction and MemoryCache."""

import pytest

from app.core.cache import MemoryCache


@pytest.mark.asyncio
async def test_memory_cache_operations() -> None:
    """Verify MemoryCache get, set, delete, exists, and clear."""
    cache = MemoryCache()

    # Exists & Get on empty
    assert await cache.exists("key1") is False
    assert await cache.get("key1") is None

    # Set & Get
    await cache.set("key1", "value1")
    assert await cache.exists("key1") is True
    assert await cache.get("key1") == "value1"

    # Delete
    deleted = await cache.delete("key1")
    assert deleted is True
    assert await cache.exists("key1") is False

    # Clear
    await cache.set("key2", "value2")
    await cache.clear()
    assert await cache.exists("key2") is False
