"""Political party aggregate root and domain events."""

from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.common.base import AggregateRoot
from app.domain.value_objects import PartyId


@dataclass(frozen=True, kw_only=True)
class PartyRegistered:
    """Event emitted when a political party is registered."""

    party_id: PartyId
    name: str
    code: str
    occurred_at: datetime = datetime.now(UTC)


class PoliticalParty(AggregateRoot[PartyId]):
    """Political party aggregate root."""

    def __init__(
        self,
        id: PartyId,
        name: str,
        code: str,
        symbol: str,
    ) -> None:
        super().__init__(id)
        if not name or not name.strip():
            raise ValueError("Party name cannot be empty.")
        if not code or not code.strip():
            raise ValueError("Party code cannot be empty.")
        if not symbol or not symbol.strip():
            raise ValueError("Party symbol cannot be empty.")

        self.name = name
        self.code = code
        self.symbol = symbol

        self.add_domain_event(
            PartyRegistered(
                party_id=id,
                name=name,
                code=code,
            )
        )

    def update_symbol(self, new_symbol: str) -> None:
        """Update the registered party symbol."""
        if not new_symbol or not new_symbol.strip():
            raise ValueError("Party symbol cannot be empty.")
        self.symbol = new_symbol
