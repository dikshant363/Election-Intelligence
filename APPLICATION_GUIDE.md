# Application Layer Architecture Guide

## Overview
The Application Layer (`backend/app/application/`) orchestrates business workflows using Command Query Responsibility Segregation (CQRS). It remains 100% independent of HTTP, FastAPI, web routes, and UI presentation concerns.

## CQRS Architectural Flow

```
   [Command Pipeline]                 [Query Pipeline]
          │                                  │
          ▼                                  ▼
 [Command Handlers]                  [Query Handlers]
          │                                  │
 ┌────────┴────────┐                         │
 ▼                 ▼                         │
[Domain Model] [UnitOfWork]                  │
          │        │                         │
          ▼        ▼                         ▼
   [Domain Event] [Repositories] ───► [Read DTO Projections]
          │
          ▼
   [Event Bus Dispatch]
```

## Layer Responsibilities

1. **Commands & Queries (`app/application/commands/` & `app/application/queries/`)**: Immutable intent data structures.
2. **DTOs (`app/application/dto/`)**: Pure data transfer objects returned by handlers. No ORM models or database entities leak beyond the Application boundary.
3. **Command Handlers (`app/application/handlers/command_handlers.py`)**: Mutate state via Domain Aggregates and `UnitOfWork`. Commit transactions atomically and dispatch recorded domain events via `EventBus`. Return `Result[DTO]`.
4. **Query Handlers (`app/application/handlers/query_handlers.py`)**: Read-only queries using `UnitOfWork`. No transaction commits or state mutations. Return `Result[DTO]` or `Result[list[DTO]]`.
5. **Validators & Pipeline (`app/application/validators/` & `app/application/pipeline/`)**: Validates structural and value rules before passing commands to handlers.

## Usage Example

```python
uow = SqlAlchemyUnitOfWork(session_factory=AsyncSessionLocal)
handlers = CommandHandlers(uow=uow, event_bus=event_bus)
pipeline = CommandPipeline(handlers=handlers)

result = await pipeline.execute_create_election(
    CreateElection(
        title="General Election 2026",
        election_type=ElectionType.GENERAL,
        start_date=date(2026, 5, 1),
        end_date=date(2026, 5, 15),
    )
)

if result.is_success:
    election_dto = result.unwrap()
```

## Test Suite Execution Reference

```bash
# Run application layer CQRS test suite
.venv/bin/pytest tests/test_application.py
```
