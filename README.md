# Election Intelligence Platform v1.0.0

[![Framework](https://img.shields.io/badge/framework-Next.js%2015-black.svg)](https://nextjs.org)
[![Runtime](https://img.shields.io/badge/node-22.x-green.svg)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/typescript-5.7-blue.svg)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/tailwind-4.0-38bdf8.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*Election Intelligence Platform is an independent, politically neutral, AI-powered public research platform that helps Indian citizens and election administrators make informed decisions by organizing, verifying, and explaining publicly available election information with complete transparency, evidence, and source attribution—without recommending or endorsing any candidate or political party.*

This application was rewritten from Dynamic (Python FastAPI backend & Flutter frontend) to a full-stack **Next.js 15 App Router** architecture, preserving all domain schemas, operational interfaces, administrative control workflows, search capabilities, and grounded AI retrieval.

---

## Key Features & Interfaces

### 1. Enterprise Control Center
- **System Health Telemetry**: Live CPU utilization, memory distribution, PostgreSQL connection pool metrics, and Redis cache latency.
- **Dynamic Feature Flags**: Interactive toggles for RAG pipelines, WebSocket streaming, async background workers, chaos hooks, and MFA enforcement.
- **AI Subsystem Control & Routing**: Multi-provider routing (Gemini 2.5 Flash, local vector fallback), strict citation attribution, and pre/post-generation safety guardrails.
- **Security & Audit Logs**: Immutable audit event stream with CSV export and role-based access control (RBAC).

### 2. Executive Command Center
- **Strategic KPIs**: Real-time tracking of managed elections, 968.8M registered electors, national voter turnout percentages, and 99.98% platform SLA.
- **Regional Performance Aggregation**: Detailed turnout analysis across Northern, Southern, Eastern, Western, and Central electoral zones.

### 3. Operations Console
- **Election Lifecycle Management**: Schedule new general and assembly elections via CQRS pipeline.
- **Candidate Registry & Form 26**: Candidate nomination filing, asset declarations, and judicial background tracking.
- **Results Declaration**: EVM and postal ballot tallying with automatic margin calculation.
- **ETL Data Ingestion**: Provenance-tracked batch import of CSV and JSON election records.

### 4. Public Portal & Search
- **Search Abstraction Layer (SAL)**: Instant multi-field search across elections, constituencies, candidates, and political parties.
- **Candidate Form 26 Transparency**: Filter candidates by political party and parliamentary constituency with verified asset and criminal record badges.

### 5. AI Intelligence Assistant & RAG Engine
- Grounded conversational Q&A referencing official Election Commission records and Form 26 affidavits.
- Full source citation attribution with confidence scores and explainability reasoning.
- Command Palette (`⌘ K` / `Ctrl + K`) for instant navigation and operations across all platform modules.

---

## API Endpoints

All endpoints are implemented as Next.js API route handlers under `/api/v1/*`:

- `GET /api/v1/health` - Platform readiness and dependency telemetry
- `GET /api/v1/version` - System version and runtime information
- `GET, POST /api/v1/elections` - List and schedule elections
- `GET, POST /api/v1/candidates` - Query and register candidates
- `GET /api/v1/constituencies` - Electoral constituencies directory
- `GET /api/v1/parties` - Political party symbols and statistics
- `GET, POST /api/v1/results` - Fetch and declare constituency election results
- `GET, PATCH /api/v1/admin/feature-flags` - Inspect and toggle runtime feature flags
- `GET /api/v1/admin/audit-logs` - Query administrative audit logs
- `GET /api/v1/search` - Multi-field search across all electoral entities
- `POST /api/v1/ai/query` - Grounded RAG query answering with citations
- `POST /api/v1/ai/chat` - Multi-turn conversational AI intelligence
- `GET /api/v1/ai/metrics` - AI grounding scores and citation coverage metrics
- `GET, POST /api/v1/etl` - Ingestion batch tracking and file import

---

## Development

```bash
# Install dependencies
npm install

# Start development server on port 3000
npm run dev

# Compile and build production bundle
npm run build
```