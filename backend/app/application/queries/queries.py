"""Pure application query objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GetElection:
    """Query to fetch a single election by ID."""

    id: str


@dataclass(frozen=True)
class ListElections:
    """Query to list elections with optional status filter and pagination."""

    status: str | None = None
    skip: int = 0
    limit: int = 100


@dataclass(frozen=True)
class GetCandidate:
    """Query to fetch a single candidate by ID."""

    id: str


@dataclass(frozen=True)
class ListCandidates:
    """Query to list candidates with optional filters and pagination."""

    constituency_id: str | None = None
    party_id: str | None = None
    skip: int = 0
    limit: int = 100


@dataclass(frozen=True)
class GetParty:
    """Query to fetch a political party by ID or code."""

    id: str | None = None
    code: str | None = None


@dataclass(frozen=True)
class ListParties:
    """Query to list political parties with pagination."""

    skip: int = 0
    limit: int = 100


@dataclass(frozen=True)
class GetConstituency:
    """Query to fetch a constituency by ID or code."""

    id: str | None = None
    code: str | None = None


@dataclass(frozen=True)
class ListConstituencies:
    """Query to list constituencies with pagination."""

    state_code: str | None = None
    skip: int = 0
    limit: int = 100



@dataclass(frozen=True)
class GetResult:
    """Query to fetch election results for an election and constituency."""

    election_id: str
    constituency_id: str
