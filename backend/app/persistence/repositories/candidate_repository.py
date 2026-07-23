"""SqlAlchemy implementation of CandidateRepository contract."""

import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.candidate import Candidate, CandidateRepository
from app.domain.value_objects import CandidateId, ConstituencyId, PartyId
from app.persistence.mappers.candidate_mapper import CandidateMapper
from app.persistence.models.candidate import CandidateModel


class SqlAlchemyCandidateRepository(CandidateRepository):
    """SQLAlchemy 2.x async repository implementation for Candidate aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: CandidateId) -> Candidate | None:
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
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
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
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
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        stmt = select(CandidateModel).where(CandidateModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one()
        model.name = entity.name
        model.age = entity.age.years
        model.email = entity.email.address
        model.phone = entity.phone.number
        model.constituency_id = (
            uuid.UUID(str(entity.constituency_id.value))
            if isinstance(entity.constituency_id.value, str)
            else entity.constituency_id.value
        )
        model.party_id = (
            uuid.UUID(str(entity.party_id.value))
            if entity.party_id and isinstance(entity.party_id.value, str)
            else entity.party_id.value
            if entity.party_id
            else None
        )
        await self._session.flush()
        return CandidateMapper.to_domain(model)

    async def delete(self, entity: Candidate) -> None:
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        stmt = select(CandidateModel).where(CandidateModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def delete_by_id(self, entity_id: CandidateId) -> bool:
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
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
        raw_con_id = (
            uuid.UUID(str(constituency_id.value))
            if isinstance(constituency_id.value, str)
            else constituency_id.value
        )
        stmt = select(CandidateModel).where(
            CandidateModel.constituency_id == raw_con_id
        )
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [CandidateMapper.to_domain(m) for m in models]

    async def find_by_party(self, party_id: PartyId) -> Sequence[Candidate]:
        raw_party_id = (
            uuid.UUID(str(party_id.value))
            if isinstance(party_id.value, str)
            else party_id.value
        )
        stmt = select(CandidateModel).where(
            CandidateModel.party_id == raw_party_id
        )
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [CandidateMapper.to_domain(m) for m in models]
