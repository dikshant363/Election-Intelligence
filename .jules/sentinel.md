## 2024-07-28 - [Hardcoded JWT Secret in JwtService]
**Vulnerability:** A hardcoded `SECRET_KEY` was found directly in the `JwtService` class.
**Learning:** This codebase relies on `pydantic-settings` (`app.config.settings.Settings`) for configuration management. Any secrets like JWT keys must be centralized there, rather than hardcoded in the service layer, to ensure they can be securely loaded from environment variables in production.
**Prevention:** Always define secrets in the `Settings` class and inject them into services (e.g., `settings.JWT_SECRET_KEY`) instead of defining them locally in classes.
