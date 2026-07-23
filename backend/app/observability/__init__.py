"""Observability, Telemetry & Operations Platform package root."""

from app.observability.alerts import AlertManager, global_alert_manager
from app.observability.exceptions import (
    AlertTriggerError,
    HealthCheckError,
    ObservabilityException,
    TelemetryError,
)
from app.observability.health import HealthChecker
from app.observability.logging import get_structured_logger
from app.observability.metrics import SystemMetricsRegistry, global_metrics
from app.observability.middleware import ObservabilityMiddleware
from app.observability.services import ObservabilityService
from app.observability.telemetry import (
    TelemetryContext,
    get_current_telemetry_context,
    set_telemetry_context,
)
from app.observability.tracing import Span, TracerProvider, global_tracer

__all__ = [
    "TelemetryContext",
    "get_current_telemetry_context",
    "set_telemetry_context",
    "TracerProvider",
    "Span",
    "global_tracer",
    "SystemMetricsRegistry",
    "global_metrics",
    "HealthChecker",
    "AlertManager",
    "global_alert_manager",
    "ObservabilityMiddleware",
    "ObservabilityService",
    "get_structured_logger",
    "ObservabilityException",
    "TelemetryError",
    "HealthCheckError",
    "AlertTriggerError",
]
