# Core Platform Architecture Directory Structure

```
backend/
├── app/
│   └── core/
│       ├── __init__.py               # Core package export entrypoint
│       ├── cache/
│       │   ├── __init__.py           # Cache exports
│       │   └── cache.py              # Cache, MemoryCache, RedisCache contracts
│       ├── events/
│       │   ├── __init__.py           # Events exports
│       │   └── events.py             # Event, DomainEvent, EventBus, InMemoryEventBus
│       ├── metrics/
│       │   ├── __init__.py           # Metrics exports
│       │   └── metrics.py            # Counter, Gauge, Histogram, Tracer contracts
│       ├── repositories/
│       │   ├── __init__.py           # Repository exports
│       │   └── repository.py         # ReadRepository, WriteRepository, Repository
│       ├── result/
│       │   ├── __init__.py           # Result exports
│       │   └── result.py             # Result, Success, Failure, DomainError, ErrorCode
│       ├── services/
│       │   ├── __init__.py           # Services exports
│       │   └── services.py           # Clock, UUID, Hash, Serializer, Config contracts
│       ├── tasks/
│       │   ├── __init__.py           # Tasks exports
│       │   └── tasks.py              # Task, TaskScheduler, Worker contracts
│       ├── types/
│       │   ├── __init__.py           # Types exports
│       │   └── types.py              # Shared generic TypeVars (T, ID, E)
│       └── validation/
│           ├── __init__.py           # Validation exports
│           └── validation.py         # ValidationError, ValidationResult, Validator
tests/
├── test_core_cache.py                # Cache abstraction unit tests
├── test_core_events.py               # Event system unit tests
├── test_core_metrics.py              # Metrics interfaces unit tests
├── test_core_repositories.py         # Base repository interface unit tests
├── test_core_result.py               # Result monad & DomainError unit tests
├── test_core_tasks.py                # Background task scheduler unit tests
└── test_core_validation.py           # Validation layer unit tests
PLATFORM_GUIDE.md                     # Platform architecture & building blocks guide
PLATFORM_STRUCTURE.md                 # Core platform directory layout documentation
PLATFORM_VALIDATION.md                # Core platform verification report
```

## Architectural Decoupling Rules
1. **Zero HTTP Coupling**: No imports of FastAPI, Starlette, or HTTP status codes in `app/core/`.
2. **Zero SQL Coupling**: No imports of SQLAlchemy or database sessions in core interfaces.
3. **Zero Business Logic**: Generic interfaces only (`T`, `ID`, `E`). Domain entities inherit from these abstractions in future milestones.
