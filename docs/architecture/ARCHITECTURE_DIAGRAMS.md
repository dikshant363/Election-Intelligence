# Architecture Diagrams

This document visually describes the Election Intelligence Platform v1.0.0 using ASCII art and sequence flows.

## 1. System Context Diagram

```text
+----------------+      +---------------------------+      +------------------+
|                |      |                           |      |                  |
|  Mobile User   +----->+  Election Intelligence    +----->+  Govt APIs       |
|  (Flutter App) |      |  Platform (Backend API)   |      |  (Future v1.4)   |
|                |      |                           |      |                  |
+----------------+      +-------------+-------------+      +------------------+
                                      |
                                      v
                             +--------+--------+
                             |                 |
                             |  LLM Provider   |
                             |  (OpenAI/etc)   |
                             |                 |
                             +-----------------+
```

## 2. Container Diagram

```text
+-----------------------------------------------------------------+
|                         Deployment Env                          |
|                                                                 |
|  +--------------+    +---------------+    +------------------+  |
|  |              |    |               |    |                  |  |
|  | Flutter App  +--->+  FastAPI App  +--->+  PostgreSQL 15   |  |
|  | (Client)     |    |  (Backend)    |    |  (Relational DB) |  |
|  |              |    |               |    |                  |  |
|  +--------------+    +-------+-------+    +------------------+  |
|                              |                                  |
|                              v                                  |
|                      +-------+-------+    +------------------+  |
|                      |               |    |                  |  |
|                      |  Redis Stack  +--->+  Celery Workers  |  |
|                      |  (Cache/Queue)|    |  (Background)    |  |
|                      |               |    |                  |  |
|                      +---------------+    +------------------+  |
+-----------------------------------------------------------------+
```

## 3. Clean Architecture Layers

```text
+-----------------------------------------------------------------------+
| Presentation Layer: backend/app/api/v1/routers/                       |
| FastAPI Endpoints, Pydantic Schemas, Dependency Injection             |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| Application Layer: backend/app/application/                           |
| CQRS Commands/Queries, Handlers, DTOs, Validators                     |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| Domain Layer: backend/app/domain/                                     |
| Entities (Election, Candidate), Value Objects, Repository Interfaces  |
+-----------------------------------+-----------------------------------+
                                    ^
                                    | (Implements Interfaces)
+-----------------------------------------------------------------------+
| Infrastructure Layer: backend/app/persistence/                        |
| SQLAlchemy Models, Repositories, Redis Clients, External APIs         |
+-----------------------------------------------------------------------+
```

## 4. Domain Model Diagram

```text
+--------------+ 1      * +----------------+
|              | -------- |                |
|  Election    |          | Constituency   |
|              | -------- |                |
+------+-------+ 1      * +-------+--------+
       |                          | 1
       | 1                        |
       |                          | *
       | *                +-------+--------+
+------+-------+ *      1 |                |
|              | -------- | PollingBooth   |
|  Candidate   |          |                |
|              |          +----------------+
+------+-------+
       | *
       |                  +----------------+
       | 1                |                |
+------+-------+          |    Result      |
|              |          | (Maps Election,|
|    Party     |          |  Candidate,    |
|              |          |  Constituency) |
+--------------+          +----------------+
```

## 5. API Request Flow Sequence

1. Client sends `GET /api/v1/candidates/{id}`
2. **Router** (`api/v1/routers/candidates.py`) receives request and creates `GetCandidateQuery(id)`.
3. **QueryHandler** (`application/handlers/get_candidate.py`) is invoked.
4. Handler calls **Repository** (`domain/candidate/repository.py` interface).
5. **SQLAlchemyRepository** (`persistence/repositories/candidate.py`) fetches data from DB.
6. **Mapper** converts ORM model to Domain Entity.
7. Handler converts Domain Entity to DTO and returns it.
8. Router serializes DTO to Pydantic Response Schema and sends to Client.

## 6. Authentication Flow Sequence

1. Client sends Credentials to `/api/v1/auth/token`.
2. Router calls Auth Service to verify credentials.
3. Auth Service checks password hash in Database.
4. If valid, Auth Service generates JWT Token.
5. Router returns JWT to Client.
6. Client sends JWT in `Authorization: Bearer <token>` header on subsequent requests.
7. FastAPI Dependency decodes JWT, verifies expiration, and injects CurrentUser.

## 7. Search Flow Sequence

1. Client sends query to `/api/v1/search?q=modi`.
2. Router creates `SearchQuery(term="modi")`.
3. Handler sends term to **Search Abstraction Layer**.
4. Abstraction Layer queries Elasticsearch/PostgreSQL Full-Text Search.
5. Results are hydrated from DB if necessary.
6. Handler formats results into `SearchResultDTO`.
7. Router returns results to Client.

## 8. RAG/AI Flow Sequence

1. Client asks "Who won in Varanasi in 2019?".
2. API converts query to embeddings via embedding model.
3. Vector DB (Redis/pgvector) searches for similar document chunks.
4. Context is assembled from retrieved chunks.
5. LLM prompt is constructed: "Use this context: {context}. Answer: {query}".
6. LLM Provider generates response.
7. Response and citations returned to Client.

## 9. ETL Pipeline Flow

1. Cron job triggers Celery Worker daily.
2. Extractor fetches raw data from Government ECI portal.
3. Transformer cleans data, maps to Domain Entities.
4. Loader bulk inserts/updates records via SQLAlchemy UnitOfWork.
5. Process updates Redis caches and rebuilds search indexes.

## 10. Real-time Event Flow

1. CommandHandler modifies an Entity (e.g., Result updated).
2. Entity generates `ResultUpdatedDomainEvent`.
3. Handler publishes event to `EventBus`.
4. EventBus routes to Redis Pub/Sub channel.
5. WebSocket/SSE Manager listens to Redis channel.
6. Manager broadcasts serialized event to connected Clients in real-time.

## 11. Deployment Architecture

```text
[ Internet ]
      |
[ Cloud Load Balancer (HTTPS) ]
      |
      +---> [ API Instance 1 ] --+
      |                          |---> [ Redis (Cache/PubSub) ]
      +---> [ API Instance 2 ] --+
                                 |---> [ PostgreSQL (Primary) ]
                                 |---> [ PostgreSQL (Replica) ]
```

## 12. CI/CD Pipeline

1. **Push**: Developer pushes code to GitHub.
2. **Lint**: GitHub Actions runs Ruff (Python) and `dart analyze`.
3. **Test**: Runs Pytest and Flutter tests. Fails if coverage < 80%.
4. **Build**: Builds Docker images, builds Flutter APK/Web bundle.
5. **Deploy**: If merged to `main`, pushes Docker image to Registry and triggers Render/AWS deployment.
