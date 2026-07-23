# Coding Standards

This document establishes the technical guidelines and coding standards for the Election Intelligence Platform.

## 1. Python Standards

- **Formatting & Linting:** Use `ruff` configured with `line-length=100`, `target-version=py312`, and `quote-style=single`.
- **Type Hints:** All function signatures and class properties must be fully typed. Use `typing` module constructs for complex types.
- **Docstrings:** Use Google-style docstrings for modules, classes, and public functions.
- **Import Ordering:** Standard library, third-party packages, local modules. (Handled automatically by `ruff`).
- **Naming:**
  - Variables/Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

## 2. FastAPI Standards

- **Router Organization:** Group endpoints by resource in `backend/app/api/v1/endpoints/`.
- **Dependency Injection:** Use FastAPI's `Depends` for providing database sessions, current user context, and service instances. Do not instantiate services directly in the route handler.
- **Response Models:** Always define explicit `response_model` on endpoints using Pydantic schemas. Avoid returning internal database models directly.
- **Status Codes:** Use appropriate HTTP status codes (e.g., 201 for creation, 404 for not found, 400 for bad request).

## 3. SQLAlchemy Standards

- **Async Sessions:** Use `AsyncSession` exclusively for non-blocking database operations.
- **Model Naming:** Database table names should be plural (e.g., `users`, `precincts`). Model classes should be singular (e.g., `User`, `Precinct`).
- **Relationship Loading:** Be explicit about relationship loading strategies (`selectinload`, `joinedload`) to prevent N+1 query problems.
- **Migrations:** Never modify database schema without an accompanying Alembic migration.

## 4. Domain Model Standards

- **Aggregate Design:** Group related entities into Aggregates. Protect invariants within the aggregate root.
- **Value Objects:** Use immutable classes (e.g., Python `dataclass(frozen=True)`) for concepts with no conceptual identity (e.g., an Address or a Coordinate).
- **Repository Interfaces:** Define repository interfaces in the domain layer and implement them in the infrastructure layer.

## 5. Test Standards

- **Test Naming:** Prefix test files with `test_` and functions with `test_`. Use descriptive names: `test_create_voter_fails_with_invalid_age`.
- **Fixtures:** Use `pytest` fixtures for setup. Keep fixtures scoped appropriately (function, module, session).
- **Isolation:** Tests must not depend on the outcome or state of other tests. Use database transaction rollbacks for isolation.
- **Mocks vs Real:** Use real database instances (via test containers or local test DB) for repository/integration tests. Use mocks only for external APIs or when strict unit testing domain logic.

## 6. Flutter / Dart Standards

- **Widget Naming:** Use descriptive `PascalCase` for Widgets.
- **State Management:** Use Riverpod (`ConsumerWidget`, `StateNotifierProvider`). Avoid `StatefulWidget` unless handling purely localized, ephemeral UI state (like an animation controller).
- **Navigation:** Use `go_router` for all routing to ensure deep-linking compatibility and declarative navigation.
- **File Structure:** One widget/class per file.

## 7. Documentation Standards

- **Docstrings:** Required for all public APIs, complex business logic, and classes.
- **Inline Comments:** Use sparingly to explain *why* something is done, not *what* is done (the code should tell what).
- **Updating Docs:** Update this repository's markdown files whenever architectural or workflow changes occur.

## 8. Security Standards

- **No Secrets in Code:** Never hardcode credentials, API keys, or tokens. Use environment variables.
- **Input Validation:** Validate all inputs at the boundary using Pydantic (Backend) or form validation (Frontend).
- **Authentication:** Protect endpoints using JWT scopes.

## 9. Git Standards

- **Commits:** Adhere strictly to the Conventional Commits format.
- **Branches:** Follow the `feature/`, `hotfix/`, `release/` naming conventions.
- **PR Size Limits:** Keep PRs small and focused (ideally under 500 lines of change) to facilitate effective review.

## 10. Prohibited Patterns

- **Global State:** Do not use mutable global variables.
- **Business Logic in Routers:** Keep FastAPI endpoint functions strictly for HTTP concerns (parsing input, calling a service, returning output).
- **DB Access from API Layer:** Never execute SQL or SQLAlchemy calls directly within a router; use a Repository.
