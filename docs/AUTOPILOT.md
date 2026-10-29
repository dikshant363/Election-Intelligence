# Election Intelligence Platform — Autopilot Engineering System

## 1. Executive Summary & Mission
The **Election Intelligence Platform Autopilot System** provides a 100% free (₹0.00 / $0.00 per month), bounded, self-maintaining engineering architecture for the Election Intelligence Platform.

It ensures that the platform remains:
- **Independent & Politically Neutral**: Statutory attribution (ECI Gazettes, ADR Form 26) and audit logs are cryptographically chained and tamper-evident.
- **Reliable & Self-Healing**: Detects regressions, runs automated health probing, deduplicates incidents, and applies bounded patches without human intervention for low-risk defects.
- **Budget-Safe**: Strictly constrained to permanent free tiers (GitHub Actions public runners, Render Free Web Service, Neon Free Serverless PostgreSQL). Zero credit cards, zero surprise bills.

---

## 2. Autopilot Architecture Map

```
                     ┌──────────────────────────────────────────────┐
                     │          GitHub Actions Scheduler            │
                     │  • Daily Health Probe (06:00 UTC)           │
                     │  • Weekly Maintenance & Security (Sun 00:00)│
                     │  • Dependabot Grouped Updates (Mon 04:00)   │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │          Health & Diagnostic Probes          │
                     │  • /ready (PostgreSQL 17 connection test)    │
                     │  • /health (Process & telemetry status)      │
                     │  • /status (Autopilot policy compliance)     │
                     │  • Core APIs: /candidates, /coverage         │
                     └──────────────────────┬───────────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    │                                               │
             [Checks Pass]                                   [Checks Fail]
                    │                                               │
                    ▼                                               ▼
     ┌─────────────────────────────┐                 ┌─────────────────────────────┐
     │ Step Summary Status Report  │                 │ Deduplicated Incident Mgr   │
     │  • Telemetry updated        │                 │  • gh issue list dedup      │
     │  • Quota limits verified    │                 │  • Secret sanitization      │
     │  • Zero billing confirmed   │                 │  • Update comment or create │
     └─────────────────────────────┘                 └──────────────┬──────────────┘
                                                                    │
                                                                    ▼
                                                     ┌─────────────────────────────┐
                                                     │   Bounded Self-Repair Loop  │
                                                     │  • Attempt limit: max 3     │
                                                     │  • Path allowlist: src/     │
                                                     │  • Block migrations & infra │
                                                     │  • PR created for review    │
                                                     └─────────────────────────────┘
```

---

## 3. The Bounded Self-Repair Loop

To guarantee safety, stability, and adherence to the platform's civic charter, automated repair is strictly bounded:

```
DETECT ──► DIAGNOSE ──► REPRODUCE ──► PATCH ──► TEST ──► GATED PR ──► ESCALATE (if >3 tries)
```

### Safety Constraints & Invariants
1. **Maximum Retry Limit**: Maximum **3 automated repair attempts** per incident. If an issue is not resolved after 3 attempts, the system halts repair cycles and flags the incident for human maintainer review.
2. **Explicit Path Allowlist**:
   - **Permitted**: `src/**`, `tests/**`, `Cargo.toml`.
   - **Strictly Denied (Protected Systems)**:
     - `migrations/**` (Database schema changes require manual DBA review).
     - `.github/**` (CI/CD workflows and security permissions are immutable to automation).
     - `render.yaml`, `Dockerfile`, `docker-compose.yml` (Hosting configuration).
     - `backups/**`, `.env*`, `LICENSE`.
3. **Destructive SQL Blocking**:
   Any patch containing destructive database operations (`DROP TABLE`, `TRUNCATE`, `DROP DATABASE`, `ALTER TABLE ... DROP COLUMN`, or deletions on `elections`/`candidacies`/`audit_ledger`) is rejected immediately.
4. **Mandatory Quality Gates**:
   Before an automated pull request is created, the repair branch must pass:
   - `cargo fmt --all -- --check`
   - `cargo clippy --all-targets --all-features -- -D warnings` (0 warnings allowed)
   - `cargo test --all-targets` (100% test pass rate)
   - `cargo build --release` (Clean compilation)

---

## 4. Deduplicated Incident Management

When a daily health check, security audit, or post-deployment verification fails:
1. **Secret Sanitization**:
   All logs pass through `AutopilotEngine::sanitize_log`:
   - Database connection passwords (`postgres://user:***@host/db`) are replaced with `[REDACTED_SECRET]`.
   - Bearer authentication tokens are replaced with `Bearer [REDACTED_SECRET]`.
   - API keys and tokens are stripped before writing to GitHub issues.
2. **Deduplication Logic**:
   The incident manager searches open issues labeled `autopilot-incident`.
   - **If an open issue exists** matching the failure title: It appends a detailed comment with the latest workflow link and sanitized failure log. No duplicate issue is created.
   - **If no open issue exists**: It opens a new issue with labels `autopilot-incident`, `bug`, and severity (`P1-High`, `P2-Medium`).

---

## 5. Continuous Dependency & Security Maintenance

- **Dependabot**:
  Configured in `.github/dependabot.yml` to check for updates every Monday morning.
  - Patch and minor updates are grouped together (`rust-minor-patch` and `actions-all`) to minimize runner minutes and conserve GitHub Actions free quotas.
- **Cargo Security Audit**:
  Weekly automated runs of `cargo audit` scan the dependency lockfile against the RustSec Advisory Database for known Common Vulnerabilities and Exposures (CVEs).
- **Accidental Secret Scan**:
  Automated regex pattern scanning verifies that developers or contributors have not accidentally committed API keys, private tokens, or connection strings into source files.

---

## 6. Zero-Cost Budget Policy (₹0.00 / month)

| Resource | Service | Monthly Cost | Free-Tier Constraints & Safeguards |
| :--- | :--- | :--- | :--- |
| **Compute / Hosting** | Render Free Web Service | **₹0.00** ($0.00) | 512 MB RAM, 0.5 CPU, 750 hours/mo. Auto-sleeps after 15m idle; resumes in ~30s. |
| **Database** | Neon Serverless Postgres | **₹0.00** ($0.00) | 0.5 GiB SSD storage, 1 project. Auto-suspends compute when idle; sub-second resume. |
| **CI / CD Runners** | GitHub Actions | **₹0.00** ($0.00) | Public repository standard runners. Strict 10–15m job timeouts and concurrency groups. |
| **Vulnerability Scanning** | Dependabot & Cargo Audit | **₹0.00** ($0.00) | Native open-source tools with zero licensing cost. |
| **SSL / TLS** | Let's Encrypt via Render | **₹0.00** ($0.00) | Automated certificate issuance and renewals. |

---

## 7. Operational Endpoints

| Endpoint | Method | Purpose | Response |
| :--- | :--- | :--- | :--- |
| `/ready` | `GET` | Readiness Probe | `{"status":"READY","database":"CONNECTED"}` |
| `/health` | `GET` | Liveness & Telemetry | Process uptime, CPU/memory, search engine health |
| `/status` | `GET` | Autopilot Status | Comprehensive policy compliance and budget verification |
| `/api/v1/coverage` | `GET` | Data Completeness | State and constituency coverage percentages |
