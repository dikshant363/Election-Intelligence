"""Request ID middleware and structured request logger."""

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from app.logging import get_logger

logger = get_logger("app.request")


async def request_id_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Middleware that injects a unique X-Request-ID and logs request lifecycle metrics."""
    request_id = (
        getattr(request.state, "request_id", None)
        or request.headers.get("X-Request-ID")
        or request.headers.get("x-request-id")
    )
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


# Alias for backward compatibility
RequestIdMiddleware = request_id_middleware
