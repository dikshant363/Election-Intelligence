"""SqlAlchemy implementation of PartyRepository contract."""

import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.party import PartyRepository, PoliticalParty
from app.domain.value_objects import PartyId
from app.persistence.mappers.party_mapper import PartyMapper
from app.persistence.models.party import PoliticalPartyModel


class SqlAlchemyPartyRepository(PartyRepository):
    """SQLAlchemy 2.x async repository implementation for PoliticalParty aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: PartyId) -> PoliticalParty | None:
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
        stmt = select(PoliticalPartyModel).where(PoliticalPartyModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return PartyMapper.to_domain(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> Sequence[PoliticalParty]:
        stmt = select(PoliticalPartyModel).offset(skip).limit(limit)
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [PartyMapper.to_domain(m) for m in models]

    async def count(self) -> int:
        stmt = select(func.count(PoliticalPartyModel.id))
        res = await self._session.execute(stmt)
        return res.scalar_one() or 0

    async def exists(self, entity_id: PartyId) -> bool:
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
        stmt = select(func.count(PoliticalPartyModel.id)).where(
            PoliticalPartyModel.id == raw_id
        )
        res = await self._session.execute(stmt)
        return (res.scalar_one() or 0) > 0

    async def add(self, entity: PoliticalParty) -> PoliticalParty:
        model = PartyMapper.to_orm(entity)
        self._session.add(model)
        await self._session.flush()
        return PartyMapper.to_domain(model)

    async def update(self, entity: PoliticalParty) -> PoliticalParty:
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        stmt = select(PoliticalPartyModel).where(PoliticalPartyModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one()
        model.name = entity.name
        model.code = entity.code
        model.symbol = entity.symbol
        await self._session.flush()
        return PartyMapper.to_domain(model)

    async def delete(self, entity: PoliticalParty) -> None:
        raw_id = (
            uuid.UUID(str(entity.id.value))
            if isinstance(entity.id.value, str)
            else entity.id.value
        )
        stmt = select(PoliticalPartyModel).where(PoliticalPartyModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def delete_by_id(self, entity_id: PartyId) -> bool:
        raw_id = (
            uuid.UUID(str(entity_id.value))
            if isinstance(entity_id.value, str)
            else entity_id.value
        )
        stmt = select(PoliticalPartyModel).where(PoliticalPartyModel.id == raw_id)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def find_by_code(self, code: str) -> PoliticalParty | None:
        stmt = select(PoliticalPartyModel).where(PoliticalPartyModel.code == code)
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return PartyMapper.to_domain(model) if model else None
