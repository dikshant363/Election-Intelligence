"""Capacity planning estimator calculating concurrency, RPS, memory, and storage growth."""

from __future__ import annotations

from app.performance.schemas import CapacityReportSchema


class CapacityPlanner:
    """Calculates growth projections, concurrency bounds, and infrastructure recommendations."""

    @staticmethod
    def estimate_capacity(
        target_concurrent_users: int = 10000,
        avg_requests_per_user_min: float = 12.0,
    ) -> CapacityReportSchema:
        max_rps = round((target_concurrent_users * avg_requests_per_user_min) / 60.0, 2)
        rec_db_conn = min(100, max(20, int(max_rps * 0.05)))
        rec_redis_mb = max(512, int(target_concurrent_users * 0.1))
        storage_gb = round((max_rps * 86400 * 30 * 2000) / (1024**3), 2)

        return CapacityReportSchema(
            max_concurrent_users=target_concurrent_users,
            estimated_max_rps=max_rps,
            recommended_db_connections=rec_db_conn,
            recommended_redis_memory_mb=rec_redis_mb,
            projected_storage_gb_per_month=storage_gb,
        )
