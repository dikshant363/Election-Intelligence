"""Political Party Data Transfer Object (DTO)."""

from dataclasses import dataclass

from app.domain.party import PoliticalParty


@dataclass(frozen=True)
class PartyDTO:
    """Immutable DTO for PoliticalParty aggregate root."""

    id: str
    name: str
    code: str
    symbol: str

    @classmethod
    def from_domain(cls, entity: PoliticalParty) -> "PartyDTO":
        """Factory creating PartyDTO from PoliticalParty domain aggregate."""
        return cls(
            id=str(entity.id.value),
            name=entity.name,
            code=entity.code,
            symbol=entity.symbol,
        )
