## 2026-07-30 - Fix Hardcoded JWT Secret Key
**Vulnerability:** A hardcoded secret key (`election-intelligence-secret-key-change-in-prod`) was used for JWT signing in `backend/app/identity/services/jwt_service.py`.
**Learning:** Hardcoded secrets in the source code can be easily extracted by attackers, leading to the ability to forge valid JWT access tokens and completely bypass the application's authentication and authorization mechanisms. This completely compromises the RBAC system.
**Prevention:** Always use environment variables (e.g., via `pydantic-settings`) to inject sensitive configuration at runtime. Never commit secrets, API keys, or passwords to the repository, not even placeholder ones, to avoid them accidentally being deployed.
