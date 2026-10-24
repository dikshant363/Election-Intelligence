# Security Policy & Guidelines — Election Intelligence Platform

## 1. Product Security Mission
Election Intelligence Platform is an independent, politically neutral civic research platform. The platform handles publicly available election data, Form 26 statutory affidavits, and official Election Commission gazette declarations. Our security posture focuses on:

1. **Evidence Integrity & Tamper Evidence**: Ensuring all public records and audit logs cannot be secretly altered or manipulated.
2. **AI Safety & Grounding Boundaries**: Preventing prompt injection from malicious external documents or user inputs from bypassing factual verification guardrails.
3. **Application & Infrastructure Hardening**: Strict parameterized database queries, memory safety via Rust, least-privilege Docker runtime, and safe secret management.

---

## 2. Supported Versions

| Version | Supported | Notes |
| :--- | :---: | :--- |
| `1.0.x` (Pure Rust) | :white_check_mark: | Current active release branch |
| `< 1.0.0` (Legacy Next.js/FastAPI) | :x: | Deprecated / Replaced |

---

## 3. Threat Model & Mitigations

### 3.1. SQL Injection Prevention
- All database queries are executed via `sqlx` with compile-time checked parameterized queries (`$1, $2, ...`). Dynamic raw string SQL concatenation is strictly forbidden.

### 3.2. Tamper-Evident SHA-256 Audit Chaining
- All administrative operations and data ingestion batches are recorded in an append-only audit ledger (`audit_log` table).
- Each audit log entry includes `current_hash = SHA256(seq || timestamp || actor || action || resource || status || prev_hash)`.
- Hash chain continuity is verified programmatically to detect tampering.

### 3.3. Prompt Injection Defense
- User research queries are sanitized against system prompt overrides, delimiter injections, and roleplay jailbreaks.
- Grounded AI responses are restricted strictly to retrieved, verified evidence passages stored in PostgreSQL. If evidence is lacking, the engine explicitly abstains.

### 3.4. Input Validation & Age Constraints
- Constitutional eligibility rules (e.g., candidate age $\ge 25$) are enforced deterministically at the domain layer before database insertion.

### 3.5. Secrets Management
- No API keys, database credentials, or JWT signing secrets are committed to the repository.
- Secrets are injected via environment variables (`.env.local` locally, GitHub Secrets / vault in CI/CD).

---

## 4. Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

- **Email**: `security@electionintelligence.org` (or open a confidential GitHub Security Advisory)
- **Response Time**: We acknowledge receipt of vulnerability reports within 24 hours and aim to provide a remediation plan within 72 hours.
- **Public Disclosure**: Please allow us reasonable time to patch the issue before making it public.
