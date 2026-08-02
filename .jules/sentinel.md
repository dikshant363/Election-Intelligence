## 2026-08-02 - Hardcoded JWT Secret Key
**Vulnerability:** Hardcoded `SECRET_KEY` found in `backend/app/identity/services/jwt_service.py` which was used for signing and verifying JWT tokens.
**Learning:** Hardcoding secrets directly in the source code exposes them to anyone with read access to the repository, leading to potential complete authentication bypass if the repository is compromised or leaked.
**Prevention:** Always use environment variables or a configuration management system (like `pydantic-settings` which is already used in the project via `BaseSettings`) to manage sensitive information such as secret keys.
