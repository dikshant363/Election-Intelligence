"""Unit and integration tests for CQRS Application layer."""

import uuid
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.application.commands import (
    CreateConstituency,
    CreateElection,
    DeclareResult,
    RegisterCandidate,
    RegisterParty,
)
from app.application.handlers import CommandHandlers, QueryHandlers
from app.application.pipeline import CommandPipeline
from app.application.queries import GetElection, ListElections
from app.config import settings
from app.core.events import InMemoryEventBus
from app.database.base import Base
from app.domain.election import ElectionCreated
from app.domain.value_objects import ElectionType
from app.persistence.uow import SqlAlchemyUnitOfWork


@pytest_asyncio.fixture
async def test_session_factory() -> async_sessionmaker[AsyncSession]:
    """Provide a fresh NullPool AsyncEngine & session factory."""
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


@pytest.mark.asyncio
async def test_create_election_command_and_event_dispatch(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Verify CreateElection command handler, UoW commit, and event bus dispatch."""
    event_bus = InMemoryEventBus()
    received_events: list[ElectionCreated] = []

    async def on_election_created(evt: ElectionCreated) -> None:
        received_events.append(evt)

    await event_bus.subscribe(ElectionCreated, on_election_created)

    uow = SqlAlchemyUnitOfWork(session_factory=test_session_factory)
    handlers = CommandHandlers(uow=uow, event_bus=event_bus)
    pipeline = CommandPipeline(handlers=handlers)

    cmd = CreateElection(
        title=f"Parliamentary Election {uuid.uuid4().hex[:6]}",
        election_type=ElectionType.GENERAL,
        start_date=date(2026, 5, 1),
        end_date=date(2026, 5, 15),
    )

    res = await pipeline.execute_create_election(cmd)
    assert res.is_success is True
    dto = res.unwrap()
    assert dto.status == "DRAFT"

    # Verify event bus dispatch after commit
    assert len(received_events) == 1
    assert received_events[0].title == dto.title

    # Query via QueryHandlers
    query_handlers = QueryHandlers(uow=uow)
    q_res = await query_handlers.handle_get_election(GetElection(id=dto.id))
    assert q_res.is_success is True
    assert q_res.unwrap().id == dto.id

    # Clean up
    async with uow:
        await uow.elections.delete_by_id(dto.id)
        await uow.commit()


@pytest.mark.asyncio
async def test_end_to_end_cqrs_workflow(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Verify full CQRS workflow: party registration, constituency creation, candidate registration, and result declaration."""
    uow = SqlAlchemyUnitOfWork(session_factory=test_session_factory)
    cmd_handlers = CommandHandlers(uow=uow)
    query_handlers = QueryHandlers(uow=uow)

    suffix = uuid.uuid4().hex[:6].upper()

    # 1. Register Party
    p_res = await cmd_handlers.handle_register_party(
        RegisterParty(
            name=f"Democratic Front {suffix}",
            code=f"DEF-{suffix}",
            symbol="Flag",
        )
    )
    assert p_res.is_success is True
    party_dto = p_res.unwrap()

    # 2. Create Constituency
    c_res = await cmd_handlers.handle_create_constituency(
        CreateConstituency(
            name=f"West Delhi {suffix}",
            code=f"WD-{suffix}",
            state_code="IN-DL",
        )
    )
    assert c_res.is_success is True
    con_dto = c_res.unwrap()

    # 3. Create Election
    e_res = await cmd_handlers.handle_create_election(
        CreateElection(
            title=f"State Election {suffix}",
            election_type=ElectionType.ASSEMBLY,
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 2),
        )
    )
    assert e_res.is_success is True
    elec_dto = e_res.unwrap()

    # 4. Register Candidate
    cand_res = await cmd_handlers.handle_register_candidate(
        RegisterCandidate(
            name="Rahul Verma",
            age=32,
            email=f"rahul-{suffix}@def.org",
            phone="+919876543210",
            constituency_id=con_dto.id,
            party_id=party_dto.id,
        )
    )
    assert cand_res.is_success is True
    cand_dto = cand_res.unwrap()

    # 5. Declare Result
    r_res = await cmd_handlers.handle_declare_result(
        DeclareResult(
            election_id=elec_dto.id,
            constituency_id=con_dto.id,
            candidate_votes={cand_dto.id: 15400},
            winning_candidate_id=cand_dto.id,
        )
    )
    assert r_res.is_success is True
    res_dto = r_res.unwrap()
    assert res_dto.is_declared is True
    assert res_dto.total_votes == 15400
    assert res_dto.winning_candidate_id == cand_dto.id

    # 6. Verify List Queries
    l_res = await query_handlers.handle_list_elections(ListElections())
    assert l_res.is_success is True
    assert len(l_res.unwrap()) >= 1

    # Clean up created entities
    async with uow:
        await uow.results.delete_by_id(res_dto.result_key)
        await uow.candidates.delete_by_id(cand_dto.id)
        await uow.elections.delete_by_id(elec_dto.id)
        await uow.constituencies.delete_by_id(con_dto.id)
        await uow.parties.delete_by_id(party_dto.id)
        await uow.commit()


@pytest.mark.asyncio
async def test_command_validation_pipeline_rejections(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Verify CommandPipeline rejects invalid commands without executing handlers."""
    uow = SqlAlchemyUnitOfWork(session_factory=test_session_factory)
    pipeline = CommandPipeline(handlers=CommandHandlers(uow=uow))

    # Invalid title
    invalid_cmd = CreateElection(
        title="",
        election_type=ElectionType.GENERAL,
        start_date=date(2026, 5, 1),
        end_date=date(2026, 5, 10),
    )
    res = await pipeline.execute_create_election(invalid_cmd)
    assert res.is_failure is True
    assert res.error.code == "VALIDATION_ERROR"
