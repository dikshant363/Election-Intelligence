"""Election result aggregate root and domain events."""

from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.common.base import AggregateRoot
from app.domain.value_objects import (
    CandidateId,
    ConstituencyId,
    ElectionId,
    VoteCount,
)


@dataclass(frozen=True, kw_only=True)
class ResultDeclared:
    """Event emitted when official election results are declared for a constituency."""

    election_id: ElectionId
    constituency_id: ConstituencyId
    winning_candidate_id: CandidateId | None
    total_votes: VoteCount
    occurred_at: datetime = datetime.now(UTC)


class ElectionResult(AggregateRoot[str]):
    """Election result aggregate root for a specific constituency in an election."""

    def __init__(
        self,
        election_id: ElectionId,
        constituency_id: ConstituencyId,
    ) -> None:
        result_key = f"{election_id}:{constituency_id}"
        super().__init__(result_key)
        self.election_id = election_id
        self.constituency_id = constituency_id
        self.candidate_votes: dict[CandidateId, VoteCount] = {}
        self.total_votes = VoteCount(count=0)
        self.winning_candidate_id: CandidateId | None = None
        self.is_declared = False

    def record_votes(self, candidate_id: CandidateId, votes: VoteCount) -> None:
        """Record or update vote tally for a candidate."""
        if self.is_declared:
            raise ValueError("Cannot modify vote tallies after results are declared.")

        old_votes = self.candidate_votes.get(candidate_id, VoteCount(count=0))
        self.candidate_votes[candidate_id] = votes

        # Recompute total votes
        current_total = self.total_votes.count - old_votes.count + votes.count
        self.total_votes = VoteCount(count=current_total)

    def declare_result(self, winning_candidate_id: CandidateId | None) -> None:
        """Declare official constituency result and emit ResultDeclared event."""
        if self.is_declared:
            raise ValueError("Election result is already declared.")

        self.winning_candidate_id = winning_candidate_id
        self.is_declared = True

        self.add_domain_event(
            ResultDeclared(
                election_id=self.election_id,
                constituency_id=self.constituency_id,
                winning_candidate_id=winning_candidate_id,
                total_votes=self.total_votes,
            )
        )
