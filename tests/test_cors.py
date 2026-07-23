"""Tests for CORS middleware configuration."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_cors_preflight_allowed_origin(async_client: AsyncClient) -> None:
    """Verify CORS preflight request for an allowed origin."""
    response = await async_client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    )
