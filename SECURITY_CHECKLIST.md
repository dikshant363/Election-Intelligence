# Security Checklist

## Authentication & Authorization
- [ ] Argon2 used for password hashing (implemented in `backend/app/security/`)
- [ ] JWT tokens issued with correct expiration times
- [ ] Refresh token rotation implemented
- [ ] Role-Based Access Control (RBAC) enforced on all administrative routes
- [ ] Session invalidation on password change
- [ ] Multi-factor authentication (MFA) logic tested
- [ ] Brute-force protection on login endpoints (RateLimiter)
- [ ] Secure password reset flows (no token leakage)
- [ ] Email verification required for specific actions

## API Security
- [ ] Rate limiting applied globally and per-route (implemented via sliding window)
- [ ] Input validation using Pydantic v2 (no arbitrary dicts accepted)
- [ ] Content-Type strictly validated (application/json)
- [ ] Max request body size restricted
- [ ] Proper error handling (no stack traces in production responses)
- [ ] CORS policies restrict origins to known frontends
- [ ] GraphQL/REST depth and complexity limits enforced
- [ ] Anti-automation/bot protection on public endpoints

## Data Protection
- [ ] Database credentials not stored in code (SecretsProvider)
- [ ] PII data encrypted at rest where required
- [ ] TLS 1.2+ enforced for all data in transit
- [ ] Sensitive headers (e.g., Authorization) stripped from logs
- [ ] Data retention policies implemented
- [ ] Secure backup snapshots configured (in `backend/app/production/`)
- [ ] Database connection pool configured securely
- [ ] SQL injection prevented (using SQLAlchemy ORM everywhere)

## Infrastructure Security
- [ ] Container images scanned for vulnerabilities
- [ ] Least privilege IAM roles for application services
- [ ] Network segmentation applied (DB inaccessible from public internet)
- [ ] WAF (Web Application Firewall) configured
- [ ] Autoscaling engine respects resource limits
- [ ] Chaos module tests failover and resilience (in `backend/app/production/`)
- [ ] Cloud metadata endpoints restricted from pods
- [ ] Immutable infrastructure deployments

## Supply Chain Security
- [ ] SPDX 2.3 SBOM generated per release (in `backend/app/production/`)
- [ ] Dependency pinning (hashes enforced in poetry/requirements)
- [ ] Automated Dependabot/Renovate alerts enabled
- [ ] Third-party libraries audited periodically
- [ ] CI/CD pipeline requires signed commits
- [ ] Pipeline secrets securely injected
- [ ] No malicious packages detected in latest scan
- [ ] Release manager enforces integrity checks (in `backend/app/production/`)

## Secret Management
- [ ] SecretsProvider integrates with external vault (e.g., AWS Secrets Manager)
- [ ] No hardcoded secrets in source code
- [ ] API keys generated with secure entropy
- [ ] Secret rotation strategy defined and tested
- [ ] Environment variables securely managed
- [ ] Tokens and keys never logged
- [ ] Ephemeral credentials used where possible

## Audit & Compliance
- [ ] Audit module logs all administrative actions (in `backend/app/production/`)
- [ ] Audit logs are append-only and tamper-evident
- [ ] User consent tracked for GDPR/privacy compliance
- [ ] ECI data compliance validated
- [ ] Data provenance tracked for all election statistics
- [ ] Access logs retained for the required compliance period
- [ ] Regular security compliance review scheduled

## Network Security
- [ ] SecurityHeadersMiddleware implements HSTS, CSP, X-Frame-Options
- [ ] DDoS mitigation active at the edge
- [ ] Internal microservices communicate over mTLS
- [ ] Default deny egress network policies
- [ ] IP allowlists for administrative portals
- [ ] Secure WebSockets (wss://) enforced for realtime streaming
- [ ] No unused ports exposed in containers

## OWASP Top 10 Coverage
- [ ] A01: Broken Access Control verified
- [ ] A02: Cryptographic Failures checked
- [ ] A03: Injection (SQL, NoSQL, OS command) prevented
- [ ] A04: Insecure Design reviewed
- [ ] A05: Security Misconfiguration audited
- [ ] A06: Vulnerable and Outdated Components patched
- [ ] A07: Identification and Authentication Failures mitigated
- [ ] A08: Software and Data Integrity Failures mitigated
- [ ] A09: Security Logging and Monitoring Failures fixed
- [ ] A10: Server-Side Request Forgery (SSRF) prevented

## Security Testing
- [ ] SAST (Static Application Security Testing) passing
- [ ] DAST (Dynamic Application Security Testing) passing
- [ ] Penetration test report reviewed and findings remediated
- [ ] Fuzz testing applied to critical parsers
- [ ] Load testing confirms resilience under attack

## Incident Response Readiness
- [ ] Runbooks updated for security incidents
- [ ] On-call rotation established and tested
- [ ] Log aggregation functioning (observability module)
- [ ] CircuitBreaker configured to shed load gracefully (in `backend/app/production/`)
- [ ] Communication templates ready for breach notification

## Pre-Release Security Review
- [ ] All code reviewed by at least one peer
- [ ] Security champion sign-off completed
- [ ] Threat model updated for new features
- [ ] Open vulnerabilities resolved according to SLA

## Pre-Deployment Security Review
- [ ] Staging environment mirrors production security controls
- [ ] Final credential rotation verified
- [ ] WAF rules tested in monitoring mode before blocking
- [ ] Rollback plan documented and tested
