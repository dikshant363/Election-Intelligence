## 2026-07-26 - [Hardcoded JWT Secret Key]
**Vulnerability:** The JWT SECRET_KEY was hardcoded in `JwtService` as "election-intelligence-secret-key-change-in-prod".
**Learning:** Hardcoding sensitive secrets like JWT signing keys directly into the source code is a critical vulnerability as it exposes the key to anyone with read access to the repository.
**Prevention:** Always read secrets from secure configuration, ideally environment variables using tools like `pydantic-settings`, rather than storing them in code.
