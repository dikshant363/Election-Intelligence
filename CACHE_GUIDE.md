# Cache Abstraction & Event-Driven Invalidation Guide

## Overview

The `CacheService` abstraction provides multi-level caching (In-Memory + Redis/KeyDB/Dragonfly/Valkey) with event-driven invalidation via `EventBus`.

---

## Cache Policy Configuration

```python
from app.performance.cache import CachePolicy, global_cache_service

policy = CachePolicy(
    ttl_seconds=3600,
    namespace="results",
    tags=["results", "elections"],
    compress=True,
)

await global_cache_service.set("result_2024_up", {"votes": 500000}, policy=policy)
```

---

## Event-Driven Cache Invalidation

The `CacheService` subscribes to EventBus events:
- `ResultPublished` -> Invalidates tags `["results", "elections"]`
- `CandidateUpdated` -> Invalidates tag `["candidates"]`

```text
Domain Action (Result Published)
        ↓
  EventBus Publish
        ↓
  CacheService Subscriber
        ↓
  Tag Invalidation (keys purged automatically)
```
