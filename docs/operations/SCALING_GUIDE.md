# Autoscaling & Capacity Planning Guide

## Overview

The `AutoscalingEngine` and `CapacityPlanner` provide horizontal scaling metrics, pod replica recommendations, and infrastructure growth projections.

---

## Autoscaling Replica Recommendation Logic

The `AutoscalingEngine` evaluates CPU utilization, memory usage, and background worker queue depth:

- **Scale Up**: CPU > 80%, Memory > 85%, or Queue Depth > 50 -> Replicas + 2
- **Scale Down**: CPU < 20% and Memory < 30% -> Replicas - 1

```python
from app.performance.autoscaling import AutoscalingEngine

rec = AutoscalingEngine.evaluate_component(
    component="background_workers",
    current_replicas=2,
    cpu_pct=90.0,
    memory_pct=80.0,
    queue_depth=60,
)
# Returns recommended_replicas = 4
```

---

## Capacity Estimation

```python
from app.performance.capacity import CapacityPlanner

report = CapacityPlanner.estimate_capacity(target_concurrent_users=10000)
# Returns estimated_max_rps, recommended_db_connections, recommended_redis_memory_mb
```
