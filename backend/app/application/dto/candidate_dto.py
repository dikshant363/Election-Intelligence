"""Candidate Data Transfer Object (DTO)."""

from dataclasses import dataclass

from app.domain.candidate import Candidate


@dataclass(frozen=True)
class CandidateDTO:
    """Immutable DTO for Candidate aggregate root."""

    id: str
    name: str
    age: int
    email: str
    phone: str
    constituency_id: str
    party_id: str | None

    @classmethod
    def from_domain(cls, entity: Candidate) -> "CandidateDTO":
        """Factory creating CandidateDTO from Candidate domain aggregate."""
        party_id_str = (
            str(entity.party_id.value) if entity.party_id else None
        )
        return cls(
            id=str(entity.id.value),
            name=entity.name,
            age=entity.age.years,
            email=entity.email.address,
            phone=entity.phone.number,
            constituency_id=str(entity.constituency_id.value),
            party_id=party_id_str,
        )
