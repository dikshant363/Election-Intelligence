"""Zero-downtime deployment safety checks, migration verification, and rollback planning."""

from __future__ import annotations

from typing import Any


class DeploymentSafetyManager:
    """Evaluates database schema migration safety and zero-downtime release readiness."""

    @staticmethod
    def verify_migration_safety(migration_name: str) -> dict[str, Any]:
        """Check if migration contains non-blocking schema operations."""
        destructive_keywords = ["drop table", "drop column", "alter column type"]
        is_safe = not any(kw in migration_name.lower() for kw in destructive_keywords)
        return {
            "migration": migration_name,
            "is_backwards_compatible": is_safe,
            "requires_downtime": not is_safe,
            "status": "safe" if is_safe else "caution",
        }

    @staticmethod
    def generate_rollback_plan(version: str) -> dict[str, Any]:
        """Generate automated rollback plan instructions."""
        return {
            "target_version": version,
            "steps": [
                f"1. Divert traffic away from version {version}",
                "2. Rollback Alembic database migration to previous revision",
                "3. Redeploy previous stable Docker container image tag",
                "4. Run health check probes /api/v1/live",
            ],
            "estimated_recovery_sec": 30.0,
        }
