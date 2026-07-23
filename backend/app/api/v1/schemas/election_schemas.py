"""Pydantic v2 schemas for Election API requests and responses."""

from datetime import date

from pydantic import BaseModel, Field

from app.application.dto import ElectionDTO


class ElectionCreateRequest(BaseModel):
    """Payload for scheduling/creating an election."""

    title: str = Field(..., min_length=3, max_length=200, example="General Election 2026")
    election_type: str = Field(..., example="GENERAL")
    start_date: date = Field(..., example="2026-05-01")
    end_date: date = Field(..., example="2026-05-15")


class ElectionResponse(BaseModel):
    """Public API response representation of an Election."""

    id: str
    title: str
    election_type: str
    start_date: date
    end_date: date
    status: str

    @classmethod
    def from_dto(cls, dto: ElectionDTO) -> "ElectionResponse":
        """Factory transforming Application DTO to API Response schema."""
        return cls(
            id=dto.id,
            title=dto.title,
            election_type=dto.election_type,
            start_date=dto.start_date,
            end_date=dto.end_date,
            status=dto.status,
        )
