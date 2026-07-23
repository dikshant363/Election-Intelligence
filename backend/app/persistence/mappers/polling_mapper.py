"""Bidirectional mapper for PollingBooth aggregate and ORM model."""

import uuid

from app.domain.polling import PollingBooth
from app.domain.value_objects import (
    ConstituencyId,
    GeoCoordinates,
    PollingBoothId,
)
from app.persistence.models.polling import PollingBoothModel


class PollingMapper:
    """Mapper translating between PollingBooth aggregate root and PollingBoothModel."""

    @staticmethod
    def to_domain(model: PollingBoothModel) -> PollingBooth:
        """Convert PollingBoothModel ORM instance to PollingBooth domain aggregate."""
        return PollingBooth(
            id=PollingBoothId(value=model.id),
            constituency_id=ConstituencyId(value=model.constituency_id),
            booth_name=model.booth_name,
            booth_number=model.booth_number,
            location=GeoCoordinates(
                latitude=model.latitude,
                longitude=model.longitude,
            ),
        )

    @staticmethod
    def to_orm(entity: PollingBooth) -> PollingBoothModel:
        """Convert PollingBooth domain aggregate to PollingBoothModel ORM instance."""
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        con_id = (
            uuid.UUID(str(entity.constituency_id.value))
            if isinstance(entity.constituency_id.value, str)
            else entity.constituency_id.value
        )
        return PollingBoothModel(
            id=raw_id,
            constituency_id=con_id,
            booth_name=entity.booth_name,
            booth_number=entity.booth_number,
            latitude=entity.location.latitude,
            longitude=entity.location.longitude,
        )
