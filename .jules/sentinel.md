
## 2024-05-24 - [CRITICAL] Fix hardcoded JWT secret key
**Vulnerability:** A hardcoded `SECRET_KEY` was found in `backend/app/identity/services/jwt_service.py` (flagged by bandit `[B105:hardcoded_password_string]`). This would allow anyone with access to the source code to forge valid JWT access tokens and completely bypass authentication/authorization.
**Learning:** Even default or "dev" secrets should not be hardcoded as constants in service classes. They should be managed via configuration systems like `pydantic-settings` to ensure they can be securely injected via environment variables in production without requiring code changes.
**Prevention:** Use `pydantic-settings` (`BaseSettings`) to manage all secrets and configurations. Load them via environment variables and never commit secrets directly in the source code.
