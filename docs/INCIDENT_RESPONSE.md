# Election Intelligence Platform — Incident Response & Triage Runbook

## 1. Incident Severity Matrix

| Severity | Definition | Target SLA | Automated Action | Notification |
| :--- | :--- | :--- | :--- | :--- |
| **P1 — Critical** | Live platform down, database unreachable (`/ready` fails), security vulnerability detected, or audit chain tampered. | 30 minutes | Deduplicated GitHub issue created (`severity:P1-High`), deployment verification blocks release, bounded self-repair triggered if test failure. | GitHub Issue + Workflow Alert |
| **P2 — Medium** | Degraded performance, search index stale, non-fatal statutory ingestion dry-run mismatch, or transient cloud sleep delay. | 4 hours | Deduplicated incident comment appended to open issue, diagnostic telemetry logged. | GitHub Issue |
| **P3 — Low** | Non-breaking formatting inconsistency, non-critical dependency patch update available, or documentation typo. | 48 hours | Grouped Dependabot PR or routine maintenance report. | Step Summary Report |

---

## 2. Deduplication Architecture

To avoid issue tracker noise during continuous daily monitoring:
1. Every health check executes `./scripts/incident_manager.sh`.
2. It queries open issues labeled `autopilot-incident` for matching title keywords (e.g. `Readiness Probe Failed`).
3. If an existing issue is found, it appends a timestamped comment with sanitized logs:
   ```markdown
   ### 🔄 Autopilot Incident Re-occurrence Update
   **Timestamp:** 2026-10-29 11:30:00 UTC
   **Workflow Run:** [View Logs](https://github.com/...)
   ```
4. Only when no matching issue exists is a new issue created.

---

## 3. Diagnostic & Remediation Playbooks

### Playbook A: Database Connection Failure (`/ready` returns 503 `DISCONNECTED`)
* **Possible Cause**:
  1. Neon Serverless Postgres compute auto-suspended after 5 minutes of inactivity.
  2. Neon branch connection limit reached (free tier limit: 1 branch).
  3. `DATABASE_URL` credential revoked or expired.
* **Diagnostic Steps**:
  ```bash
  # Test connection directly from CLI
  psql "${DATABASE_URL}" -c "SELECT 1;"

  # Check Neon compute status via dashboard
  # Verify connection string includes sslmode=require
  ```
* **Remediation**:
  - If compute was suspended, the first connection automatically wakes it up in 500–800ms.
  - Verify that `DATABASE_URL` in Render environment settings matches the Neon dashboard.

### Playbook B: Post-Deployment Verification Timeout
* **Possible Cause**:
  Render free tier container cold start took longer than the initial timeout window.
* **Diagnostic Steps**:
  ```bash
  curl -i "${DEPLOYMENT_URL}/ready"
  ```
* **Remediation**:
  The CD workflow (`cd-deploy.yml`) automatically retries up to 6 times at 15-second intervals (total 90s grace period) to accommodate Render cold starts. If still unresponsive, inspect Render deployment logs in the Render dashboard.

### Playbook C: Broken Automated Test in Pull Request
* **Possible Cause**:
  A candidate schema or API endpoint regression was introduced.
* **Diagnostic Steps**:
  ```bash
  cargo test --all-targets -- --nocapture
  ```
* **Remediation**:
  Trigger bounded self-repair:
  ```bash
  ./scripts/autopilot_repair.sh <issue_number>
  ```
  The repair engine will enforce the path allowlist (`src/`, `tests/`), run formatting and clippy, verify that all 80 tests pass, and generate an updated PR.

---

## 4. Emergency Rollback Playbook

If an unhealthy deployment slips through:
1. Identify the last known good commit:
   ```bash
   git log -5 --oneline
   ```
2. Because all database migrations (`0001`, `0002`, `0003`) are backward-compatible and additive, rolling back application code does not require destructive database downgrades.
3. In the Render Dashboard:
   - Click **Deployments** → Select the last successful commit (e.g., `6a020bf`).
   - Click **Rollback to this revision**.
4. Verify readiness:
   ```bash
   curl -i https://election-intelligence.onrender.com/ready
   ```
