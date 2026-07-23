"""Real-Time Intelligence & Event Streaming Platform package root."""

from app.realtime.eventbus import EventBus, InMemoryEventBus, global_event_bus
from app.realtime.events import EventEnvelope
from app.realtime.exceptions import (
    BackpressureError,
    EventBusError,
    RealtimeException,
    WorkerError,
)
from app.realtime.services import RealtimeService
from app.realtime.streaming import ConnectionManager
from app.realtime.workers import BackgroundWorker, DeadLetterQueue, Job

__all__ = [
    "EventEnvelope",
    "EventBus",
    "InMemoryEventBus",
    "global_event_bus",
    "RealtimeService",
    "ConnectionManager",
    "BackgroundWorker",
    "Job",
    "DeadLetterQueue",
    "RealtimeException",
    "EventBusError",
    "WorkerError",
    "BackpressureError",
]
