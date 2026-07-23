# Identity & Access Management (IAM) Architecture Guide

## Overview
The Identity Layer (`backend/app/identity/`) manages authentication, role-based authorization, token security, and audit logging as pure infrastructure concerns. The domain model remains 100% agnostic to JWTs, HTTP headers, OAuth, or user accounts.

## Identity Architecture

```
[HTTP Client Request]
       │ (Authorization: Bearer <token>)
       ▼
[IdentityContextMiddleware]
       │
       ▼ (Populates request.state.identity)
[FastAPI Auth Dependencies]  (get_current_user, require_role, require_permission)
       │
       ▼
[REST Routers & Application Pipelines]
```

## Core Infrastructure Components
1. **User & Credentials (`app/identity/models/user.py`)**: `UserModel`, `UserRoleModel`, `RolePermissionModel`.
2. **Password Security (`app/identity/services/password_service.py`)**: Salted PBKDF2-HMAC-SHA256 password hashing, strength policy validator, secure reset token generator.
3. **JWT Service (`app/identity/services/jwt_service.py`)**: Short-lived access tokens, refresh token rotation, revocation tracking, HMAC-SHA256 signature verification, clock-skew tolerance.
4. **RBAC Engine (`app/identity/services/rbac_service.py`)**: Hierarchical role evaluation (`PlatformAdmin`, `ElectionCommissioner`, `StateOfficer`, `DistrictOfficer`, `Analyst`, `Auditor`, `PublicUser`).
5. **API Keys (`app/identity/services/api_key_service.py`)**: `ei_live_` prefixed developer keys, SHA-256 hashed storage, scope checking.
6. **Audit Service (`app/identity/services/audit_service.py`)**: Immutable `AuditEntryModel` event records.
7. **OIDC Readiness (`app/identity/providers/oidc_providers.py`)**: `GoogleOidcProvider`, `GithubOidcProvider`, `MicrosoftOidcProvider`.
