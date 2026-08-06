"""Pytest configuration and shared fixtures."""

import os
import sys
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Ensure backend root is on sys.path for app imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

# Setup test environment variables before any application code is imported
os.environ["JWT_SECRET_KEY"] = "test-secret-key-do-not-use-in-prod"

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for session scope."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an AsyncClient for FastAPI endpoint testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
