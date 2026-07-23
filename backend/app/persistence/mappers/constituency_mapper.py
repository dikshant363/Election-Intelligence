"""Bidirectional mapper for Constituency aggregate and ORM model."""

import uuid

from app.domain.constituency import Constituency
from app.domain.value_objects import ConstituencyId, StateCode
from app.persistence.models.constituency import ConstituencyModel


class ConstituencyMapper:
    """Mapper translating between Constituency aggregate root and ConstituencyModel."""

    @staticmethod
    def to_domain(model: ConstituencyModel) -> Constituency:
        """Convert ConstituencyModel ORM instance to Constituency domain aggregate."""
        return Constituency(
            id=ConstituencyId(value=model.id),
            name=model.name,
            code=model.code,
            state_code=StateCode(code=model.state_code),
            constituency_type=model.constituency_type,
        )

    @staticmethod
    def to_orm(entity: Constituency) -> ConstituencyModel:
        """Convert Constituency domain aggregate to ConstituencyModel ORM instance."""
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        return ConstituencyModel(
            id=raw_id,
            name=entity.name,
            code=entity.code,
            state_code=entity.state_code.code,
            constituency_type=entity.constituency_type,
        )
