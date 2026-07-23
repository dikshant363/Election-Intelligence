"""Realtime Layer Application Service coordinator."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from app.realtime.eventbus import EventBus, global_event_bus
from app.realtime.events import EventEnvelope
from app.realtime.metrics import MetricsCollector
from app.realtime.notifications import NotificationService
from app.realtime.presence import ClientPresence
from app.realtime.schemas import PresenceInfoSchema, RealtimeMetricsSchema
from app.realtime.streaming import ConnectionManager
from app.realtime.workers import BackgroundWorker, Job


class RealtimeService:
    """
    Realtime Intelligence Service.
    Coordinates EventBus publishing, streaming connections, background workers, notifications, and presence.
    """

    def __init__(
        self,
        event_bus: EventBus | None = None,
        connection_manager: ConnectionManager | None = None,
        worker: BackgroundWorker | None = None,
    ) -> None:
        self.event_bus = event_bus or global_event_bus
        self.connection_manager = connection_manager or ConnectionManager()
        self.worker = worker or BackgroundWorker()
        self.notification_service = NotificationService(event_bus=self.event_bus)
        self.metrics_collector = MetricsCollector()

    async def publish_event(self, topic: str, event: EventEnvelope) -> None:
        """Publish event to EventBus and broadcast to connected WebSocket clients."""
        await self.event_bus.publish(topic, event)
        await self.connection_manager.broadcast_event(topic, event)
        self.metrics_collector.record_message()

    def replay_events(
        self, topic: str, from_timestamp: str | None = None
    ) -> list[EventEnvelope]:
        """Replay historical events from EventBus for a topic."""
        return self.event_bus.replay(topic, from_timestamp=from_timestamp)

    async def stream_topic(self, topic: str) -> AsyncGenerator[EventEnvelope, None]:
        """Stream events for a topic as an async generator (used for SSE endpoints)."""
        queue: asyncio.Queue[EventEnvelope] = asyncio.Queue()

        async def _handler(event: EventEnvelope) -> None:
            await queue.put(event)

        self.event_bus.subscribe(topic, _handler)
        try:
            while True:
                event = await queue.get()
                yield event
        finally:
            self.event_bus.unsubscribe(topic, _handler)

    def list_presence(self) -> list[PresenceInfoSchema]:
        """List current connected client presence information."""
        clients: list[ClientPresence] = self.connection_manager.presence.list_presence()
        return [
            PresenceInfoSchema(
                client_id=c.client_id,
                user_id=c.user_id,
                connected_at=c.connected_at,
                last_heartbeat=c.last_heartbeat,
                topics=list(c.topics),
            )
            for c in clients
        ]

    def get_metrics(self) -> RealtimeMetricsSchema:
        """Get system throughput, connection count, and latency metrics."""
        active_count = self.connection_manager.presence.count()
        return self.metrics_collector.get_snapshot(active_clients=active_count)

    async def enqueue_background_job(
        self, job: Job, handler: Any
    ) -> None:
        """Enqueue background worker task."""
        await self.worker.enqueue(job, handler)
