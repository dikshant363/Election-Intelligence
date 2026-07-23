# Security Threat Model

## 1. Trust Boundary Diagram

```text
               +-------------------+
               | Unauthenticated   |
               | Internet Users    |
               +---------+---------+
                         | HTTPS
                 +-------v-------+
                 |  API Gateway  |
                 | (Rate Limit/  |
                 |  CORS/HSTS)   |
                 +-------+-------+
                         |
  +----------------------+----------------------+
  |                  FastAPI App                |
  |  [SecurityHeaders, RequestLimit, AuthZ]     |
  +------+---------------+---------------+------+
         |               |               |
   +-----v-----+   +-----v-----+   +-----v-----+
   |PostgreSQL |   |  Redis 7  |   |    LLM    |
   | (Data)    |   | (Cache/RL)|   | Provider  |
   +-----------+   +-----------+   +-----------+
         |                               |
   +-----v-----+                   +-----v-----+
   |Secrets/   |                   | Audit Log |
   |Vault      |                   | Subsystem |
   +-----------+                   +-----------+
```

*Trust Boundaries:*
1. **Public Internet -> API Gateway:** Boundary between completely untrusted external networks and our edge ingress point.
2. **API Gateway -> FastAPI App:** Boundary passing filtered, rate-limited traffic to the application layer.
3. **App -> Database/Cache:** Internal boundary where the application communicates with stateful storage using trusted credentials.
4. **App -> External Services (LLM):** Boundary where the application acts as a client communicating with third-party providers.

## 2. Assets to Protect

| Asset | Description | Value |
|-------|-------------|-------|
| **Election Data Integrity** | Raw and processed election intelligence data | High - Core platform value |
| **User Credentials** | Passwords, password hashes (Argon2id), and active JWTs | Critical - Protects system access |
| **API Keys & Secrets** | Database credentials, Vault tokens, third-party API keys | Critical - Lateral movement vectors |
| **Audit Logs** | Immutable records of administrative and security events | High - Required for forensic analysis |
| **AI Model Access** | Connectivity to external LLM providers and model weights | Medium - Prevents billing abuse |

## 3. Threat Actors

- **Unauthenticated Internet Users:** Script kiddies, botnets, automated scanners attempting DoS or exploiting common web vulnerabilities.
- **Authenticated Users:** Valid platform users attempting to access data outside their authorized role or tenant.
- **Malicious Insiders:** Employees or contractors with excessive privileges attempting to exfiltrate data or sabotage systems.
- **Third-Party AI Providers:** External vendors who may suffer a breach, potentially exposing prompt data or API keys.
- **Compromised Dependencies:** Malicious packages introduced via supply chain attacks in Python or Flutter ecosystems.

## 4. STRIDE Threat Analysis

### API Layer
- **Spoofing:** Mitigated by strict JWT validation and Argon2id password hashing. Tokens are signed and verifiable.
- **Tampering:** Mitigated by TLS 1.3 enforced at the Gateway and `SecurityHeadersMiddleware`.
- **Repudiation:** Mitigated by comprehensive audit logging in `backend/app/production/audit/`.
- **Information Disclosure:** Mitigated by `SecurityHeadersMiddleware`, removing server banners, and rigorous Pydantic response models preventing over-fetching.
- **Denial of Service (DoS):** Mitigated by `RequestLimitMiddleware` using a Redis-backed sliding window rate limiter.
- **Elevation of Privilege:** Mitigated by RBAC enforcement (`rbac_service.py`) and strict endpoint role bindings.

### Database (PostgreSQL)
- **Spoofing:** Mitigated by restricted network access and strong password/certificate authentication for the App layer.
- **Tampering:** Mitigated by SQLAlchemy ORM preventing SQL injection and rigorous data validation.
- **Repudiation:** Mitigated by database-level query logging for administrative actions.
- **Information Disclosure:** Mitigated by encryption at rest and column-level encryption for sensitive PII.
- **Denial of Service:** Mitigated by connection pooling and query timeout configurations.
- **Elevation of Privilege:** Mitigated by least-privilege database roles (App user cannot drop tables).

### Cache (Redis)
- **Spoofing/Tampering:** Mitigated by requirepass configuration and isolating Redis to internal networks.
- **Information Disclosure:** Mitigated by not storing PII in cache, only transient IDs and rate-limit counters.

### External Integrations (LLM)
- **Information Disclosure:** Mitigated by redacting PII from prompts before sending to the LLM.
- **Denial of Service:** Mitigated by `backend/app/production/resilience/` circuit breakers preventing cascading failures if the LLM provider is down.

## 5. Attack Surface Inventory

- **Exposed HTTP Endpoints:** 12 API routers under `/api/v1` (Auth, Users, Elections, Analytics, etc.).
- **Health/Diagnostic Endpoints:** `/api/v1/health`, `/ready`, `/live`, `/diagnostics` (Must ensure no sensitive config is leaked).
- **WebSockets/SSE:** Real-time election updates stream (Requires token validation on connection upgrade).
- **Admin Interfaces:** Back-office endpoints (Must be restricted by RBAC `admin` role and potentially IP whitelists).

## 6. Data Classification

- **Public:** Election results, public candidate profiles, general statistics.
- **Internal Operational:** System health metrics, generic application logs, non-sensitive configuration.
- **Confidential:** User credentials (hashes), API keys, connection strings.
- **Restricted:** Detailed audit logs, pre-release intelligence reports, user PII.

## 7. Security Controls Matrix

| Threat | Security Control | Implementation Location |
|--------|------------------|-------------------------|
| Credential Theft | Argon2id Hashing | `backend/app/identity/services/auth_service.py` |
| Session Hijacking | JWT Bearer Tokens, HSTS | `backend/app/identity/`, `SecurityHeadersMiddleware` |
| Unauthorized Access | RBAC validation | `backend/app/identity/services/rbac_service.py` |
| Brute Force / DoS | Redis Sliding Window Rate Limiting | `backend/app/performance/ratelimit/` |
| XSS / Clickjacking | CSP, CORS, X-Frame-Options | `SecurityHeadersMiddleware`, `CORS` middleware |
| Host Header Attacks| TrustedHosts validation | `TrustedHosts` middleware |
| Supply Chain Attacks | SBOM generation | `backend/app/production/sbom/` |
| Lack of Traceability | Audit Logging | `backend/app/production/audit/` |

## 8. Residual Risks and Accepted Risks

- **Accepted Risk:** DoS attacks utilizing highly distributed botnets may overwhelm the API Gateway before the application-level rate limiting can effectively block them. Mitigation relies on upstream WAF (Web Application Firewall) capabilities.
- **Residual Risk:** Zero-day vulnerabilities in core dependencies (FastAPI, SQLAlchemy). Mitigated by strict adherence to the Dependency Update Policy.

## 9. Threat Model Review Cadence

This threat model must be reviewed and updated:
- Annually by the security and architecture teams.
- Whenever a new major architectural component is introduced.
- Following any significant security incident or breach.
