"""Tests for request payload size limit middleware."""

import pytest
from httpx import AsyncClient

from app.config import settings


@pytest.mark.asyncio
async def test_oversized_payload_rejected(async_client: AsyncClient) -> None:
    """Verify requests exceeding MAX_REQUEST_SIZE return 413 Payload Too Large."""
    oversized_length = str(settings.MAX_REQUEST_SIZE + 100)
    response = await async_client.post(
        "/api/v1/health",
        headers={"Content-Length": oversized_length},
    )
    assert response.status_code == 413
    data = response.json()
    assert "exceeds maximum allowed size" in data.get("detail", "")
    assert "request_id" in data
