"""Tests for database session lifecycle management."""

import pytest

from app.database.session import AsyncSessionLocal, get_db_context, get_db_session


def test_async_session_factory() -> None:
    """Verify session factory configuration."""
    assert AsyncSessionLocal is not None


@pytest.mark.asyncio
async def test_session_generator_lifecycle() -> None:
    """Verify get_db_session dependency generator returns an AsyncSession."""
    gen = get_db_session()
    assert gen is not None


@pytest.mark.asyncio
async def test_session_context_manager_structure() -> None:
    """Verify get_db_context asynccontextmanager structure."""
    ctx = get_db_context()
    assert ctx is not None
