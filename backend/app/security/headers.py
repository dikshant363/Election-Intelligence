"""Security headers middleware."""

from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing secure response headers."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response: Response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        if settings.CONTENT_SECURITY_POLICY:
            response.headers["Content-Security-Policy"] = (
                settings.CONTENT_SECURITY_POLICY
            )

        if settings.ENABLE_HSTS or settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = (
                f"max-age={settings.HSTS_MAX_AGE}; includeSubDomains"
            )

        return response
