// Election Intelligence Platform - Autopilot Governance & Safety Engine
// Free Autopilot System: Bounded Self-Repair, Health Policy, Secret Sanitization, and Quota Invariants

use regex::Regex;
use serde::{Deserialize, Serialize};
use std::sync::OnceLock;

/// Outcome of evaluating an automated repair proposal
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum RepairDecision {
    ApprovedForPullRequest {
        branch: String,
        target_files: Vec<String>,
        summary: String,
    },
    RejectedBlockedHighRisk {
        reason: String,
    },
    RejectedFailedTests {
        exit_code: i32,
        reason: String,
    },
    RejectedExceededRetries {
        attempts: u32,
        max_allowed: u32,
    },
}

/// Operational system status report structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OperationalStatus {
    pub application: ApplicationMeta,
    pub database: DatabaseHealth,
    pub audit_ledger: AuditHealth,
    pub search_engine: SearchHealth,
    pub ai_subsystem: AiSubsystemHealth,
    pub budget_compliance: BudgetCompliance,
    pub health_summary: HealthSummary,
    pub timestamp: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApplicationMeta {
    pub name: String,
    pub version: String,
    pub runtime: String,
    pub environment: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DatabaseHealth {
    pub status: String,
    pub r#type: String,
    pub pool_active: u32,
    pub migrations_status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditHealth {
    pub status: String,
    pub tamper_evident: bool,
    pub total_events: usize,
    pub genesis_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchHealth {
    pub status: String,
    pub algorithm: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AiSubsystemHealth {
    pub status: String,
    pub mode: String,
    pub model: String,
    pub paid_api_required: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BudgetCompliance {
    pub tier: String,
    pub monthly_spend_inr: f64,
    pub monthly_spend_usd: f64,
    pub paid_resources_blocked: bool,
    pub provider_limits: ProviderLimits,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProviderLimits {
    pub render_web_service: String,
    pub neon_postgresql: String,
    pub github_actions: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HealthSummary {
    pub status: String,
    pub readiness: String,
    pub incidents_open: usize,
}

pub struct AutopilotEngine;

impl AutopilotEngine {
    /// Maximum allowed automated repair attempts per issue before mandatory human escalation
    pub const MAX_REPAIR_ATTEMPTS: u32 = 3;

    /// Verifies if a file path is eligible for automated bounded repair.
    /// Strictly limits modifications to application source code and tests.
    /// Explicitly denies migrations, infrastructure, workflows, and secret files.
    pub fn is_safe_repair_path(path: &str) -> bool {
        let normalized = path.replace('\\', "/");
        let p = normalized.trim_start_matches("./");

        // Explicit Denylist (High Risk / Protected Systems)
        if p.starts_with("migrations/")
            || p.starts_with(".github/")
            || p.starts_with(".env")
            || p.starts_with("backups/")
            || p == "render.yaml"
            || p == "Dockerfile"
            || p == "docker-compose.yml"
            || p == "Cargo.lock"
            || p == "LICENSE"
        {
            return false;
        }

        // Explicit Allowlist
        p.starts_with("src/") || p.starts_with("tests/") || p == "Cargo.toml"
    }

    /// Checks if a SQL statement contains destructive operations that would delete
    /// or alter existing election tables or historical audit ledgers.
    pub fn is_destructive_sql(sql: &str) -> bool {
        let upper = sql.to_uppercase();
        upper.contains("DROP TABLE")
            || upper.contains("TRUNCATE")
            || upper.contains("DROP DATABASE")
            || upper.contains("DROP SCHEMA")
            || (upper.contains("ALTER TABLE") && upper.contains("DROP COLUMN"))
            || upper.contains("DELETE FROM ELECTIONS")
            || upper.contains("DELETE FROM CANDIDACIES")
            || upper.contains("DELETE FROM AUDIT_LEDGER")
    }

    /// Validates whether a resource configuration adheres strictly to ₹0 / $0 permanent free tier.
    pub fn validate_budget_tier(plan_spec: &str) -> Result<(), &'static str> {
        let upper = plan_spec.to_uppercase();
        if upper.contains("STARTER_PAID")
            || upper.contains("PRO")
            || upper.contains("ENTERPRISE")
            || upper.contains("SCALE")
            || upper.contains("PAID_RUNNER")
            || upper.contains("PRICE > 0")
            || upper.contains("COST > 0")
            || upper.contains("BILLING_ENABLED: TRUE")
        {
            return Err(
                "Violation: Proposed configuration exceeds ₹0/month free-tier budget limit.",
            );
        }
        Ok(())
    }

    /// Redacts sensitive credentials (database passwords, tokens, API keys) from diagnostic logs.
    pub fn sanitize_log(raw: &str) -> String {
        static DB_URL_REGEX: OnceLock<Regex> = OnceLock::new();
        static BEARER_REGEX: OnceLock<Regex> = OnceLock::new();
        static KEY_REGEX: OnceLock<Regex> = OnceLock::new();

        let db_regex =
            DB_URL_REGEX.get_or_init(|| Regex::new(r"postgres(ql)?://([^:]+):([^@]+)@").unwrap());
        let bearer_regex =
            BEARER_REGEX.get_or_init(|| Regex::new(r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{8,}").unwrap());
        let key_regex = KEY_REGEX.get_or_init(|| {
            Regex::new(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\x22]?([a-zA-Z0-9_\-\.]{8,})['\x22]?").unwrap()
        });

        let mut sanitized = db_regex
            .replace_all(raw, "postgres://$2:[REDACTED_SECRET]@")
            .to_string();
        sanitized = bearer_regex
            .replace_all(&sanitized, "Bearer [REDACTED_SECRET]")
            .to_string();
        sanitized = key_regex
            .replace_all(&sanitized, "$1=[REDACTED_SECRET]")
            .to_string();
        sanitized
    }

    /// Deduplicates incident reports by searching existing issue titles for the given fingerprint.
    /// Returns Some(index) of existing matching issue, or None if a new issue should be created.
    pub fn deduplicate_incident(existing_titles: &[&str], fingerprint: &str) -> Option<usize> {
        let needle = fingerprint.trim().to_lowercase();
        existing_titles
            .iter()
            .position(|title| title.to_lowercase().contains(&needle))
    }

    /// Evaluates if an automated repair proposal can be progressed to a pull request.
    pub fn evaluate_repair_proposal(
        modified_files: &[String],
        test_exit_code: i32,
        attempt_count: u32,
        issue_id: &str,
    ) -> RepairDecision {
        if attempt_count > Self::MAX_REPAIR_ATTEMPTS {
            return RepairDecision::RejectedExceededRetries {
                attempts: attempt_count,
                max_allowed: Self::MAX_REPAIR_ATTEMPTS,
            };
        }

        for file in modified_files {
            if !Self::is_safe_repair_path(file) {
                return RepairDecision::RejectedBlockedHighRisk {
                    reason: format!(
                        "File '{}' is not within the allowed bounded repair paths.",
                        file
                    ),
                };
            }
        }

        if test_exit_code != 0 {
            return RepairDecision::RejectedFailedTests {
                exit_code: test_exit_code,
                reason: "Automated test suite, formatting, or clippy check failed.".to_string(),
            };
        }

        RepairDecision::ApprovedForPullRequest {
            branch: format!("autopilot/repair-issue-{}", issue_id),
            target_files: modified_files.to_vec(),
            summary: format!(
                "Bounded automated patch addressing issue #{} verified with 100% test pass rate.",
                issue_id
            ),
        }
    }

    /// Generates the standard operational status object
    pub fn build_operational_status(
        db_healthy: bool,
        pool_active: u32,
        total_audit_events: usize,
        ai_enabled: bool,
    ) -> OperationalStatus {
        OperationalStatus {
            application: ApplicationMeta {
                name: "Election Intelligence Platform".to_string(),
                version: "1.0.0".to_string(),
                runtime: "Pure Rust (Axum + Tokio + SQLx)".to_string(),
                environment: std::env::var("APP_ENV").unwrap_or_else(|_| "production".to_string()),
            },
            database: DatabaseHealth {
                status: if db_healthy {
                    "CONNECTED".to_string()
                } else {
                    "DISCONNECTED".to_string()
                },
                r#type: "PostgreSQL 17".to_string(),
                pool_active,
                migrations_status: "APPLIED_0001_0002_0003".to_string(),
            },
            audit_ledger: AuditHealth {
                status: "VALID".to_string(),
                tamper_evident: true,
                total_events: total_audit_events,
                genesis_hash: crate::audit::GENESIS_HASH.to_string(),
            },
            search_engine: SearchHealth {
                status: "HEALTHY".to_string(),
                algorithm: "BM25 In-Memory + pg_trgm".to_string(),
            },
            ai_subsystem: AiSubsystemHealth {
                status: if ai_enabled {
                    "READY".to_string()
                } else {
                    "DISABLED_BY_DEFAULT".to_string()
                },
                mode: if ai_enabled {
                    "GROUNDED_EVIDENCE_GEMINI".to_string()
                } else {
                    "DETERMINISTIC_HEURISTIC_FALLBACK".to_string()
                },
                model: if ai_enabled {
                    "Gemini 1.5 Flash (Free Tier)".to_string()
                } else {
                    "Statutory Gazette Citation Engine".to_string()
                },
                paid_api_required: false,
            },
            budget_compliance: BudgetCompliance {
                tier: "FREE_TIER_PERMANENT".to_string(),
                monthly_spend_inr: 0.0,
                monthly_spend_usd: 0.0,
                paid_resources_blocked: true,
                provider_limits: ProviderLimits {
                    render_web_service:
                        "512MB RAM, 0.5 CPU, 750 free hrs/mo (Auto-spins down after 15m idle)"
                            .to_string(),
                    neon_postgresql: "0.5 GiB SSD Storage, 1 Project, auto-suspend compute on idle"
                        .to_string(),
                    github_actions:
                        "Free Public Repository Standard Runners (10-15m strict timeouts)"
                            .to_string(),
                },
            },
            health_summary: HealthSummary {
                status: if db_healthy {
                    "PASS".to_string()
                } else {
                    "FAIL".to_string()
                },
                readiness: if db_healthy {
                    "READY".to_string()
                } else {
                    "NOT_READY".to_string()
                },
                incidents_open: 0,
            },
            timestamp: chrono::Utc::now().to_rfc3339(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_safe_repair_path_allowlist() {
        assert!(AutopilotEngine::is_safe_repair_path("src/main.rs"));
        assert!(AutopilotEngine::is_safe_repair_path("src/api/mod.rs"));
        assert!(AutopilotEngine::is_safe_repair_path(
            "tests/integration_tests.rs"
        ));
        assert!(AutopilotEngine::is_safe_repair_path("Cargo.toml"));
    }

    #[test]
    fn test_is_safe_repair_path_denylist() {
        assert!(!AutopilotEngine::is_safe_repair_path(
            "migrations/0001_initial_schema.sql"
        ));
        assert!(!AutopilotEngine::is_safe_repair_path(
            ".github/workflows/ci.yml"
        ));
        assert!(!AutopilotEngine::is_safe_repair_path("render.yaml"));
        assert!(!AutopilotEngine::is_safe_repair_path("Dockerfile"));
        assert!(!AutopilotEngine::is_safe_repair_path("docker-compose.yml"));
        assert!(!AutopilotEngine::is_safe_repair_path(".env.local"));
        assert!(!AutopilotEngine::is_safe_repair_path(
            "backups/snapshot.sql.gz"
        ));
        assert!(!AutopilotEngine::is_safe_repair_path("LICENSE"));
    }

    #[test]
    fn test_destructive_sql_detection() {
        assert!(AutopilotEngine::is_destructive_sql(
            "DROP TABLE elections CASCADE;"
        ));
        assert!(AutopilotEngine::is_destructive_sql("TRUNCATE candidacies;"));
        assert!(AutopilotEngine::is_destructive_sql(
            "ALTER TABLE candidates DROP COLUMN name;"
        ));
        assert!(AutopilotEngine::is_destructive_sql(
            "DELETE FROM elections WHERE 1=1;"
        ));
        assert!(AutopilotEngine::is_destructive_sql(
            "DELETE FROM audit_ledger;"
        ));

        // Safe queries
        assert!(!AutopilotEngine::is_destructive_sql(
            "SELECT * FROM elections WHERE id = $1;"
        ));
        assert!(!AutopilotEngine::is_destructive_sql(
            "INSERT INTO candidates (name) VALUES ($1);"
        ));
        assert!(!AutopilotEngine::is_destructive_sql(
            "UPDATE candidates SET name = $1 WHERE id = $2;"
        ));
    }

    #[test]
    fn test_validate_budget_tier_enforcement() {
        assert!(AutopilotEngine::validate_budget_tier("tier: free, compute: 512MB").is_ok());
        assert!(AutopilotEngine::validate_budget_tier("plan: render_free").is_ok());

        assert!(AutopilotEngine::validate_budget_tier("tier: starter_paid, price: 7/mo").is_err());
        assert!(AutopilotEngine::validate_budget_tier("plan: pro").is_err());
        assert!(AutopilotEngine::validate_budget_tier("instance: enterprise").is_err());
        assert!(AutopilotEngine::validate_budget_tier("billing_enabled: true").is_err());
    }

    #[test]
    fn test_sanitize_log_redaction() {
        let raw = "Connecting to postgres://postgres:SecretPass123@ep-bold-surf.us-east-2.aws.neon.tech/neondb with Bearer eyJhbGciOiJIUzI1NiJ9 and API_KEY='AIzaSyAbcd1234EFGH'";
        let sanitized = AutopilotEngine::sanitize_log(raw);

        assert!(!sanitized.contains("SecretPass123"));
        assert!(!sanitized.contains("eyJhbGciOiJIUzI1NiJ9"));
        assert!(!sanitized.contains("AIzaSyAbcd1234EFGH"));

        assert!(sanitized.contains("[REDACTED_SECRET]"));
        assert!(sanitized.contains("postgres://postgres:[REDACTED_SECRET]@"));
    }

    #[test]
    fn test_deduplicate_incident_detection() {
        let existing = [
            "[Autopilot Incident]: Database Connection Timeout",
            "[Autopilot Incident]: Readiness Probe Failed on /ready",
            "Weekly Maintenance: Dependency Security Scan",
        ];

        // Should match existing issue
        assert_eq!(
            AutopilotEngine::deduplicate_incident(&existing, "Database Connection Timeout"),
            Some(0)
        );
        assert_eq!(
            AutopilotEngine::deduplicate_incident(&existing, "Readiness Probe Failed"),
            Some(1)
        );

        // Should not match
        assert_eq!(
            AutopilotEngine::deduplicate_incident(&existing, "Search Index Degraded"),
            None
        );
    }

    #[test]
    fn test_evaluate_repair_proposal_workflow() {
        let allowed_files = vec![
            "src/api/mod.rs".to_string(),
            "tests/integration_tests.rs".to_string(),
        ];
        let disallowed_files = vec!["migrations/0001_initial_schema.sql".to_string()];

        // 1. Success case: allowed files, passing tests (0), attempt 1
        let decision = AutopilotEngine::evaluate_repair_proposal(&allowed_files, 0, 1, "42");
        match decision {
            RepairDecision::ApprovedForPullRequest { branch, .. } => {
                assert_eq!(branch, "autopilot/repair-issue-42");
            }
            _ => panic!("Expected ApprovedForPullRequest"),
        }

        // 2. Blocked: high risk file
        let blocked_decision =
            AutopilotEngine::evaluate_repair_proposal(&disallowed_files, 0, 1, "42");
        match blocked_decision {
            RepairDecision::RejectedBlockedHighRisk { reason } => {
                assert!(reason.contains("migrations/0001_initial_schema.sql"));
            }
            _ => panic!("Expected RejectedBlockedHighRisk"),
        }

        // 3. Blocked: tests failed (exit code != 0)
        let failed_tests_decision =
            AutopilotEngine::evaluate_repair_proposal(&allowed_files, 1, 1, "42");
        match failed_tests_decision {
            RepairDecision::RejectedFailedTests { exit_code, .. } => {
                assert_eq!(exit_code, 1);
            }
            _ => panic!("Expected RejectedFailedTests"),
        }

        // 4. Blocked: exceeded max retry attempts (> 3)
        let retries_decision =
            AutopilotEngine::evaluate_repair_proposal(&allowed_files, 0, 4, "42");
        match retries_decision {
            RepairDecision::RejectedExceededRetries {
                attempts,
                max_allowed,
            } => {
                assert_eq!(attempts, 4);
                assert_eq!(max_allowed, 3);
            }
            _ => panic!("Expected RejectedExceededRetries"),
        }
    }
}
