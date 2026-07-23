# Quality Assurance Guide

This document outlines the quality assurance standards, philosophy, and gates for the Election Intelligence Platform v1.0.0.

## 1. Quality Philosophy

Our quality approach is built on three core pillars:
- **Shift-Left Testing**: Identify and resolve defects as early in the software development lifecycle as possible. Developers own the quality of their code.
- **Test Pyramid**: Favor a high volume of fast, reliable unit tests at the base, supported by fewer, broader integration tests, and a minimal number of end-to-end UI tests.
- **Zero-Defect Release Policy**: No known critical or high-severity defects are permitted in a production release. All tests must pass before any code is merged.

## 2. Quality Gates

Every pull request and release candidate must pass the following quality gates.

| Gate | Command | Expected Output | Failure Action |
| --- | --- | --- | --- |
| **Backend Lint** | `ruff check backend` | Clean exit (no errors) | Fix linting violations. |
| **Backend Compile** | `python -m compileall backend` | Clean exit (no syntax errors) | Fix Python syntax errors. |
| **Backend Test** | `pytest` | `287 passed` (or current total) | Fix failing tests. Do not skip tests without an issue link. |
| **Flutter Analyze** | `flutter analyze` | `No issues found!` | Fix Dart/Flutter analysis warnings and errors. |
| **Flutter Test** | `flutter test` | `All tests passed!` (6/6) | Fix failing Flutter widget/unit tests. |

## 3. Code Quality Tools

### Backend (Python)
We use `ruff` as our primary linter and formatter, configured via `pyproject.toml`:
- **Line Length**: 100 characters.
- **Target Version**: Python 3.12.
- **Rules Selected**: `E` (pycodestyle), `W` (warnings), `F` (pyflakes), `I` (isort), `UP` (pyupgrade), `B` (flake8-bugbear), `C4` (flake8-comprehensions), `SIM` (flake8-simplify), `ARG` (flake8-unused-arguments), `PTH` (flake8-use-pathlib).
- **Quote Style**: Single quotes.

We use `mypy` for static type checking. All new code must be strictly typed.

### Frontend (Flutter)
We rely on the standard Dart analyzer configured in `analysis_options.yaml` to enforce effective Dart guidelines.

## 4. Test Quality Standards

- **Coverage Targets**: Minimum 85% line coverage for backend business logic and API routes. Minimum 80% coverage for Flutter UI state management.
- **What Must Be Tested**:
  - All API endpoints (success and failure modes).
  - Database access layer and complex queries.
  - Core business logic (especially AI intelligence processing).
  - Flutter UI state transitions and complex widgets.
- **Mutation Testing**: Consider using `mutmut` periodically to evaluate the effectiveness of the test suite by injecting faults and ensuring tests catch them.

## 5. Performance Quality

We mandate the following performance targets:
- **API Latency**: <100ms for standard CRUD operations.
- **Search Latency**: <200ms for semantic and keyword searches.
- **Dashboard Load**: <1s for rendering analytical dashboards.
- **Mobile Startup**: <2s time-to-interactive for the Flutter application.

## 6. Security Quality

- **OWASP Top 10**: Code must be reviewed against OWASP Top 10 vulnerabilities (e.g., injection, broken authentication).
- **Dependency Scanning**: Run `pip-audit` for Python and `dart pub outdated` / security scanners for Flutter to identify vulnerable dependencies.
- **SBOM**: A Software Bill of Materials (SBOM) must be generated and archived for every production release.

## 7. Documentation Quality

- **What Must Be Documented**: Complex business logic, API schemas (via OpenAPI), architectural decisions (ADRs), and deployment procedures.
- **Review Process**: Documentation updates must be included in the PR that changes the corresponding code. Doc reviews are part of the standard code review.

## 8. CI/CD Quality Gates

Our GitHub Actions pipeline (`.github/workflows/ci.yml`) enforces quality automatically.
- **Pipeline Stages**: Lint, Compile, Backend Test, Flutter Analyze, Flutter Test, Docker Build.
- **Merge Blockers**: A pull request cannot be merged unless all CI checks pass and at least one approving review is received from a code owner.

## 9. Quality Review Checklist

### Before Merge
- [ ] Code compiles and passes all local quality gates.
- [ ] Unit and integration tests added/updated.
- [ ] CI pipeline is green.
- [ ] Documentation updated.
- [ ] Code owner review approved.

### Before Release
- [ ] All integration tests passing.
- [ ] Performance benchmarks met.
- [ ] Security scans clean.
- [ ] SBOM generated.
- [ ] Changelog updated.

## 10. Measuring and Tracking Quality

We track the following metrics over time to ensure quality does not degrade:
- **Test Coverage Percentage**: Tracked via CI reports.
- **Defect Escape Rate**: Number of bugs reported in production versus caught in QA/CI.
- **Mean Time to Resolution (MTTR)**: How quickly critical bugs are fixed and deployed.
- **CI Pipeline Success Rate**: Frequency of failing builds in the main branch.