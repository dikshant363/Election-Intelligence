"""SqlAlchemy implementation of ResultRepository contract."""

import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.results import ElectionResult, ResultRepository
from app.domain.value_objects import ConstituencyId, ElectionId
from app.persistence.mappers.result_mapper import ResultMapper
from app.persistence.models.results import ElectionResultModel


class SqlAlchemyResultRepository(ResultRepository):
    """SQLAlchemy 2.x async repository implementation for ElectionResult aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: str) -> ElectionResult | None:
        stmt = select(ElectionResultModel).where(
            ElectionResultModel.result_key == entity_id
        )
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return ResultMapper.to_domain(model) if model else None

    async def find_all(
        self, skip: int = 0, limit: int = 100
    ) -> Sequence[ElectionResult]:
        stmt = select(ElectionResultModel).offset(skip).limit(limit)
        res = await self._session.execute(stmt)
        models = res.scalars().all()
        return [ResultMapper.to_domain(m) for m in models]

    async def count(self) -> int:
        stmt = select(func.count(ElectionResultModel.id))
        res = await self._session.execute(stmt)
        return res.scalar_one() or 0

    async def exists(self, entity_id: str) -> bool:
        stmt = select(func.count(ElectionResultModel.id)).where(
            ElectionResultModel.result_key == entity_id
        )
        res = await self._session.execute(stmt)
        return (res.scalar_one() or 0) > 0

    async def add(self, entity: ElectionResult) -> ElectionResult:
        model = ResultMapper.to_orm(entity)
        self._session.add(model)
        await self._session.flush()
        return ResultMapper.to_domain(model)

    async def update(self, entity: ElectionResult) -> ElectionResult:
        stmt = select(ElectionResultModel).where(
            ElectionResultModel.result_key == str(entity.id)
        )
        res = await self._session.execute(stmt)
        model = res.scalar_one()
        updated_model = ResultMapper.to_orm(entity)
        model.total_votes = updated_model.total_votes
        model.candidate_votes_json = updated_model.candidate_votes_json
        model.winning_candidate_id = updated_model.winning_candidate_id
        model.is_declared = updated_model.is_declared
        await self._session.flush()
        return ResultMapper.to_domain(model)

    async def delete(self, entity: ElectionResult) -> None:
        stmt = select(ElectionResultModel).where(
            ElectionResultModel.result_key == str(entity.id)
        )
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def delete_by_id(self, entity_id: str) -> bool:
        stmt = select(ElectionResultModel).where(
            ElectionResultModel.result_key == entity_id
        )
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def find_by_election_and_constituency(
        self, election_id: ElectionId, constituency_id: ConstituencyId
    ) -> ElectionResult | None:
        raw_e_id = (
            uuid.UUID(str(election_id.value))
            if isinstance(election_id.value, str)
            else election_id.value
        )
        raw_con_id = (
            uuid.UUID(str(constituency_id.value))
            if isinstance(constituency_id.value, str)
            else constituency_id.value
        )
        stmt = select(ElectionResultModel).where(
            ElectionResultModel.election_id == raw_e_id,
            ElectionResultModel.constituency_id == raw_con_id,
        )
        res = await self._session.execute(stmt)
        model = res.scalar_one_or_none()
        return ResultMapper.to_domain(model) if model else None
