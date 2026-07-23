"""Candidate application command objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterCandidate:
    """Command to register a nominated candidate."""

    name: str
    age: int
    email: str
    phone: str
    constituency_id: str
    party_id: str | None = None
