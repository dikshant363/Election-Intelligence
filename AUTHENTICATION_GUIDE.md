# Authentication & Token Security Guide

## Overview
The Authentication module (`backend/app/identity/services/`) manages user credential verification, short-lived JWT access tokens, refresh token rotation, and API key authentication.

## Token Lifecycle Architecture

```
   [POST /api/v1/auth/login]
               │
               ▼ (Validates credentials via PasswordService Argon2id)
  [Returns Access & Refresh Tokens]
               │
   ┌───────────┴───────────┐
   ▼                       ▼
[Access Token]       [Refresh Token]
 (HMAC-SHA256,         (Tracked & Revocable in DB)
  30 min validity)
```

## Security Guarantees
1. **Argon2id Hashing**: Memory-hard Argon2id password hashing via `argon2-cffi` with transparent legacy PBKDF2 verification and automatic rehash migration (`PasswordService.needs_rehash`).
2. **Token Revocation**: Refresh tokens are stored as SHA-256 hashes in `refresh_tokens` table with explicit `is_revoked` revocation flags.
3. **API Key Security**: Developer API keys (`ei_live_...`) are hashed with SHA-256 before database insertion. Constant-time comparisons (`secrets.compare_digest`) prevent timing side-channel attacks.
4. **Clock Skew Tolerance**: 60-second leeway provided during JWT expiration verification.
