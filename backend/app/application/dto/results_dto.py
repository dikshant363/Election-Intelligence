"""Election Result Data Transfer Object (DTO)."""

from dataclasses import dataclass

from app.domain.results import ElectionResult


@dataclass(frozen=True)
class ElectionResultDTO:
    """Immutable DTO for ElectionResult aggregate root."""

    result_key: str
    election_id: str
    constituency_id: str
    winning_candidate_id: str | None
    total_votes: int
    candidate_votes: dict[str, int]
    is_declared: bool

    @classmethod
    def from_domain(cls, entity: ElectionResult) -> "ElectionResultDTO":
        """Factory creating ElectionResultDTO from ElectionResult domain aggregate."""
        winner_id_str = (
            str(entity.winning_candidate_id.value)
            if entity.winning_candidate_id
            else None
        )
        votes_dict = {
            str(cand_id.value): count.count
            for cand_id, count in entity.candidate_votes.items()
        }
        return cls(
            result_key=str(entity.id),
            election_id=str(entity.election_id.value),
            constituency_id=str(entity.constituency_id.value),
            winning_candidate_id=winner_id_str,
            total_votes=entity.total_votes.count,
            candidate_votes=votes_dict,
            is_declared=entity.is_declared,
        )
