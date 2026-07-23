"""Real-Time Intelligence Layer exception hierarchy."""

from __future__ import annotations


class RealtimeException(Exception):
    """Base exception for all realtime & event-streaming operations."""

    def __init__(self, message: str, code: str = "REALTIME_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class EventBusError(RealtimeException):
    """Raised when event publishing or subscription fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="EVENT_BUS_ERROR")


class WorkerError(RealtimeException):
    """Raised when background job or worker execution fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="WORKER_ERROR")


class BackpressureError(RealtimeException):
    """Raised when outbound connection queue is full or rate limit is exceeded."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="BACKPRESSURE_OVERFLOW")
