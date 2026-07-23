# Role-Based Access Control (RBAC) Guide

## Overview
The RBAC system enforces granular role and permission checks across API endpoints without embedding hardcoded authorization logic in routers or domain aggregates.

## Hierarchical Role Matrix

| System Role | Scope / Intent | Inherited Permissions |
| :--- | :--- | :--- |
| `PlatformAdmin` | Platform Superuser | `*` (All permissions) |
| `ElectionCommissioner` | National Election Authority | `elections:create`, `candidates:register`, `parties:register`, `results:declare`, `audit:read` |
| `StateOfficer` | State Election Commission | `elections:read`, `constituencies:create`, `polling:create`, `candidates:register` |
| `DistrictOfficer` | District Returning Officer | `elections:read`, `polling:create` |
| `Analyst` | Data Analyst / Researcher | `elections:read`, `candidates:read`, `parties:read`, `results:read` |
| `Auditor` | Compliance & Security Auditor | `audit:read`, `elections:read` |
| `PublicUser` | Citizen / Observer | `elections:read`, `candidates:read`, `parties:read`, `results:read` |

## Router Dependency Integration

```python
@router.post("/elections", dependencies=[Depends(require_role("ElectionCommissioner"))])
async def create_election(...):
    ...
```

```python
@router.post("/results", dependencies=[Depends(require_permission("results:declare"))])
async def declare_result(...):
    ...
```
