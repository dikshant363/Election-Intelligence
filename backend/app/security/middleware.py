"""Request size limit and request timeout middleware."""

import asyncio
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.logging import get_logger

logger = get_logger("app.security")


class RequestLimitMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing max payload size and request execution timeouts."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = getattr(request.state, "request_id", "unknown")

        # 1. Content-Length Header Check
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                length = int(content_length)
                if length > settings.MAX_REQUEST_SIZE:
                    logger.warning(
                        f"Request payload size {length} bytes exceeds limit of "
                        f"{settings.MAX_REQUEST_SIZE} bytes. RequestID={request_id}"
                    )
                    return JSONResponse(
                        status_code=413,
                        content={
                            "detail": "Request payload exceeds maximum allowed size limit.",
                            "request_id": request_id,
                        },
                    )
            except ValueError:
                pass

        # 2. Timeout enforcement
        try:
            return await asyncio.wait_for(
                call_next(request),
                timeout=settings.REQUEST_TIMEOUT,
            )
        except TimeoutError:
            logger.warning(
                f"Request execution timed out after {settings.REQUEST_TIMEOUT}s. "
                f"RequestID={request_id}"
            )
            return JSONResponse(
                status_code=504,
                content={
                    "detail": "Request execution timed out.",
                    "request_id": request_id,
                },
            )
