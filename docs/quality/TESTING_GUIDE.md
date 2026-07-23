# Testing Guide

This document outlines the testing strategy, structure, and procedures for the Election Intelligence Platform (v1.0.0).

## 1. Test Philosophy
We follow the **Test Pyramid**:
- **Unit Tests**: Fast, isolated tests for domain logic and utility functions. (Bulk of the tests).
- **Integration Tests**: Test interactions between components (e.g., API to database).
- **End-to-End (E2E) Tests**: Full system tests simulating real user flows. (Used sparingly for critical paths).

## 2. Directory Structure
All tests reside in the `tests/` directory at the project root. Tests are organized by subsystem and type:
```
tests/
  test_domain_*.py       # Domain logic unit tests
  test_core_*.py         # Core application services
  test_api.py            # API routing and serialization
  test_persistence.py    # Database interactions
  test_e2e_integration.py# Full flow E2E tests
  ...
```

## 3. Running Tests
The project uses `pytest` configured via `pyproject.toml` or `pytest.ini` (`testpaths=[tests]`, `addopts=-v --tb=short`).

- **All tests**: `pytest`
- **Single file**: `pytest tests/test_search.py`
- **Single test**: `pytest tests/test_search.py::TestRanking::test_scored_hit_calculation`
- **With coverage**: `pytest --cov=backend/app`
- **Parallel execution**: `pytest -n auto` (requires `pytest-xdist`)

## 4. Test Categories with Locations
- **Domain Tests**: `test_domain_aggregates.py`, `test_domain_events.py`, `test_domain_value_objects.py`, `test_domain_specifications.py`
- **Application Tests**: `test_application.py`, `test_core_*.py`
- **Infrastructure Tests**: `test_persistence.py`, `test_database_connection.py`, `test_session_lifecycle.py`
- **API Tests**: `test_api.py`, `test_health_endpoint.py`, `test_metadata.py`
- **Feature Tests**: `test_ai.py`, `test_search.py`, `test_etl.py`, `test_realtime.py`, `test_identity.py`, `test_observability.py`, `test_performance.py`, `test_production.py`
- **Security Tests**: `test_security_headers.py`, `test_cors.py`, `test_trusted_hosts.py`, `test_request_id.py`, `test_request_size.py`
- **E2E Tests**: `test_e2e_integration.py`

## 5. Writing New Tests
- **Fixtures**: Use pytest fixtures for dependency injection and setup/teardown.
- **Mocking**: Use `unittest.mock` or `pytest-mock` to isolate unit tests from external dependencies (e.g., mocking the database in domain tests).
- **Async**: Use `@pytest.mark.asyncio` for asynchronous test functions.

## 6. Test Data and Fixtures
- Shared fixtures are defined in `tests/conftest.py`.
- Use factory patterns (e.g., `factory_boy`) or specific fixtures for creating test data objects (users, datasets) to keep test setup clean.

## 7. Performance Tests
- Performance limits (e.g., max request size of 10MB, 30-second timeouts) are tested in `test_performance.py` and infrastructure configurations.
- Load testing (via tools like Locust or k6) should be run periodically against staging environments.

## 8. Flutter Testing
For the frontend mobile/web application:
- **Run tests**: `flutter test`
- Write **Unit Tests** for Dart logic and ViewModels.
- Write **Widget Tests** for UI components.

## 9. CI Pipeline Test Execution
- Tests are executed automatically on every pull request and merge to the main branch via GitHub Actions / GitLab CI.
- The pipeline will fail if any test fails or if coverage drops below the required threshold.

## 10. What to Test vs What NOT to Test
- **DO Test**: Domain business rules, security middleware (CORS, headers), complex queries, ETL transformations, RBAC enforcement.
- **DO NOT Test**: Third-party library internals (assume they work), trivial getters/setters, boilerplate code with no logic.
