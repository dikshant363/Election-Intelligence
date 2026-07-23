# ENTERPRISE CONTROL CENTER — MASTER PLATFORM GUIDE
## Election Intelligence Platform — Version 1.0.0

---

## 1. Executive Summary & Control Hierarchy

The Election Intelligence Enterprise Control Center is the unified operational command system for managing the entire Election Intelligence Platform. Rather than relying on a single monolithic admin panel, the platform implements a 4-tier hierarchy of specialized control interfaces:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ELECTION INTELLIGENCE PLATFORM                      │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
   ┌───────────────────┬─────────────┴─────────────┬───────────────────┐
   │                   │                           │                   │
   ▼                   ▼                           ▼                   ▼
┌──────────────┐ ┌──────────────┐          ┌──────────────┐    ┌──────────────┐
│    PUBLIC    │ │  OPERATIONS  │          │  ENTERPRISE  │    │  EXECUTIVE   │
│    PORTAL    │ │   CONSOLE    │          │   CONTROL    │    │   COMMAND    │
└──────────────┘ └──────────────┘          └──────────────┘    └──────────────┘
 Public Citizens  Election Officials        DevOps / Admins     Leadership
 Search, Reports  Candidates, ETL          Infra, AI, RBAC     KPIs, Insights
```

---

## 2. Interface Hierarchy & Access Model

| Interface | Primary Users | Purpose & Scope | Route |
| :--- | :--- | :--- | :--- |
| **Public Portal** | Citizens, Media, Voters | Public election search, candidate affidavits, constituency map | `/portal` |
| **Operations Console** | Election Officials, Data Entry | Election lifecycle, candidates, parties, booth mapping, CSV ETL | `/ops` |
| **Enterprise Control Center** | Platform Admins, DevOps, AI Engineers | System health, Redis/DB pools, AI routing, RBAC, audit stream | `/admin` |
| **Executive Command Center** | Leadership, Election Commissioners | Strategic KPIs, national turnout, regional analytics, platform SLAs | `/executive` |

---

## 3. Core Administrative Modules

The Enterprise Control Center provides unified management across 35+ platform modules:

1. **Dashboard & Telemetry**: CPU, RAM, Disk, DB pool active connections, Redis latency, and live worker counts.
2. **Election Operations**: Election lifecycle, candidate Form 26 affidavits, constituency delimitation, and polling booth allocations.
3. **AI Control Center**: LLM provider routing (`openai`, `gemini`, `claude`, `ollama`), vector store, prompt registry, token usage, and safety guardrails.
4. **Search Center (SAL)**: Full-text search reindexing, BM25 scoring parameters, and autocomplete dictionary management.
5. **ETL & Ingestion**: CSV/JSON data ingestion pipeline tracking, data validation, and provenance records.
6. **Security & Governance**: RBAC role assignments, user accounts, MFA enforcement, and real-time audit log stream.
7. **Feature Flags**: Dynamic zero-downtime feature toggles for RAG, WebSockets, background workers, and chaos hooks.
