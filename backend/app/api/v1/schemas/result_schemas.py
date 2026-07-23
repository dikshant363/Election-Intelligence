"""Pydantic v2 schemas for Election Result API requests and responses."""

from pydantic import BaseModel, Field

from app.application.dto import ElectionResultDTO


class ElectionResultRequest(BaseModel):
    """Payload for tallying votes and declaring election result."""

    election_id: str = Field(..., example="3b934268-dcaf-4269-8833-a9fbb1b82d0b")
    constituency_id: str = Field(..., example="7c934268-dcaf-4269-8833-a9fbb1b82d0c")
    candidate_votes: dict[str, int] = Field(..., example={"candidate-uuid-1": 12500, "candidate-uuid-2": 9400})
    winning_candidate_id: str | None = Field(default=None, example="candidate-uuid-1")


class ElectionResultResponse(BaseModel):
    """Public API response representation of an Election Result."""

    result_key: str
    election_id: str
    constituency_id: str
    winning_candidate_id: str | None
    total_votes: int
    candidate_votes: dict[str, int]
    is_declared: bool

    @classmethod
    def from_dto(cls, dto: ElectionResultDTO) -> "ElectionResultResponse":
        """Factory transforming Application DTO to API Response schema."""
        return cls(
            result_key=dto.result_key,
            election_id=dto.election_id,
            constituency_id=dto.constituency_id,
            winning_candidate_id=dto.winning_candidate_id,
            total_votes=dto.total_votes,
            candidate_votes=dto.candidate_votes,
            is_declared=dto.is_declared,
        )
