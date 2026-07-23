# Database Infrastructure Directory Structure

```
backend/
├── alembic/
│   ├── env.py                        # Alembic environment configuration (reads settings)
│   ├── script.py.mako                # Revision template
│   └── versions/
│       └── 0001_initial_empty_migration.py  # Initial baseline migration
├── alembic.ini                       # Alembic configuration file
├── app/
│   ├── config/
│   │   └── settings.py               # DATABASE_URL and pool configuration
│   ├── database/
│   │   ├── __init__.py               # Exports Base, engine, session providers
│   │   ├── base.py                   # Base declarative and abstract BaseModel
│   │   ├── engine.py                 # Async SQLAlchemy engine with connection pooling
│   │   ├── metadata.py               # PostgreSQL constraint naming conventions
│   │   └── session.py                # AsyncSession factory, dependency, & context managers
│   ├── models/
│   │   └── __init__.py               # Infrastructure models package
│   └── repositories/
│       └── __init__.py               # Infrastructure repositories package
docker-compose.yml                    # PostgreSQL 16 service with volume & healthcheck
tests/
├── conftest.py                       # AsyncClient & pytest fixtures
├── test_database_connection.py       # Engine & configuration unit tests
├── test_health_endpoint.py           # Health check endpoint database integration test
├── test_metadata.py                  # Declarative base & naming convention tests
└── test_session_lifecycle.py         # Session provider & context manager tests
```

## Module Responsibilities
- **`app/database/engine.py`**: Configures async PostgreSQL pool parameters.
- **`app/database/session.py`**: Manages async session creation, cleanup, and transaction rollback.
- **`app/database/base.py`**: Defines abstract `BaseModel` (`id`, `created_at`, `updated_at`, `deleted_at`, `version`).
- **`app/database/metadata.py`**: Enforces strict foreign key, primary key, index, unique, and check constraint naming patterns.
