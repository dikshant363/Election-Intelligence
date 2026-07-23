"""Unified Telemetry Context standard and context propagation."""

from __future__ import annotations

import contextvars
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TelemetryContext:
    """Unified Telemetry Context accompanying every request, event, and background job."""

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    causation_id: str = ""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str | None = None
    session_id: str | None = None
    service: str = "election-intelligence"
    component: str = "api"
    environment: str = "production"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize context to dictionary."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "request_id": self.request_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "service": self.service,
            "component": self.component,
            "environment": self.environment,
            "metadata": self.metadata,
        }


# Global context variable for thread/task async context propagation
_current_telemetry_ctx: contextvars.ContextVar[TelemetryContext | None] = (
    contextvars.ContextVar("current_telemetry_ctx", default=None)
)


def get_current_telemetry_context() -> TelemetryContext:
    """Get current async task TelemetryContext or create a default one."""
    ctx = _current_telemetry_ctx.get()
    if ctx is None:
        ctx = TelemetryContext()
        _current_telemetry_ctx.set(ctx)
    return ctx


def set_telemetry_context(ctx: TelemetryContext) -> None:
    """Set TelemetryContext for current async execution context."""
    _current_telemetry_ctx.set(ctx)
