"""Pydantic v2 schemas for Polling Booth API requests and responses."""

from pydantic import BaseModel, Field

from app.application.dto import PollingBoothDTO


class PollingBoothCreateRequest(BaseModel):
    """Payload for establishing a new polling booth."""

    constituency_id: str = Field(..., example="3b934268-dcaf-4269-8833-a9fbb1b82d0b")
    booth_name: str = Field(..., min_length=2, max_length=150, example="Central High School Station A")
    booth_number: str = Field(..., min_length=1, max_length=20, example="PB-12")
    latitude: float = Field(..., ge=-90.0, le=90.0, example=28.6139)
    longitude: float = Field(..., ge=-180.0, le=180.0, example=77.2090)


class PollingBoothResponse(BaseModel):
    """Public API response representation of a Polling Booth."""

    id: str
    constituency_id: str
    booth_name: str
    booth_number: str
    latitude: float
    longitude: float

    @classmethod
    def from_dto(cls, dto: PollingBoothDTO) -> "PollingBoothResponse":
        """Factory transforming Application DTO to API Response schema."""
        return cls(
            id=dto.id,
            constituency_id=dto.constituency_id,
            booth_name=dto.booth_name,
            booth_number=dto.booth_number,
            latitude=dto.latitude,
            longitude=dto.longitude,
        )
