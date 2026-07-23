"""Tests for API health check endpoint with database status."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_response_structure(async_client: AsyncClient) -> None:
    """Verify GET /api/v1/health returns status and database keys without credentials."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert data["database"] in ["connected", "disconnected"]
    # Verify no credentials or sensitive URLs exposed
    response_str = str(data)
    assert "password" not in response_str
    assert "postgresql://" not in response_str
