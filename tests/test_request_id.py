"""Tests for Request ID middleware and lifecycle tracking."""

import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_request_id_generated_if_missing(async_client: AsyncClient) -> None:
    """Verify X-Request-ID is generated as UUID when omitted by client."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200

    request_id = response.headers.get("x-request-id")
    assert request_id is not None
    # Validate UUID format
    parsed_uuid = uuid.UUID(request_id)
    assert str(parsed_uuid) == request_id

    data = response.json()
    assert data.get("request_id") == request_id


@pytest.mark.asyncio
async def test_request_id_preserved_if_provided(async_client: AsyncClient) -> None:
    """Verify custom X-Request-ID provided by client is preserved."""
    custom_id = str(uuid.uuid4())
    response = await async_client.get(
        "/api/v1/health",
        headers={"X-Request-ID": custom_id},
    )
    assert response.status_code == 200
    assert response.headers.get("x-request-id") == custom_id
    assert response.json().get("request_id") == custom_id
