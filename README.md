# Election Intelligence Platform v1.0.0

[![Architecture](https://img.shields.io/badge/architecture-Pure%20Rust%20%7C%20Axum-orange.svg)](https://www.rust-lang.org)
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL%2017-blue.svg)](https://www.postgresql.org)
[![Design](https://img.shields.io/badge/design-Apple%20HIG%20%26%20WCAG%202.2%20AA-silver.svg)](https://developer.apple.com/design/human-interface-guidelines/)
[![Frontend Compatibility](https://img.shields.io/badge/frontend-Next.js%2015%20%7C%20Leptos-black.svg)](https://nextjs.org)
[![Security](https://img.shields.io/badge/audit-SHA--256%20Tamper--Evident-success.svg)](SECURITY.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*Election Intelligence Platform is an independent, politically neutral, AI-powered public research platform that helps Indian citizens, researchers, and election administrators make informed decisions by organizing, verifying, and explaining publicly available election records with complete transparency, evidence, and statutory source attribution—without recommending or endorsing any candidate or political party.*

---

## Architecture Overview

The platform features an enterprise-grade full-stack architecture engineered for sub-millisecond latency, verified data persistence, and strict political neutrality:

```
[ Indian Citizen / Administrator ]
               │
               ▼
┌──────────────────────────────────────────────┐
│  Civic Restraint UI (Apple HIG / Stitch)    │
│  - Warm Studio Canvas & Tabular Numerals     │
│  - Public Research Homepage (/)             │
│  - Candidate Profiles & Form 26 (/candidates)│
│  - Constituency Explorer (/constituencies)   │
│  - Certified Results & Analytics (/results)  │
│  - Grounded AI Research Assistant (/ai)      │
│  - Evidence Source Explorer (/evidence)      │
│  - Community & Ingestion Pipeline (/admin)   │
│  - Command Palette (⌘K) & AI Query (⌘J)     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│       Axum 0.7 + Tokio + SQLx Backend        │
│  - RESTful OpenAPI v1 Endpoints              │
│  - In-Process Multi-Field BM25 Ranker        │
│  - Grounded AI Verifier (Statutory Citations)│
│  - Cryptographic SHA-256 Chained Audit Log   │
│  - CQRS Transactional Pipelines & Invariants │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│           PostgreSQL 17 Database             │
│  - 20 Relational Tables & Trigram Indexes    │
│  - ECI Declarations & Form 26 Disclosures    │
│  - Immutable Audit Event Hash Ledger         │
└──────────────────────────────────────────────┘
```

---

## Core Guarantees

1. **Strict Political Neutrality**: Equal representation of all political parties (BJP, INC, SP, AITC, DMK, AAP, independents). No endorsements, partisan rankings, or algorithmic bias.
2. **Evidence-First Grounding**: All candidate assertions, vote tallies, and declared assets cite verified sources (ECI Gazettes, ADR/MyNeta Form 26 filings).
3. **Legal Distinction Integrity**: Strict statutory differentiation between pending criminal allegations/trials in progress and judicial convictions.
4. **Tamper-Evident Auditability**: Cryptographically chained SHA-256 audit ledger with sequence verification to guarantee administrative log integrity.
5. **Apple HIG Design Restraint**: High-contrast, accessibility-first (WCAG 2.2 AA) typography and layout with keyboard navigation (`⌘K`, `⌘J`, `Esc`).

---

## Key Features & Production Surfaces

### 1. Public Research Homepage (`/`)
- Verbatim non-partisan mission statement, ECI gazette links, registered elector counts, and live search hub with keyboard shortcut (`⌘K`).

### 2. Candidate Profiles & Form 26 Disclosures (`/candidates`)
- Complete breakdown of declared movable/immovable assets, declared liabilities, educational credentials, and verified criminal case disclosures distinguishing pending allegations from convictions.

### 3. Constituency Explorer & Boundaries (`/constituencies`)
- Demographic statistics, reserved status (General, SC, ST), registered voter counts, booth allocations, and historical turnout metrics.

### 4. Certified Results & Analytics Workspace (`/results`)
- Verified vote tallies, margin computations, postal vs EVM ballot distributions, and regional turnout aggregations.

### 5. Evidence-Grounded AI Research Assistant (`/ai`)
- Conversational research engine citing specific statutory paragraphs from ECI declarations and ADR filings. Pre/post-generation prompt injection guardrails with deterministic abstention when evidence is insufficient.

### 6. Evidence Source Explorer & Provenance (`/evidence`)
- Complete source provenance registry with publisher authority categories, retrieval dates, and document hashes.

### 7. Community Ingestion & Administration (`/community`, `/admin`)
- Batch CSV/JSON data ingestion pipeline, dynamic runtime feature flags, and append-only cryptographic SHA-256 audit ledger.

---

## API Endpoints

All endpoints are available under `/api/v1/*`:

- `GET /api/v1/health` — Platform telemetry, component health, and database connection pool status
- `GET /api/v1/version` — System version and runtime details
- `GET, POST /api/v1/elections` — List and schedule elections
- `GET, POST /api/v1/candidates` — Query and register candidates with Form 26 disclosures
- `GET /api/v1/constituencies` — Parliamentary and Assembly constituencies directory
- `GET /api/v1/parties` — Political party profiles, symbols, and statistical history
- `GET, POST /api/v1/results` — Fetch and declare constituency election outcomes
- `GET /api/v1/search?q=:query` — Multi-field BM25 full-text search
- `POST /api/v1/ai/query` — Grounded RAG query answering with statutory citations
- `POST /api/v1/ai/chat` — Multi-turn conversational research intelligence
- `GET /api/v1/ai/metrics` — Grounding verification metrics and citation coverage
- `GET, PATCH /api/v1/admin/feature-flags` — Runtime feature toggle administration
- `GET /api/v1/admin/audit-logs` — Query immutable SHA-256 chained audit logs
- `GET /api/v1/observability` — Comprehensive system diagnostics telemetry

---

## Quickstart & Verification

### 1. Database Setup (PostgreSQL 17)
```bash
# Start PostgreSQL service
brew services start postgresql@17

# Apply database migrations and seed data
psql -d election_intelligence -f migrations/0001_initial_schema.sql
psql -d election_intelligence -f migrations/0002_seed_initial_data.sql
```

### 2. High-Performance Rust Server
```bash
# Run automated tests (20 unit & integration tests)
cargo test

# Compile release binary
cargo build --release

# Run native binary on port 3000
./target/release/election-intelligence
# Or run with cargo:
cargo run
```

### 3. Containerized Production Deployment
```bash
# Build multi-stage Docker image
docker build -t election-intelligence-platform:latest .

# Run container with environment configuration
docker run -p 3000:3000 \
  -e DATABASE_URL="postgres://postgres:password@host.docker.internal:5432/election_intelligence" \
  election-intelligence-platform:latest
```

---

## Automated Verification Status

- **Unit & Integration Tests**: 20/20 PASSED (`cargo test --all-features`)
- **Code Formatting**: PASSED (`cargo fmt --all -- --check`)
- **Linter & Type Integrity**: PASSED (`cargo clippy --all-targets --all-features -- -D warnings`)
- **Production Containerization**: Multi-stage hardened Debian container with healthchecks
- **Release Binary**: 9.3 MB native executable for Darwin ARM64 / Linux x86_64
