"""Unit tests for event system interfaces and in-memory event bus."""

from dataclasses import dataclass

import pytest
from app.core.events import DomainEvent, InMemoryEventBus, IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class SampleDomainEvent(DomainEvent):
    payload: str


@dataclass(frozen=True, kw_only=True)
class SampleIntegrationEvent(IntegrationEvent):
    payload: str


@pytest.mark.asyncio
async def test_event_instantiation_properties() -> None:
    """Verify event class defaults and immutability."""
    evt = SampleDomainEvent(payload="domain_test")
    assert evt.event_id is not None
    assert evt.occurred_at is not None
    assert evt.payload == "domain_test"


@pytest.mark.asyncio
async def test_in_memory_event_bus_pub_sub() -> None:
    """Verify InMemoryEventBus pub/sub dispatch."""
    bus = InMemoryEventBus()
    received: list[str] = []

    async def handle_event(event: SampleDomainEvent) -> None:
        received.append(event.payload)

    await bus.subscribe(SampleDomainEvent, handle_event)
    await bus.publish(SampleDomainEvent(payload="event_message"))

    assert len(received) == 1
    assert received[0] == "event_message"
