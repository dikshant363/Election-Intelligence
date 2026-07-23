"""Tests for security response headers middleware."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_security_headers_present(async_client: AsyncClient) -> None:
    """Verify essential security headers are present in HTTP responses."""
    response = await async_client.get("/api/v1/")
    assert response.status_code == 200

    headers = response.headers
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-frame-options") == "DENY"
    assert "strict-origin" in headers.get("referrer-policy", "")
    assert "camera=()" in headers.get("permissions-policy", "")
    assert headers.get("cross-origin-opener-policy") == "same-origin"
    assert headers.get("cross-origin-resource-policy") == "same-origin"
    assert "default-src" in headers.get("content-security-policy", "")
