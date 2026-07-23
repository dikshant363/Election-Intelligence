"""Core event system abstractions and event bus contracts."""

import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, kw_only=True)
class Event:
    """Base immutable event structure."""

    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, kw_only=True)
class DomainEvent(Event):
    """Base domain event emitted within a single bounded context."""

    pass


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent(Event):
    """Base integration event emitted across system boundaries."""

    pass


class Publisher[E: Event](ABC):
    """Abstract event publisher interface."""

    @abstractmethod
    async def publish(self, event: E) -> None:
        """Publish an event to subscribers."""
        pass


class Subscriber[E: Event](ABC):
    """Abstract event subscriber interface."""

    @abstractmethod
    async def subscribe(
        self,
        event_type: type[E],
        handler: Callable[[E], Awaitable[None]],
    ) -> None:
        """Register an async handler function for an event type."""
        pass


class EventBus[E: Event](Publisher[E], Subscriber[E], ABC):
    """Abstract combined EventBus contract."""

    pass


class InMemoryEventBus(EventBus[Event]):
    """Lightweight in-memory EventBus implementation placeholder."""

    def __init__(self) -> None:
        self._subscribers: dict[
            type[Event], list[Callable[[Event], Awaitable[None]]]
        ] = defaultdict(list)

    async def subscribe(
        self,
        event_type: type[Event],
        handler: Callable[[Event], Awaitable[None]],
    ) -> None:
        """Subscribe an async handler function to an event type."""
        self._subscribers[event_type].append(handler)

    async def publish(self, event: Event) -> None:
        """Publish an event instance to all registered handlers."""
        handlers = self._subscribers.get(type(event), [])
        for handler in handlers:
            await handler(event)
