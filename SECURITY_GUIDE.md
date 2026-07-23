# Security Baseline Architecture Guide

## Overview
The Election Intelligence Platform security baseline enforces secure-by-default backend infrastructure. Every future endpoint inherits security defaults without requiring manual per-route security implementation.

## Core Architectural Controls

### 1. Hardened Security Headers (`app/security/headers.py`)
- **`X-Content-Type-Options: nosniff`**: Prevents MIME-type sniffing vulnerabilities.
- **`X-Frame-Options: DENY`**: Mitigates clickjacking attacks.
- **`Referrer-Policy: strict-origin-when-cross-origin`**: Protects referral metadata.
- **`Permissions-Policy: camera=(), microphone=(), geolocation=()`**: Disables unused browser device APIs.
- **`Cross-Origin-Opener-Policy: same-origin`** & **`Cross-Origin-Resource-Policy: same-origin`**: Enforces process isolation.
- **`Content-Security-Policy`**: Enforces strict default resource loading restrictions.
- **`Strict-Transport-Security` (HSTS)**: Enforces HTTPS transport in production.

### 2. Environment-Driven CORS (`app/security/cors.py`)
- Enforces strict origin allowlists via `ALLOWED_ORIGINS`.
- Wildcard origin (`*`) is explicitly prohibited in production configurations.
- Exposes `X-Request-ID` header for client-side distributed tracing.

### 3. Host Validation (`app/security/trusted_hosts.py`)
- Enforces `TrustedHostMiddleware` based on `ALLOWED_HOSTS` to prevent HTTP Host header injection and cache poisoning attacks.

### 4. Distributed Tracing & Request ID (`app/security/request_id.py`)
- Every incoming request receives a UUID `X-Request-ID`.
- Request ID is injected into request state, attached to response headers, included in `GET /health` responses, and embedded in structured logs.

### 5. Structured Request Logging (`app/security/request_id.py`)
- Structured logging captures `Method`, `Path`, `Status`, `Duration`, `ClientIP`, and `RequestID`.
- Excludes sensitive headers, body contents, and credentials.

### 6. Payload Limits & Timeouts (`app/security/middleware.py`)
- Enforces maximum request payload size via `MAX_REQUEST_SIZE` (default 10 MB, returns `413 Payload Too Large`).
- Enforces request execution timeout via `REQUEST_TIMEOUT` (default 30.0s, returns `504 Gateway Timeout`).

## Testing & Operations

```bash
# Run security test suite
.venv/bin/pytest tests/test_security_headers.py tests/test_request_id.py tests/test_trusted_hosts.py tests/test_cors.py tests/test_request_size.py
```
