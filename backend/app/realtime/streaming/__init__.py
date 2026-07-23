"""Streaming Gateway supporting WebSockets, SSE, topic channels, and connection manager."""

from __future__ import annotations

import asyncio
import json
import logging
from collections import defaultdict
from collections.abc import AsyncGenerator

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from app.realtime.backpressure import BackpressureController
from app.realtime.events import EventEnvelope
from app.realtime.presence import PresenceManager

logger = logging.getLogger("app.realtime.streaming")


class ConnectionManager:
    """Manages WebSocket client connections, topic subscriptions, and broadcast dispatch."""

    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}
        self.topic_subscriptions: dict[str, set[str]] = defaultdict(set)
        self.presence = PresenceManager()
        self.backpressure = BackpressureController()

    async def connect(self, client_id: str, websocket: WebSocket) -> None:
        """Accept WebSocket connection and register client presence."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.presence.register(client_id=client_id)
        logger.info("WebSocket client connected: %s", client_id)

    def disconnect(self, client_id: str) -> None:
        """Disconnect client and clean up presence and subscriptions."""
        self.active_connections.pop(client_id, None)
        self.presence.unregister(client_id)
        for topic in list(self.topic_subscriptions.keys()):
            self.topic_subscriptions[topic].discard(client_id)
        logger.info("WebSocket client disconnected: %s", client_id)

    def subscribe(self, client_id: str, topic: str) -> None:
        """Subscribe client to a topic channel."""
        self.topic_subscriptions[topic].add(client_id)
        self.presence.subscribe_topic(client_id, topic)

    def unsubscribe(self, client_id: str, topic: str) -> None:
        """Unsubscribe client from a topic channel."""
        self.topic_subscriptions[topic].discard(client_id)
        self.presence.unsubscribe_topic(client_id, topic)

    async def send_personal_message(self, message: dict, client_id: str) -> None:
        """Send message to specific connected client."""
        ws = self.active_connections.get(client_id)
        if ws:
            self.backpressure.check_rate_limit(client_id)
            await ws.send_json(jsonable_encoder(message))

    async def broadcast_event(self, topic: str, event: EventEnvelope) -> None:
        """Broadcast EventEnvelope to all clients subscribed to topic."""
        subscribers = list(self.topic_subscriptions.get(topic, set()))
        if not subscribers:
            return

        payload = jsonable_encoder(event.to_dict())
        for client_id in subscribers:
            ws = self.active_connections.get(client_id)
            if ws:
                try:
                    self.backpressure.check_rate_limit(client_id)
                    await ws.send_json(payload)
                except Exception as err:  # noqa: BLE001
                    logger.warning("Failed sending to client %s: %s", client_id, err)

    async def send_heartbeat(self) -> None:
        """Periodic heartbeat broadcast to all active connections."""
        ping = {"type": "ping", "timestamp": asyncio.get_event_loop().time()}
        for client_id, ws in list(self.active_connections.items()):
            try:
                await ws.send_json(ping)
                self.presence.update_heartbeat(client_id)
            except Exception:  # noqa: BLE001
                self.disconnect(client_id)


async def sse_event_generator(
    events: AsyncGenerator[EventEnvelope, None],
) -> AsyncGenerator[str, None]:
    """Format EventEnvelope instances as Server-Sent Events (SSE) string chunks."""
    async for event in events:
        data = json.dumps(jsonable_encoder(event.to_dict()))
        yield f"event: {event.event_type}\ndata: {data}\n\n"
