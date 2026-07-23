"""Bidirectional mapper for Election aggregate and ORM model."""

import uuid

from app.domain.election import Election, ElectionStatus
from app.domain.value_objects import ElectionDate, ElectionId, ElectionType
from app.persistence.models.election import ElectionModel


class ElectionMapper:
    """Mapper translating between Election aggregate root and ElectionModel."""

    @staticmethod
    def to_domain(model: ElectionModel) -> Election:
        """Convert ElectionModel ORM instance to Election domain aggregate root."""
        return Election(
            id=ElectionId(value=model.id),
            title=model.title,
            election_type=ElectionType(model.election_type),
            election_date=ElectionDate(
                start_date=model.start_date,
                end_date=model.end_date,
            ),
            status=ElectionStatus(model.status),
        )

    @staticmethod
    def to_orm(entity: Election) -> ElectionModel:
        """Convert Election domain aggregate root to ElectionModel ORM instance."""
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        return ElectionModel(
            id=raw_id,
            title=entity.title,
            election_type=entity.election_type.value,
            start_date=entity.election_date.start_date,
            end_date=entity.election_date.end_date,
            status=entity.status.value,
        )
