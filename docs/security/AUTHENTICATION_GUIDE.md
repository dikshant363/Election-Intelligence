# Authentication Guide

This document details the authentication mechanisms for the Election Intelligence Platform (v1.0.0).

## 1. Authentication Architecture
The platform relies on a stateless, token-based authentication architecture. 
- **Middleware**: `identity_context_middleware` intercepts incoming requests, extracts the JWT from the `Authorization` header, and populates the request context with the authenticated user's identity.
- **Flow**: Clients authenticate via login endpoints to receive access and refresh tokens. Subsequent requests must include the access token.

## 2. Password Hashing
- **Algorithm**: Argon2id via `argon2-cffi`.
- **Why Argon2id**: It provides resistance against both GPU cracking attacks (via memory hardness) and side-channel timing attacks, making it superior to bcrypt or PBKDF2 for modern applications.
- **Parameters**: Configured to balance security and performance (e.g., time cost=2, memory cost=65536 KiB, parallelism=4).

## 3. JWT Token Lifecycle
- **Issue**: Generated upon successful login or via a refresh token.
- **Validate**: Validated by the `identity_context_middleware` using the public key (if asymmetric) or shared secret, checking the signature, expiry (`exp`), and issuer (`iss`).
- **Refresh**: Short-lived access tokens (e.g., 15 minutes) are renewed using long-lived refresh tokens (e.g., 7 days).
- **Revoke**: While JWTs are stateless, refresh tokens can be revoked by blacklisting them or tracking their lineage in the database.

## 4. Token Storage Recommendations
- **Web Clients**: Store access tokens in memory or `sessionStorage`. Store refresh tokens in `HttpOnly`, `Secure`, `SameSite=Strict` cookies to prevent XSS and CSRF attacks. Do NOT store tokens in `localStorage`.
- **Mobile Clients**: Store tokens in the secure enclave (iOS Keychain, Android Keystore).

## 5. Session Management
- Sessions are fundamentally stateless on the backend.
- State is managed via **Refresh Token Rotation**. When a refresh token is used, a new access token and a *new* refresh token are issued. The old refresh token is invalidated.

## 6. Multi-Factor Authentication Readiness
The authentication architecture is designed to support MFA. The JWT payload can include an `amr` (Authentication Methods References) claim to indicate whether the user has completed MFA, allowing endpoints to require stronger authentication levels.

## 7. API Authentication
- API requests must include the access token in the `Authorization` header using the `Bearer` schema:
  `Authorization: Bearer <access_token>`

## 8. Authentication Error Codes
- `401 Unauthorized`: Missing, invalid, or expired token.
- `403 Forbidden`: Authenticated, but lacks permissions (handled by authorization layer).
- `AUTH_001`: Invalid credentials during login.
- `AUTH_002`: Token expired.
- `AUTH_003`: Invalid token signature.

## 9. Testing Authentication
- Use the `test_identity.py` suite for unit tests.
- **Test Tokens**: Use the `create_test_token()` fixture in `conftest.py` to generate valid tokens with specific roles for integration testing (e.g., in `test_e2e_integration.py`).

## 10. Security Considerations
- **HTTPS**: All authentication endpoints and API requests MUST occur over HTTPS. The application enforces HSTS.
- **Token Expiry**: Access tokens must be short-lived to minimize the window of opportunity if compromised.
- **Secure Cookies**: If utilizing cookies for refresh tokens, they must be flagged as `Secure` and `HttpOnly`.
