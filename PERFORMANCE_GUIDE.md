# Performance Guide

## 1. Performance Philosophy and Targets
The Election Intelligence Platform is built with performance as a first-class feature. Our targets are:
- **API Response Time**: < 100ms (p95)
- **Search Latency**: < 200ms (p95)
- **Authentication**: < 100ms
- **Dashboard Load**: < 1s
- **Mobile App Startup**: < 2s

## 2. CacheService Architecture
Located in `backend/app/performance/`, the `CacheService` supports two backends:
- **MemoryCache**: For local development and single-node setups.
- **RedisCache**: For production deployments.
Supports tag-based invalidation to clear related keys simultaneously.

```python
await cache_service.set("key", value, tags=["election_1"])
await cache_service.invalidate_by_tag("election_1")
```

## 3. Caching Strategy
- **Read-heavy endpoints**: Cached for 5-15 minutes (e.g., constituency lists).
- **Static data**: Cached for 24 hours.
- **Cache-aside pattern**: Read from cache, if miss, read from DB and populate cache.
- **Invalidation**: On write operations, corresponding tags are invalidated immediately.

## 4. Connection Pool Configuration
We use SQLAlchemy with AsyncPG. The connection pool is tuned as follows:
- `DB_POOL_SIZE=5`
- `DB_MAX_OVERFLOW=10`
- `DB_POOL_TIMEOUT=30`
- `DB_POOL_RECYCLE=1800`
- `pool_pre_ping=True` (Ensures connections are alive before use).

## 5. Rate Limiting
Implemented via a sliding window algorithm in `backend/app/performance/`.
- Default: 100 requests / minute per IP.
- Headers returned: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

## 6. Async Patterns
- **Always async/await**: Never block the event loop.
- **No blocking I/O**: Use async libraries for DB, HTTP, and file operations.

## 7. Database Performance
- **GIN Indexes**: Used for Full Text Search (FTS) on text columns.
- **EXPLAIN ANALYZE**: Use this to optimize slow queries.

## 8. Search Performance
- Search results are cached.
- GIN index maintenance is run periodically to ensure fast lookups.

## 9. Autoscaling Engine
- Located in `backend/app/performance/`.
- **Triggers**: CPU > 70%, Memory > 80%, or high request queue.
- **Rules**: Scales up by 1 instance per 5 minutes; scales down when load drops below 30% for 15 minutes.

## 10. Capacity Planning
- Analyzes historical metrics to predict required capacity for upcoming election events.
- Tracks requests per second (RPS), concurrent users, and DB load.

## 11. Benchmarking
- Located in `backend/app/performance/benchmark/`.
- Run load tests using provided scripts before major releases.

## 12. Performance Debugging
- Profiling via `/diagnostics` endpoint.
- Slow query traces are logged to the Observability platform.
