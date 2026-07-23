# Database Infrastructure Guide

## Overview
The Election Intelligence Platform database foundation is powered by **PostgreSQL** using **SQLAlchemy 2.x (async)** with `asyncpg` for application runtime queries and `psycopg` for synchronous **Alembic** schema migrations.

## Core Architectural Components

### 1. Connection Engine (`app/database/engine.py`)
- Async engine initialized via `create_async_engine()`.
- Built with connection pooling (`pool_size=5`, `max_overflow=10`, `pool_timeout=30`, `pool_recycle=1800`).
- Configured with `pool_pre_ping=True` to detect and refresh stale database connections before execution.

### 2. Session Management (`app/database/session.py`)
- **`AsyncSessionLocal`**: Async session factory bound to the async engine.
- **`get_db_session`**: FastAPI dependency provider for request lifecycle scoping with automatic rollback and closing.
- **`get_db_context`**: Standalone async context manager for background tasks and batch scripts.

### 3. Declarative Base & Naming Convention (`app/database/base.py`, `app/database/metadata.py`)
- **`Base`**: Root `DeclarativeBase` inheriting explicit PostgreSQL constraint naming conventions (`pk_`, `fk_`, `ix_`, `uq_`, `ck_`).
- **`BaseModel`**: Abstract base model enforcing consistent entity columns across future milestones:
  - `id`: Primary key UUID (UUIDv4)
  - `created_at`: UTC timestamp with timezone
  - `updated_at`: UTC timestamp with timezone on update
  - `deleted_at`: Soft delete timestamp (nullable)
  - `version`: Optimistic locking integer counter

### 4. Database Migrations (`backend/alembic/`)
- Managed via Alembic (`alembic.ini`, `alembic/env.py`).
- Automatic environment URL resolution via `settings.sync_database_url`.

## Operations Command Reference

```bash
# Run database migrations to latest schema
.venv/bin/alembic -c backend/alembic.ini upgrade head

# Rollback migrations to base
.venv/bin/alembic -c backend/alembic.ini downgrade base

# Run database tests
.venv/bin/pytest tests/test_database_connection.py tests/test_session_lifecycle.py tests/test_metadata.py
```
