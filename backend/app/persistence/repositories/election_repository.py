"""SqlAlchemy implementation of ElectionRepository contract."""

import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.election import Election, ElectionRepository, ElectionStatus
from app.domain.value_objects import ElectionId
from app.persistence.mappers.election_mapper import ElectionMapper
from app.persistence.models.election import ElectionModel


def _to_uuid(entity_id: Any) -> uuid.UUID:
    raw = entity_id.value if hasattr(entity_id, "value") else entity_id
    return uuid.UUID(str(raw)) if isinstance(raw, str) else raw


class SqlAlchemyElectionRepository(ElectionRepository):
    """SQLAlchemy 2.x async repository implementation for Election aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: ElectionId) -> Election | None:
        raw_id = _to_uuid(entity_id)
        stmt = select(ElectionModel).where(ElectionModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return ElectionMapper.to_domain(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> Sequence[Election]:
        stmt = select(ElectionModel).offset(skip).limit(limit)
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [ElectionMapper.to_domain(m) for m in models]

    async def count(self) -> int:
        stmt = select(func.count(ElectionModel.id))
        res = await self._session.execute(stmt)
        return res.scalar_one() or 0

    async def exists(self, entity_id: ElectionId) -> bool:
        raw_id = _to_uuid(entity_id)
        stmt = select(func.count(ElectionModel.id)).where(
            ElectionModel.id == raw_id
        )
        res = await self._session.execute(stmt)
        return (res.scalar_one() or 0) > 0

    async def add(self, entity: Election) -> Election:
        model = ElectionMapper.to_orm(entity)
        self._session.add(model)
        await self._session.flush()
        return ElectionMapper.to_domain(model)

    async def update(self, entity: Election) -> Election:
        raw_id = _to_uuid(entity.id)
        stmt = select(ElectionModel).where(ElectionModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one()
        model.title = entity.title
        model.election_type = entity.election_type.value
        model.start_date = entity.election_date.start_date
        model.end_date = entity.election_date.end_date
        model.status = entity.status.value
        await self._session.flush()
        return ElectionMapper.to_domain(model)

    async def delete(self, entity: Election) -> None:
        raw_id = _to_uuid(entity.id)
        stmt = select(ElectionModel).where(ElectionModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def delete_by_id(self, entity_id: ElectionId) -> bool:
        raw_id = _to_uuid(entity_id)
        stmt = select(ElectionModel).where(ElectionModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def find_by_status(self, status: ElectionStatus) -> Sequence[Election]:
        stmt = select(ElectionModel).where(ElectionModel.status == status.value)
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [ElectionMapper.to_domain(m) for m in models]
