"""Constituency repository contract."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.core.repositories import Repository
from app.domain.constituency.constituency import Constituency
from app.domain.value_objects import ConstituencyId, StateCode


class ConstituencyRepository(Repository[Constituency, ConstituencyId], ABC):
    """Domain repository contract for Constituency aggregate root."""

    @abstractmethod
    async def find_by_state(
        self,
        state_code: StateCode,
    ) -> Sequence[Constituency]:
        """Find constituencies within a specific state/territory."""
        pass

    @abstractmethod
    async def find_by_code(self, code: str) -> Constituency | None:
        """Find a constituency by its unique electoral code."""
        pass
