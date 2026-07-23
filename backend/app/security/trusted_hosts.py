"""Trusted hosts security configuration."""

from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings


def setup_trusted_hosts(app: FastAPI) -> None:
    """Configure TrustedHostMiddleware on the FastAPI application."""
    allowed_hosts = list(settings.ALLOWED_HOSTS)
    if not allowed_hosts:
        allowed_hosts = ["localhost", "127.0.0.1", "testserver"]

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts,
    )
