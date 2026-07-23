"""Application event dispatcher integrating Domain Events with EventBus."""

from app.core.events import EventBus
from app.domain.common import AggregateRoot


class EventDispatcher:
    """Dispatches recorded domain events from AggregateRoots through EventBus interface."""

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._event_bus = event_bus

    async def dispatch_events_for(self, aggregate: AggregateRoot) -> int:
        """Collect recorded domain events, publish via EventBus, and clear aggregate queue."""
        events = aggregate.domain_events
        if not events:
            return 0

        dispatched_count = 0
        if self._event_bus is not None:
            for event in events:
                await self._event_bus.publish(event)
                dispatched_count += 1

        aggregate.clear_domain_events()
        return dispatched_count
