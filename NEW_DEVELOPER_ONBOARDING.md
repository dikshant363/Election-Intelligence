# New Developer Onboarding

Welcome to the Election Intelligence Platform! This document provides a structured onboarding path to get you productive quickly.

## Day 1: Environment & Context

**Goals:** Get the application running locally and understand the high-level architecture.

1. **Setup:** Follow the steps in [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) to install dependencies, configure your environment, and start the local services.
2. **Run the Platform:** Ensure both the backend (`uvicorn app.main:app`) and frontend (`flutter run`) start without errors.
3. **Explore the UI:** Navigate through the Flutter app locally.
4. **Read Architecture Docs:** (If available, review the `ARCHITECTURE.md` file). Understand the core components:
   - FastAPI for the backend API.
   - PostgreSQL as the primary relational database.
   - Flutter for the cross-platform frontend.
   - Redis for caching and background tasks.

## Day 2: Codebase Navigation & Testing

**Goals:** Understand code structure, data flows, and testing.

1. **Backend Structure (`backend/`):**
   - `app/api/`: FastAPI routers and endpoints.
   - `app/domain/`: Core business logic, entities, and value objects.
   - `app/infrastructure/`: Database repositories, external API clients.
   - `app/schemas/`: Pydantic models for request/response validation.
2. **Frontend Structure (`frontend/`):**
   - `lib/domain/`: Dart models.
   - `lib/presentation/`: Flutter widgets and screens.
   - `lib/providers/`: State management (Riverpod).
3. **Data Flow:** Trace a request from the Flutter UI, through an API endpoint, into the domain logic, down to the database, and back up.
4. **Run Tests:**
   - Run `pytest` in the backend. Look at `backend/tests/` to see how tests are structured (unit vs integration).
   - Run `flutter test` in the frontend.

## Day 3: First Contribution

**Goals:** Add a small feature or fix a bug and open your first Pull Request.

1. **Pick an Issue:** Grab a "good first issue" from the issue tracker.
2. **Branch:** Create a branch following the [DEVELOPER_WORKFLOW.md](DEVELOPER_WORKFLOW.md) (e.g., `feature/sprint-1.1-button-color`).
3. **Implement:** Write the code. Remember to update or add tests.
4. **Quality Gates:** Run `ruff check`, `pytest`, `flutter analyze`, and `flutter test`.
5. **Commit & Push:** Use conventional commits.
6. **Open PR:** Submit a Pull Request and ask a team member for a review.

## Week 1: Mastery & Deep Dive

**Goals:** Become comfortable with the PR process and subsystem integration.

1. **Code Review:** Participate in code reviews. Read PRs opened by senior engineers to learn project idioms.
2. **Domain Model Mapping:** Understand how real-world election concepts (Voters, Precincts, Ballots, Candidates) map to our Domain Entities and SQLAlchemy models.
3. **Subsystems:** Deep dive into background task processing, caching strategies, and deployment pipelines.
4. **Ask Questions:** Reach out to the team via Slack/Discord if you hit blockers.

## Important Concepts to Understand First

- **Dependency Injection in FastAPI:** How we inject database sessions and services into endpoints.
- **Riverpod State Management:** How Flutter components react to state changes without deep widget tree rebuilds.
- **Alembic Migrations:** How database schemas are evolved safely.

## Common Mistakes New Devs Make

- **Skipping Migrations:** Forgetting to generate or apply Alembic migrations when changing SQLAlchemy models.
- **Leaking DB logic to Routers:** Writing direct SQLAlchemy queries inside FastAPI routers instead of using Repository interfaces.
- **Committing Secrets:** Accidentally pushing `.env` files or API keys. Always double-check your commits.
- **Ignoring Lints:** Overlooking `ruff` or `flutter analyze` warnings. CI will fail if these are ignored.
