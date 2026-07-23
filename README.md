# Election Intelligence Platform v1.0.0

[![CI/CD Pipeline](https://github.com/CivicLens-India/Election-Intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/CivicLens-India/Election-Intelligence/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/CivicLens-India/Election-Intelligence)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![Flutter](https://img.shields.io/badge/flutter-3.x-blue.svg)](https://flutter.dev)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **"The Election Intelligence Platform is an independent, politically neutral, AI-powered public research platform that helps Indian citizens make informed voting decisions by organizing, verifying, and explaining publicly available election information with complete transparency, evidence, and source attribution—without recommending or endorsing any candidate or political party."**

---

## Quick Start

```bash
# 1. Clone and set up
git clone https://github.com/CivicLens-India/Election-Intelligence.git
cd Election-Intelligence
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env   # edit DATABASE_URL and other required vars

# 3. Run database migrations
PYTHONPATH=backend .venv/bin/alembic upgrade head

# 4. Start the API server
PYTHONPATH=backend .venv/bin/uvicorn app.main:app --reload --port 8000

# 5. API docs
open http://localhost:8000/api/v1/docs
```

**Or with Docker:**
```bash
docker compose up -d --build
```

**Flutter mobile app:**
```bash
cd frontend && flutter pub get && flutter run
```

---

## Quality Status

| Gate | Command | Status |
| :--- | :--- | :--- |
| Backend lint | `ruff check backend` | ✅ 0 errors |
| Python compile | `python -m compileall backend` | ✅ 0 errors |
| Backend tests | `pytest` | ✅ 287 / 287 passed |
| Flutter analysis | `flutter analyze` | ✅ 0 issues |
| Flutter tests | `flutter test` | ✅ 6 / 6 passed |

---

## Documentation

All documentation lives in **[`docs/`](docs/INDEX.md)** — organized into 13 categories.

**→ [Browse the Documentation Index](docs/INDEX.md)**

Key starting points:

| I want to… | Document |
| :--- | :--- |
| Understand the full system | [System Operation Guide](docs/architecture/SYSTEM_OPERATION_GUIDE.md) |
| Set up my environment | [Development Guide](docs/development/DEVELOPMENT_GUIDE.md) |
| Onboard as a new developer | [New Developer Onboarding](docs/onboarding/NEW_DEVELOPER_ONBOARDING.md) |
| Deploy to production | [Deployment Runbook](docs/operations/DEPLOYMENT_RUNBOOK.md) |
| Understand the architecture | [Architecture](docs/architecture/ARCHITECTURE.md) |
| Read all commands | [Command Reference](docs/reference/COMMAND_REFERENCE.md) |

---

## Technology Stack

| Layer | Technology |
| :--- | :--- |
| API | Python 3.12, FastAPI 0.115, Pydantic v2 |
| Database | PostgreSQL 15, SQLAlchemy 2 async, Alembic |
| Cache | Redis 7, CacheService abstraction |
| Security | Argon2id, JWT, RBAC, OWASP headers |
| AI | Hybrid BM25 + Vector RAG, pluggable LLMProvider |
| Realtime | EventEnvelope, InMemoryEventBus, SSE, WebSocket |
| Observability | OpenTelemetry, Prometheus, JSON structured logs |
| Mobile | Flutter 3.x, Material 3, Riverpod, GoRouter |
| CI/CD | GitHub Actions, multi-stage Docker |

---

## Repository Structure

```text
.
├── backend/          # FastAPI Python backend (15 subsystems)
├── frontend/         # Flutter cross-platform app
├── tests/            # 287 pytest tests
├── docs/             # All documentation (70+ files, 13 categories)
├── .github/          # CI/CD workflows and CODEOWNERS
├── Dockerfile        # Multi-stage production image
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── CODE_OF_CONDUCT.md
```

---

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/development/DEVELOPER_WORKFLOW.md](docs/development/DEVELOPER_WORKFLOW.md) before submitting a pull request.

---

## Security

To report a security vulnerability, see [SECURITY.md](SECURITY.md).