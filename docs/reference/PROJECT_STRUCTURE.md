# Project Structure Guide

This document outlines the organization of the Election Intelligence Platform v1.0.0.

## 1. Repository Root Overview

| File/Directory | Purpose |
|----------------|---------|
| `backend/` | Python FastAPI backend application, containing domain, application, and persistence layers. |
| `frontend/` | Flutter mobile and web application. |
| `tests/` | Comprehensive test suite for all components. |
| `.github/` | GitHub Actions CI/CD workflows and repository configurations. |
| `docs/` | Additional technical documentation (if applicable). |
| `pyproject.toml` | Python dependency and tooling configuration. |
| `docker-compose.yml` | Local development infrastructure orchestrator. |
| `README.md` | Entry point for the project. |

## 2. Backend Structure Tree (`backend/`)

```
backend/
├── alembic/                 # Database migrations (versions, env.py)
├── app/                     # Main application source
│   ├── api/                 # Presentation Layer
│   │   └── v1/              # Version 1 API
│   │       ├── routers/     # 12 API routers
│   │       ├── schemas/     # Pydantic models for request/response validation
│   │       └── dependencies.py # FastAPI dependencies
│   ├── application/         # Application Layer (Use Cases)
│   │   ├── commands/        # CQRS Command models
│   │   ├── queries/         # CQRS Query models
│   │   ├── handlers/        # Command and Query Handlers
│   │   ├── pipeline/        # Request pipelines and middleware
│   │   ├── validators/      # Business logic validators
│   │   ├── dto/             # Data Transfer Objects
│   │   └── events/          # Application-level event processing
│   ├── domain/              # Domain Layer (Core Business Logic)
│   │   ├── election/        # Election entity, value objects, repo interface
│   │   ├── candidate/       # Candidate entity, value objects, repo interface
│   │   ├── party/           # Party entity, value objects, repo interface
│   │   ├── constituency/    # Constituency entity, value objects, repo interface
│   │   ├── polling/         # PollingBooth entity, value objects, repo interface
│   │   └── results/         # Result entity, value objects, repo interface
│   ├── persistence/         # Infrastructure Layer (Data Access)
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── repositories/    # SQLAlchemy implementations of domain interfaces
│   │   ├── mappers/         # Mapping between Domain and ORM models
│   │   └── uow/             # UnitOfWork implementation
│   └── database/            # Database connection and session management
└── main.py                  # FastAPI application entry point
```

## 3. Frontend Structure Tree (`frontend/`)

```
frontend/
├── lib/
│   ├── core/                # Shared utilities, constants, theme, network client
│   ├── features/            # Feature-based organization (e.g., auth, election, candidate)
│   │   └── {feature_name}/
│   │       ├── data/        # Data sources, repositories, models
│   │       ├── domain/      # Entities, use cases
│   │       └── presentation/# UI, widgets, state management (Riverpod)
│   └── routing/             # App routing configuration (GoRouter)
├── test/                    # Frontend tests
├── pubspec.yaml             # Dart dependencies
└── build/                   # Build artifacts
```

## 4. Tests Structure (`tests/`)

```
tests/
├── backend/
│   ├── unit/                # Fast, isolated tests for domain and application layers
│   ├── integration/         # Tests involving DB, Redis, external APIs
│   └── e2e/                 # End-to-end API tests
└── frontend/
    ├── unit/                # Dart unit tests
    └── widget/              # Flutter widget tests
```

## 5. CI/CD Workflows (`.github/`)

```
.github/
└── workflows/
    ├── test-backend.yml     # Runs Pytest, Ruff linting
    ├── test-frontend.yml    # Runs Flutter test, analyze
    └── deploy.yml           # Deployment pipeline (build Docker, push, deploy)
```

## 6. Configuration Files

- **`pyproject.toml`**: Controls Python dependencies (via Poetry or pip), Ruff linting rules, Pytest configuration, and project metadata.
- **`pubspec.yaml`**: Controls Flutter/Dart dependencies, assets, and app versioning.
- **`Dockerfile`**: Defines the container image build process for the backend.
- **`docker-compose.yml`**: Configures local development services (PostgreSQL, Redis, Backend, etc.).
- **`alembic.ini`**: Configures the Alembic database migration environment and database connection string.

## 7. Documentation Files Map

- **System Context & Flow**: `ARCHITECTURE_DIAGRAMS.md`
- **Core Architecture Principles**: `ARCHITECTURE.md`
- **Change History**: `CHANGELOG.md`
- **Security Protocols**: `SECURITY.md`
- **Contribution Guidelines**: `CONTRIBUTING.md`
- **Database Rules**: `DATABASE_GUIDE.md`
- **Engineering Quality**: `ENGINEERING_STANDARDS.md`
- **Disaster Recovery**: `BACKUP_RECOVERY.md`
- **Historical Decisions**: `DECISION_LOG.md`

## 8. Adding New Files

- **New Domain Entity**: Add to `backend/app/domain/<entity_name>/` (needs aggregate root, repo interface).
- **New API Endpoint**: Add router to `backend/app/api/v1/routers/` and schemas to `schemas/`.
- **New Test**: Place in `tests/backend/unit/` or `integration/` mirroring the app structure.
- **New Migration**: Run `alembic revision --autogenerate -m "msg"` which creates a file in `backend/alembic/versions/`.
- **New Flutter Screen**: Add to `frontend/lib/features/<feature>/presentation/screens/`.

## 9. File Naming Conventions

- **Python**: `snake_case.py` (e.g., `election_repository.py`)
- **Dart**: `snake_case.dart` (e.g., `election_screen.dart`)
- **Test Files**: `test_*.py` for Python, `*_test.dart` for Dart.

## 10. What NOT to Put in Each Directory

- **`backend/app/domain/`**: DO NOT put ORM models (`Base`), FastAPI routers, or HTTP responses here. Only pure Python classes.
- **`backend/app/application/`**: DO NOT put SQL queries here. Use the repository interface.
- **`frontend/lib/presentation/`**: DO NOT put network request logic here. Call use cases or repositories.
- **`tests/unit/`**: DO NOT put tests that require a running database or external network.
