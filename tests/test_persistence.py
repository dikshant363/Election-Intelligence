"""Integration and unit tests for SQLAlchemy persistence layer."""

from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.config import settings
from app.database.base import Base
from app.domain.candidate import Candidate
from app.domain.constituency import Constituency
from app.domain.election import Election
from app.domain.party import PoliticalParty
from app.domain.polling import PollingBooth
from app.domain.results import ElectionResult
from app.domain.value_objects import (
    Age,
    CandidateId,
    ConstituencyId,
    ElectionDate,
    ElectionId,
    ElectionType,
    Email,
    GeoCoordinates,
    PartyId,
    PhoneNumber,
    PollingBoothId,
    StateCode,
    VoteCount,
)
import app.persistence.models  # noqa: F401
from app.persistence.mappers import (
    CandidateMapper,
    ConstituencyMapper,
    ElectionMapper,
    PartyMapper,
    PollingMapper,
    ResultMapper,
)
from app.persistence.uow import SqlAlchemyUnitOfWork


@pytest_asyncio.fixture
async def test_session_factory() -> async_sessionmaker[AsyncSession]:
    """Provide a fresh NullPool AsyncEngine & session factory bound to the active loop."""
    test_engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
    )
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    yield session_factory
    await test_engine.dispose()


def test_mapper_round_trips() -> None:
    """Verify bidirectional mapper fidelity for all domain aggregates."""
    # 1. Election
    e_id = ElectionId.generate()
    election = Election(
        id=e_id,
        title="Roundtrip Election",
        election_type=ElectionType.GENERAL,
        election_date=ElectionDate(
            start_date=date(2026, 5, 1), end_date=date(2026, 5, 10)
        ),
    )
    e_orm = ElectionMapper.to_orm(election)
    e_domain = ElectionMapper.to_domain(e_orm)
    assert e_domain.id == election.id
    assert e_domain.title == election.title
    assert e_domain.status == election.status

    # 2. PoliticalParty
    p_id = PartyId.generate()
    party = PoliticalParty(
        id=p_id, name="Test Alliance", code="TAL", symbol="Torch"
    )
    p_orm = PartyMapper.to_orm(party)
    p_domain = PartyMapper.to_domain(p_orm)
    assert p_domain.id == party.id
    assert p_domain.code == party.code

    # 3. Constituency
    con_id = ConstituencyId.generate()
    constituency = Constituency(
        id=con_id,
        name="North District",
        code="ND-01",
        state_code=StateCode("IN-DL"),
    )
    c_orm = ConstituencyMapper.to_orm(constituency)
    c_domain = ConstituencyMapper.to_domain(c_orm)
    assert c_domain.id == constituency.id
    assert c_domain.state_code == constituency.state_code

    # 4. Candidate
    cand_id = CandidateId.generate()
    candidate = Candidate(
        id=cand_id,
        name="John Doe",
        age=Age(30),
        email=Email("john@test.org"),
        phone=PhoneNumber("+919876543210"),
        constituency_id=con_id,
        party_id=p_id,
    )
    cand_orm = CandidateMapper.to_orm(candidate)
    cand_domain = CandidateMapper.to_domain(cand_orm)
    assert cand_domain.id == candidate.id
    assert cand_domain.email == candidate.email

    # 5. PollingBooth
    booth_id = PollingBoothId.generate()
    booth = PollingBooth(
        id=booth_id,
        constituency_id=con_id,
        booth_name="Station A",
        booth_number="PB-10",
        location=GeoCoordinates(latitude=28.5, longitude=77.2),
    )
    b_orm = PollingMapper.to_orm(booth)
    b_domain = PollingMapper.to_domain(b_orm)
    assert b_domain.id == booth.id
    assert b_domain.location == booth.location

    # 6. ElectionResult
    res = ElectionResult(election_id=e_id, constituency_id=con_id)
    res.record_votes(cand_id, VoteCount(1200))
    res.declare_result(winning_candidate_id=cand_id)
    res_orm = ResultMapper.to_orm(res)
    res_domain = ResultMapper.to_domain(res_orm)
    assert res_domain.election_id == res.election_id
    assert res_domain.winning_candidate_id == res.winning_candidate_id
    assert res_domain.is_declared is True


@pytest.mark.asyncio
async def test_uow_repository_crud_and_commit(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Verify SqlAlchemyUnitOfWork CRUD operations and commit functionality."""
    async with SqlAlchemyUnitOfWork(session_factory=test_session_factory) as uow:
        # Create election
        e_id = ElectionId.generate()
        election = Election(
            id=e_id,
            title="Assembly Election 2026",
            election_type=ElectionType.ASSEMBLY,
            election_date=ElectionDate(
                start_date=date(2026, 6, 1), end_date=date(2026, 6, 5)
            ),
        )
        await uow.elections.add(election)

        # Create party
        p_id = PartyId.generate()
        party = PoliticalParty(
            id=p_id, name="Progress Party", code="PRG", symbol="Sun"
        )
        await uow.parties.add(party)

        # Create constituency
        con_id = ConstituencyId.generate()
        constituency = Constituency(
            id=con_id,
            name="East Central",
            code="EC-05",
            state_code=StateCode("IN-MH"),
        )
        await uow.constituencies.add(constituency)

        await uow.commit()

    # Verify persistence in separate UoW transaction
    async with SqlAlchemyUnitOfWork(session_factory=test_session_factory) as uow:
        fetched_e = await uow.elections.get_by_id(e_id)
        assert fetched_e is not None
        assert fetched_e.title == "Assembly Election 2026"

        fetched_p = await uow.parties.find_by_code("PRG")
        assert fetched_p is not None
        assert fetched_p.symbol == "Sun"

        fetched_c = await uow.constituencies.get_by_id(con_id)
        assert fetched_c is not None
        assert fetched_c.state_code.code == "IN-MH"

        # Update election
        fetched_e.start_election()
        await uow.elections.update(fetched_e)

        # Clean up
        await uow.elections.delete_by_id(e_id)
        await uow.parties.delete_by_id(p_id)
        await uow.constituencies.delete_by_id(con_id)
        await uow.commit()

    # Verify deletion
    async with SqlAlchemyUnitOfWork(session_factory=test_session_factory) as uow:
        assert await uow.elections.get_by_id(e_id) is None


@pytest.mark.asyncio
async def test_uow_rollback_on_exception(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Verify SqlAlchemyUnitOfWork automatic rollback on exception."""
    e_id = ElectionId.generate()
    election = Election(
        id=e_id,
        title="Rollback Election",
        election_type=ElectionType.MUNICIPAL,
        election_date=ElectionDate(
            start_date=date(2026, 7, 1), end_date=date(2026, 7, 2)
        ),
    )

    with pytest.raises(RuntimeError, match="Simulated failure"):
        async with SqlAlchemyUnitOfWork(
            session_factory=test_session_factory
        ) as uow:
            await uow.elections.add(election)
            raise RuntimeError("Simulated failure during transaction")

    # Verify election was rolled back and not persisted
    async with SqlAlchemyUnitOfWork(session_factory=test_session_factory) as uow:
        assert await uow.elections.get_by_id(e_id) is None
