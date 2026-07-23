# Frequently Asked Questions (FAQ)

This FAQ covers common questions about the Election Intelligence Platform v1.0.0.

## Setup & Environment (Q1-Q15)

1. **What version of Python is required?** Python 3.12 is required for backend compatibility.
2. **How do I configure the database URL?** Set the `DATABASE_URL` environment variable in your `.env` file using the postgres:// format.
3. **Do I need Redis locally?** Yes, Redis is required for caching and rate limiting. Use Docker Compose to spin it up.
4. **How do I install Flutter dependencies?** Run `flutter pub get` in the `frontend/` directory.
5. **Why isn't my `.env` file loading?** Ensure it's in the project root and you're running uvicorn from the root directory.
6. **How do I manage environment variables in production?** We use Pydantic `BaseSettings` which reads from environment variables seamlessly in Docker/k8s.
7. **Is Docker required for local development?** It's recommended for dependencies like PostgreSQL and Redis, though you can run the FastAPI app locally.
8. **How do I start the entire stack?** `docker compose up --build`.
9. **What is the `PYTHONPATH=backend` requirement?** Our imports are structured as `app.module`, so the `backend` folder must be on the python path.
10. **Can I use SQLite instead of PostgreSQL?** No, we rely on PostgreSQL-specific features like pg_trgm and JSONB.
11. **How do I clear the local cache?** Connect to redis (`redis-cli`) and run `FLUSHALL`.
12. **How do I update the frontend SDK?** Update the version in `pubspec.yaml` and run `flutter pub upgrade`.
13. **Where are the environment templates?** Copy `.env.example` to `.env` to start.
14. **How do I format my code?** Run `ruff format backend/`.
15. **What IDE is recommended?** VS Code or PyCharm for backend, VS Code or Android Studio for Flutter.

## Architecture & Design (Q16-Q30)

16. **Why Clean Architecture?** It separates business logic from framework details, making the codebase easier to test and maintain.
17. **What is the UnitOfWork pattern used for?** It manages database transactions, ensuring all operations in a request commit or rollback together.
18. **Where does business logic go?** In the `app/services/` layer, never in API routers or database models.
19. **What's an EventEnvelope?** A standardized schema used for publishing messages to our message broker or webhooks.
20. **Why AsyncPG?** It's a highly performant, fully asynchronous driver for PostgreSQL, ideal for FastAPI.
21. **How is configuration managed?** Through `app/settings.py` using Pydantic `BaseSettings`.
22. **What is the repository pattern used for?** To abstract database queries, allowing us to swap implementations or mock data for tests.
23. **Why use Redis?** For high-speed caching of expensive search queries and managing API rate limiting.
24. **How are background tasks handled?** Currently using FastAPI's `BackgroundTasks`, moving to Celery/ARQ for heavy ETL in the future.
25. **Is the backend monolithic or microservices?** It's a modular monolith.
26. **What is the role of OpenTelemetry?** To provide distributed tracing across the backend, database, and external API calls.
27. **Why Argon2 over bcrypt?** Argon2 is the winner of the Password Hashing Competition and provides better resistance against GPU cracking.
28. **How do we handle dependencies?** We use FastAPI's dependency injection (`Depends()`).
29. **What architectural pattern does the Flutter app use?** Provider/Riverpod for state management with a repository pattern for API calls.
30. **How does RAG work here?** Retrieval-Augmented Generation fetches relevant documents from PostgreSQL (FTS) and passes them to the LLM.

## Backend Development (Q31-Q45)

31. **How do I add an endpoint?** Create a route in the appropriate file in `app/api/routers/` and register it in `app/main.py`.
32. **How do I add a new domain entity?** Create a SQLAlchemy model in `app/models/`, a Pydantic schema in `app/schemas/`, and a repository in `app/repositories/`.
33. **What is the correct way to return errors?** Raise an `HTTPException` with the proper status code and detail string.
34. **How do I parse JSON requests?** Define a Pydantic model and use it as a type hint in the router function.
35. **How do I validate query parameters?** Use FastAPI's `Query()` dependency with Pydantic types.
36. **How do I handle file uploads?** Use FastAPI's `UploadFile` type in the route definition.
37. **What linter do we use?** Ruff. It's fast and replaces both flake8 and black.
38. **How do I resolve a Ruff error?** Read the error code, fix it manually, or run `ruff check --fix`.
39. **Where should I put third-party API integrations?** In the `app/integrations/` or `app/services/` folder.
40. **How do I mock external APIs?** Use `responses` or `pytest-httpx` in tests.
41. **How are dates handled?** Always use UTC datetimes and `pydantic` datetime fields.
42. **What is `db: AsyncSession = Depends(get_db)`?** It injects a fresh database session into the request context.
43. **How do I serialize SQLAlchemy models?** Return them directly from the router; FastAPI will validate and serialize them via the `response_model`.
44. **Why are some routes sync and others async?** DB or IO operations must be `async def`. Pure CPU or simple returns can be `def`.
45. **How do I log something?** Import the configured logger from `app.logging` and use `logger.info()`.

## Database & Migrations (Q46-Q55)

46. **How do I create a new migration?** `alembic revision --autogenerate -m "description"`.
47. **Why did my migration fail?** Ensure your database is running and `DATABASE_URL` is correct.
48. **How do I seed the database?** Use the `scripts/seed_db.py` script.
49. **How do I rollback a migration?** `alembic downgrade -1`.
50. **Where are models imported for Alembic?** In `alembic/env.py`.
51. **How do I use JSONB?** Use SQLAlchemy's `JSONB` type from `sqlalchemy.dialects.postgresql`.
52. **How do I create an index?** Define it in the SQLAlchemy model `__table_args__` or directly in the Alembic migration.
53. **Why use UUIDs for primary keys?** They are secure against enumeration and allow distributed ID generation.
54. **How do I write raw SQL safely?** Use SQLAlchemy's `text()` function and bind parameters to prevent SQL injection.
55. **How is the DB pool configured?** In `app/db/session.py` via `create_async_engine()`.

## API & Authentication (Q56-Q65)

56. **How does authentication work?** We use JWT Bearer tokens passed in the `Authorization` header.
57. **How do I protect an endpoint?** Use `Depends(get_current_user)`.
58. **How is RBAC implemented?** Use `Depends(require_role("admin"))` in the router.
59. **How long do tokens live?** Configured via `ACCESS_TOKEN_EXPIRE_MINUTES` in settings (default 30 mins).
60. **How do I refresh a token?** Use the `/api/v1/auth/refresh` endpoint.
61. **Where can I see the API docs?** Navigate to `/api/v1/docs` (Swagger UI).
62. **How do I customize Swagger documentation?** Use the `summary`, `description`, and `responses` params in the router decorator.
63. **How does rate limiting work?** Using Redis sliding window. Configurable via annotations on the route.
64. **What hashing algorithm is used?** Argon2.
65. **How do I reset a password?** Admins can reset it via the users CRUD endpoint, or users via the forgot-password flow.

## Search & AI (Q66-Q75)

66. **How is search implemented?** Using PostgreSQL Full-Text Search (FTS).
67. **How do I filter search results?** Pass query params to `/api/v1/search`.
68. **What does the AI query endpoint do?** It takes a prompt, enriches it via RAG, and queries the configured LLM.
69. **Which LLM providers are supported?** OpenAI and Anthropic, configurable via `.env`.
70. **How are AI guardrails implemented?** We intercept prompts and screen them against blocklists in `app/ai/guardrails.py`.
71. **What is geospatial search used for?** Filtering electoral data by bounding boxes or distance from coordinates.
72. **How do I update the search index?** It updates automatically via SQLAlchemy event listeners or DB triggers.
73. **Is the AI context window limited?** Yes, we truncate RAG documents to fit within the model's token limits.
74. **How is AI output validated?** We request JSON format from the LLM and parse it via Pydantic.
75. **How do I mock AI responses in tests?** Use the dummy LLM provider in `app/ai/dummy.py` during testing.

## Testing (Q76-Q85)

76. **How do I run the tests?** `pytest`.
77. **Where are the tests located?** In the `backend/tests/` directory.
78. **How do I write an async test?** Use the `@pytest.mark.asyncio` decorator.
79. **How is the test database handled?** A temporary PostgreSQL DB is created, migrated, and torn down in fixtures.
80. **What is a fixture?** A reusable test dependency provided by `conftest.py`.
81. **How do I test an API endpoint?** Use `AsyncClient` from `httpx`.
82. **How do I mock the database?** Use `unittest.mock.MagicMock` on the repository layer.
83. **How do I check test coverage?** Run `pytest --cov=app`.
84. **Why are my tests slow?** Database IO is the main bottleneck. Use transactional rollback fixtures to speed them up.
85. **How do I run a single test?** `pytest tests/path_to_test.py::test_function_name`.

## Flutter & Mobile (Q86-Q90)

86. **How do I build the Flutter app?** `flutter build apk` or `flutter build ios`.
87. **How does the app talk to the backend?** Using the `http` or `dio` package, mapped to repository classes.
88. **How is state managed?** Using `Riverpod`.
89. **How do I handle environment variables in Flutter?** Using the `flutter_dotenv` package.
90. **How do I test Flutter UI?** Use `flutter test` for widget tests.

## DevOps & Deployment (Q91-Q95)

91. **How is the app deployed?** Via Docker containers to ECS/Kubernetes.
92. **How are secrets managed?** Using AWS Secrets Manager or HashiCorp Vault in production.
93. **What CI/CD tool is used?** GitHub Actions.
94. **How do I view production logs?** Check Datadog or CloudWatch.
95. **How are backups handled?** RDS automated backups for PostgreSQL.

## Troubleshooting (Q96-Q105)

96. **Uvicorn exits immediately.** Check `.env` and database connectivity.
97. **502 Bad Gateway.** The backend container crashed or the load balancer is pointing to a dead port.
98. **Database pool exhausted.** Increase `DB_POOL_SIZE` or fix connection leaks.
99. **401 Unauthorized.** Your JWT token is expired or invalid.
100. **Search is empty.** Ensure Alembic migrations are up to date and data is seeded.
101. **AI Query times out.** Check your `OPENAI_API_KEY` or LLM provider status.
102. **Redis connection refused.** Ensure the Redis container is running.
103. **ETL ingestion fails.** Check the CSV format and column types.
104. **Performance is slow.** Check Grafana metrics for slow queries.
105. **Tests fail locally.** Ensure you have a running PostgreSQL instance for testing.
