"""Election Result application command objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeclareResult:
    """Command to tally votes and declare constituency election result."""

    election_id: str
    constituency_id: str
    candidate_votes: dict[str, int]
    winning_candidate_id: str | None = None
