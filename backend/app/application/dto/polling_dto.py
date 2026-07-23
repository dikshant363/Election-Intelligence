"""Polling Booth Data Transfer Object (DTO)."""

from dataclasses import dataclass

from app.domain.polling import PollingBooth


@dataclass(frozen=True)
class PollingBoothDTO:
    """Immutable DTO for PollingBooth aggregate root."""

    id: str
    constituency_id: str
    booth_name: str
    booth_number: str
    latitude: float
    longitude: float

    @classmethod
    def from_domain(cls, entity: PollingBooth) -> "PollingBoothDTO":
        """Factory creating PollingBoothDTO from PollingBooth domain aggregate."""
        return cls(
            id=str(entity.id.value),
            constituency_id=str(entity.constituency_id.value),
            booth_name=entity.booth_name,
            booth_number=entity.booth_number,
            latitude=entity.location.latitude,
            longitude=entity.location.longitude,
        )
