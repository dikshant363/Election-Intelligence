"""Polling Booth application command objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreatePollingBooth:
    """Command to establish a new polling booth station."""

    constituency_id: str
    booth_name: str
    booth_number: str
    latitude: float
    longitude: float
