"""SqlAlchemy implementation of ConstituencyRepository contract."""

import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.constituency import Constituency, ConstituencyRepository
from app.domain.value_objects import ConstituencyId, StateCode
from app.persistence.mappers.constituency_mapper import ConstituencyMapper
from app.persistence.models.constituency import ConstituencyModel


def _to_uuid(entity_id: Any) -> uuid.UUID:
    raw = entity_id.value if hasattr(entity_id, "value") else entity_id
    return uuid.UUID(str(raw)) if isinstance(raw, str) else raw


class SqlAlchemyConstituencyRepository(ConstituencyRepository):
    """SQLAlchemy 2.x async repository implementation for Constituency aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: ConstituencyId) -> Constituency | None:
        raw_id = _to_uuid(entity_id)
        stmt = select(ConstituencyModel).where(ConstituencyModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return ConstituencyMapper.to_domain(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> Sequence[Constituency]:
        stmt = select(ConstituencyModel).offset(skip).limit(limit)
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [ConstituencyMapper.to_domain(m) for m in models]

    async def count(self) -> int:
        stmt = select(func.count(ConstituencyModel.id))
        res = await self._session.execute(stmt)
        return res.scalar_one() or 0

    async def exists(self, entity_id: ConstituencyId) -> bool:
        raw_id = _to_uuid(entity_id)
        stmt = select(func.count(ConstituencyModel.id)).where(
            ConstituencyModel.id == raw_id
        )
        res = await self._session.execute(stmt)
        return (res.scalar_one() or 0) > 0

    async def add(self, entity: Constituency) -> Constituency:
        model = ConstituencyMapper.to_orm(entity)
        self._session.add(model)
        await self._session.flush()
        return ConstituencyMapper.to_domain(model)

    async def update(self, entity: Constituency) -> Constituency:
        raw_id = _to_uuid(entity.id)
        stmt = select(ConstituencyModel).where(ConstituencyModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one()
        model.name = entity.name
        model.code = entity.code
        model.state_code = entity.state_code.code
        model.constituency_type = entity.constituency_type
        await self._session.flush()
        return ConstituencyMapper.to_domain(model)

    async def delete(self, entity: Constituency) -> None:
        raw_id = _to_uuid(entity.id)
        stmt = select(ConstituencyModel).where(ConstituencyModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def delete_by_id(self, entity_id: ConstituencyId) -> bool:
        raw_id = _to_uuid(entity_id)
        stmt = select(ConstituencyModel).where(ConstituencyModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def find_by_state(self, state_code: StateCode) -> Sequence[Constituency]:
        stmt = select(ConstituencyModel).where(
            ConstituencyModel.state_code == state_code.code
        )
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [ConstituencyMapper.to_domain(m) for m in models]

    async def find_by_code(self, code: str) -> Constituency | None:
        stmt = select(ConstituencyModel).where(ConstituencyModel.code == code)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return ConstituencyMapper.to_domain(model) if model else None
