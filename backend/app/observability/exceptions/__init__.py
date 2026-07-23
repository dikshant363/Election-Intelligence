"""Observability Layer exception hierarchy."""

from __future__ import annotations


class ObservabilityException(Exception):
    """Base exception for all observability and telemetry operations."""

    def __init__(self, message: str, code: str = "OBSERVABILITY_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class TelemetryError(ObservabilityException):
    """Raised when trace context propagation or metric export fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="TELEMETRY_ERROR")


class HealthCheckError(ObservabilityException):
    """Raised when a critical health/readiness check fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="HEALTH_CHECK_ERROR")


class AlertTriggerError(ObservabilityException):
    """Raised when an alert rule evaluation or dispatch fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="ALERT_TRIGGER_ERROR")
