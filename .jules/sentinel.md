## 2026-07-29 - [CRITICAL] Fix hardcoded JWT secret key
**Vulnerability:** A hardcoded secret key (`"election-intelligence-secret-key-change-in-prod"`) was found in `backend/app/identity/services/jwt_service.py` for JWT signing.
**Learning:** Hardcoded credentials and secrets allow attackers who gain access to the source code to trivially bypass security mechanisms like authentication.
**Prevention:** Always rely on application settings loaded securely from environment variables (e.g., using `pydantic-settings`) for all cryptographic keys, passwords, and API keys. Provide safe development defaults via `.env.example` but mandate strong, random values in production environments.
