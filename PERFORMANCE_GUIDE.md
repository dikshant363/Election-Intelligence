# Performance, Scalability & Distributed Infrastructure Guide

## Overview

The **Performance & Scalability Platform** (`backend/app/performance/`) transforms the Election Intelligence Platform into a horizontally scalable, high-throughput distributed system.

---

## Architectural Principles

```text
Client Request
      ↓
API & Rate Limiter (Sliding Window / Token Bucket)
      ↓
CacheService Abstraction (MemoryCache / RedisAdapter)
      ↓
Database Connection Pool & ReadReplicaRouter
      ↓
EventBus (Event-Driven Cache Invalidation)
```

1. **Dedicated Module Isolation**: All performance & scaling infrastructure resides strictly inside `backend/app/performance/`.
2. **Cache Abstraction**: Application layers depend exclusively on `CacheService`, preserving independence from underlying stores (Memory, Redis, KeyDB, Dragonfly, Valkey).
3. **Non-Invasive Optimization**: Payload compression, O(1) cursor pagination, and result streaming optimize system performance without altering business logic.

---

## Core Components

| Component | Location | Purpose |
| :--- | :--- | :--- |
| **Cache Engine** | `backend/app/performance/cache/` | `CacheService`, `MemoryCache`, `RedisAdapter` with TTL, tags, and compression |
| **Pool Monitor** | `backend/app/performance/pooling/` | `ConnectionPoolMonitor` and `ReadReplicaRouter` for read/write splitting |
| **Optimizations** | `backend/app/performance/optimization/` | `compress_payload`, `CursorPaginator`, `StreamingResultOptimizer` |
| **Rate Limiter** | `backend/app/performance/ratelimit/` | `SlidingWindowRateLimiter` and `TokenBucket` algorithm abstraction |
| **Benchmark** | `backend/app/performance/benchmark/` | `BenchmarkRunner` scenario load tester measuring throughput and P95/P99 latency |
| **Autoscaling** | `backend/app/performance/autoscaling/` | `AutoscalingEngine` recommending horizontal replica counts |
| **Capacity** | `backend/app/performance/capacity/` | `CapacityPlanner` calculating concurrency, RPS, and storage growth projections |

---

## API Endpoints

- `GET /api/v1/cache` — Cache engine status & hit ratio statistics
- `POST /api/v1/cache/invalidate` — Invalidate cache entries by pattern or tags
- `GET /api/v1/performance` — Overall system performance & pool metrics
- `GET /api/v1/benchmark` — Execute synthetic benchmark load test
- `GET /api/v1/capacity` — Capacity planning report & growth projections
