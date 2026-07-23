"""Polling booth aggregate root and domain events."""

from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.common.base import AggregateRoot
from app.domain.value_objects import (
    ConstituencyId,
    GeoCoordinates,
    PollingBoothId,
)


@dataclass(frozen=True, kw_only=True)
class PollingBoothCreated:
    """Event emitted when a new polling booth is established."""

    booth_id: PollingBoothId
    constituency_id: ConstituencyId
    booth_number: str
    occurred_at: datetime = datetime.now(UTC)


class PollingBooth(AggregateRoot[PollingBoothId]):
    """Polling booth aggregate root representing a designated voting station."""

    def __init__(
        self,
        id: PollingBoothId,
        constituency_id: ConstituencyId,
        booth_name: str,
        booth_number: str,
        location: GeoCoordinates,
    ) -> None:
        super().__init__(id)
        if not booth_name or not booth_name.strip():
            raise ValueError("Polling booth name cannot be empty.")
        if not booth_number or not booth_number.strip():
            raise ValueError("Polling booth number cannot be empty.")

        self.constituency_id = constituency_id
        self.booth_name = booth_name
        self.booth_number = booth_number
        self.location = location

        self.add_domain_event(
            PollingBoothCreated(
                booth_id=id,
                constituency_id=constituency_id,
                booth_number=booth_number,
            )
        )
