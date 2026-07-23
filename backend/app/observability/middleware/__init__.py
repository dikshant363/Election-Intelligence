"""FastAPI Observability Middleware for automatic span creation and trace propagation."""

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.metrics import global_metrics
from app.observability.telemetry import TelemetryContext, set_telemetry_context
from app.observability.tracing import global_tracer


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware extracting/injecting trace headers and recording request metrics."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        t0 = time.monotonic()

        # Extract context headers or request.state request_id
        request_id = (
            getattr(request.state, "request_id", None)
            or request.headers.get("x-request-id")
            or str(uuid.uuid4())
        )
        trace_id = request.headers.get("x-trace-id", str(uuid.uuid4()))
        correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        span_id = str(uuid.uuid4())[:16]

        ctx = TelemetryContext(
            trace_id=trace_id,
            span_id=span_id,
            correlation_id=correlation_id,
            request_id=request_id,
            component="api",
        )
        set_telemetry_context(ctx)

        request.state.request_id = request_id

        # Execute request within tracer span
        endpoint = request.url.path
        method = request.method

        with global_tracer.start_span(
            name=f"HTTP {method} {endpoint}",
            component="api",
            attributes={"http.method": method, "http.url": str(request.url)},
        ) as span:
            try:
                response = await call_next(request)
                status_code = response.status_code
                span.attributes["http.status_code"] = status_code
            except Exception as err:  # noqa: BLE001
                status_code = 500
                span.attributes["http.status_code"] = 500
                span.attributes["error.message"] = str(err)
                raise
            finally:
                duration_sec = time.monotonic() - t0
                global_metrics.record_http(
                    method=method,
                    endpoint=endpoint,
                    status_code=status_code,
                    duration_sec=duration_sec,
                )

        # Inject trace headers into response
        response.headers["X-Trace-ID"] = ctx.trace_id
        response.headers["X-Span-ID"] = ctx.span_id
        response.headers["X-Correlation-ID"] = ctx.correlation_id
        response.headers["X-Request-ID"] = ctx.request_id

        return response
