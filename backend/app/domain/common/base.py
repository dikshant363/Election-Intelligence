"""Base Domain-Driven Design (DDD) building blocks."""

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class ValueObject:
    """Base class for all Domain Value Objects (immutable, value-equality)."""

    pass


@dataclass(frozen=True)
class Identifier(ValueObject):
    """Immutable domain identifier wrapping a UUID or string value."""

    value: uuid.UUID | str

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"


@dataclass(frozen=True)
class Timestamp(ValueObject):
    """Immutable domain UTC timestamp."""

    value: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __repr__(self) -> str:
        return f"Timestamp({self.value.isoformat()})"


class Entity[ID]:
    """Base class for domain entities with identity."""

    def __init__(self, id: ID) -> None:
        self._id = id

    @property
    def id(self) -> ID:
        """Return unique entity identifier."""
        return self._id

    def __eq__(self, other: object) -> bool:
        """Check equality based on entity identity."""
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class AggregateRoot[ID](Entity[ID]):
    """Base class for DDD Aggregate Roots managing domain events."""

    def __init__(self, id: ID) -> None:
        super().__init__(id)
        self._domain_events: list[Any] = []

    @property
    def domain_events(self) -> list[Any]:
        """Return copy of recorded domain events."""
        return list(self._domain_events)

    def add_domain_event(self, event: Any) -> None:
        """Record a domain event."""
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Clear recorded domain events."""
        self._domain_events.clear()
