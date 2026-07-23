# Decision Log

This document records the architectural and technological decisions made during the lifecycle of the Election Intelligence Platform.

## 1. Decision Log Format

When making a significant architectural, tooling, or process change, append a new entry to this document using the following format:
- **Date**: YYYY-MM-DD
- **Context**: The problem being solved.
- **Decision**: What was decided.
- **Rationale**: Why this decision was made.
- **Trade-offs**: Known drawbacks of the decision.
- **Status**: Proposed, Accepted, Deprecated, or Superseded.

---

## 2. Technology Selection Decisions

### Why FastAPI over Django/Flask
- **Date**: 2023-10-01
- **Decision**: Use FastAPI for the backend API.
- **Rationale**: Superior performance with ASGI, automatic OpenAPI documentation, out-of-the-box async support, and excellent Pydantic integration for data validation.
- **Trade-offs**: Smaller ecosystem of plugins compared to Django; requires manual setup of ORM and auth.
- **Status**: Accepted

### Why Pydantic v2 over alternatives
- **Date**: 2023-10-05
- **Decision**: Adopt Pydantic v2 for data validation.
- **Rationale**: Core rewrite in Rust provides massive performance gains over v1; industry standard for FastAPI.
- **Trade-offs**: Slightly stricter parsing rules required some initial schema adjustments.
- **Status**: Accepted

### Why SQLAlchemy 2 async over alternatives
- **Date**: 2023-10-10
- **Decision**: Use SQLAlchemy 2.0 in fully async mode.
- **Rationale**: Strong type support, seamless integration with Python `asyncio` to prevent I/O blocking during heavy database reads.
- **Trade-offs**: Async ORM debugging can be complex; lazy loading relationships requires explicit configuration.
- **Status**: Accepted

### Why PostgreSQL over MySQL/MongoDB
- **Date**: 2023-09-15
- **Decision**: Use PostgreSQL 15+.
- **Rationale**: Robust relational integrity, advanced JSONB support for unstructured data, and pgvector extension for future AI/RAG capabilities.
- **Trade-offs**: Slightly higher operational complexity than MongoDB for purely document-based data.
- **Status**: Accepted

### Why Redis for caching
- **Date**: 2023-11-01
- **Decision**: Use Redis Stack.
- **Rationale**: In-memory speed for caching frequent queries (e.g., live election results), Pub/Sub for real-time events, and potential for vector search.
- **Trade-offs**: Adds an extra infrastructure component to maintain.
- **Status**: Accepted

### Why Flutter for mobile
- **Date**: 2023-09-20
- **Decision**: Build the frontend with Flutter.
- **Rationale**: Single codebase for iOS, Android, and Web; high rendering performance; rich UI component library.
- **Trade-offs**: Dart language learning curve; slightly larger app size compared to native.
- **Status**: Accepted

### Why Riverpod over Provider/Bloc
- **Date**: 2023-10-15
- **Decision**: Use Riverpod for Flutter state management.
- **Rationale**: Compile-time safety, no `BuildContext` dependency for reading state, and robust async data handling (AsyncValue).
- **Trade-offs**: Syntax can be verbose; steep initial learning curve.
- **Status**: Accepted

### Why Ruff over Black+isort+flake8
- **Date**: 2023-10-20
- **Decision**: Consolidate Python linting/formatting into Ruff.
- **Rationale**: Written in Rust, it replaces multiple tools and executes in milliseconds, drastically speeding up CI pipelines.
- **Trade-offs**: Newer tool, though rapidly becoming the industry standard.
- **Status**: Accepted

---

## 3. Architecture Decisions

### Why Clean Architecture (vs MVC, MVVM)
- **Date**: 2023-11-05
- **Decision**: Implement strict Clean Architecture in the backend.
- **Rationale**: Isolates business domain from framework dependencies, making the core logic highly testable and robust against framework changes.
- **Trade-offs**: Higher boilerplate and initial development overhead.
- **Status**: Accepted

### Why CQRS (vs simple CRUD)
- **Date**: 2023-11-10
- **Decision**: Separate Commands (writes) and Queries (reads).
- **Rationale**: Allows independent scaling and optimization of read and write paths, crucial for heavy read loads during election days.
- **Trade-offs**: Increased code complexity; requires distinct models for read and write.
- **Status**: Accepted

### Why UnitOfWork pattern
- **Date**: 2023-11-15
- **Decision**: Use Unit of Work (UoW) for transaction management.
- **Rationale**: Ensures atomic operations across multiple repositories; abstracts database session management from the application layer.
- **Trade-offs**: Can be tricky to implement correctly with async SQLAlchemy.
- **Status**: Accepted

### Why Repository pattern (vs direct ORM in services)
- **Date**: 2023-11-12
- **Decision**: Abstract data access behind Repository interfaces.
- **Rationale**: Allows swapping underlying storage (e.g., moving to a NoSQL DB for certain data) without altering business logic; simplifies mocking in tests.
- **Trade-offs**: Additional layer of mapping between ORM models and Domain Entities.
- **Status**: Accepted

### Why EventEnvelope for realtime
- **Date**: 2023-12-01
- **Decision**: Standardize real-time events using an EventEnvelope structure.
- **Rationale**: Provides consistent metadata (timestamp, event_type, correlation_id) for all WebSocket/SSE broadcasts.
- **Trade-offs**: Slight payload size increase.
- **Status**: Accepted

### Why Search Abstraction Layer
- **Date**: 2024-01-10
- **Decision**: Create a generic Search Interface.
- **Rationale**: Allows initial implementation using Postgres Full-Text Search, with seamless future migration to Elasticsearch if needed.
- **Trade-offs**: Limits usage of backend-specific search features to maintain compatibility.
- **Status**: Accepted

### Why hybrid RAG (BM25 + vector)
- **Date**: 2024-02-05
- **Decision**: Implement Hybrid Search for the AI Intelligence module (v1.1).
- **Rationale**: Pure vector search struggles with exact keyword matches (e.g., specific candidate IDs or party acronyms). BM25 handles keywords while vectors handle semantics.
- **Trade-offs**: Requires maintaining two indexing strategies and a re-ranking mechanism.
- **Status**: Accepted

### Why SecretsProvider abstraction
- **Date**: 2024-02-15
- **Decision**: Abstract secret retrieval.
- **Rationale**: Enables seamless transition from local `.env` files to AWS Secrets Manager in production without application code changes.
- **Trade-offs**: Minor overhead in secret resolution at startup.
- **Status**: Accepted

---

## 4. Process Decisions

### Why conventional commits
- **Date**: 2023-09-10
- **Decision**: Enforce Conventional Commits (`feat:`, `fix:`, etc.).
- **Rationale**: Standardizes git history, enables automated changelog generation, and semver bumping.
- **Trade-offs**: Requires developer discipline.
- **Status**: Accepted

### Why feature branches (vs trunk-based)
- **Date**: 2023-09-10
- **Decision**: Use feature branches mapped to tickets.
- **Rationale**: Ensures code review via Pull Requests before merging to `main`, maintaining code quality in a distributed team.
- **Trade-offs**: Can lead to merge conflicts if branches are long-lived.
- **Status**: Accepted

### Why GitHub Actions for CI
- **Date**: 2023-09-12
- **Decision**: Use GitHub Actions for CI/CD.
- **Rationale**: Deeply integrated with the code repository, zero external infrastructure to maintain for basic runners.
- **Trade-offs**: Vendor lock-in; testing complex local infrastructure requires Docker-compose in the runner.
- **Status**: Accepted
