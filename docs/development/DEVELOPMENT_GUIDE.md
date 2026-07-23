# Development Guide: Election Intelligence Platform

Welcome to the Election Intelligence Platform v1.0.0. This guide outlines the setup and daily development workflow.

## 1. Prerequisites

Ensure the following tools are installed on your system before proceeding:
- **Python 3.12+**
- **Flutter 3.x+** (with iOS/Android toolchains if required)
- **Docker & Docker Compose**
- **PostgreSQL 16+** (Local or via Docker)
- **Redis 7+** (Local or via Docker)
- **Git**

## 2. Environment Setup

Clone the repository and set up the development environment:

```bash
# 1. Clone the repository
git clone https://github.com/organization/election-intelligence.git
cd election-intelligence

# 2. Set up Python virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Set up Flutter environment
cd frontend
flutter pub get
cd ..
```

## 3. Environment Variables (.env)

Create a `.env` file in the root directory based on `.env.example`.

```env
# Database configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/election_db
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
DB_POOL_PRE_PING=True
DB_ECHO=False

# Application Environment
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG

# Security and Networking
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
ALLOWED_HOSTS=localhost,127.0.0.1
SECURE_COOKIES=False
MAX_REQUEST_SIZE=5242880
ENABLE_HSTS=False
CONTENT_SECURITY_POLICY="default-src 'self'"
```

## 4. Database Setup

We use Alembic for PostgreSQL database migrations. Ensure your database is running before executing these steps.

```bash
# Navigate to the backend directory
cd backend

# Run all migrations up to head
alembic upgrade head

# Seed initial development data
python -m scripts.seed_data
```

## 5. Running the Backend

Start the FastAPI application using Uvicorn. The backend runs on port 8000.

```bash
PYTHONPATH=backend uvicorn app.main:app --reload --port 8000
```
**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12347]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 6. Running the Flutter App

Navigate to the frontend directory and start the application.

```bash
cd frontend
flutter run -d chrome  # Run on web
# OR
flutter run            # Run on available device/emulator
```

## 7. Quality Gates

Run all quality checks before committing code.

**Backend Checks:**
```bash
# Linting & Formatting (Ruff)
ruff check backend
ruff format backend

# Compile Check
python -m compileall backend

# Tests (Pytest)
pytest
```
*Expected output for pytest:*
```
================ test session starts ================
collected 287 items
tests/test_api.py ...
tests/test_domain.py ...
...
================ 287 passed in 4.52s ================
```

**Frontend Checks:**
```bash
cd frontend

# Static Analysis
flutter analyze

# Unit & Widget Tests
flutter test
```
*Expected output for flutter test:*
```
00:02 +6: All tests passed!
```

## 8. Docker Compose Workflow

To run the entire stack (Database, Redis, API) via Docker:

```bash
# Start all services in the background
docker compose up -d

# View logs for the backend API
docker compose logs -f api

# Execute a command inside the DB container
docker compose exec db psql -U user -d election_db

# Stop and remove containers
docker compose down
```

## 9. Common Development Tasks

- **Adding a route:** Create a new router in `backend/app/api/v1/endpoints/`, then include it in `backend/app/api/v1/api.py`.
- **Running a specific test:** `pytest backend/tests/test_file.py::test_function_name -v`
- **Checking logs:** Monitor logs in the terminal running uvicorn or via `docker compose logs`.
- **Connecting to DB:** Use a tool like DBeaver or run `psql $DATABASE_URL`.

## 10. IDE Recommendations

**VS Code Setup:**
- Extensions: Python, Pylance, Ruff, Flutter, Dart, Docker.
- `settings.json`:
  ```json
  {
    "[python]": {
      "editor.defaultFormatter": "charliermarsh.ruff",
      "editor.formatOnSave": true,
      "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
      }
    },
    "[dart]": {
      "editor.formatOnSave": true
    },
    "python.testing.pytestEnabled": true
  }
  ```
