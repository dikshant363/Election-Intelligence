"""Domain Specification Pattern implementations."""

from abc import ABC, abstractmethod

from app.domain.candidate import Candidate
from app.domain.constituency import Constituency
from app.domain.election import Election, ElectionStatus
from app.domain.party import PoliticalParty
from app.domain.value_objects import MAX_PERCENTAGE, Percentage

DEFAULT_MIN_CANDIDATE_AGE = 25


class Specification[T](ABC):
    """Abstract specification contract."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate entity satisfies the specification criteria."""
        pass


class CandidateEligibility(Specification[Candidate]):
    """Specification enforcing minimum age requirement for candidates."""

    def __init__(self, min_age_years: int = DEFAULT_MIN_CANDIDATE_AGE) -> None:
        self.min_age_years = min_age_years

    def is_satisfied_by(self, candidate: Candidate) -> bool:
        """Return True if candidate age meets or exceeds minimum requirement."""
        return candidate.age.years >= self.min_age_years


class ElectionOpen(Specification[Election]):
    """Specification checking if an election is currently open for voting."""

    def is_satisfied_by(self, candidate: Election) -> bool:
        """Return True if election status is ACTIVE."""
        return candidate.status == ElectionStatus.ACTIVE


class ValidVotePercentage(Specification[Percentage]):
    """Specification validating percentage boundary rules."""

    def is_satisfied_by(self, candidate: Percentage) -> bool:
        """Return True if percentage value is between 0.0 and 100.0 inclusive."""
        return 0.0 <= candidate.value <= MAX_PERCENTAGE


class UniquePartySymbol(Specification[PoliticalParty]):
    """Specification validating political party symbol rules."""

    def is_satisfied_by(self, candidate: PoliticalParty) -> bool:
        """Return True if political party symbol is valid."""
        return bool(candidate.symbol and candidate.symbol.strip())


class ValidConstituency(Specification[Constituency]):
    """Specification validating constituency structural integrity."""

    def is_satisfied_by(self, candidate: Constituency) -> bool:
        """Return True if constituency attributes are valid."""
        return bool(candidate.name and candidate.code and candidate.state_code)
