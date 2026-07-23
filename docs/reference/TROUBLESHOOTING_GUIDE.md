# Troubleshooting Guide

This document provides comprehensive troubleshooting steps for the Election Intelligence Platform v1.0.0. For every problem, you will find symptoms, likely causes, diagnostic commands, and resolution steps.

## 1. Backend Startup Failures

**Symptoms:**
- The FastAPI application fails to start.
- `uvicorn` exits immediately with an error code.
- 502 Bad Gateway from reverse proxy.

**Likely Causes:**
- Missing or malformed `.env` file.
- `PYTHONPATH` not set correctly.
- Database connection refused (PostgreSQL not running or wrong `DATABASE_URL`).
- Redis connection refused.
- Python import errors due to missing dependencies.

**Diagnostic Commands:**
```bash
# Check uvicorn logs
cat logs/app.log
# Verify environment variables
env | grep DATABASE_URL
# Test python imports
python -c "import app.main"
```

**Resolution Steps:**
1. Ensure `.env` is present in the root directory and contains all required keys from `settings.py`.
2. Export `PYTHONPATH=backend` before running `uvicorn`.
3. Verify PostgreSQL and Redis are running (`docker ps`).
4. Run `pip install -r backend/requirements.txt` to ensure all dependencies are present.

## 2. Database Connection Issues

**Symptoms:**
- `asyncpg.exceptions.TooManyConnectionsError`.
- API endpoints return 500 Internal Server Error with timeout exceptions.
- `psycopg2.OperationalError: Connection refused`.

**Likely Causes:**
- PostgreSQL connection pool is exhausted.
- Incorrect `DATABASE_URL` credentials.
- Database migrations (`alembic upgrade head`) haven't been run.

**Diagnostic Commands:**
```bash
# Check active connections
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"
# Check migration status
alembic current
```

**Resolution Steps:**
1. Increase pool size in `settings.py` (e.g., `DB_POOL_SIZE=20`).
2. Verify `DATABASE_URL` matches your local or production database.
3. Run `alembic upgrade head` to apply missing migrations.

## 3. Authentication Failures

**Symptoms:**
- API returns 401 Unauthorized or 403 Forbidden.
- Login endpoint returns 400 Bad Request.

**Likely Causes:**
- Expired or invalid JWT token.
- User lacks required RBAC role.
- Argon2 hash mismatch due to changed secret keys.

**Diagnostic Commands:**
```bash
# Decode JWT to check expiration (exp) and roles
curl -s https://jwt.io/api/decode -d "token=<YOUR_TOKEN>"
```

**Resolution Steps:**
1. Re-authenticate to obtain a fresh JWT token.
2. Check the user's role in the database (`SELECT roles FROM users WHERE email='...';`).
3. Ensure the `JWT_SECRET` in `.env` matches the one used to generate the token.

## 4. Search Returning Empty Results

**Symptoms:**
- `/api/v1/search` returns `[]` for known entities.
- Geospatial queries return no results.

**Likely Causes:**
- Full-Text Search (FTS) index is missing or corrupted.
- Elasticsearch/PostgreSQL pg_trgm indices not updated.
- Incorrect search parameters (e.g., wrong bounding box).

**Diagnostic Commands:**
```bash
# Test raw SQL search
psql $DATABASE_URL -c "SELECT * FROM elections WHERE document_tokens @@ to_tsquery('english', 'query');"
```

**Resolution Steps:**
1. Rebuild the search index using the admin endpoint or script.
2. Verify the geospatial bounding box coordinates (Longitude, Latitude).
3. Ensure the search query is correctly formatted for FTS.

## 5. AI Query Failures

**Symptoms:**
- `/api/v1/ai/query` returns 500 or 503.
- Slow responses (>10s) ending in timeouts.
- Guardrail blocking valid queries.

**Likely Causes:**
- LLM provider API key missing or invalid.
- Rate limiting from the LLM provider.
- Strict guardrail rules blocking the prompt.

**Diagnostic Commands:**
```bash
# Check AI query logs
grep "ai_query" logs/app.log
```

**Resolution Steps:**
1. Verify `OPENAI_API_KEY` (or equivalent) in `.env`.
2. Implement exponential backoff for rate limits.
3. Review and adjust guardrail prompts in `app/ai/guardrails.py`.

## 6. Redis Connection Failures

**Symptoms:**
- CacheService throws exceptions.
- Rate limiting fails (either allows everything or blocks everything).
- API latency increases significantly.

**Likely Causes:**
- Redis server is down.
- Redis out of memory (OOM).
- Incorrect `REDIS_URL`.

**Diagnostic Commands:**
```bash
redis-cli -u $REDIS_URL ping
redis-cli -u $REDIS_URL info memory
```

**Resolution Steps:**
1. Restart Redis container (`docker compose restart redis`).
2. Ensure the app gracefully degrades if cache is unavailable (check fallback logic in `CacheService`).
3. Clear Redis cache if corrupted (`redis-cli flushall`).

## 7. ETL Ingestion Failures

**Symptoms:**
- Data import pipeline halts.
- CSV parsing errors logged.
- Staging table validations fail.

**Likely Causes:**
- Malformed CSV (e.g., missing columns, unescaped quotes).
- Data type mismatch (e.g., string in integer column).
- Unique constraint violations.

**Diagnostic Commands:**
```bash
# Check ETL error logs
grep "ETL_ERROR" logs/etl.log
```

**Resolution Steps:**
1. Sanitize the input CSV (ensure UTF-8 encoding, correct headers).
2. Check Pydantic validation models in `app/schemas/etl.py`.
3. Clear the staging table and restart the job.

## 8. Performance Degradation

**Symptoms:**
- P99 latency > 1000ms.
- Connection pool exhaustion.
- High CPU usage on the API servers.

**Likely Causes:**
- Missing database indexes causing sequential scans.
- N+1 query problems in SQLAlchemy/AsyncPG.
- Cache miss storm.

**Diagnostic Commands:**
```bash
# Check slow queries in PostgreSQL
psql $DATABASE_URL -c "SELECT query, total_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 5;"
```

**Resolution Steps:**
1. Analyze slow queries using `EXPLAIN ANALYZE` and add indexes.
2. Verify Redis cache hit ratios.
3. Optimize ORM queries to use joins (`selectinload` or equivalent).

## 9. Docker Compose Issues

**Symptoms:**
- `docker compose up` fails.
- Containers exit with code 1 or 137 (OOM).
- Networking issues between containers (e.g., API can't reach DB).

**Likely Causes:**
- Port conflicts on the host machine.
- Incorrect volume mounts.
- Insufficient memory allocated to Docker.

**Diagnostic Commands:**
```bash
docker compose logs backend
docker compose ps
docker inspect <container_id>
```

**Resolution Steps:**
1. Free up required ports (e.g., 8000, 5432, 6379).
2. Remove orphaned volumes (`docker compose down -v`) and rebuild.
3. Increase Docker Desktop memory limits.

## 10. Flutter App Issues

**Symptoms:**
- `flutter run` fails to build.
- App crashes on startup.
- Network errors when connecting to the local API.

**Likely Causes:**
- Incompatible Flutter SDK version.
- Missing dependencies (`flutter pub get` not run).
- iOS/Android build misconfigurations (e.g., missing CocoaPods).
- App pointing to wrong API URL (e.g., `localhost` instead of `10.0.2.2` on Android emulator).

**Diagnostic Commands:**
```bash
flutter doctor -v
flutter clean
flutter run -v
```

**Resolution Steps:**
1. Run `flutter clean` and `flutter pub get`.
2. Update the API base URL in the Flutter `.env` or config to match the emulator environment.
3. For iOS, run `cd ios && pod install`.

## 11. Test Failures

**Symptoms:**
- `pytest` reports failures or errors.
- Tests hang indefinitely.
- "Database already exists" or "Table not found" errors.

**Likely Causes:**
- Async event loop conflicts.
- Test database not properly initialized or torn down.
- Missing test environment variables.

**Diagnostic Commands:**
```bash
pytest -v --tb=short
pytest --setup-show
```

**Resolution Steps:**
1. Ensure `pytest-asyncio` is configured properly (e.g., `asyncio_mode = auto`).
2. Use a separate test database and apply Alembic migrations in the test setup fixture.
3. Check for leaked connections in async tests.

## 12. Linting Failures

**Symptoms:**
- CI pipeline fails on the linting step.
- `ruff check` returns multiple errors.

**Likely Causes:**
- Trailing whitespace, unused imports, or line length violations.
- Missing docstrings.

**Diagnostic Commands:**
```bash
ruff check .
ruff format --check .
```

**Resolution Steps:**
1. Run `ruff format .` to auto-format code.
2. Run `ruff check --fix .` to auto-fix safe linting errors.
3. Use `# noqa: <CODE>` sparingly to suppress unavoidable warnings.
