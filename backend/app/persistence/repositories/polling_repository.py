"""SqlAlchemy implementation of PollingBoothRepository contract."""

import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.polling import PollingBooth, PollingBoothRepository
from app.domain.value_objects import ConstituencyId, PollingBoothId
from app.persistence.mappers.polling_mapper import PollingMapper
from app.persistence.models.polling import PollingBoothModel


class SqlAlchemyPollingRepository(PollingBoothRepository):
    """SQLAlchemy 2.x async repository implementation for PollingBooth aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: PollingBoothId) -> PollingBooth | None:
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
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
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
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
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        stmt = select(PollingBoothModel).where(PollingBoothModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one()
        model.booth_name = entity.booth_name
        model.booth_number = entity.booth_number
        model.latitude = entity.location.latitude
        model.longitude = entity.location.longitude
        model.constituency_id = (
            uuid.UUID(str(entity.constituency_id.value))
            if isinstance(entity.constituency_id.value, str)
            else entity.constituency_id.value
        )
        await self._session.flush()
        return PollingMapper.to_domain(model)

    async def delete(self, entity: PollingBooth) -> None:
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        stmt = select(PollingBoothModel).where(PollingBoothModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def delete_by_id(self, entity_id: PollingBoothId) -> bool:
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
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
        raw_con_id = (
            uuid.UUID(str(constituency_id.value))
            if isinstance(constituency_id.value, str)
            else constituency_id.value
        )
        stmt = select(PollingBoothModel).where(
            PollingBoothModel.constituency_id == raw_con_id
        )
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [PollingMapper.to_domain(m) for m in models]
