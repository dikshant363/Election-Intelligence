# Secrets Management Guide

This document outlines the approach to managing, storing, and rotating secrets within the Election Intelligence Platform (v1.0.0).

## 1. SecretsProvider Abstraction Design
The platform uses a `SecretsProvider` abstraction to manage secrets uniformly, regardless of the underlying storage mechanism. This design prevents vendor lock-in and allows seamless transitions between environments. 

Supported backends:
- **Environment Variables**: For local development or simple deployments.
- **HashiCorp Vault**: Primary solution for production, utilizing dynamic secrets and lease management.
- **Cloud Secret Managers**: (e.g., AWS Secrets Manager, GCP Secret Manager) as alternative production backends.

## 2. Secret Categories
Secrets are classified into the following categories:
- **Database Credentials**: Usernames and passwords for PostgreSQL and other datastores.
- **JWT Secrets**: Keys used for signing and verifying JSON Web Tokens.
- **API Keys**: Keys for internal services and bounded contexts.
- **Third-Party Tokens**: Credentials for external integrations (e.g., LLM APIs, external data sources).

## 3. Local Development Secrets
- Use a `.env` file at the project root for local development.
- **Never commit `.env` to version control.** It is explicitly excluded via `.gitignore`.
- Distribute `.env.template` with empty or safe default values as a starting point for developers.

## 4. Production Secrets
- Production environments must use **Vault** or a **Cloud Secret Manager**. Environment variables should not be used for high-value secrets in production due to the risk of exposure in logs or process listings.
- Automated rotation procedures must be configured for all supported backends.

## 5. Secret Rotation Process
- **Database Credentials**: Use Vault's dynamic database secrets to generate short-lived credentials. If using static credentials, schedule automated rotation during low-traffic windows.
- **JWT Secrets**: Support multiple active signing keys. To achieve zero-downtime rotation:
  1. Introduce a new key and begin signing new tokens with it.
  2. Retain the old key for verifying existing tokens until they expire.
  3. Remove the old key once all tokens signed with it have expired.

## 6. Emergency Secret Revocation Process
In the event of a suspected compromise:
1. Immediately revoke the compromised secret in the central secret manager (Vault/Cloud).
2. Generate and deploy a new secret.
3. For JWTs, rotate the signing key immediately and flush active sessions if necessary.
4. Restart application instances to clear any cached secrets.
5. Review the audit logs to identify the source of the compromise.

## 7. Secret Scanning
To prevent accidental leaks:
- **Pre-commit Hooks**: `truffleHog` and `git-secrets` are configured in `.pre-commit-config.yaml` to scan for high-entropy strings and known secret formats before allowing commits.
- **CI/CD Pipeline**: Automated secret scanning runs on every pull request and push to the main branch.

## 8. Audit Trail for Secret Access
- The `backend/app/production/audit/` module logs all access to secrets by the application.
- Vault and cloud secret managers maintain their own immutable audit logs for administrative access and secret retrieval.

## 9. Secret Inventory Table

| Secret Name | Purpose | Rotation Frequency | Storage Location |
| :--- | :--- | :--- | :--- |
| `DB_PASSWORD` | Primary PostgreSQL database password | 30 Days (Dynamic preferred) | Vault / Cloud Secret Manager |
| `JWT_PRIVATE_KEY` | Signs access and refresh tokens | 90 Days | Vault / Cloud Secret Manager |
| `LLM_API_KEY` | Authentication for external AI models | 90 Days | Vault / Cloud Secret Manager |
| `EXTERNAL_DATA_TOKEN` | Access tokens for election data APIs | 180 Days / Provider Spec | Vault / Cloud Secret Manager |
