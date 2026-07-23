"""EventBus abstraction, InMemory implementation, topic registry, and replay support."""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Awaitable, Callable

from app.realtime.events import EventEnvelope

logger = logging.getLogger("app.realtime.eventbus")

# Callback type signature: Async function accepting an EventEnvelope
EventHandler = Callable[[EventEnvelope], Awaitable[None]]


class EventBus(ABC):
    """Abstract base class for vendor-independent EventBus messaging."""

    @abstractmethod
    async def publish(self, topic: str, event: EventEnvelope) -> None:
        """Publish an EventEnvelope to a specific topic."""

    @abstractmethod
    def subscribe(self, topic: str, handler: EventHandler) -> None:
        """Subscribe an async handler to a topic."""

    @abstractmethod
    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        """Unsubscribe an async handler from a topic."""

    @abstractmethod
    def replay(self, topic: str, from_timestamp: str | None = None) -> list[EventEnvelope]:
        """Replay historical events published to a topic."""


class InMemoryEventBus(EventBus):
    """In-memory EventBus with async dispatch, topic isolation, and replay store."""

    def __init__(self, max_history: int = 1000) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._event_store: dict[str, list[EventEnvelope]] = defaultdict(list)
        self._max_history = max_history

    async def publish(self, topic: str, event: EventEnvelope) -> None:
        """Publish event and dispatch asynchronously to all registered subscribers."""
        # Save to replay event log
        history = self._event_store[topic]
        history.append(event)
        if len(history) > self._max_history:
            history.pop(0)

        handlers = list(self._handlers.get(topic, []))
        if not handlers:
            return

        # Execute handlers concurrently
        tasks = [asyncio.create_task(self._safe_call(h, event)) for h in handlers]
        await asyncio.gather(*tasks, return_exceptions=True)

    @staticmethod
    async def _safe_call(handler: EventHandler, event: EventEnvelope) -> None:
        try:
            await handler(event)
        except Exception as err:  # noqa: BLE001
            logger.error("Event handler error for topic %s: %s", event.event_type, err)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        """Subscribe handler to a topic."""
        if handler not in self._handlers[topic]:
            self._handlers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        """Unsubscribe handler from a topic."""
        if handler in self._handlers[topic]:
            self._handlers[topic].remove(handler)

    def replay(self, topic: str, from_timestamp: str | None = None) -> list[EventEnvelope]:
        """Replay historical events for a topic."""
        events = self._event_store.get(topic, [])
        if not from_timestamp:
            return list(events)
        return [e for e in events if e.timestamp >= from_timestamp]

    def clear(self) -> None:
        """Clear all subscribers and history (for testing)."""
        self._handlers.clear()
        self._event_store.clear()


# Singleton global event bus
global_event_bus = InMemoryEventBus()
