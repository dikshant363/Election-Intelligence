"""Pydantic v2 schemas for Political Party API requests and responses."""

from pydantic import BaseModel, Field

from app.application.dto import PartyDTO


class PartyCreateRequest(BaseModel):
    """Payload for registering a new political party."""

    name: str = Field(..., min_length=2, max_length=150, example="Progressive Front")
    code: str = Field(..., min_length=2, max_length=10, example="PFR")
    symbol: str = Field(..., min_length=2, max_length=50, example="Rising Sun")


class PartyResponse(BaseModel):
    """Public API response representation of a Political Party."""

    id: str
    name: str
    code: str
    symbol: str

    @classmethod
    def from_dto(cls, dto: PartyDTO) -> "PartyResponse":
        """Factory transforming Application DTO to API Response schema."""
        return cls(
            id=dto.id,
            name=dto.name,
            code=dto.code,
            symbol=dto.symbol,
        )
