"""Candidate repository contract."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.core.repositories import Repository
from app.domain.candidate.candidate import Candidate
from app.domain.value_objects import CandidateId, ConstituencyId, PartyId


class CandidateRepository(Repository[Candidate, CandidateId], ABC):
    """Domain repository contract for Candidate aggregate root."""

    @abstractmethod
    async def find_by_constituency(
        self,
        constituency_id: ConstituencyId,
    ) -> Sequence[Candidate]:
        """Find candidates contesting in a specific constituency."""
        pass

    @abstractmethod
    async def find_by_party(self, party_id: PartyId) -> Sequence[Candidate]:
        """Find candidates affiliated with a specific political party."""
        pass
