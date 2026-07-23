# Database Guide

## 1. Database Architecture
- **PostgreSQL 15** acts as the primary datastore.
- We use **AsyncPG** for non-blocking database interaction.

## 2. Domain Entities to ORM Models
6 core entities mapped to tables:
- `Election`
- `Candidate`
- `Party`
- `Constituency`
- `PollingBooth`
- `Result`

## 3. SQLAlchemy 2 Async Patterns
- Sessions are created using `async_sessionmaker`.
- Injected into handlers via FastAPI dependencies (`Depends(get_db)`).

## 4. Unit of Work Pattern
- Ensures transaction integrity.
- `uow.commit()` and `uow.rollback()` manage the lifecycle.
- Handlers use UoW to persist changes atomically.

## 5. Repository Pattern
- **Domain Interface**: `backend/app/domain/`
- **SQLAlchemy Implementation**: `backend/app/persistence/repositories/`
- **Mapper**: Translates ORM models to domain entities (`backend/app/persistence/mappers/`).

## 6. Alembic Migrations
- **Create**: `alembic revision --autogenerate -m "description"`
- **Run**: `alembic upgrade head`
- **Rollback**: `alembic downgrade -1`
- **Status**: `alembic current`

## 7. Connection Pool Management
- Settings are configured centrally (see Performance Guide).
- `pool_pre_ping=True` handles dropped connections gracefully.

## 8. Database Indexes
- B-Tree for foreign keys and lookups.
- **GIN** for Full Text Search.
- Added via Alembic migrations.

## 9. Query Patterns
- Use `selectinload` or `joinedload` to prevent N+1 queries.
- Optimize async queries and avoid loading unnecessary columns.

## 10. Backup and Restore
- **Backup**: `pg_dump -U user -d dbname -F c -f backup.dump`
- **Restore**: `pg_restore -U user -d dbname -1 backup.dump`

## 11. Database Monitoring
- View active connections with `pg_stat_activity`.
- Slow queries are logged if they exceed 500ms.

## 12. Local Development Setup
1. Install PostgreSQL 15.
2. Create DB: `CREATE DATABASE election_intelligence;`
3. Run migrations: `alembic upgrade head`
