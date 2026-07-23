"""Election Data Transfer Object (DTO)."""

from dataclasses import dataclass
from datetime import date

from app.domain.election import Election


@dataclass(frozen=True)
class ElectionDTO:
    """Immutable DTO for Election aggregate root."""

    id: str
    title: str
    election_type: str
    start_date: date
    end_date: date
    status: str

    @classmethod
    def from_domain(cls, entity: Election) -> "ElectionDTO":
        """Factory creating ElectionDTO from Election domain aggregate."""
        return cls(
            id=str(entity.id.value),
            title=entity.title,
            election_type=entity.election_type.value,
            start_date=entity.election_date.start_date,
            end_date=entity.election_date.end_date,
            status=entity.status.value,
        )
