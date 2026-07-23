"""OpenTelemetry tracing abstraction, span processors, and distributed tracing."""

from __future__ import annotations

import time
import uuid
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from app.observability.telemetry import TelemetryContext, get_current_telemetry_context


@dataclass
class Span:
    """OpenTelemetry-compatible span representation."""

    name: str
    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    component: str = "api"
    start_time: float = field(default_factory=time.monotonic)
    end_time: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    status: str = "OK"  # OK, ERROR

    def end(self) -> None:
        self.end_time = time.monotonic()

    @property
    def duration_ms(self) -> float:
        if self.end_time is None:
            return round((time.monotonic() - self.start_time) * 1000.0, 2)
        return round((self.end_time - self.start_time) * 1000.0, 2)


class TracerProvider:
    """Tracer provider creating and tracking spans across distributed operations."""

    def __init__(self) -> None:
        self._spans: list[Span] = []

    @contextmanager
    def start_span(
        self, name: str, component: str = "api", attributes: dict[str, Any] | None = None
    ) -> Generator[Span, None, None]:
        ctx: TelemetryContext = get_current_telemetry_context()
        span = Span(
            name=name,
            trace_id=ctx.trace_id,
            span_id=str(uuid.uuid4())[:16],
            parent_span_id=ctx.span_id,
            component=component,
            attributes=attributes or {},
        )
        self._spans.append(span)

        try:
            yield span
        except Exception as err:  # noqa: BLE001
            span.status = "ERROR"
            span.attributes["error.message"] = str(err)
            raise
        finally:
            span.end()

    def get_spans(self) -> list[Span]:
        return list(self._spans)


# Singleton tracer instance
global_tracer = TracerProvider()
