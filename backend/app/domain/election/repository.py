"""Election repository contract."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.core.repositories import Repository
from app.domain.election.election import Election, ElectionStatus
from app.domain.value_objects import ElectionId


class ElectionRepository(Repository[Election, ElectionId], ABC):
    """Domain repository contract for Election aggregate root."""

    @abstractmethod
    async def find_by_status(self, status: ElectionStatus) -> Sequence[Election]:
        """Find elections matching a specific status."""
        pass
