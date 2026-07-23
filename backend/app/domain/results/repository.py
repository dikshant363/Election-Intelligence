"""Election result repository contract."""

from abc import ABC, abstractmethod

from app.core.repositories import Repository
from app.domain.results.results import ElectionResult
from app.domain.value_objects import ConstituencyId, ElectionId


class ResultRepository(Repository[ElectionResult, str], ABC):
    """Domain repository contract for ElectionResult aggregate root."""

    @abstractmethod
    async def find_by_election_and_constituency(
        self,
        election_id: ElectionId,
        constituency_id: ConstituencyId,
    ) -> ElectionResult | None:
        """Find election result record for a specific election and constituency."""
        pass
