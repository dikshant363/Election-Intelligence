# Command Reference

The definitive cheat sheet for the Election Intelligence Platform v1.0.0.

## 1. Setup Commands

**Clone the repository:**
```bash
git clone https://github.com/civiclens/election-intelligence.git
cd election-intelligence
```

**Create and activate virtual environment:**
```bash
python3.12 -m venv venv
source venv/bin/activate
```

**Install backend dependencies:**
```bash
pip install -r backend/requirements.txt
```

**Install Flutter dependencies:**
```bash
cd frontend
flutter pub get
```

## 2. Backend Run Commands

**Run in development (with reload):**
```bash
PYTHONPATH=backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*Expected Output: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)*

**Run in production:**
```bash
PYTHONPATH=backend uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

## 3. Quality Gate Commands

**Linting (Ruff):**
```bash
ruff check backend/
ruff format backend/
```

**Run Backend Tests:**
```bash
PYTHONPATH=backend pytest backend/tests/ -v --cov=app
```

**Flutter Analyze & Test:**
```bash
cd frontend
flutter analyze
flutter test
```

## 4. Database Commands

**Run all migrations:**
```bash
PYTHONPATH=backend alembic upgrade head
```

**Rollback one migration:**
```bash
PYTHONPATH=backend alembic downgrade -1
```

**Create a new migration:**
```bash
PYTHONPATH=backend alembic revision --autogenerate -m "Add new table"
```

**Connect to database via psql:**
```bash
psql $DATABASE_URL
```

## 5. Docker Commands

**Start all services:**
```bash
docker compose up -d
```

**Stop all services:**
```bash
docker compose down
```

**View logs:**
```bash
docker compose logs -f backend
```

**Rebuild images:**
```bash
docker compose build --no-cache
```

## 6. Git Commands

**Conventional Commits format:**
```bash
git commit -m "feat(auth): add JWT bearer validation"
git commit -m "fix(db): resolve connection pool leak"
```

**Create feature branch:**
```bash
git checkout -b feature/xyz
```

## 7. API Testing Commands

**Check Health:**
```bash
curl -X GET http://localhost:8000/api/v1/health
```
*Expected Output: `{"status": "ok"}`*

**Login (Get Token):**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password"
```

**Search:**
```bash
curl -X GET "http://localhost:8000/api/v1/search?q=election" \
  -H "Authorization: Bearer <TOKEN>"
```

**AI Query:**
```bash
curl -X POST http://localhost:8000/api/v1/ai/query \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarize the election data."}'
```

## 8. Debugging Commands

**Connect to Redis:**
```bash
docker exec -it election_redis redis-cli
```

**Check active DB connections:**
```bash
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"
```

## 9. Observability Commands

**Get Metrics (Prometheus format):**
```bash
curl -s http://localhost:8000/api/v1/metrics
```

**Get Diagnostics:**
```bash
curl -s http://localhost:8000/api/v1/diagnostics
```

## 10. Flutter Commands

**Run App:**
```bash
flutter run
```

**Build APK for Android:**
```bash
flutter build apk --release
```

**Build iOS App:**
```bash
flutter build ios --release
```