"""Pydantic v2 schemas for Real-Time & Event-Streaming APIs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EventEnvelopeSchema(BaseModel):
    """Standardized EventEnvelope API representation."""

    model_config = ConfigDict(frozen=True)

    event_id: str
    event_type: str
    event_version: str = "v1"
    aggregate_id: str
    timestamp: str
    correlation_id: str
    causation_id: str
    producer: str = "election-platform"
    payload: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)


class PublishEventRequestSchema(BaseModel):
    """Request payload to publish a custom event."""

    model_config = ConfigDict(frozen=True)

    event_type: str = Field(..., description="e.g. ElectionCreated, ResultPublished")
    aggregate_id: str = Field(...)
    payload: dict[str, Any] = Field(default_factory=dict)
    topic: str = Field(default="system_notifications")


class NotificationSchema(BaseModel):
    """Notification message container."""

    model_config = ConfigDict(frozen=True)

    id: str
    topic: str
    title: str
    message: str
    priority: str = Field(default="normal", description="low, normal, high, urgent")
    timestamp: str
    payload: dict[str, Any] = Field(default_factory=dict)


class PresenceInfoSchema(BaseModel):
    """Connected user & session presence status."""

    model_config = ConfigDict(frozen=True)

    client_id: str
    user_id: str | None = None
    connected_at: str
    last_heartbeat: str
    topics: list[str]
    is_idle: bool = False


class RealtimeMetricsSchema(BaseModel):
    """Realtime system throughput and connection metrics."""

    model_config = ConfigDict(frozen=True)

    connected_clients: int
    messages_per_sec: float
    dropped_messages: int
    worker_throughput: float
    avg_latency_ms: float
    reconnect_count: int
    queue_depth: int
