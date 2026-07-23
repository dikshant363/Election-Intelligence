"""Security module initialization."""

from app.security.cors import setup_cors
from app.security.headers import SecurityHeadersMiddleware
from app.security.middleware import RequestLimitMiddleware
from app.security.request_id import RequestIdMiddleware, request_id_middleware
from app.security.trusted_hosts import setup_trusted_hosts

__all__ = [
    "RequestIdMiddleware",
    "RequestLimitMiddleware",
    "SecurityHeadersMiddleware",
    "request_id_middleware",
    "setup_cors",
    "setup_trusted_hosts",
]
