"""Tests for Trusted Hosts middleware."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_trusted_host_allowed(async_client: AsyncClient) -> None:
    """Verify requests with allowed Host header succeed."""
    response = await async_client.get(
        "/api/v1/",
        headers={"Host": "testserver"},
    )
    assert response.status_code == 200
