"""SqlAlchemy implementation of PollingBoothRepository contract."""

import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.polling import PollingBooth, PollingBoothRepository
from app.domain.value_objects import ConstituencyId, PollingBoothId
from app.persistence.mappers.polling_mapper import PollingMapper
from app.persistence.models.polling import PollingBoothModel


def _to_uuid(entity_id: Any) -> uuid.UUID:
    raw = entity_id.value if hasattr(entity_id, "value") else entity_id
    return uuid.UUID(str(raw)) if isinstance(raw, str) else raw


class SqlAlchemyPollingRepository(PollingBoothRepository):
    """SQLAlchemy 2.x async repository implementation for PollingBooth aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: PollingBoothId) -> PollingBooth | None:
        raw_id = _to_uuid(entity_id)
        stmt = select(PollingBoothModel).where(PollingBoothModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return PollingMapper.to_domain(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> Sequence[PollingBooth]:
        stmt = select(PollingBoothModel).offset(skip).limit(limit)
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [PollingMapper.to_domain(m) for m in models]

    async def count(self) -> int:
        stmt = select(func.count(PollingBoothModel.id))
        res = await self._session.execute(stmt)
        return res.scalar_one() or 0

    async def exists(self, entity_id: PollingBoothId) -> bool:
        raw_id = _to_uuid(entity_id)
        stmt = select(func.count(PollingBoothModel.id)).where(
            PollingBoothModel.id == raw_id
        )
        res = await self._session.execute(stmt)
        return (res.scalar_one() or 0) > 0

    async def add(self, entity: PollingBooth) -> PollingBooth:
        model = PollingMapper.to_orm(entity)
        self._session.add(model)
        await self._session.flush()
        return PollingMapper.to_domain(model)

    async def update(self, entity: PollingBooth) -> PollingBooth:
        raw_id = _to_uuid(entity.id)
        stmt = select(PollingBoothModel).where(PollingBoothModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one()
        model.booth_name = entity.booth_name
        model.booth_number = entity.booth_number
        model.latitude = entity.location.latitude
        model.longitude = entity.location.longitude
        model.constituency_id = _to_uuid(entity.constituency_id)
        await self._session.flush()
        return PollingMapper.to_domain(model)

    async def delete(self, entity: PollingBooth) -> None:
        raw_id = _to_uuid(entity.id)
        stmt = select(PollingBoothModel).where(PollingBoothModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def delete_by_id(self, entity_id: PollingBoothId) -> bool:
        raw_id = _to_uuid(entity_id)
        stmt = select(PollingBoothModel).where(PollingBoothModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def find_by_constituency(
        self, constituency_id: ConstituencyId
    ) -> Sequence[PollingBooth]:
        raw_con_id = _to_uuid(constituency_id)
        stmt = select(PollingBoothModel).where(
            PollingBoothModel.constituency_id == raw_con_id
        )
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [PollingMapper.to_domain(m) for m in models]
