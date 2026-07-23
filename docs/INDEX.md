# Election Intelligence Platform — Documentation Index

> **Version 1.0.0** | The single entry point to all platform documentation.
> Any engineer, AI agent, or maintainer should start here.

---

## 📌 Start Here

| I want to… | Go to |
| :--- | :--- |
| Understand the platform in 1 hour | [SYSTEM_OPERATION_GUIDE.md](architecture/SYSTEM_OPERATION_GUIDE.md) |
| Set up my development environment | [DEVELOPMENT_GUIDE.md](development/DEVELOPMENT_GUIDE.md) |
| Onboard as a new team member | [NEW_DEVELOPER_ONBOARDING.md](onboarding/NEW_DEVELOPER_ONBOARDING.md) |
| Add a new feature | [DEVELOPER_WORKFLOW.md](development/DEVELOPER_WORKFLOW.md) |
| Debug a problem | [TROUBLESHOOTING_GUIDE.md](reference/TROUBLESHOOTING_GUIDE.md) |
| Deploy to production | [DEPLOYMENT_RUNBOOK.md](operations/DEPLOYMENT_RUNBOOK.md) |
| Respond to an incident | [INCIDENT_RESPONSE.md](operations/INCIDENT_RESPONSE.md) |
| Understand the architecture | [ARCHITECTURE.md](architecture/ARCHITECTURE.md) |
| Check all commands | [COMMAND_REFERENCE.md](reference/COMMAND_REFERENCE.md) |
| Read the FAQ | [FAQ.md](reference/FAQ.md) |

---

## 🏗️ Architecture & Design

| Document | Description |
| :--- | :--- |
| [ARCHITECTURE.md](architecture/ARCHITECTURE.md) | System architecture overview |
| [SYSTEM_OPERATION_GUIDE.md](architecture/SYSTEM_OPERATION_GUIDE.md) | 24-section master operational handbook |
| [ARCHITECTURE_DECISIONS.md](architecture/ARCHITECTURE_DECISIONS.md) | 25 Architecture Decision Records (ADRs) |
| [ARCHITECTURE_DIAGRAMS.md](architecture/ARCHITECTURE_DIAGRAMS.md) | ASCII and sequence diagrams |
| [DATA_FLOW.md](architecture/DATA_FLOW.md) | 8 end-to-end data flow traces |
| [DEPENDENCY_RULES.md](architecture/DEPENDENCY_RULES.md) | Layer dependency matrix and enforcement |
| [DEPENDENCY_POLICY.md](architecture/DEPENDENCY_POLICY.md) | Import and coupling policy |
| [SYSTEM_INTEGRATION_MATRIX.md](architecture/SYSTEM_INTEGRATION_MATRIX.md) | Subsystem interaction map |
| [THREAT_MODEL.md](architecture/THREAT_MODEL.md) | STRIDE security threat model |
| [DOMAIN_GUIDE.md](architecture/DOMAIN_GUIDE.md) | Domain model and entities |
| [APPLICATION_GUIDE.md](architecture/APPLICATION_GUIDE.md) | Application layer guide |
| [API_GUIDE.md](architecture/API_GUIDE.md) | API design guide |
| [REALTIME_GUIDE.md](architecture/REALTIME_GUIDE.md) | Real-time event streaming architecture |
| [EVENTBUS_GUIDE.md](architecture/EVENTBUS_GUIDE.md) | EventBus and EventEnvelope design |
| [STREAMING_GUIDE.md](architecture/STREAMING_GUIDE.md) | SSE and WebSocket streaming guide |
| [PLATFORM_GUIDE.md](architecture/PLATFORM_GUIDE.md) | Platform-level design decisions |

---

## 🛠️ Development

| Document | Description |
| :--- | :--- |
| [DEVELOPMENT_GUIDE.md](development/DEVELOPMENT_GUIDE.md) | **Start here** — full environment setup |
| [DEVELOPER_WORKFLOW.md](development/DEVELOPER_WORKFLOW.md) | Git, PR, review, and release workflow |
| [CODING_STANDARDS.md](development/CODING_STANDARDS.md) | Python, FastAPI, Flutter, test standards |
| [ENGINEERING_STANDARDS.md](development/ENGINEERING_STANDARDS.md) | Engineering principles and policies |
| [ENVIRONMENT_SETUP.md](development/ENVIRONMENT_SETUP.md) | Environment variables and configuration |
| [DX_GUIDE.md](development/DX_GUIDE.md) | Developer experience tooling guide |
| [LOCAL_AUTOMATION.md](development/LOCAL_AUTOMATION.md) | Local automation scripts |
| [SCRIPT_REFERENCE.md](development/SCRIPT_REFERENCE.md) | Available scripts and their usage |

---

## ⚙️ Operations

| Document | Description |
| :--- | :--- |
| [RUNBOOK.md](operations/RUNBOOK.md) | On-call operational runbook |
| [DEPLOYMENT_RUNBOOK.md](operations/DEPLOYMENT_RUNBOOK.md) | Dev / staging / prod deployment |
| [INCIDENT_RESPONSE.md](operations/INCIDENT_RESPONSE.md) | P0–P3 incident playbooks |
| [BACKUP_RECOVERY.md](operations/BACKUP_RECOVERY.md) | Backup procedures and disaster recovery |
| [MONITORING_GUIDE.md](operations/MONITORING_GUIDE.md) | Metrics, tracing, logs, SLOs |
| [SLO_SLI.md](operations/SLO_SLI.md) | Service Level Objectives and Indicators |
| [OBSERVABILITY_GUIDE.md](operations/OBSERVABILITY_GUIDE.md) | OpenTelemetry and Prometheus guide |
| [LOGGING_GUIDE.md](operations/LOGGING_GUIDE.md) | Structured JSON logging guide |
| [METRICS_GUIDE.md](operations/METRICS_GUIDE.md) | Prometheus metrics reference |
| [TELEMETRY_GUIDE.md](operations/TELEMETRY_GUIDE.md) | Distributed tracing guide |
| [DISASTER_RECOVERY_GUIDE.md](operations/DISASTER_RECOVERY_GUIDE.md) | Disaster recovery procedures |
| [SCALING_GUIDE.md](operations/SCALING_GUIDE.md) | Horizontal and vertical scaling |
| [PRODUCTION_GUIDE.md](operations/PRODUCTION_GUIDE.md) | Production hardening guide |
| [PRODUCTION_RELEASE_GUIDE.md](operations/PRODUCTION_RELEASE_GUIDE.md) | v1.0.0 release guide |
| [WORKER_GUIDE.md](operations/WORKER_GUIDE.md) | Background worker configuration |

---

## 🔒 Security

| Document | Description |
| :--- | :--- |
| [SECURITY_GUIDE.md](security/SECURITY_GUIDE.md) | Security architecture overview |
| [THREAT_MODEL.md](architecture/THREAT_MODEL.md) | STRIDE threat model |
| [SECRETS_MANAGEMENT.md](security/SECRETS_MANAGEMENT.md) | Secret storage, rotation, revocation |
| [AUTHENTICATION_GUIDE.md](security/AUTHENTICATION_GUIDE.md) | JWT + Argon2id authentication |
| [AUTHORIZATION_GUIDE.md](security/AUTHORIZATION_GUIDE.md) | RBAC authorization model |
| [SECURITY_CHECKLIST.md](security/SECURITY_CHECKLIST.md) | 80+ item security checklist |
| [RBAC_GUIDE.md](security/RBAC_GUIDE.md) | Role-based access control detail |
| [IDENTITY_GUIDE.md](security/IDENTITY_GUIDE.md) | Identity subsystem guide |
| [SECURITY_OPERATIONS_GUIDE.md](security/SECURITY_OPERATIONS_GUIDE.md) | Security operations procedures |

---

## 🤖 AI & Machine Learning

| Document | Description |
| :--- | :--- |
| [AI_ARCHITECTURE.md](ai/AI_ARCHITECTURE.md) | AI subsystem architecture |
| [RAG_GUIDE.md](ai/RAG_GUIDE.md) | Hybrid BM25 + vector RAG pipeline |
| [AI_PROVIDER_GUIDE.md](ai/AI_PROVIDER_GUIDE.md) | OpenAI / Gemini / local configuration |
| [MODEL_CONFIGURATION.md](ai/MODEL_CONFIGURATION.md) | Model selection and tuning |
| [PROMPT_ENGINEERING.md](ai/PROMPT_ENGINEERING.md) | Prompt design, versioning, testing |
| [AI_GUIDE.md](ai/AI_GUIDE.md) | General AI subsystem guide |
| [PROMPT_GUIDE.md](ai/PROMPT_GUIDE.md) | Prompt templates reference |
| [PROVIDER_GUIDE.md](ai/PROVIDER_GUIDE.md) | LLM provider abstraction guide |

---

## 📊 Data

| Document | Description |
| :--- | :--- |
| [DATABASE_GUIDE.md](data/DATABASE_GUIDE.md) | SQLAlchemy, UoW, Alembic, PostgreSQL |
| [ETL_GUIDE.md](data/ETL_GUIDE.md) | Ingestion pipeline end-to-end |
| [SEARCH_GUIDE.md](data/SEARCH_GUIDE.md) | Search Abstraction Layer, BM25, FTS |
| [DATA_LINEAGE.md](data/DATA_LINEAGE.md) | Provenance tracking |
| [DATA_RETENTION.md](data/DATA_RETENTION.md) | Retention policy |
| [PERSISTENCE_GUIDE.md](data/PERSISTENCE_GUIDE.md) | Persistence layer guide |
| [CACHE_GUIDE.md](data/CACHE_GUIDE.md) | CacheService and Redis guide |
| [INDEXING_GUIDE.md](data/INDEXING_GUIDE.md) | Database index management |
| [QUERY_GUIDE.md](data/QUERY_GUIDE.md) | Query patterns and optimisation |

---

## 🏛️ Infrastructure

| Document | Description |
| :--- | :--- |
| [INFRASTRUCTURE_GUIDE.md](infrastructure/INFRASTRUCTURE_GUIDE.md) | Docker, networking, resource requirements |
| [VERSION_COMPATIBILITY.md](infrastructure/VERSION_COMPATIBILITY.md) | Python / Flutter / PostgreSQL / Redis matrix |
| [PERFORMANCE_GUIDE.md](infrastructure/PERFORMANCE_GUIDE.md) | Caching, pools, rate limiting, autoscaling |
| [BENCHMARK_GUIDE.md](infrastructure/BENCHMARK_GUIDE.md) | Load testing and benchmarking |

---

## ✅ Quality

| Document | Description |
| :--- | :--- |
| [QUALITY_GUIDE.md](quality/QUALITY_GUIDE.md) | Quality gates and standards |
| [TESTING_GUIDE.md](quality/TESTING_GUIDE.md) | Test pyramid, 287 backend tests |
| [RELEASE_GUIDE.md](quality/RELEASE_GUIDE.md) | SemVer release process |
| [VERSIONING.md](quality/VERSIONING.md) | Versioning policy |

---

## 🏢 Governance

| Document | Description |
| :--- | :--- |
| [GOVERNANCE.md](governance/GOVERNANCE.md) | Project governance model |
| [DECISION_LOG.md](governance/DECISION_LOG.md) | Technology and architecture decisions |
| [AI_AGENT_COLLABORATION.md](governance/AI_AGENT_COLLABORATION.md) | Multi-agent coordination rules |
| [DEPENDENCY_UPDATE_POLICY.md](governance/DEPENDENCY_UPDATE_POLICY.md) | Dependency update and patching policy |
| [SUPPORT_LIFECYCLE.md](governance/SUPPORT_LIFECYCLE.md) | Version support and deprecation policy |

---

## 📦 Product

| Document | Description |
| :--- | :--- |
| [ROADMAP.md](product/ROADMAP.md) | v1.0 → v2.0 product roadmap |
| [PRODUCT_VISION.md](product/PRODUCT_VISION.md) | Vision, mission, target users |
| [FUTURE.md](product/FUTURE.md) | Long-term direction notes |

---

## 🎓 Onboarding

| Document | Description |
| :--- | :--- |
| [NEW_DEVELOPER_ONBOARDING.md](onboarding/NEW_DEVELOPER_ONBOARDING.md) | Day 1 → Week 1 structured plan |
| [ELECTION_DOMAIN_GUIDE.md](research/ELECTION_DOMAIN_GUIDE.md) | Indian election domain knowledge |
| [AGENT_RULES.md](onboarding/AGENT_RULES.md) | Rules for AI coding agents |

---

## 📖 Reference

| Document | Description |
| :--- | :--- |
| [COMMAND_REFERENCE.md](reference/COMMAND_REFERENCE.md) | Complete command cheat sheet |
| [FAQ.md](reference/FAQ.md) | 100+ Q&A for developers |
| [PROJECT_STRUCTURE.md](reference/PROJECT_STRUCTURE.md) | Every directory explained |
| [TROUBLESHOOTING_GUIDE.md](reference/TROUBLESHOOTING_GUIDE.md) | 12-category problem guide |

---

## 🔬 Research

| Document | Description |
| :--- | :--- |
| [ELECTION_DOMAIN_GUIDE.md](research/ELECTION_DOMAIN_GUIDE.md) | Indian election system knowledge base |

---

## Root-Level Files (GitHub Standards)

| File | Purpose |
| :--- | :--- |
| `README.md` | Project introduction and quick start |
| `CHANGELOG.md` | Version history |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CODE_OF_CONDUCT.md` | Community standards |
| `SECURITY.md` | Vulnerability reporting |
| `SUPPORT.md` | Support channels |
| `.github/CODEOWNERS` | Code ownership assignments |
| `.github/workflows/ci.yml` | CI/CD pipeline |

---

> Last updated: v1.0.0 | Maintained by the Principal Architect.
> To propose a documentation change, open a PR and update the relevant `docs/` file.
