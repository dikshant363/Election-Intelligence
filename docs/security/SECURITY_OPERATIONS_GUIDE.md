# Security Operations & Secrets Management Guide

## Overview

The `SecurityHardener`, `SecretsProvider`, and `AuditLogger` enforce enterprise security, secrets protection, and compliance auditing.

---

## Secrets Management Abstraction

Applications access secrets through `SecretsProvider`:

```python
from app.production.secrets import global_secrets_provider

database_url = global_secrets_provider.get_secret("DATABASE_URL")
```

Supports:
- `EnvSecretsProvider` (Environment variables)
- `VaultSecretsAdapter` (HashiCorp Vault)
- `CloudSecretManagerAdapter` (AWS / GCP Secret Manager)

---

## Security Headers & CSP Policies

```text
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

---

## Immutable Audit Trail

Administrative and security actions log immutable events:

```python
from app.production.audit import global_audit_logger

global_audit_logger.log_event(
    event_type="security",
    actor_id="admin_1",
    action="update_role_permissions",
    resource="role_election_officer",
)
```
