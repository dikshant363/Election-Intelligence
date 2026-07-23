"""Tests for database engine configuration and connection settings."""

from app.config import settings
from app.database.engine import engine


def test_database_settings_configuration() -> None:
    """Verify database settings defaults and properties."""
    assert settings.DATABASE_URL is not None
    assert "postgresql" in settings.DATABASE_URL
    assert settings.sync_database_url.startswith("postgresql+psycopg://")
    assert isinstance(settings.DB_ECHO, bool)
    assert settings.DB_POOL_SIZE > 0
    assert settings.DB_MAX_OVERFLOW >= 0
    assert settings.DB_POOL_TIMEOUT > 0
    assert settings.DB_POOL_RECYCLE > 0
    assert settings.DB_POOL_PRE_PING is True


def test_async_engine_initialization() -> None:
    """Verify async SQLAlchemy engine properties."""
    assert engine is not None
    assert str(engine.url).startswith("postgresql+asyncpg://")
    assert engine.pool is not None
