"""Pydantic v2 schemas for Constituency API requests and responses."""

from pydantic import BaseModel, Field

from app.application.dto import ConstituencyDTO


class ConstituencyCreateRequest(BaseModel):
    """Payload for creating a new electoral constituency."""

    name: str = Field(..., min_length=2, max_length=150, example="North Delhi")
    code: str = Field(..., min_length=2, max_length=20, example="ND-01")
    state_code: str = Field(..., example="IN-DL")
    constituency_type: str = Field(default="ASSEMBLY", example="ASSEMBLY")


class ConstituencyResponse(BaseModel):
    """Public API response representation of a Constituency."""

    id: str
    name: str
    code: str
    state_code: str
    constituency_type: str

    @classmethod
    def from_dto(cls, dto: ConstituencyDTO) -> "ConstituencyResponse":
        """Factory transforming Application DTO to API Response schema."""
        return cls(
            id=dto.id,
            name=dto.name,
            code=dto.code,
            state_code=dto.state_code,
            constituency_type=dto.constituency_type,
        )
