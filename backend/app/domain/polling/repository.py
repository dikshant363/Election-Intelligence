"""Polling booth repository contract."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.core.repositories import Repository
from app.domain.polling.polling import PollingBooth
from app.domain.value_objects import ConstituencyId, PollingBoothId


class PollingBoothRepository(Repository[PollingBooth, PollingBoothId], ABC):
    """Domain repository contract for PollingBooth aggregate root."""

    @abstractmethod
    async def find_by_constituency(
        self,
        constituency_id: ConstituencyId,
    ) -> Sequence[PollingBooth]:
        """Find all polling booths assigned to a specific constituency."""
        pass
