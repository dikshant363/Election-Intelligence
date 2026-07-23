"""Pydantic v2 schemas for Candidate API requests and responses."""

from pydantic import BaseModel, Field

from app.application.dto import CandidateDTO


class CandidateCreateRequest(BaseModel):
    """Payload for registering a candidate."""

    name: str = Field(..., min_length=2, max_length=150, example="Anand Kumar")
    age: int = Field(..., ge=25, le=120, example=35)
    email: str = Field(
        ...,
        pattern=r"^[^@]+@[^@]+\.[^@]+$",
        example="anand@pfr.org",
    )
    phone: str = Field(..., min_length=10, max_length=15, example="+919876543210")
    constituency_id: str = Field(..., example="3b934268-dcaf-4269-8833-a9fbb1b82d0b")
    party_id: str | None = Field(default=None, example="8a123456-dcaf-4269-8833-a9fbb1b82d0b")


class CandidateResponse(BaseModel):
    """Public API response representation of a Candidate."""

    id: str
    name: str
    age: int
    email: str
    phone: str
    constituency_id: str
    party_id: str | None

    @classmethod
    def from_dto(cls, dto: CandidateDTO) -> "CandidateResponse":
        """Factory transforming Application DTO to API Response schema."""
        return cls(
            id=dto.id,
            name=dto.name,
            age=dto.age,
            email=dto.email,
            phone=dto.phone,
            constituency_id=dto.constituency_id,
            party_id=dto.party_id,
        )
