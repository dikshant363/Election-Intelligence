"""Pure Domain Service Interfaces."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.core.result import Result
from app.domain.candidate import Candidate
from app.domain.constituency import Constituency
from app.domain.election import Election, ElectionType
from app.domain.polling import PollingBooth
from app.domain.results import ElectionResult
from app.domain.value_objects import (
    CandidateId,
    ElectionDate,
    Percentage,
)


class ElectionService(ABC):
    """Domain service interface for Election orchestrations."""

    @abstractmethod
    async def initialize_election(
        self,
        title: str,
        election_type: ElectionType,
        election_date: ElectionDate,
    ) -> Result[Election]:
        """Initialize a new election aggregate."""
        pass


class ResultCalculationService(ABC):
    """Domain service interface for computing election outcomes and vote shares."""

    @abstractmethod
    async def calculate_winner(
        self,
        result: ElectionResult,
    ) -> Result[CandidateId | None]:
        """Determine the winning candidate based on vote counts."""
        pass

    @abstractmethod
    async def compute_vote_shares(
        self,
        result: ElectionResult,
    ) -> Result[dict[CandidateId, Percentage]]:
        """Calculate vote share percentage for each candidate."""
        pass


class CandidateValidationService(ABC):
    """Domain service interface for candidate nomination verification."""

    @abstractmethod
    async def validate_candidate_registration(
        self,
        candidate: Candidate,
    ) -> Result[bool]:
        """Validate candidate eligibility and nomination criteria."""
        pass


class ConstituencyService(ABC):
    """Domain service interface for constituency and polling booth mappings."""

    @abstractmethod
    async def map_polling_booths(
        self,
        constituency: Constituency,
        booths: Sequence[PollingBooth],
    ) -> Result[bool]:
        """Validate and associate polling booths with a constituency."""
        pass
