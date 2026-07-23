# Persistence Layer Architecture Guide

## Overview
The Persistence layer (`backend/app/persistence/`) bridges the Domain Model to PostgreSQL using SQLAlchemy 2.x, repository pattern, and Unit of Work context management.

## Architectural Separation & Data Flow

```
Domain Aggregate Root
       ▲
       │ (Mapper Translation)
       ▼
SQLAlchemy ORM Model
       ▲
       │ (SQL Execution)
       ▼
PostgreSQL Database
```

### Layer Responsibilities
1. **`app/persistence/models/`**: SQLAlchemy 2.x Declarative ORM models. Contains column definitions, indexes, foreign keys, and relationships. Zero business rules.
2. **`app/persistence/mappers/`**: Pure translation functions mapping between Domain Aggregate Roots $\leftrightarrow$ SQLAlchemy ORM models. No SQL queries.
3. **`app/persistence/repositories/`**: Asynchronous SQLAlchemy implementations of domain repository contracts (`ElectionRepository`, `CandidateRepository`, etc.).
4. **`app/persistence/uow/`**: `SqlAlchemyUnitOfWork` implementing transaction boundary management, atomic multi-repository commits, and context-managed automatic rollback on exception.

## Database Models & Relationships

| ORM Model | Table Name | Foreign Keys | Relationships |
| :--- | :--- | :--- | :--- |
| `ElectionModel` | `elections` | None | `results` (1-to-many) |
| `PoliticalPartyModel` | `political_parties` | None | `candidates` (1-to-many) |
| `ConstituencyModel` | `constituencies` | None | `polling_booths`, `candidates`, `results` |
| `CandidateModel` | `candidates` | `constituencies.id`, `political_parties.id` | `constituency`, `party` |
| `PollingBoothModel` | `polling_booths` | `constituencies.id` | `constituency` |
| `ElectionResultModel` | `election_results` | `elections.id`, `constituencies.id`, `candidates.id` | `election`, `constituency`, `winning_candidate` |

## Unit of Work Usage Pattern

```python
async with SqlAlchemyUnitOfWork(session_factory=AsyncSessionFactory) as uow:
    election = await uow.elections.get_by_id(election_id)
    election.start_election()
    await uow.elections.update(election)
    await uow.commit()  # Commits atomic transaction
```

## Migration & Testing Reference

```bash
# Run database migrations
.venv/bin/alembic -c backend/alembic.ini upgrade head

# Run persistence integration test suite
.venv/bin/pytest tests/test_persistence.py
```
