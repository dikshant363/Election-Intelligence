"""Candidate aggregate root and domain events."""

from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.common.base import AggregateRoot
from app.domain.value_objects import (
    Age,
    CandidateId,
    ConstituencyId,
    Email,
    PartyId,
    PhoneNumber,
)


@dataclass(frozen=True, kw_only=True)
class CandidateRegistered:
    """Event emitted when a candidate registers for an election."""

    candidate_id: CandidateId
    name: str
    constituency_id: ConstituencyId
    party_id: PartyId | None
    occurred_at: datetime = datetime.now(UTC)


class Candidate(AggregateRoot[CandidateId]):
    """Candidate aggregate root representing a nominated candidate."""

    def __init__(  # noqa: PLR0913
        self,
        id: CandidateId,
        name: str,
        age: Age,
        email: Email,
        phone: PhoneNumber,
        constituency_id: ConstituencyId,
        party_id: PartyId | None = None,
    ) -> None:
        super().__init__(id)
        if not name or not name.strip():
            raise ValueError("Candidate name cannot be empty.")

        self.name = name
        self.age = age
        self.email = email
        self.phone = phone
        self.constituency_id = constituency_id
        self.party_id = party_id

        self.add_domain_event(
            CandidateRegistered(
                candidate_id=id,
                name=name,
                constituency_id=constituency_id,
                party_id=party_id,
            )
        )

    def assign_party(self, party_id: PartyId) -> None:
        """Assign or change the candidate's political party affiliation."""
        self.party_id = party_id

    def update_contact(self, email: Email, phone: PhoneNumber) -> None:
        """Update candidate contact information."""
        self.email = email
        self.phone = phone
