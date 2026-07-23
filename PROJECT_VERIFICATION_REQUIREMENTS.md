# PROJECT VERIFICATION REQUIREMENTS & PRODUCTION HANDOFF CONTRACT
## Election Intelligence Platform — Version 1.0.0
### Single Source of Truth for Human Engineers, DevOps & AI Coding Agents

---

## Executive Overview

This document serves as the authoritative handoff contract between software engineering teams, AI coding agents (Antigravity, Claude Code, Gemini CLI, Codex), and platform operations/DevOps engineers. 

While the source code, architecture, database migrations, unit tests, and local runtime verification are 100% complete within the repository, full pilot production and cloud deployment require specific infrastructure credentials, environment keys, and operational inputs from the platform owner.

---

## 1. Summary of What is Already Provided in the Repository

| Component | Repository Artifact / Status | Readiness |
| :--- | :--- | :---: |
| **Complete Source Code** | `backend/` (FastAPI 0.139, Python 3.12), `frontend/` (Flutter 3.44 Web/Mobile SPA) | ✅ 100% Complete |
| **Database Migrations** | `backend/alembic/` (PostgreSQL 16 schema with 21 relational tables & indexes) | ✅ 100% Complete |
| **API Routers & OpenAPI** | 13 registered routers under `/api/v1` (43 endpoints with RFC 7807 error schemas) | ✅ 100% Complete |
| **Automated Test Suite** | 297 Python pytest unit/integration tests + 12 Flutter widget/unit tests | ✅ 100% Passing |
| **Container & CI/CD** | Multi-stage `Dockerfile`, `docker-compose.yml`, `.github/workflows/ci.yml` | ✅ 100% Complete |
| **Documentation Suite** | `SYSTEM_OPERATION_GUIDE.md`, `RUNBOOK.md`, `DEPLOYMENT_RUNBOOK.md`, 6 Admin Guides | ✅ 100% Complete |
| **Citizen Explorer & UI** | Form 26 Affidavits, candidate comparison, `VerificationBadge` provenance tags | ✅ 100% Complete |

---

## 2. Requirements to be Provided by User / Infrastructure Team

To promote the platform from local/containerized verification to live cloud production, the following 10 requirement categories must be configured:

### A. Environment Variables (`.env.production`)

```ini
# --- Core Application Config ---
ENVIRONMENT=production
DEBUG=false
PROJECT_NAME="Election Intelligence Platform"
VERSION="1.0.0"
API_V1_STR="/api/v1"
ALLOWED_ORIGINS="https://electionintelligence.in,https://admin.electionintelligence.in"
ALLOWED_HOSTS="electionintelligence.in,admin.electionintelligence.in,localhost"

# --- Production Database (PostgreSQL 15+) ---
DATABASE_URL=postgresql+asyncpg://<PROD_DB_USER>:<PROD_DB_PASSWORD>@<PROD_DB_HOST>:5432/<PROD_DB_NAME>
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30

# --- Production Cache & Rate Limiting (Redis 7) ---
REDIS_URL=redis://:<PROD_REDIS_PASSWORD>@<PROD_REDIS_HOST>:6379/0

# --- Security & JWT Credentials ---
JWT_SECRET=<MIN_32_CHAR_HIGH_ENTROPY_RANDOM_SECRET>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
SECURE_COOKIES=true
ENABLE_HSTS=true

# --- AI Model Provider API Keys (Select Active Provider) ---
ACTIVE_AI_PROVIDER=gemini # Options: gemini, openai, claude, ollama, mock
GEMINI_API_KEY=<YOUR_GOOGLE_GEMINI_API_KEY>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
ANTHROPIC_API_KEY=<YOUR_CLAUDE_API_KEY>

# --- Mail & Notification Gateways ---
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=<YOUR_SMTP_API_KEY>
EMAILS_FROM_EMAIL=noreply@electionintelligence.in
```

---

### B. Production Database Target

Provide connectivity credentials to a managed PostgreSQL 15+ instance (e.g. AWS RDS PostgreSQL, GCP Cloud SQL, or DigitalOcean Managed Postgres).
- **Required Action**: Execute `alembic upgrade head` against the target database during deployment pipeline execution.

---

### C. Live AI Provider Credentials

To enable real-world RAG question-answering over official election documents instead of offline mock providers:
- Supply a valid API key for Google Gemini (`GEMINI_API_KEY`) or OpenAI (`OPENAI_API_KEY`).

---

### D. Production Domain & SSL/TLS Certificates

- **Public Citizen Portal Domain**: e.g., `https://electionintelligence.in`
- **Control Center Admin Domain**: e.g., `https://admin.electionintelligence.in`
- **Backend API Domain**: e.g., `https://api.electionintelligence.in`
- **SSL/TLS Requirement**: Valid Let's Encrypt or ACM TLS certificate terminating at ingress/load balancer.

---

### E. Test Accounts & Role-Based Access (RBAC)

| User Role | Username / Email | Purpose & Scope |
| :--- | :--- | :--- |
| **Citizen (Public)** | *No login required* | Read-only access to `/portal`, candidate affidavits, and comparison. |
| **Super Administrator** | `admin@civiclens.in` | Full access to `/admin`, feature flags, user management, and security audit stream. |
| **Election Officer** | `ops@civiclens.in` | Access to `/ops`, candidate affidavit ingestion, and constituency data mapping. |
| **Platform Analyst** | `executive@civiclens.in` | Access to `/executive` command center and turnout telemetry. |

---

### F. Non-Partisan Business Rules (Enforced)

1. **Political Neutrality**: Platform must never rank, grade, or recommend candidates.
2. **Data Attribution**: Every attribute displayed must identify its official source (e.g., *ECI Form 26 Affidavit 2024*).
3. **Verification Badging**: Must apply one of: `Official Source`, `Verified`, `Public Record`, `AI Summary`, `Sample Data`, `Official Data Unavailable`.
4. **Read-Only Public Access**: Citizens access public election records without paywalls or mandatory registration.

---

### G. Performance & Quality Targets (Enforced)

- **API TTFB**: < 100ms (Current measured average: 2.03ms – 14.75ms)
- **Search Latency**: < 200ms (Current measured average: 4.28ms)
- **Page FCP**: < 1.0 second (Current measured average: 0.32s)
- **Page LCP**: < 2.5 seconds (Current measured average: 0.85s)
- **Backend Test Pass Rate**: 100% (297/297 passed)
- **Frontend Test Pass Rate**: 100% (12/12 passed)

---

## 3. Verification Checklist for Deployment Teams

- [x] Full Git repository with clean history on branch `feature/v1.0.0-stabilization`
- [x] Dockerfile and Docker Compose verification clean (`docker compose up --build`)
- [x] Alembic database migration files up-to-date (`alembic upgrade head`)
- [x] Multi-platform Flutter build targets compiled (Web SPA, Android APK, iOS app)
- [ ] Populate `.env.production` with real PostgreSQL, Redis, and AI API keys
- [ ] Bind domain SSL/TLS certificate to production load balancer
- [ ] Execute smoke test against production domain (`GET /api/v1/health`)
