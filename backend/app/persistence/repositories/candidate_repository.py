"""SqlAlchemy implementation of CandidateRepository contract."""

import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.candidate import Candidate, CandidateRepository
from app.domain.value_objects import CandidateId, ConstituencyId, PartyId
from app.persistence.mappers.candidate_mapper import CandidateMapper
from app.persistence.models.candidate import CandidateModel


def _to_uuid(entity_id: Any) -> uuid.UUID:
    raw = entity_id.value if hasattr(entity_id, "value") else entity_id
    return uuid.UUID(str(raw)) if isinstance(raw, str) else raw


class SqlAlchemyCandidateRepository(CandidateRepository):
    """SQLAlchemy 2.x async repository implementation for Candidate aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: CandidateId) -> Candidate | None:
        raw_id = _to_uuid(entity_id)
        stmt = select(CandidateModel).where(CandidateModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return CandidateMapper.to_domain(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> Sequence[Candidate]:
        stmt = select(CandidateModel).offset(skip).limit(limit)
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [CandidateMapper.to_domain(m) for m in models]

    async def count(self) -> int:
        stmt = select(func.count(CandidateModel.id))
        res = await self._session.execute(stmt)
        return res.scalar_one() or 0

    async def exists(self, entity_id: CandidateId) -> bool:
        raw_id = _to_uuid(entity_id)
        stmt = select(func.count(CandidateModel.id)).where(
            CandidateModel.id == raw_id
        )
        res = await self._session.execute(stmt)
        return (res.scalar_one() or 0) > 0

    async def add(self, entity: Candidate) -> Candidate:
        model = CandidateMapper.to_orm(entity)
        self._session.add(model)
        await self._session.flush()
        return CandidateMapper.to_domain(model)

    async def update(self, entity: Candidate) -> Candidate:
        raw_id = _to_uuid(entity.id)
        stmt = select(CandidateModel).where(CandidateModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one()
        model.name = entity.name
        model.age = entity.age.years
        model.email = entity.email.address
        model.phone = entity.phone.number
        model.constituency_id = _to_uuid(entity.constituency_id)
        model.party_id = (
            _to_uuid(entity.party_id) if entity.party_id else None
        )
        await self._session.flush()
        return CandidateMapper.to_domain(model)

    async def delete(self, entity: Candidate) -> None:
        raw_id = _to_uuid(entity.id)
        stmt = select(CandidateModel).where(CandidateModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def delete_by_id(self, entity_id: CandidateId) -> bool:
        raw_id = _to_uuid(entity_id)
        stmt = select(CandidateModel).where(CandidateModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def find_by_constituency(
        self, constituency_id: ConstituencyId
    ) -> Sequence[Candidate]:
        raw_con_id = _to_uuid(constituency_id)
        stmt = select(CandidateModel).where(
            CandidateModel.constituency_id == raw_con_id
        )
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [CandidateMapper.to_domain(m) for m in models]

    async def find_by_party(self, party_id: PartyId) -> Sequence[Candidate]:
        raw_party_id = _to_uuid(party_id)
        stmt = select(CandidateModel).where(
            CandidateModel.party_id == raw_party_id
        )
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [CandidateMapper.to_domain(m) for m in models]
