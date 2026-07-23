"""Integration tests for FastAPI REST API endpoints."""

import uuid

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.api.v1.dependencies import get_uow
from app.config import settings
from app.database.base import Base
from app.main import app
from app.persistence.uow import SqlAlchemyUnitOfWork, UnitOfWork


@pytest_asyncio.fixture
async def test_session_factory() -> async_sessionmaker[AsyncSession]:
    """Provide NullPool AsyncEngine & session factory."""
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


@pytest_asyncio.fixture
async def async_client(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncClient:
    """Async HTTP client overriding get_uow with test session factory."""

    async def override_get_uow() -> UnitOfWork:
        uow = SqlAlchemyUnitOfWork(session_factory=test_session_factory)
        yield uow

    app.dependency_overrides[get_uow] = override_get_uow

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_openapi_schema_endpoint(async_client: AsyncClient) -> None:
    """Verify OpenAPI schema generation."""
    response = await async_client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Election Intelligence Platform"
    assert "/api/v1/elections" in schema["paths"]


@pytest.mark.asyncio
async def test_elections_api_workflow(async_client: AsyncClient) -> None:
    """Verify POST /elections, GET /elections/{id}, and GET /elections list."""
    payload = {
        "title": "National General Election 2026",
        "election_type": "GENERAL",
        "start_date": "2026-05-01",
        "end_date": "2026-05-15",
    }
    post_res = await async_client.post("/api/v1/elections", json=payload)
    assert post_res.status_code == 201
    created = post_res.json()
    e_id = created["id"]
    assert created["title"] == payload["title"]

    get_res = await async_client.get(f"/api/v1/elections/{e_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == e_id

    list_res = await async_client.get("/api/v1/elections?page=1&size=10")
    assert list_res.status_code == 200
    data = list_res.json()
    assert "items" in data
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_full_domain_entities_api_lifecycle(
    async_client: AsyncClient,
) -> None:
    """Verify Party, Constituency, Candidate, and Result endpoints."""
    suffix = uuid.uuid4().hex[:6].upper()

    # 1. Register Party
    party_payload = {
        "name": f"United Citizens Alliance {suffix}",
        "code": f"UCA-{suffix}",
        "symbol": "Star",
    }
    p_res = await async_client.post("/api/v1/parties", json=party_payload)
    assert p_res.status_code == 201
    party_id = p_res.json()["id"]

    # 2. Create Constituency
    constituency_payload = {
        "name": f"Central District {suffix}",
        "code": f"CD-{suffix}",
        "state_code": "IN-DL",
        "constituency_type": "ASSEMBLY",
    }
    c_res = await async_client.post(
        "/api/v1/constituencies", json=constituency_payload
    )
    assert c_res.is_success is True or c_res.status_code == 201
    con_id = c_res.json()["id"]

    # 3. Create Election
    e_res = await async_client.post(
        "/api/v1/elections",
        json={
            "title": f"Assembly Election {suffix}",
            "election_type": "ASSEMBLY",
            "start_date": "2026-06-01",
            "end_date": "2026-06-05",
        },
    )
    assert e_res.status_code == 201
    elec_id = e_res.json()["id"]

    # 4. Register Candidate
    candidate_payload = {
        "name": "Sunil Sharma",
        "age": 38,
        "email": f"sunil-{suffix}@uca.org",
        "phone": "+919876543210",
        "constituency_id": con_id,
        "party_id": party_id,
    }
    cand_res = await async_client.post(
        "/api/v1/candidates", json=candidate_payload
    )
    assert cand_res.status_code == 201
    cand_id = cand_res.json()["id"]

    # 5. Establish Polling Booth
    booth_res = await async_client.post(
        "/api/v1/polling-booths",
        json={
            "constituency_id": con_id,
            "booth_name": "Government Primary School",
            "booth_number": "PB-01",
            "latitude": 28.6139,
            "longitude": 77.2090,
        },
    )
    assert booth_res.status_code == 201

    # 6. Declare Result
    result_payload = {
        "election_id": elec_id,
        "constituency_id": con_id,
        "candidate_votes": {cand_id: 18500},
        "winning_candidate_id": cand_id,
    }
    r_res = await async_client.post("/api/v1/results", json=result_payload)
    assert r_res.status_code == 201
    result_data = r_res.json()
    assert result_data["is_declared"] is True
    assert result_data["total_votes"] == 18500


@pytest.mark.asyncio
async def test_rfc_7807_error_handling(async_client: AsyncClient) -> None:
    """Verify HTTP 404 and 422 return RFC 7807 Problem Details."""
    # 404 Not Found
    fake_uuid = str(uuid.uuid4())
    res_404 = await async_client.get(f"/api/v1/elections/{fake_uuid}")
    assert res_404.status_code == 404
    body_404 = res_404.json()
    assert body_404["status"] == 404
    assert body_404["code"] == "NOT_FOUND"

    # 422 Unprocessable Entity (Invalid payload)
    res_422 = await async_client.post(
        "/api/v1/elections",
        json={"title": ""},  # Missing required fields
    )
    assert res_422.status_code == 422
    body_422 = res_422.json()
    assert body_422["status"] == 422
    assert "code" in body_422
