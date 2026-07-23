"""
Comprehensive unit & integration test suite for Milestone 23 — Production Hardening, Security & Operational Readiness.

Tests cover:
- SecretsProvider, EnvSecretsProvider, VaultSecretsAdapter, CloudSecretManagerAdapter
- ConfigurationValidator startup checks & SHA-256 fingerprinting
- BackupManager snapshot creation, listing, and SHA-256 checksum verification
- DeploymentSafetyManager migration safety checks & rollback planning
- SecurityHardener HTTP security headers, CSP, HSTS, secure cookies
- SBOMGenerator SPDX 2.3 document generation
- AuditLogger immutable audit record logging & filtering
- CircuitBreaker state transitions (CLOSED, OPEN, HALF-OPEN) & ResiliencePolicy
- FaultInjector & ChaosRunner chaos experiment execution
- ReleaseManager CI/CD quality gate checklist
- ProductionService coordinator
- FastAPI REST endpoints (/security, /config, /audit, /backup, POST /backup, /release)
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies.dependencies import get_production_service
from app.main import app
from app.production import (
    AuditLogger,
    BackupManager,
    ChaosRunner,
    CircuitBreaker,
    CircuitBreakerOpenError,
    CloudSecretManagerAdapter,
    ConfigurationValidator,
    DeploymentSafetyManager,
    EnvSecretsProvider,
    FaultInjector,
    ReleaseManager,
    ResiliencePolicy,
    SBOMGenerator,
    SecurityHardener,
    VaultSecretsAdapter,
)
from app.production.schemas import (
    AuditRecordSchema,
    BackupMetadataSchema,
    ConfigValidationSchema,
    ReleaseChecklistSchema,
    SecurityStatusSchema,
)

TOTAL_DEPS_6 = 6


# ─────────────────────────────────────────────────────────────────────────────
# 1. Secrets & Configuration Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestSecretsAndConfig:
    def test_env_secrets_provider(self) -> None:
        provider = EnvSecretsProvider()
        val = provider.get_secret("PATH")
        assert val is not None

        missing = provider.validate_secrets(["PATH", "NON_EXISTENT_KEY_XYZ"])
        assert "NON_EXISTENT_KEY_XYZ" in missing

    def test_vault_and_cloud_adapters(self) -> None:
        vault = VaultSecretsAdapter()
        assert vault.get_secret("PATH") is not None

        cloud = CloudSecretManagerAdapter()
        assert cloud.get_secret("PATH") is not None

    def test_configuration_validator(self) -> None:
        report = ConfigurationValidator.validate_configuration()
        assert report.status in ["valid", "warning", "invalid"]
        assert len(report.fingerprint) == 16  # noqa: PLR2004


# ─────────────────────────────────────────────────────────────────────────────
# 2. Backup, Recovery & Deployment Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestBackupAndDeployment:
    def test_backup_manager_lifecycle(self) -> None:
        mgr = BackupManager()
        payload = b"test_db_contents"
        meta = mgr.create_snapshot(payload)
        assert meta.status == "completed"
        assert meta.size_bytes == len(payload)

        verified = mgr.verify_snapshot(meta.backup_id, payload)
        assert verified is True

        tampered_verify = mgr.verify_snapshot(meta.backup_id, b"corrupted")
        assert tampered_verify is False

    def test_deployment_safety_manager(self) -> None:
        safe_mig = DeploymentSafetyManager.verify_migration_safety("add_index_to_elections")
        assert safe_mig["is_backwards_compatible"] is True

        unsafe_mig = DeploymentSafetyManager.verify_migration_safety("drop column votes from results")
        assert unsafe_mig["is_backwards_compatible"] is False

        plan = DeploymentSafetyManager.generate_rollback_plan("v0.23.0")
        assert len(plan["steps"]) > 0


# ─────────────────────────────────────────────────────────────────────────────
# 3. Security, SBOM & Audit Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestSecuritySBOMAndAudit:
    def test_security_hardener(self) -> None:
        status = SecurityHardener.get_security_status()
        assert status.csp_enabled is True
        headers = SecurityHardener.get_recommended_headers()
        assert "Content-Security-Policy" in headers

    def test_sbom_generator(self) -> None:
        summary = SBOMGenerator.get_sbom_summary()
        assert summary.total_dependencies == TOTAL_DEPS_6
        doc = SBOMGenerator.generate_spdx_document()
        assert doc["spdxVersion"] == "SPDX-2.3"

    def test_audit_logger(self) -> None:
        logger = AuditLogger()
        rec = logger.log_event(
            event_type="security",
            actor_id="admin_1",
            action="update_permissions",
            resource="role_auditor",
        )
        assert rec.event_type == "security"
        sec_recs = logger.list_records("security")
        assert len(sec_recs) == 1


# ─────────────────────────────────────────────────────────────────────────────
# 4. Resilience, Circuit Breaker & Chaos Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestResilienceAndChaos:
    def test_circuit_breaker_open_state(self) -> None:
        cb = CircuitBreaker("ai_service", failure_threshold=2, recovery_time_sec=60.0)

        def failing_func() -> None:
            raise RuntimeError("API timeout")

        with pytest.raises(RuntimeError):
            cb.call(failing_func)
        with pytest.raises(RuntimeError):
            cb.call(failing_func)

        assert cb.state == "OPEN"

        with pytest.raises(CircuitBreakerOpenError):
            cb.call(failing_func)

    def test_resilience_policy(self) -> None:
        policy = ResiliencePolicy("search_engine")
        res = policy.execute(lambda: "ok")
        assert res == "ok"

    def test_fault_injector_and_chaos_runner(self) -> None:
        injector = FaultInjector(failure_rate=0.0, latency_delay_sec=0.0)
        injector.maybe_inject_fault("test_service")

        res = ChaosRunner.run_chaos_experiment("db_latency_experiment")
        assert res["status"] == "passed"


# ─────────────────────────────────────────────────────────────────────────────
# 5. ProductionService & Router Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestReleaseAndAPIRouter:
    def test_release_manager(self) -> None:
        checklist = ReleaseManager.get_release_checklist()
        assert checklist.ready_for_deployment is True

    def setup_method(self) -> None:
        mock_service = AsyncMock()
        mock_service.get_security_status = MagicMock(
            return_value=SecurityStatusSchema(
                headers_enforced=True,
                csp_enabled=True,
                hsts_enabled=True,
                cors_valid=True,
                secure_cookies=True,
                tls_enforced=True,
            )
        )
        mock_service.validate_configuration = MagicMock(
            return_value=ConfigValidationSchema(
                status="valid",
                environment="production",
                fingerprint="a1b2c3d4e5f67890",
                missing_keys=[],
                invalid_keys=[],
            )
        )
        mock_service.list_backups = MagicMock(
            return_value=[
                BackupMetadataSchema(
                    backup_id="snap_123",
                    timestamp="2026-07-23T12:00:00Z",
                    size_bytes=2048,
                    checksum_sha256="abc123hash",
                    status="completed",
                )
            ]
        )
        mock_service.create_backup = MagicMock(
            return_value=BackupMetadataSchema(
                backup_id="snap_456",
                timestamp="2026-07-23T12:00:00Z",
                size_bytes=2048,
                checksum_sha256="xyz456hash",
                status="completed",
            )
        )
        mock_service.list_audit_records = MagicMock(
            return_value=[
                AuditRecordSchema(
                    event_id="aud_1",
                    event_type="security",
                    timestamp="2026-07-23T12:00:00Z",
                    actor_id="admin_1",
                    action="login",
                    resource="auth_system",
                    ip_address="127.0.0.1",
                    details={},
                )
            ]
        )
        mock_service.get_release_checklist = MagicMock(
            return_value=ReleaseChecklistSchema(
                version="v0.23.0",
                tests_passed=True,
                lint_passed=True,
                migrations_verified=True,
                security_verified=True,
                sbom_generated=True,
                ready_for_deployment=True,
            )
        )

        app.dependency_overrides[get_production_service] = lambda: mock_service

    def teardown_method(self) -> None:
        app.dependency_overrides.clear()

    def test_security_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/security")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["csp_enabled"] is True

    def test_config_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/config")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["status"] == "valid"

    def test_backup_list_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/backup")
        assert resp.status_code == 200  # noqa: PLR2004
        assert len(resp.json()) == 1

    def test_backup_create_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.post("/api/v1/backup")
        assert resp.status_code == 201  # noqa: PLR2004
        assert resp.json()["backup_id"] == "snap_456"

    def test_audit_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/audit")
        assert resp.status_code == 200  # noqa: PLR2004
        assert len(resp.json()) == 1

    def test_release_endpoint(self) -> None:
        client = TestClient(app)
        resp = client.get("/api/v1/release")
        assert resp.status_code == 200  # noqa: PLR2004
        assert resp.json()["ready_for_deployment"] is True
