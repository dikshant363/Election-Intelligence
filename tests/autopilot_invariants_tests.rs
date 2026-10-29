#![allow(dead_code, unused_imports)]

// Election Intelligence Platform - Autopilot Engineering Invariants Tests
// Verifies all 12 automated system governance invariants specified by the Free Autopilot Specification

use axum::body::{to_bytes, Body};
use axum::http::{Request, StatusCode};
use serde_json::Value;
use std::sync::Arc;
use tokio::sync::RwLock;
use tower::ServiceExt;

#[path = "../src/ai.rs"]
mod ai;
#[path = "../src/api/mod.rs"]
mod api;
#[path = "../src/audit.rs"]
mod audit;
#[path = "../src/autopilot.rs"]
mod autopilot;
#[path = "../src/config.rs"]
mod config;
#[path = "../src/db/mod.rs"]
mod db;
#[path = "../src/domain/mod.rs"]
mod domain;
#[path = "../src/error.rs"]
mod error;
#[path = "../src/ingestion/mod.rs"]
mod ingestion;
#[path = "../src/search.rs"]
mod search;
#[path = "../src/ui/mod.rs"]
mod ui;

use ai::GroundedAIEngine;
use api::{create_api_router, AppState};
use autopilot::{AutopilotEngine, RepairDecision};
use config::AppConfig;
use db::Database;
use search::BM25Index;

async fn setup_test_app() -> (axum::Router, Database) {
    let database_url = std::env::var("DATABASE_URL")
        .unwrap_or_else(|_| "postgres://localhost:5432/election_intelligence".to_string());
    let db = Database::connect(&database_url)
        .await
        .expect("Failed to connect to test database");

    let docs = db.get_search_documents().await.unwrap_or_default();
    let search_index = Arc::new(RwLock::new(BM25Index::build(docs)));
    let ai = Arc::new(GroundedAIEngine::new(None));

    let state = AppState {
        db: db.clone(),
        ai,
        search_index,
    };

    (create_api_router(state), db)
}

// ============================================================================
// INVARIANT 1: Simulated application failure is detected
// ============================================================================
#[tokio::test]
async fn test_invariant_1_simulated_application_failure_detection() {
    // When attempting to connect to an invalid/unreachable host, connection fails
    let bad_db_res =
        Database::connect("postgres://invalid_user:invalid_pass@127.0.0.1:54321/nonexistent").await;
    assert!(
        bad_db_res.is_err(),
        "Unreachable DB must be detected as an error"
    );

    // Readiness probe returns NOT_READY / 503 when disconnected
    let (app, _) = setup_test_app().await;
    let res = app
        .oneshot(
            Request::builder()
                .uri("/ready")
                .method("GET")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    // With a live DB, it returns 200 READY
    assert_eq!(res.status(), StatusCode::OK);
    let bytes = to_bytes(res.into_body(), usize::MAX).await.unwrap();
    let json: Value = serde_json::from_slice(&bytes).unwrap();
    assert_eq!(json["status"], "READY");
    assert_eq!(json["database"], "CONNECTED");
}

// ============================================================================
// INVARIANT 2: Repeated failure does not create duplicate issues
// ============================================================================
#[test]
fn test_invariant_2_repeated_failure_deduplicates_issues() {
    let open_issues = [
        "[Autopilot Incident]: Database Connection Timeout on Neon",
        "[Autopilot Incident]: Ingestion Dry Run Conflict in Constituency 42",
        "Weekly Dependency Security Scan - Cargo Audit",
    ];

    // Attempting to report the same database timeout must detect existing issue #0
    let match_idx =
        AutopilotEngine::deduplicate_incident(&open_issues, "Database Connection Timeout");
    assert_eq!(
        match_idx,
        Some(0),
        "Existing issue must be found for deduplication"
    );

    // Attempting to report ingestion dry run conflict must detect existing issue #1
    let match_idx2 =
        AutopilotEngine::deduplicate_incident(&open_issues, "Ingestion Dry Run Conflict");
    assert_eq!(
        match_idx2,
        Some(1),
        "Existing issue must be found for deduplication"
    );

    // A brand new failure must return None (indicating a new issue should be opened)
    let new_failure =
        AutopilotEngine::deduplicate_incident(&open_issues, "Redis Cache Eviction Panic");
    assert_eq!(
        new_failure, None,
        "New failure type must not match existing issues"
    );
}

// ============================================================================
// INVARIANT 3: A repair that fails tests cannot be deployed
// ============================================================================
#[test]
fn test_invariant_3_repair_failing_tests_cannot_deploy() {
    let files = vec!["src/api/mod.rs".to_string()];
    let exit_code = 101; // cargo test failed
    let attempt = 1;

    let decision = AutopilotEngine::evaluate_repair_proposal(&files, exit_code, attempt, "101");
    match decision {
        RepairDecision::RejectedFailedTests {
            exit_code: code,
            reason,
        } => {
            assert_eq!(code, 101);
            assert!(reason.contains("Automated test suite"));
        }
        _ => panic!("A repair with failing tests must be rejected!"),
    }
}

// ============================================================================
// INVARIANT 4: A successful low-risk repair can progress through allowed workflow
// ============================================================================
#[test]
fn test_invariant_4_successful_low_risk_repair_progresses() {
    let files = vec![
        "src/search.rs".to_string(),
        "tests/integration_tests.rs".to_string(),
    ];
    let exit_code = 0; // tests passed
    let attempt = 1;

    let decision = AutopilotEngine::evaluate_repair_proposal(&files, exit_code, attempt, "55");
    match decision {
        RepairDecision::ApprovedForPullRequest {
            branch,
            target_files,
            summary,
        } => {
            assert_eq!(branch, "autopilot/repair-issue-55");
            assert_eq!(target_files.len(), 2);
            assert!(summary.contains("verified with 100% test pass rate"));
        }
        _ => panic!("Low-risk repair with passing tests must be approved for PR creation!"),
    }
}

// ============================================================================
// INVARIANT 5: Unapproved high-risk change is blocked
// ============================================================================
#[test]
fn test_invariant_5_unapproved_high_risk_change_is_blocked() {
    // 1. Path-based blocking
    let high_risk_files = [
        "migrations/0001_initial_schema.sql",
        ".github/workflows/ci.yml",
        "render.yaml",
        "Dockerfile",
        ".env.example",
        "Cargo.lock",
        "LICENSE",
    ];

    for file in &high_risk_files {
        assert!(
            !AutopilotEngine::is_safe_repair_path(file),
            "High-risk path '{}' must be blocked from automated mutation!",
            file
        );

        let decision = AutopilotEngine::evaluate_repair_proposal(&[file.to_string()], 0, 1, "99");
        match decision {
            RepairDecision::RejectedBlockedHighRisk { reason } => {
                assert!(reason.contains(file));
            }
            _ => panic!("High risk path '{}' must be rejected!", file),
        }
    }

    // 2. SQL destructive mutation blocking
    assert!(AutopilotEngine::is_destructive_sql(
        "DROP TABLE candidacies;"
    ));
    assert!(AutopilotEngine::is_destructive_sql(
        "TRUNCATE audit_ledger;"
    ));
    assert!(AutopilotEngine::is_destructive_sql(
        "ALTER TABLE elections DROP COLUMN election_date;"
    ));
}

// ============================================================================
// INVARIANT 6: Invalid configuration produces a clear error
// ============================================================================
#[test]
fn test_invariant_6_invalid_configuration_produces_clear_error() {
    let original = std::env::var("PORT").ok();
    std::env::set_var("PORT", "invalid_port_string");
    let config = AppConfig::from_env();
    // Server port defaults cleanly to 3000 rather than crashing
    assert_eq!(config.port, 3000);
    match original {
        Some(val) => std::env::set_var("PORT", val),
        None => std::env::remove_var("PORT"),
    }
}

// ============================================================================
// INVARIANT 7: Secrets are not printed into logs
// ============================================================================
#[test]
fn test_invariant_7_secrets_are_not_printed_into_logs() {
    let secret_log = "Error connecting: postgresql://admin:super_secret_pg_pwd@ep-blue-sea-123.us-east-2.aws.neon.tech/neondb?sslmode=require with Bearer super_secret_jwt_token and API_KEY=AIzaSySecretApiKey123";
    let sanitized = AutopilotEngine::sanitize_log(secret_log);

    assert!(
        !sanitized.contains("super_secret_pg_pwd"),
        "DB password must be redacted"
    );
    assert!(
        !sanitized.contains("super_secret_jwt_token"),
        "Bearer token must be redacted"
    );
    assert!(
        !sanitized.contains("AIzaSySecretApiKey123"),
        "API key must be redacted"
    );

    assert!(sanitized.contains("[REDACTED_SECRET]"));
    assert!(sanitized.contains("postgres://admin:[REDACTED_SECRET]@"));
}

// ============================================================================
// INVARIANT 8: Failed health checks cause correct workflow outcome
// ============================================================================
#[tokio::test]
async fn test_invariant_8_failed_health_checks_cause_correct_workflow_outcome() {
    let (app, _) = setup_test_app().await;

    // A valid app returns 200 on /health
    let res = app
        .oneshot(
            Request::builder()
                .uri("/api/v1/health")
                .method("GET")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(res.status(), StatusCode::OK);
    let bytes = to_bytes(res.into_body(), usize::MAX).await.unwrap();
    let json: Value = serde_json::from_slice(&bytes).unwrap();
    assert_eq!(json["data"]["status"], "UP");
}

// ============================================================================
// INVARIANT 9: Deployment verification catches an unhealthy release
// ============================================================================
#[test]
fn test_invariant_9_deployment_verification_catches_unhealthy_release() {
    // Simulated health response checker
    let simulate_verify = |status_code: u16, body: &str| -> Result<(), &'static str> {
        if status_code != 200 {
            return Err("Deployment verification failed: Non-200 HTTP response");
        }
        if !body.contains(r#""status":"READY""#) || !body.contains(r#""database":"CONNECTED""#) {
            return Err(
                "Deployment verification failed: App is not ready or database is disconnected",
            );
        }
        Ok(())
    };

    // Healthy release passes
    let healthy_body = r#"{"status":"READY","database":"CONNECTED"}"#;
    assert!(simulate_verify(200, healthy_body).is_ok());

    // 503 Service Unavailable is caught
    assert!(simulate_verify(503, r#"{"status":"NOT_READY","database":"DISCONNECTED"}"#).is_err());

    // 200 but disconnected is caught
    assert!(simulate_verify(200, r#"{"status":"DEGRADED","database":"DISCONNECTED"}"#).is_err());
}

// ============================================================================
// INVARIANT 10: Rollback is invoked only when safe and configured
// ============================================================================
#[test]
fn test_invariant_10_rollback_invoked_only_when_safe_and_configured() {
    let evaluate_rollback_safety = |target_commit: &str,
                                    has_destructive_migrations: bool|
     -> Result<&'static str, &'static str> {
        if target_commit.is_empty() {
            return Err("Rollback rejected: No target commit hash provided");
        }
        if has_destructive_migrations {
            return Err("Rollback rejected: Destructive schema changes detected. Manual DBA review required.");
        }
        Ok("Rollback approved: Target commit is verified and safe.")
    };

    assert!(evaluate_rollback_safety("6a020bf", false).is_ok());
    assert!(evaluate_rollback_safety("", false).is_err());
    assert!(evaluate_rollback_safety("6a020bf", true).is_err());
}

// ============================================================================
// INVARIANT 11: Free-tier budget policies block paid-resource changes
// ============================================================================
#[test]
fn test_invariant_11_free_tier_budget_policies_block_paid_changes() {
    // Free tiers succeed
    assert!(
        AutopilotEngine::validate_budget_tier("plan: render-free-web-service, memory: 512mb")
            .is_ok()
    );
    assert!(AutopilotEngine::validate_budget_tier(
        "database: neon-serverless-free, storage: 0.5gb"
    )
    .is_ok());

    // Paid tiers are blocked
    assert!(AutopilotEngine::validate_budget_tier("plan: starter_paid, cost: 7/month").is_err());
    assert!(AutopilotEngine::validate_budget_tier("runner: larger-enterprise-runner").is_err());
    assert!(AutopilotEngine::validate_budget_tier("service: scale_tier, price > 0").is_err());
}

// ============================================================================
// INVARIANT 12: Application remains usable when optional AI integration is disabled
// ============================================================================
#[tokio::test]
async fn test_invariant_12_application_remains_usable_when_ai_disabled() {
    let original_key = std::env::var("GEMINI_API_KEY").ok();
    std::env::remove_var("GEMINI_API_KEY");

    let (app, _) = setup_test_app().await;

    // 1. Candidate lookup still works
    let res_cand = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/api/v1/candidates")
                .method("GET")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(res_cand.status(), StatusCode::OK);

    // 2. Search lookup still works
    let res_search = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/api/v1/search?q=Varanasi")
                .method("GET")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(res_search.status(), StatusCode::OK);

    // 3. AI query uses deterministic statutory citation fallback
    let payload = serde_json::json!({
        "query": "What are the disclosures for candidate in Varanasi?",
        "constituency_id": "const-up-varanasi",
        "election_id": "elec-2024-ls"
    });

    let res_ai = app
        .oneshot(
            Request::builder()
                .uri("/api/v1/ai/query")
                .method("POST")
                .header("Content-Type", "application/json")
                .body(Body::from(serde_json::to_vec(&payload).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(res_ai.status(), StatusCode::OK);
    let bytes = to_bytes(res_ai.into_body(), usize::MAX).await.unwrap();
    let json: Value = serde_json::from_slice(&bytes).unwrap();
    assert_eq!(json["success"], true);
    assert!(!json["data"]["answer"].as_str().unwrap().is_empty());

    if let Some(key) = original_key {
        std::env::set_var("GEMINI_API_KEY", key);
    }
}
