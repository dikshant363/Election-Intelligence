#!/usr/bin/env bash
# Reorganise all root-level docs into docs/ hierarchy
set -e

REPO="/Users/dikshantagarwal/Desktop/CivicLens India/Election-Intelligence"
cd "$REPO"

# ── Create directory structure ──────────────────────────────────────────────
mkdir -p docs/{architecture,development,operations,security,ai,data,infrastructure,quality,quality/validation,governance,product,onboarding,reference,research}

# ── Helper: git mv only if file exists ──────────────────────────────────────
gmv() { [ -f "$1" ] && git mv "$1" "$2" || true; }

# ── ARCHITECTURE ─────────────────────────────────────────────────────────────
gmv ARCHITECTURE.md                    docs/architecture/ARCHITECTURE.md
gmv ARCHITECTURE_DECISIONS.md          docs/architecture/ARCHITECTURE_DECISIONS.md
gmv ARCHITECTURE_DIAGRAMS.md           docs/architecture/ARCHITECTURE_DIAGRAMS.md
gmv DEPENDENCY_RULES.md                docs/architecture/DEPENDENCY_RULES.md
gmv DATA_FLOW.md                       docs/architecture/DATA_FLOW.md
gmv SYSTEM_OPERATION_GUIDE.md          docs/architecture/SYSTEM_OPERATION_GUIDE.md
gmv DEPENDENCY_POLICY.md               docs/architecture/DEPENDENCY_POLICY.md
gmv DOMAIN_GUIDE.md                    docs/architecture/DOMAIN_GUIDE.md
gmv APPLICATION_GUIDE.md               docs/architecture/APPLICATION_GUIDE.md
gmv API_GUIDE.md                       docs/architecture/API_GUIDE.md
gmv PLATFORM_GUIDE.md                  docs/architecture/PLATFORM_GUIDE.md
gmv REALTIME_GUIDE.md                  docs/architecture/REALTIME_GUIDE.md
gmv EVENTBUS_GUIDE.md                  docs/architecture/EVENTBUS_GUIDE.md
gmv STREAMING_GUIDE.md                 docs/architecture/STREAMING_GUIDE.md
gmv SYSTEM_INTEGRATION_MATRIX.md       docs/architecture/SYSTEM_INTEGRATION_MATRIX.md

# ── DEVELOPMENT ──────────────────────────────────────────────────────────────
gmv DEVELOPMENT_GUIDE.md               docs/development/DEVELOPMENT_GUIDE.md
gmv DEVELOPER_WORKFLOW.md              docs/development/DEVELOPER_WORKFLOW.md
gmv DEVELOPMENT_WORKFLOW.md            docs/development/DEVELOPMENT_WORKFLOW_LEGACY.md
gmv DEVELOPMENT_SETUP.md               docs/development/DEVELOPMENT_SETUP.md
gmv CODING_STANDARDS.md                docs/development/CODING_STANDARDS.md
gmv SETUP.md                           docs/development/SETUP.md
gmv ENVIRONMENT_SETUP.md               docs/development/ENVIRONMENT_SETUP.md
gmv DX_GUIDE.md                        docs/development/DX_GUIDE.md
gmv LOCAL_AUTOMATION.md                docs/development/LOCAL_AUTOMATION.md
gmv SCRIPT_REFERENCE.md                docs/development/SCRIPT_REFERENCE.md
gmv ENGINEERING_STANDARDS.md           docs/development/ENGINEERING_STANDARDS.md
gmv WORKSPACE_GUIDE.md                 docs/development/WORKSPACE_GUIDE.md

# ── OPERATIONS ───────────────────────────────────────────────────────────────
gmv RUNBOOK.md                         docs/operations/RUNBOOK.md
gmv DEPLOYMENT_RUNBOOK.md              docs/operations/DEPLOYMENT_RUNBOOK.md
gmv INCIDENT_RESPONSE.md               docs/operations/INCIDENT_RESPONSE.md
gmv BACKUP_RECOVERY.md                 docs/operations/BACKUP_RECOVERY.md
gmv MONITORING_GUIDE.md                docs/operations/MONITORING_GUIDE.md
gmv DISASTER_RECOVERY_GUIDE.md         docs/operations/DISASTER_RECOVERY_GUIDE.md
gmv OBSERVABILITY_GUIDE.md             docs/operations/OBSERVABILITY_GUIDE.md
gmv LOGGING_GUIDE.md                   docs/operations/LOGGING_GUIDE.md
gmv METRICS_GUIDE.md                   docs/operations/METRICS_GUIDE.md
gmv TELEMETRY_GUIDE.md                 docs/operations/TELEMETRY_GUIDE.md
gmv SCALING_GUIDE.md                   docs/operations/SCALING_GUIDE.md
gmv WORKER_GUIDE.md                    docs/operations/WORKER_GUIDE.md
gmv PRODUCTION_GUIDE.md                docs/operations/PRODUCTION_GUIDE.md
gmv PRODUCTION_RELEASE_GUIDE.md        docs/operations/PRODUCTION_RELEASE_GUIDE.md

# ── SECURITY ─────────────────────────────────────────────────────────────────
gmv SECURITY_GUIDE.md                  docs/security/SECURITY_GUIDE.md
gmv SECURITY_OPERATIONS_GUIDE.md       docs/security/SECURITY_OPERATIONS_GUIDE.md
gmv SECRETS_MANAGEMENT.md              docs/security/SECRETS_MANAGEMENT.md
gmv AUTHENTICATION_GUIDE.md            docs/security/AUTHENTICATION_GUIDE.md
gmv AUTHORIZATION_GUIDE.md             docs/security/AUTHORIZATION_GUIDE.md
gmv SECURITY_CHECKLIST.md              docs/security/SECURITY_CHECKLIST.md
gmv RBAC_GUIDE.md                      docs/security/RBAC_GUIDE.md
gmv IDENTITY_GUIDE.md                  docs/security/IDENTITY_GUIDE.md

# ── AI ───────────────────────────────────────────────────────────────────────
gmv AI_ARCHITECTURE.md                 docs/ai/AI_ARCHITECTURE.md
gmv AI_GUIDE.md                        docs/ai/AI_GUIDE.md
gmv AI_PROVIDER_GUIDE.md               docs/ai/AI_PROVIDER_GUIDE.md
gmv PROMPT_ENGINEERING.md              docs/ai/PROMPT_ENGINEERING.md
gmv PROMPT_GUIDE.md                    docs/ai/PROMPT_GUIDE.md
gmv RAG_GUIDE.md                       docs/ai/RAG_GUIDE.md
gmv MODEL_CONFIGURATION.md             docs/ai/MODEL_CONFIGURATION.md
gmv PROVIDER_GUIDE.md                  docs/ai/PROVIDER_GUIDE.md

# ── DATA ─────────────────────────────────────────────────────────────────────
gmv DATABASE_GUIDE.md                  docs/data/DATABASE_GUIDE.md
gmv ETL_GUIDE.md                       docs/data/ETL_GUIDE.md
gmv SEARCH_GUIDE.md                    docs/data/SEARCH_GUIDE.md
gmv DATA_LINEAGE.md                    docs/data/DATA_LINEAGE.md
gmv DATA_RETENTION.md                  docs/data/DATA_RETENTION.md
gmv PERSISTENCE_GUIDE.md               docs/data/PERSISTENCE_GUIDE.md
gmv INDEXING_GUIDE.md                  docs/data/INDEXING_GUIDE.md
gmv QUERY_GUIDE.md                     docs/data/QUERY_GUIDE.md
gmv CACHE_GUIDE.md                     docs/data/CACHE_GUIDE.md

# ── INFRASTRUCTURE ───────────────────────────────────────────────────────────
gmv PERFORMANCE_GUIDE.md               docs/infrastructure/PERFORMANCE_GUIDE.md
gmv BENCHMARK_GUIDE.md                 docs/infrastructure/BENCHMARK_GUIDE.md

# ── QUALITY ──────────────────────────────────────────────────────────────────
gmv QUALITY_GUIDE.md                   docs/quality/QUALITY_GUIDE.md
gmv TESTING_GUIDE.md                   docs/quality/TESTING_GUIDE.md
gmv RELEASE_GUIDE.md                   docs/quality/RELEASE_GUIDE.md
gmv VERSIONING.md                      docs/quality/VERSIONING.md
gmv PRODUCTION_RELEASE_VALIDATION.md   docs/quality/PRODUCTION_RELEASE_VALIDATION.md
gmv RELEASE_CANDIDATE_VALIDATION.md    docs/quality/RELEASE_CANDIDATE_VALIDATION.md

# ── QUALITY / VALIDATION (milestone artefacts) ───────────────────────────────
for f in MILESTONE_3_VALIDATION.md MILESTONE_4_VALIDATION.md MILESTONE_5_VALIDATION.md \
          AI_VALIDATION.md API_VALIDATION.md APPLICATION_VALIDATION.md \
          DATABASE_VALIDATION.md DOMAIN_VALIDATION.md DX_VALIDATION.md \
          IDENTITY_VALIDATION.md OBSERVABILITY_VALIDATION.md PERFORMANCE_VALIDATION.md \
          PERSISTENCE_VALIDATION.md PLATFORM_VALIDATION.md PRODUCTION_VALIDATION.md \
          REALTIME_VALIDATION.md SEARCH_VALIDATION.md SECURITY_VALIDATION.md \
          ENVIRONMENT_REPORT.md DEVELOPMENT_INFRASTRUCTURE_REPORT.md \
          REPOSITORY_GOVERNANCE_REPORT.md REPOSITORY_REVIEW.md \
          PROJECT_INITIALIZATION_REVIEW.md QUALITY_REFERENCE.md QUALITY_REVIEW.md \
          DX_REVIEW.md; do
  gmv "$f" "docs/quality/validation/$f"
done

# ── GOVERNANCE ───────────────────────────────────────────────────────────────
gmv GOVERNANCE.md                      docs/governance/GOVERNANCE.md
gmv DECISION_LOG.md                    docs/governance/DECISION_LOG.md

# ── PRODUCT ──────────────────────────────────────────────────────────────────
gmv ROADMAP.md                         docs/product/ROADMAP.md
gmv FUTURE.md                          docs/product/FUTURE.md

# ── ONBOARDING ───────────────────────────────────────────────────────────────
gmv NEW_DEVELOPER_ONBOARDING.md        docs/onboarding/NEW_DEVELOPER_ONBOARDING.md
gmv MEMORY.md                          docs/onboarding/MEMORY.md
gmv AGENT_RULES.md                     docs/onboarding/AGENT_RULES.md

# ── REFERENCE ────────────────────────────────────────────────────────────────
gmv FAQ.md                             docs/reference/FAQ.md
gmv COMMAND_REFERENCE.md               docs/reference/COMMAND_REFERENCE.md
gmv PROJECT_STRUCTURE.md               docs/reference/PROJECT_STRUCTURE.md
gmv TROUBLESHOOTING_GUIDE.md           docs/reference/TROUBLESHOOTING_GUIDE.md
gmv TROUBLESHOOTING.md                 docs/reference/TROUBLESHOOTING_LEGACY.md

# ── Leftover structure/guide files ───────────────────────────────────────────
for f in DOMAIN_STRUCTURE.md API_STRUCTURE.md APPLICATION_STRUCTURE.md \
          DATABASE_STRUCTURE.md PERSISTENCE_STRUCTURE.md PLATFORM_STRUCTURE.md \
          SECURITY_STRUCTURE.md; do
  gmv "$f" "docs/reference/$f"
done

# ── Misc ──────────────────────────────────────────────────────────────────────
gmv TASKS.md                           docs/reference/TASKS.md

echo "Done — all git mv operations complete"
git status --short | head -40
