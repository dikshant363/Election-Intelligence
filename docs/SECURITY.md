# Election Intelligence Platform — Security Architecture & Policy

## 1. Core Security Guarantees

The Election Intelligence Platform is built on defense-in-depth principles:

1. **Memory & Concurrency Safety**:
   - Built 100% in pure Rust (Axum, Tokio, SQLx).
   - Eliminates entire classes of memory corruption vulnerabilities (buffer overflows, use-after-free, dangling pointers, data races).
2. **SQL Injection Immunity**:
   - 100% of database interactions are performed via SQLx compile-time checked parameterized queries (`$1`, `$2`, etc.).
   - Zero raw string concatenation in SQL queries.
3. **Secret Sanitization**:
   - `AutopilotEngine::sanitize_log` automatically intercepts and redacts database passwords, Bearer tokens, and API keys before diagnostic logging or issue creation.
4. **Administrative Protection**:
   - Admin-only routes (`/api/v1/etl/ingest`, `/api/v1/corrections/:id/review`, `/api/v1/admin/feature-flags`) require explicit authentication via `Bearer` token or `X-Admin-Key` header verified against `ADMIN_API_KEY`.
5. **Audit Ledger Cryptographic Chaining**:
   - Every administrative change, data correction, and system mutation writes an append-only entry to `audit_ledger`.
   - Each entry includes a SHA-256 hash chaining back to the previous event (`previous_hash -> current_hash`), preventing silent record tampering or historical modification.

---

## 2. GitHub Actions Least Privilege Policy

Workflows strictly adhere to least-privilege permissions:

| Workflow | Read Permissions | Write Permissions | Justification |
| :--- | :--- | :--- | :--- |
| `ci.yml` | `contents: read` | None | Only builds, lints, and tests code |
| `health-monitoring.yml` | `contents: read`, `pull-requests: read` | `issues: write` | Required to create or update deduplicated incident issues |
| `maintenance.yml` | `contents: read` | `issues: write`, `security-events: write` | Reports vulnerability alerts and security scan results |
| `autopilot-repair.yml` | `contents: read` | `contents: write`, `pull-requests: write`, `issues: write` | Creates bounded repair branches and pull requests |
| `cd-deploy.yml` | `contents: read` | `issues: write` | Triggers external webhook and reports deployment health |

---

## 3. Supply Chain Security

- **Dependabot**: Automated weekly checks for outdated crates and GitHub actions.
- **Cargo Audit**: Scans `Cargo.lock` against the RustSec Advisory Database for known Common Vulnerabilities and Exposures (CVEs).
- **Protected Paths**: Automated autopilot repair cannot modify `migrations/`, `.github/`, `render.yaml`, `Dockerfile`, or `.env*` files.

---

## 4. Reporting Security Vulnerabilities

If you discover a potential security vulnerability, please report it responsibly:
- **Email:** `security@electionintelligence.in` (or open an issue with label `security-confidential`).
- Do **not** post public exploit code or unredacted credentials.
- Reports are triaged under SLA: acknowledgment within 24 hours, patch deployment within 72 hours.
