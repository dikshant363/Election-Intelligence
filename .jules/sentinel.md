## 2026-08-04 - [Remove Hardcoded JWT Secret]
 **Vulnerability:** Hardcoded JWT secret key found in `JwtService` class. If the source code is compromised or accidentally exposed, the secret would be leaked.
 **Learning:** Security critical secrets like JWT signing keys must not be hardcoded in the codebase, even with a warning comment to change in production. They should be configured via environment variables.
 **Prevention:** Use `pydantic-settings` to manage environment variables and provide a secure default in development, and ensure production deployments always supply the environment variable.
