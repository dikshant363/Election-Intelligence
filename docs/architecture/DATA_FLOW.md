# Data Flow

This document traces the path of data through the platform for primary operations.

## 1. HTTP Request → Response (Standard CRUD: Election Create)
1. **Presentation Layer**: Client sends `POST /api/v1/elections`. `ElectionRouter` receives JSON.
2. **Presentation Layer**: FastAPI / Pydantic validates JSON into an `ElectionCreateRequest` schema.
3. **Presentation Layer**: Router constructs a `CreateElectionCommand` and passes it to the `CommandHandler`.
4. **Application Layer**: `CreateElectionHandler` receives the command. It opens a `UnitOfWork` (UoW).
5. **Application Layer**: Inside UoW, handler checks invariants (e.g., election name uniqueness via `ElectionRepository`).
6. **Domain Layer**: Handler instantiates the `Election` aggregate root.
7. **Infrastructure Layer**: Handler calls `uow.elections.add(election)`.
8. **Infrastructure Layer**: `UoW.commit()` is called. `SQLAlchemyUnitOfWork` flushes changes to Postgres via `AsyncPG`.
9. **Application Layer**: Handler returns the domain object ID or DTO.
10. **Presentation Layer**: Router maps DTO to `ElectionResponse` schema and returns HTTP 201.
*Failures*: Pydantic validation errors (422), Domain rule violations (400), DB constraints (500).

## 2. Authentication Flow
1. **Presentation Layer**: Client POSTs credentials to `/api/v1/auth/login`.
2. **Application Layer**: `AuthenticateUserCommand` sent to handler.
3. **Infrastructure Layer**: `UserRepository` fetches user by email.
4. **Infrastructure Layer**: `PasswordService` hashes input via Argon2id and compares.
5. **Application Layer**: On success, `JwtService` generates Access and Refresh tokens.
6. **Presentation Layer**: Tokens returned. Subsequent requests include Access token in `Authorization` header.
7. **Security Layer**: FastAPI `Depends(get_current_user)` decodes JWT, verifies signature, checks expiration and roles.

## 3. Search Flow
1. **Presentation Layer**: `GET /api/v1/search?q=delhi`.
2. **Application Layer**: `GlobalSearchQuery` sent to handler.
3. **Infrastructure Layer**: Handler invokes `SearchAbstractionLayer.search()`.
4. **Infrastructure Layer**: SAL translates query to OpenSearch/Elasticsearch DSL.
5. **Infrastructure Layer**: Search Engine ranks and highlights results.
6. **Application Layer**: SAL maps raw engine hits back to `SearchResultDTO`s.
7. **Presentation Layer**: Router formats and returns HTTP 200.

## 4. AI/RAG Flow
1. **Presentation Layer**: Client asks question via WebSocket or HTTP.
2. **Application Layer**: `AnswerQuestionCommand` is dispatched.
3. **Infrastructure Layer**: Embed user query using Embedding Model.
4. **Infrastructure Layer**: Query Vector Database for similar document chunks (Hybrid RAG).
5. **Infrastructure Layer**: Format retrieved context and query into LLM Prompt.
6. **Infrastructure Layer**: Stream LLM response, verifying against Output Guardrails.
7. **Presentation Layer**: Stream chunks back to client with citations.

## 5. ETL Ingestion Flow
1. **Presentation Layer**: Admin uploads CSV to `/api/v1/etl/upload`.
2. **Infrastructure Layer**: CSV stored in temporary staging storage.
3. **Application Layer**: `ProcessEtlJobCommand` enqueued.
4. **Infrastructure Layer**: ETL worker reads CSV, parses rows.
5. **Domain/Application Layer**: Data validated against expected schemas.
6. **Infrastructure Layer**: Transformed data bulk-loaded into Staging tables.
7. **Infrastructure Layer**: SQL MERGE/UPSERT into production tables. Provenance metadata updated.

## 6. Real-Time Event Flow
1. **Domain Layer**: An `Election` changes status to "Active". `ElectionStatusChanged` event created.
2. **Application Layer**: UoW collects domain events during commit.
3. **Application Layer**: Events wrapped in `EventEnvelope` and published to `InMemoryEventBus`.
4. **Realtime Layer**: Listeners on EventBus receive envelope.
5. **Presentation Layer**: SSE / WebSocket manager filters events by client subscriptions.
6. **Presentation Layer**: Serialized event pushed to connected clients.

## 7. Cache Invalidation Flow
1. **Infrastructure Layer**: A write operation (e.g., updating a Candidate) commits successfully.
2. **Application Layer**: Post-commit event `CandidateUpdatedEvent` dispatched.
3. **Infrastructure Layer**: Cache listener receives event.
4. **Infrastructure Layer**: `CacheService.invalidate_tags(["candidate:{id}", "constituency_candidates"])` called.
5. **Infrastructure Layer**: Redis deletes all keys associated with those tags.

## 8. Health Check Flow
1. **Presentation Layer**: Load Balancer calls `GET /health`.
2. **Application Layer**: `GetSystemHealthQuery` dispatched.
3. **Infrastructure Layer**: Pings Postgres (`SELECT 1`).
4. **Infrastructure Layer**: Pings Redis (`PING`).
5. **Infrastructure Layer**: Checks disk space, memory usage.
6. **Application Layer**: Aggregates subsystem statuses into `HealthStatusDTO`.
7. **Presentation Layer**: Returns HTTP 200 (if healthy) or 503 (if critical systems down).
