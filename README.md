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

## Product Roadmap & Release Milestones

### 🟢 Version 1.0.0 — Production Core Release (Current Stable)
- ✅ **Core CQRS & FastAPI Backend**: 43 endpoints across 13 domain routers.
- ✅ **PostgreSQL 16 Schema**: 21 relational tables with Alembic migrations.
- ✅ **Live AI RAG Integration**: Live Mistral AI (`mistral-small-latest`) & Google Gemini AI adapters with 1 RPS rate-limit throttling.
- ✅ **Form 26 Affidavit Data Models**: Asset declarations, liabilities, educational qualifications, and criminal antecedents.
- ✅ **Flutter Web & Mobile SPA**: Citizen explorer portal & non-partisan side-by-side candidate comparison views.
- ✅ **Data Provenance System**: `Official Source`, `Verified Public Record`, `AI Summary`, `Sample Data`, `Data Not Available`.
- ✅ **Strict Neutrality Engine**: Pure evidence-first summaries without candidate ratings or voting recommendations.

### 🟡 Version 1.1.0 — Milestone 26: Deep Constituency & Party Analytics
- 🚀 **Deep Constituency Intelligence**: Population demographics, literacy rates, historical vote margins, and development indicators.
- 🚀 **Deep Party Intelligence**: Manifesto archives, alliance trackers, historical seat share charts, and leadership timelines.
- 🚀 **Multi-Tier Election Filters**: Dedicated navigation tabs for Lok Sabha, Vidhan Sabha (State Assembly), Municipal Corporations, and Panchayats.
- 🚀 **Affidavit Report Exporter**: Downloadable PDF/CSV candidate comparison reports for offline voter discussions.

### 🔵 Version 1.2.0 — Milestone 27: Fact-Check & Media Timeline Integration
- 🚀 **Verified Fact-Check Engine**: Integration with IFCN-certified fact-checking organizations (Alt News, Boom Live, Quint WebQoof).
- 🚀 **Candidate News Timeline**: Chronological stream of verified public news reports linked with primary source URLs.
- 🚀 **Promise Tracker**: Automated tracking of candidate manifesto commitments vs completed infrastructure projects.

### 🟣 Version 1.3.0 — Milestone 28: Multi-Lingual & Voice Intelligence
- 🚀 **12 Indian Languages**: Native support for Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese, and Urdu.
- 🚀 **Voice Assistant**: Voice-activated natural language queries for low-literacy rural voters.

### 🔴 Version 2.0.0 — Milestone 29: Open API & Decentralized Civic Network
- 🚀 **Public Developer API**: Open API platform for journalists, researchers, NGOs, and civil society organizations.
- 🚀 **Crowdsourced Affidavit Audit**: Decentralized peer verification of candidate affidavit disclosures.
- 🚀 **Offline-First SMS & WhatsApp Bot**: Automated querying for citizens without high-speed internet access.

---

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/development/DEVELOPER_WORKFLOW.md](docs/development/DEVELOPER_WORKFLOW.md) before submitting a pull request.

---

## Security

To report a security vulnerability, see [SECURITY.md](SECURITY.md).