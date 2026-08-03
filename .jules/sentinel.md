## YYYY-MM-DD - [Title]\n**Vulnerability:** ...\n**Learning:** ...\n**Prevention:** ...
## 2026-08-03 - Fix Hardcoded JWT Secret Key
**Vulnerability:** Hardcoded JWT secret key in `jwt_service.py`.
**Learning:** Hardcoded secrets in code pose a critical security risk.
**Prevention:** Use `pydantic-settings` to load secrets like `JWT_SECRET_KEY` from environment variables.
