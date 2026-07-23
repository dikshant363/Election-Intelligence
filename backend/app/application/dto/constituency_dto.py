"""Constituency Data Transfer Object (DTO)."""

from dataclasses import dataclass

from app.domain.constituency import Constituency


@dataclass(frozen=True)
class ConstituencyDTO:
    """Immutable DTO for Constituency aggregate root."""

    id: str
    name: str
    code: str
    state_code: str
    constituency_type: str

    @classmethod
    def from_domain(cls, entity: Constituency) -> "ConstituencyDTO":
        """Factory creating ConstituencyDTO from Constituency domain aggregate."""
        return cls(
            id=str(entity.id.value),
            name=entity.name,
            code=entity.code,
            state_code=entity.state_code.code,
            constituency_type=entity.constituency_type,
        )
