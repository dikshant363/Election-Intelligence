"""Unit and integration tests for the Enterprise Control Center admin router."""

from fastapi import status
from fastapi.testclient import TestClient

from app.identity.services.jwt_service import JwtService
from app.identity.services.rbac_service import RoleHierarchy
from app.main import app


def get_auth_headers():
    token = JwtService.create_access_token(
        subject="test_admin",
        roles=[RoleHierarchy.PLATFORM_ADMIN],
        permissions=[]
    )
    return {"Authorization": f"Bearer {token}"}


client = TestClient(app)


def test_get_admin_overview():
    """Test retrieving consolidated Enterprise Control Center overview telemetry."""
    response = client.get("/api/v1/admin/overview", headers=get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["platform_name"] == "Election Intelligence Platform"
    assert data["version"] == "1.0.0"
    assert "system_health" in data
    assert "entity_counts" in data
    assert data["entity_counts"]["elections"] == 24


def test_get_feature_flags():
    """Test listing platform feature flags."""
    response = client.get("/api/v1/admin/feature-flags", headers=get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    flag_names = [item["name"] for item in data]
    assert "enable_rag" in flag_names
    assert "enable_websockets" in flag_names


def test_toggle_feature_flag():
    """Test toggling feature flag state."""
    # Turn off enable_chaos_testing
    response = client.post(
        "/api/v1/admin/feature-flags/enable_chaos_testing/toggle",
        json={"enabled": True},
        headers=get_auth_headers(),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "enable_chaos_testing"
    assert data["enabled"] is True

    # Revert back
    client.post(
        "/api/v1/admin/feature-flags/enable_chaos_testing/toggle",
        json={"enabled": False},
        headers=get_auth_headers(),
    )


def test_toggle_nonexistent_feature_flag():
    """Test toggling a non-existent feature flag returns 404."""
    response = client.post(
        "/api/v1/admin/feature-flags/non_existent_flag/toggle",
        json={"enabled": True},
        headers=get_auth_headers(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_admin_users():
    """Test listing administrative user accounts and roles."""
    response = client.get("/api/v1/admin/security/users", headers=get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4
    roles = [user["role"] for user in data]
    assert "Super Administrator" in roles
    assert "Election Administrator" in roles


def test_get_audit_logs():
    """Test querying security audit log entries."""
    response = client.get("/api/v1/admin/security/audit-logs?limit=2", headers=get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert "actor" in data[0]
    assert "action" in data[0]


def test_get_ai_status():
    """Test retrieving AI control center status."""
    response = client.get("/api/v1/admin/ai/status", headers=get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["active_provider"] == "openai"
    assert data["active_model"] == "gpt-4o"
    assert "available_providers" in data


def test_ops_flush_cache():
    """Test triggering manual cache eviction."""
    response = client.post("/api/v1/admin/ops/flush-cache", headers=get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "SUCCESS"


def test_ops_trigger_reindex():
    """Test triggering search reindexing."""
    response = client.post("/api/v1/admin/ops/reindex", headers=get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "SUCCESS"


def test_get_executive_kpis():
    """Test retrieving Executive Command Center strategic KPIs."""
    response = client.get("/api/v1/admin/executive/kpis", headers=get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_elections_managed"] == 24
    assert data["total_voters_registered"] == 968800000
    assert "regional_insights" in data
    assert len(data["regional_insights"]) == 5
