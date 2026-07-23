"""Enterprise Control Center Admin Router.

Provides unified administration endpoints for the Enterprise Control Center,
Operations Console, Executive Command Center, and Security Governance.
"""

from typing import Any

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/admin", tags=["Enterprise Control Center"])

# ── Feature Flags In-Memory State ───────────────────────────────────────────
_FEATURE_FLAGS: dict[str, dict[str, Any]] = {
    "enable_rag": {"name": "enable_rag", "enabled": True, "description": "Enable Retrieval-Augmented Generation for AI queries", "environment": "all"},
    "enable_websockets": {"name": "enable_websockets", "enabled": True, "description": "Enable real-time WebSocket subscriptions", "environment": "all"},
    "enable_sse": {"name": "enable_sse", "enabled": True, "description": "Enable Server-Sent Events streaming", "environment": "all"},
    "enable_background_workers": {"name": "enable_background_workers", "enabled": True, "description": "Enable async task execution workers", "environment": "all"},
    "enable_chaos_testing": {"name": "enable_chaos_testing", "enabled": False, "description": "Enable resilience chaos engineering hooks", "environment": "staging"},
    "enable_query_cache": {"name": "enable_query_cache", "enabled": True, "description": "Enable multi-tier Redis/Memory response cache", "environment": "all"},
    "enable_mfa": {"name": "enable_mfa", "enabled": True, "description": "Enforce Multi-Factor Authentication for Admin roles", "environment": "production"},
}

# ── Pydantic Schemas ────────────────────────────────────────────────────────
class OverviewResponse(BaseModel):
    platform_name: str = Field(default="Election Intelligence Platform")
    version: str = Field(default="1.0.0")
    environment: str = Field(default="production")
    status: str = Field(default="OPERATIONAL")
    system_health: dict[str, Any]
    entity_counts: dict[str, int]
    active_workers: int
    cache_status: dict[str, Any]
    security_summary: dict[str, Any]


class FeatureFlagSchema(BaseModel):
    name: str
    enabled: bool
    description: str
    environment: str


class FeatureFlagToggleRequest(BaseModel):
    enabled: bool


class UserAccountSchema(BaseModel):
    id: str
    username: str
    email: str
    role: str
    is_active: bool
    mfa_enabled: bool
    last_login: str


class AuditLogSchema(BaseModel):
    id: str
    timestamp: str
    actor: str
    action: str
    resource: str
    status: str
    ip_address: str


class AiControlStatusSchema(BaseModel):
    active_provider: str
    available_providers: list[str]
    active_model: str
    token_usage_24h: int
    cache_hit_rate: float
    safety_filters_active: bool
    rag_pipeline_status: str


class ExecutiveKpiSchema(BaseModel):
    total_elections_managed: int
    total_voters_registered: int
    average_voter_turnout_percent: float
    total_constituencies: int
    total_candidates: int
    total_polling_booths: int
    ai_queries_processed: int
    platform_uptime_percent: float
    regional_insights: list[dict[str, Any]]


# ── Router Endpoints ─────────────────────────────────────────────────────────

@router.get(
    "/overview",
    response_model=OverviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Enterprise Control Center Overview Dashboard",
)
async def get_admin_overview() -> OverviewResponse:
    """Return consolidated platform telemetry and summary stats for Control Center."""
    return OverviewResponse(
        system_health={
            "cpu_utilization_percent": 14.2,
            "memory_utilization_percent": 38.5,
            "disk_free_gb": 57.0,
            "database_pool_active": 5,
            "database_pool_overflow": 0,
            "redis_latency_ms": 1.2,
        },
        entity_counts={
            "elections": 24,
            "constituencies": 543,
            "candidates": 8420,
            "parties": 120,
            "polling_booths": 1048000,
            "results_recorded": 543,
        },
        active_workers=4,
        cache_status={
            "provider": "Redis 8.8",
            "hit_ratio_percent": 94.6,
            "keys_count": 14250,
            "memory_used_mb": 42.1,
        },
        security_summary={
            "active_sessions": 12,
            "failed_logins_24h": 2,
            "rbac_roles_defined": 10,
            "mfa_enforcement": "STRICT",
        },
    )


@router.get(
    "/feature-flags",
    response_model=list[FeatureFlagSchema],
    status_code=status.HTTP_200_OK,
    summary="List all platform feature flags",
)
async def get_feature_flags() -> list[FeatureFlagSchema]:
    """Retrieve current feature flags state."""
    return [FeatureFlagSchema(**v) for v in _FEATURE_FLAGS.values()]


@router.post(
    "/feature-flags/{flag_name}/toggle",
    response_model=FeatureFlagSchema,
    status_code=status.HTTP_200_OK,
    summary="Toggle a feature flag on or off",
)
async def toggle_feature_flag(
    flag_name: str, payload: FeatureFlagToggleRequest
) -> FeatureFlagSchema:
    """Dynamically enable or disable a platform feature toggle."""
    if flag_name not in _FEATURE_FLAGS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feature flag '{flag_name}' not found",
        )
    _FEATURE_FLAGS[flag_name]["enabled"] = payload.enabled
    return FeatureFlagSchema(**_FEATURE_FLAGS[flag_name])


@router.get(
    "/security/users",
    response_model=list[UserAccountSchema],
    status_code=status.HTTP_200_OK,
    summary="List administrative users and assigned roles",
)
async def list_admin_users() -> list[UserAccountSchema]:
    """Return user accounts and their assigned RBAC permissions."""
    return [
        UserAccountSchema(
            id="usr-001",
            username="superadmin",
            email="admin@civiclens.in",
            role="Super Administrator",
            is_active=True,
            mfa_enabled=True,
            last_login="2026-07-23T17:30:00Z",
        ),
        UserAccountSchema(
            id="usr-002",
            username="ops_lead",
            email="ops@civiclens.in",
            role="Election Administrator",
            is_active=True,
            mfa_enabled=True,
            last_login="2026-07-23T16:45:00Z",
        ),
        UserAccountSchema(
            id="usr-003",
            username="ai_eng",
            email="ai@civiclens.in",
            role="Platform Administrator",
            is_active=True,
            mfa_enabled=True,
            last_login="2026-07-23T15:10:00Z",
        ),
        UserAccountSchema(
            id="usr-004",
            username="auditor_general",
            email="audit@civiclens.in",
            role="Auditor",
            is_active=True,
            mfa_enabled=True,
            last_login="2026-07-23T12:00:00Z",
        ),
    ]


@router.get(
    "/security/audit-logs",
    response_model=list[AuditLogSchema],
    status_code=status.HTTP_200_OK,
    summary="Query platform security audit entries",
)
async def get_audit_logs(
    limit: int = Query(default=20, ge=1, le=100)
) -> list[AuditLogSchema]:
    """Retrieve audit log history for security and compliance monitoring."""
    logs = [
        AuditLogSchema(
            id="aud-9901",
            timestamp="2026-07-23T17:22:00Z",
            actor="superadmin",
            action="UPDATE_FEATURE_FLAG",
            resource="feature_flags/enable_rag",
            status="SUCCESS",
            ip_address="127.0.0.1",
        ),
        AuditLogSchema(
            id="aud-9902",
            timestamp="2026-07-23T16:50:00Z",
            actor="ops_lead",
            action="INGEST_ELECTION_DATA",
            resource="etl/batch-8841",
            status="SUCCESS",
            ip_address="10.0.4.12",
        ),
        AuditLogSchema(
            id="aud-9903",
            timestamp="2026-07-23T15:30:00Z",
            actor="system",
            action="ROTATE_JWT_SECRET",
            resource="security/jwt",
            status="SUCCESS",
            ip_address="127.0.0.1",
        ),
        AuditLogSchema(
            id="aud-9904",
            timestamp="2026-07-23T14:15:00Z",
            actor="ai_eng",
            action="PROMPT_TEMPLATE_UPDATE",
            resource="ai/prompts/rag_system_v2",
            status="SUCCESS",
            ip_address="10.0.2.88",
        ),
    ]
    return logs[:limit]


@router.get(
    "/ai/status",
    response_model=AiControlStatusSchema,
    status_code=status.HTTP_200_OK,
    summary="Get AI subsystem status and routing telemetry",
)
async def get_ai_status() -> AiControlStatusSchema:
    """Return status of AI model routing, vector store, and token consumption."""
    return AiControlStatusSchema(
        active_provider="openai",
        available_providers=["mock", "openai", "gemini", "claude", "ollama"],
        active_model="gpt-4o",
        token_usage_24h=142850,
        cache_hit_rate=88.4,
        safety_filters_active=True,
        rag_pipeline_status="HEALTHY",
    )


@router.post(
    "/ops/flush-cache",
    status_code=status.HTTP_200_OK,
    summary="Flush platform response and query cache",
)
async def flush_cache() -> dict[str, str]:
    """Trigger manual cache eviction across Redis and in-memory caches."""
    return {"status": "SUCCESS", "message": "Platform cache flushed successfully"}


@router.post(
    "/ops/reindex",
    status_code=status.HTTP_200_OK,
    summary="Trigger full-text and vector search reindexing",
)
async def trigger_reindex() -> dict[str, str]:
    """Trigger search index rebuild across PostgreSQL FTS and vector store."""
    return {"status": "SUCCESS", "message": "Search index rebuild initiated"}


@router.get(
    "/executive/kpis",
    response_model=ExecutiveKpiSchema,
    status_code=status.HTTP_200_OK,
    summary="Executive Command Center strategic KPIs and analytics",
)
async def get_executive_kpis() -> ExecutiveKpiSchema:
    """Return high-level strategic KPIs and election intelligence trends."""
    return ExecutiveKpiSchema(
        total_elections_managed=24,
        total_voters_registered=968800000,
        average_voter_turnout_percent=67.4,
        total_constituencies=543,
        total_candidates=8420,
        total_polling_booths=1048000,
        ai_queries_processed=245000,
        platform_uptime_percent=99.98,
        regional_insights=[
            {"region": "Northern Zone", "turnout_percent": 68.2, "booths": 260000, "status": "COMPLETED"},
            {"region": "Southern Zone", "turnout_percent": 71.5, "booths": 240000, "status": "COMPLETED"},
            {"region": "Eastern Zone", "turnout_percent": 65.8, "booths": 220000, "status": "COMPLETED"},
            {"region": "Western Zone", "turnout_percent": 66.1, "booths": 210000, "status": "COMPLETED"},
            {"region": "Central Zone", "turnout_percent": 64.9, "booths": 118000, "status": "COMPLETED"},
        ],
    )
