"""Bidirectional mapper for PoliticalParty aggregate and ORM model."""

import uuid

from app.domain.party import PoliticalParty
from app.domain.value_objects import PartyId
from app.persistence.models.party import PoliticalPartyModel


class PartyMapper:
    """Mapper translating between PoliticalParty aggregate root and PoliticalPartyModel."""

    @staticmethod
    def to_domain(model: PoliticalPartyModel) -> PoliticalParty:
        """Convert PoliticalPartyModel ORM instance to PoliticalParty domain aggregate."""
        return PoliticalParty(
            id=PartyId(value=model.id),
            name=model.name,
            code=model.code,
            symbol=model.symbol,
        )

    @staticmethod
    def to_orm(entity: PoliticalParty) -> PoliticalPartyModel:
        """Convert PoliticalParty domain aggregate to PoliticalPartyModel ORM instance."""
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        return PoliticalPartyModel(
            id=raw_id,
            name=entity.name,
            code=entity.code,
            symbol=entity.symbol,
        )
