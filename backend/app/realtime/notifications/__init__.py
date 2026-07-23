"""Notification service providing targeted, broadcast, and prioritized alert delivery."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from app.realtime.eventbus import EventBus, global_event_bus
from app.realtime.events import EventEnvelope
from app.realtime.schemas import NotificationSchema


@dataclass
class NotificationService:
    """Targeted and broadcast priority notification manager."""

    event_bus: EventBus = global_event_bus

    async def notify(
        self,
        topic: str,
        title: str,
        message: str,
        priority: str = "normal",
        payload: dict[str, Any] | None = None,
    ) -> NotificationSchema:
        """Publish prioritized notification event to topic."""
        notif_id = str(uuid.uuid4())
        timestamp = datetime.now(UTC).isoformat()

        schema = NotificationSchema(
            id=notif_id,
            topic=topic,
            title=title,
            message=message,
            priority=priority,
            timestamp=timestamp,
            payload=payload or {},
        )

        event = EventEnvelope(
            event_type="NotificationSent",
            aggregate_id=notif_id,
            payload=schema.model_dump(),
            metadata={"priority": priority, "topic": topic},
        )

        await self.event_bus.publish(topic, event)
        return schema
