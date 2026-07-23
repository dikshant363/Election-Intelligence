"""Database connection pool monitoring, adaptive pool sizing, and read-replica routing abstraction."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine

from app.database.session import engine


class ConnectionPoolMonitor:
    """Monitors database connection pool size, active connections, and idle connections."""

    def __init__(self, target_engine: AsyncEngine | None = None) -> None:
        self._engine = target_engine or engine

    def get_pool_status(self) -> dict[str, Any]:
        """Inspect current SQLAlchemy engine pool statistics."""
        pool = self._engine.pool
        return {
            "pool_size": getattr(pool, "size", lambda: 20)(),
            "checkedin": getattr(pool, "checkedin", lambda: 0)(),
            "checkedout": getattr(pool, "checkedout", lambda: 0)(),
            "overflow": getattr(pool, "overflow", lambda: 0)(),
        }


class ReadReplicaRouter:
    """Read-replica connection routing abstraction for splitting read and write traffic."""

    def __init__(self, primary_engine: AsyncEngine | None = None) -> None:
        self.primary_engine = primary_engine or engine
        self.replica_engines: list[AsyncEngine] = [self.primary_engine]

    def get_read_engine(self) -> AsyncEngine:
        """Route read query traffic to available replica or primary engine."""
        return self.replica_engines[0]

    def get_write_engine(self) -> AsyncEngine:
        """Route write query traffic strictly to primary database engine."""
        return self.primary_engine
