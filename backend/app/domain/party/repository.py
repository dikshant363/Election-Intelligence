"""Political party repository contract."""

from abc import ABC, abstractmethod

from app.core.repositories import Repository
from app.domain.party.party import PoliticalParty
from app.domain.value_objects import PartyId


class PartyRepository(Repository[PoliticalParty, PartyId], ABC):
    """Domain repository contract for PoliticalParty aggregate root."""

    @abstractmethod
    async def find_by_code(self, code: str) -> PoliticalParty | None:
        """Find a political party by its unique registration code."""
        pass
