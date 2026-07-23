# Core Platform Infrastructure Guide

## Overview
The Election Intelligence Platform core platform layer (`backend/app/core/`) provides pure, framework-agnostic building blocks and abstractions that all domain modules inherit.

## Core Platform Contracts

### 1. Result Monad & Error Hierarchy (`app/core/result/`)
- **`Result[T]`**: Generic immutable monad (`Result.ok(value)` / `Result.fail(error)`).
- **`DomainError`**: Standardized domain exception payload (`code: ErrorCode`, `message: str`, `details: dict`).
- Encapsulates operation outcomes without HTTP framework coupling.

### 2. Base Repository Contracts (`app/core/repositories/`)
- **`ReadRepository[T, ID]`**: Async query interface (`get_by_id`, `find_all`, `count`, `exists`).
- **`WriteRepository[T, ID]`**: Async mutation interface (`add`, `update`, `delete`, `delete_by_id`).
- **`Repository[T, ID]`**: Combined async CRUD repository contract.
- Pure abstract interfaces decoupled from SQL / ORM specifics.

### 3. Pure Service Contracts (`app/core/services/`)
- **`ClockService`**: Datetime abstraction (`now()`, `utcnow()`).
- **`UUIDService`**: Identifier generation (`generate_v4()`, `generate_v7()`).
- **`HashService`**: Cryptographic string hashing (`hash_string()`, `verify_hash()`).
- **`Serializer[T]`**: Object serialization contract (`serialize()`, `deserialize()`).
- **`ConfigurationService`**: Parameter retrieval (`get()`).

### 4. Event System Contracts (`app/core/events/`)
- **`Event` / `DomainEvent` / `IntegrationEvent`**: Immutable event payloads with UUIDs and UTC timestamps.
- **`Publisher[E]`** & **`Subscriber[E]`**: Asynchronous messaging interfaces.
- **`InMemoryEventBus`**: Lightweight thread-safe in-memory pub/sub implementation.

### 5. Cache Abstraction (`app/core/cache/`)
- **`Cache[T]`**: Async cache interface (`get`, `set`, `delete`, `clear`, `exists`).
- **`MemoryCache`**: Dictionary-backed cache provider for development/testing.
- **`RedisCache`**: Abstract contract for future external cache providers.

### 6. Background Tasks (`app/core/tasks/`)
- **`Task[T]`**: Abstract task execution contract (`task_id`, `name`, `execute()`).
- **`TaskScheduler`** & **`Worker`**: Asynchronous queue processing contracts and in-memory test harnesses.

### 7. Validation Layer (`app/core/validation/`)
- **`ValidationError`** & **`ValidationResult`**: Immutable validation error containers.
- **`Validator[T]`**: Abstract validation interface (`validate()`).

### 8. Metrics & Telemetry (`app/core/metrics/`)
- **`Counter`**, **`Gauge`**, **`Histogram`**, **`Tracer`**, and **`MetricsRegistry`**: Provider-agnostic telemetry contracts.

## Testing & Operations

```bash
# Run core platform unit tests
.venv/bin/pytest tests/test_core_*.py
```
