# Security Architecture Directory Structure

```
backend/
├── app/
│   ├── config/
│   │   └── settings.py               # Security environment settings (CORS, Hosts, Limits)
│   ├── main.py                       # Application factory with middleware stack
│   └── security/
│       ├── __init__.py               # Exports security middlewares and setup handlers
│       ├── cors.py                   # Environment-driven CORS configuration
│       ├── headers.py                # Security response headers middleware
│       ├── middleware.py             # Payload size limit & timeout middleware
│       ├── request_id.py             # Request ID injection & structured logging
│       └── trusted_hosts.py          # TrustedHostMiddleware configuration
tests/
├── test_cors.py                      # CORS preflight unit tests
├── test_request_id.py                # UUID request tracking unit tests
├── test_request_size.py              # Payload size limit unit tests
├── test_security_headers.py          # Security response header unit tests
└── test_trusted_hosts.py             # Host header validation unit tests
SECURITY_GUIDE.md                     # Security architecture & controls guide
SECURITY_STRUCTURE.md                 # Security directory layout documentation
SECURITY_VALIDATION.md                # Security baseline verification report
```

## Security Pipeline Execution Order
1. **`TrustedHostMiddleware`**: Rejects invalid HTTP Host headers.
2. **`CORSMiddleware`**: Manages cross-origin resource access.
3. **`RequestIdMiddleware`**: Injects `X-Request-ID` UUID and initializes latency timer.
4. **`RequestLimitMiddleware`**: Validates payload size and manages execution timeouts.
5. **`SecurityHeadersMiddleware`**: Injects security response headers.
