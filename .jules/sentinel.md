## 2025-02-23 - Hardcoded JWT Secret Key in `JwtService`
**Vulnerability:** A hardcoded string ("election-intelligence-secret-key-change-in-prod") is being used as the `SECRET_KEY` in `backend/app/identity/services/jwt_service.py` to sign and verify JWT tokens.
**Learning:** Hardcoding a secret key in source code allows anyone with access to the code to forge authentication tokens, bypassing all authorization checks in the application. Although the environment example has `JWT_SECRET_KEY`, the actual implementation does not read from it.
**Prevention:** Always read security-sensitive values, such as secret keys, from secure configuration sources (e.g., environment variables) instead of placing them directly in the codebase.
