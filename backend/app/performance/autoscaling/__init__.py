"""Autoscaling abstraction and horizontal replica recommendation engine."""

from __future__ import annotations

from app.performance.schemas import AutoscalingRecommendationSchema

HIGH_CPU_THRESH = 80.0
HIGH_MEM_THRESH = 85.0
HIGH_QUEUE_THRESH = 50
LOW_CPU_THRESH = 20.0
LOW_MEM_THRESH = 30.0
MIN_REPLICAS_2 = 2


class AutoscalingEngine:
    """Evaluates component workload metrics to recommend horizontal pod/worker replica count."""

    @staticmethod
    def evaluate_component(
        component: str,
        current_replicas: int,
        cpu_pct: float,
        memory_pct: float,
        queue_depth: int = 0,
    ) -> AutoscalingRecommendationSchema:
        recommended = current_replicas
        reason = "Optimal workload bounds"

        if cpu_pct > HIGH_CPU_THRESH or memory_pct > HIGH_MEM_THRESH or queue_depth > HIGH_QUEUE_THRESH:
            recommended = current_replicas + 2
            reason = f"High resource utilization (CPU={cpu_pct}%, Queue={queue_depth})"
        elif cpu_pct < LOW_CPU_THRESH and memory_pct < LOW_MEM_THRESH and current_replicas > MIN_REPLICAS_2:
            recommended = max(1, current_replicas - 1)
            reason = f"Underutilized resources (CPU={cpu_pct}%)"

        return AutoscalingRecommendationSchema(
            component=component,
            current_replicas=current_replicas,
            recommended_replicas=recommended,
            cpu_utilization_pct=cpu_pct,
            memory_utilization_pct=memory_pct,
            scaling_reason=reason,
        )
