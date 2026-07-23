"""Election aggregate root and domain events."""

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from app.domain.common.base import AggregateRoot
from app.domain.value_objects import ElectionDate, ElectionId, ElectionType


class ElectionStatus(StrEnum):
    """Lifecycle states of an election."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True, kw_only=True)
class ElectionCreated:
    """Event emitted when a new election is scheduled/created."""

    election_id: ElectionId
    title: str
    election_type: ElectionType
    occurred_at: datetime = datetime.now(UTC)


class Election(AggregateRoot[ElectionId]):
    """Election aggregate root representing an electoral contest event."""

    def __init__(
        self,
        id: ElectionId,
        title: str,
        election_type: ElectionType,
        election_date: ElectionDate,
        status: ElectionStatus = ElectionStatus.DRAFT,
    ) -> None:
        super().__init__(id)
        if not title or not title.strip():
            raise ValueError("Election title cannot be empty.")

        self.title = title
        self.election_type = election_type
        self.election_date = election_date
        self.status = status

        self.add_domain_event(
            ElectionCreated(
                election_id=id,
                title=title,
                election_type=election_type,
            )
        )

    def start_election(self) -> None:
        """Transition election to ACTIVE status."""
        if self.status != ElectionStatus.DRAFT:
            raise ValueError(f"Cannot start election in status: {self.status}")
        self.status = ElectionStatus.ACTIVE

    def complete_election(self) -> None:
        """Transition election to COMPLETED status."""
        if self.status != ElectionStatus.ACTIVE:
            raise ValueError(f"Cannot complete election in status: {self.status}")
        self.status = ElectionStatus.COMPLETED

    def cancel_election(self) -> None:
        """Cancel the election."""
        if self.status == ElectionStatus.COMPLETED:
            raise ValueError("Cannot cancel a completed election.")
        self.status = ElectionStatus.CANCELLED
