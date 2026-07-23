"""Request ID middleware and structured request logger."""

import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging import get_logger

logger = get_logger("app.request")


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware that injects a unique X-Request-ID and logs request lifecycle metrics."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())

        request.state.request_id = request_id
        start_time = time.perf_counter()

        client_ip = request.client.host if request.client else "unknown"

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                f"Method={request.method} Path={request.url.path} Status=500 "
                f"Duration={duration_ms}ms ClientIP={client_ip} RequestID={request_id} Error={exc}"
            )
            raise

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"Method={request.method} Path={request.url.path} Status={response.status_code} "
            f"Duration={duration_ms}ms ClientIP={client_ip} RequestID={request_id}"
        )

        return response
