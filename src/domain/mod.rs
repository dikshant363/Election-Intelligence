// Election Intelligence Platform - Domain Entities & Invariants
// Comprehensive models reflecting the Evidence-First PostgreSQL Schema

use chrono::NaiveDate;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[allow(non_camel_case_types, dead_code, clippy::upper_case_acronyms)]
pub enum ElectionType {
    GENERAL,
    ASSEMBLY,
    BY_ELECTION,
    MUNICIPAL,
}

#[allow(dead_code)]
impl ElectionType {
    pub fn as_str(&self) -> &'static str {
        match self {
            ElectionType::GENERAL => "GENERAL",
            ElectionType::ASSEMBLY => "ASSEMBLY",
            ElectionType::BY_ELECTION => "BY_ELECTION",
            ElectionType::MUNICIPAL => "MUNICIPAL",
        }
    }

    pub fn from_str_opt(s: &str) -> Option<Self> {
        match s.to_uppercase().as_str() {
            "GENERAL" => Some(ElectionType::GENERAL),
            "ASSEMBLY" => Some(ElectionType::ASSEMBLY),
            "BY_ELECTION" | "BY-ELECTION" => Some(ElectionType::BY_ELECTION),
            "MUNICIPAL" => Some(ElectionType::MUNICIPAL),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[allow(dead_code, clippy::upper_case_acronyms)]
pub enum ElectionStatus {
    SCHEDULED,
    ACTIVE,
    COMPLETED,
    CANCELLED,
}

#[allow(dead_code)]
impl ElectionStatus {
    pub fn as_str(&self) -> &'static str {
        match self {
            ElectionStatus::SCHEDULED => "SCHEDULED",
            ElectionStatus::ACTIVE => "ACTIVE",
            ElectionStatus::COMPLETED => "COMPLETED",
            ElectionStatus::CANCELLED => "CANCELLED",
        }
    }

    pub fn from_str_opt(s: &str) -> Option<Self> {
        match s.to_uppercase().as_str() {
            "SCHEDULED" => Some(ElectionStatus::SCHEDULED),
            "ACTIVE" => Some(ElectionStatus::ACTIVE),
            "COMPLETED" => Some(ElectionStatus::COMPLETED),
            "CANCELLED" => Some(ElectionStatus::CANCELLED),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Election {
    pub id: String,
    pub title: String,
    pub election_type: String,
    pub start_date: String,
    pub end_date: String,
    pub status: String,
    pub total_registered_voters: i64,
    pub turnout_percentage: f64,
    pub total_constituencies: i32,
    pub phases: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ElectionCreateRequest {
    pub title: String,
    pub election_type: String,
    pub start_date: String,
    pub end_date: String,
    pub total_registered_voters: i64,
    pub total_constituencies: i32,
    pub phases: i32,
}

impl ElectionCreateRequest {
    pub fn validate(&self) -> Result<(), String> {
        if self.title.trim().is_empty() {
            return Err("Election title cannot be empty.".to_string());
        }
        if self.total_registered_voters < 0 {
            return Err("Total registered voters cannot be negative.".to_string());
        }
        if self.total_constituencies <= 0 {
            return Err("Total constituencies must be greater than zero.".to_string());
        }
        if self.phases <= 0 {
            return Err("Election phases must be at least 1.".to_string());
        }
        let start = NaiveDate::parse_from_str(&self.start_date, "%Y-%m-%d")
            .map_err(|_| "Invalid start_date format, expected YYYY-MM-DD.".to_string())?;
        let end = NaiveDate::parse_from_str(&self.end_date, "%Y-%m-%d")
            .map_err(|_| "Invalid end_date format, expected YYYY-MM-DD.".to_string())?;
        if end < start {
            return Err("Election end_date cannot be earlier than start_date.".to_string());
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Constituency {
    pub id: String,
    pub name: String,
    pub code: String,
    pub state_code: String,
    pub state_name: String,
    pub constituency_type: String,
    pub total_voters: i64,
    pub total_booths: i32,
    pub reserved_category: String,
    pub phase: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Party {
    pub id: String,
    pub name: String,
    pub code: String,
    pub symbol: String,
    pub color: String,
    pub founded_year: i32,
    pub seats_contested: i32,
    pub seats_won: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CriminalCaseDetail {
    pub case_no: String,
    pub court: String,
    pub sections: String,
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CandidateView {
    pub id: String,
    pub name: String,
    pub age: i32,
    pub email: String,
    pub phone: String,
    pub constituency_id: String,
    pub constituency_name: Option<String>,
    pub party_id: String,
    pub party_name: Option<String>,
    pub party_symbol: Option<String>,
    pub party_color: Option<String>,
    pub education: String,
    pub declared_assets_cr: f64,
    pub declared_liabilities_cr: f64,
    pub criminal_cases: i32,
    pub criminal_cases_details: Vec<CriminalCaseDetail>,
    pub affidavit_status: String,
    pub submission_date: String,
    pub source_ref: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CandidateCreateRequest {
    pub name: String,
    pub age: i32,
    pub email: String,
    pub phone: String,
    pub constituency_id: String,
    pub party_id: String,
    pub education: String,
    pub declared_assets_cr: f64,
    pub criminal_cases: i32,
}

impl CandidateCreateRequest {
    pub fn validate(&self) -> Result<(), String> {
        if self.name.trim().is_empty() {
            return Err("Candidate name cannot be empty.".to_string());
        }
        // Constitutional age requirement for Lok Sabha / Vidhan Sabha is 25 years
        if self.age < 25 {
            return Err(
                "Candidate age must be at least 25 years under the Constitution of India."
                    .to_string(),
            );
        }
        if self.declared_assets_cr < 0.0 {
            return Err("Declared assets cannot be negative.".to_string());
        }
        if self.criminal_cases < 0 {
            return Err("Criminal cases count cannot be negative.".to_string());
        }
        if self.constituency_id.trim().is_empty() {
            return Err("constituency_id must be provided.".to_string());
        }
        if self.party_id.trim().is_empty() {
            return Err("party_id must be provided.".to_string());
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeclaredResultView {
    pub result_key: String,
    pub election_id: String,
    pub constituency_id: String,
    pub constituency_name: Option<String>,
    pub winning_candidate_id: String,
    pub winning_candidate_name: Option<String>,
    pub winning_party_name: Option<String>,
    pub total_votes: i64,
    pub candidate_votes: HashMap<String, i64>,
    pub margin: i64,
    pub is_declared: bool,
    pub declaration_time: String,
    pub source_publisher: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResultDeclarationRequest {
    pub election_id: String,
    pub constituency_id: String,
    pub winning_candidate_id: String,
    pub total_votes: i64,
    pub candidate_votes: HashMap<String, i64>,
    pub margin: i64,
}

impl ResultDeclarationRequest {
    pub fn validate(&self) -> Result<(), String> {
        if self.election_id.trim().is_empty() {
            return Err("election_id cannot be empty.".to_string());
        }
        if self.constituency_id.trim().is_empty() {
            return Err("constituency_id cannot be empty.".to_string());
        }
        if self.winning_candidate_id.trim().is_empty() {
            return Err("winning_candidate_id cannot be empty.".to_string());
        }
        if self.total_votes <= 0 {
            return Err("total_votes must be greater than zero.".to_string());
        }
        if self.margin < 0 {
            return Err("margin cannot be negative.".to_string());
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RegionalTurnout {
    pub region: String,
    pub polling_booths: i32,
    pub voter_turnout_percent: f64,
    pub phase_status: String,
    pub total_voters: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ETLBatch {
    pub id: String,
    pub source_file: String,
    pub records_count: String,
    pub provenance: String,
    pub status: String,
    pub imported_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ETLImportRequest {
    pub source_file: String,
    pub records_count: i32,
    pub provenance: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FeatureFlag {
    pub name: String,
    pub enabled: bool,
    pub description: String,
    pub environment: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[allow(dead_code)]
pub struct FeatureFlagUpdate {
    pub enabled: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemMetrics {
    pub cpu_utilization: f64,
    pub memory_utilization: f64,
    pub disk_free_gb: f64,
    pub db_pool_active: i32,
    pub db_pool_overflow: i32,
    pub redis_latency_ms: f64,
    pub api_requests_per_sec: i32,
    pub p99_latency_ms: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditLog {
    pub id: String,
    pub sequence_number: i64,
    pub timestamp: String,
    pub actor: String,
    pub action: String,
    pub resource: String,
    pub status: String,
    pub ip_address: String,
    pub previous_hash: String,
    pub current_hash: String,
    pub metadata: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchHit {
    pub id: String,
    pub title: String,
    pub category: String, // "election" | "constituency" | "candidate" | "party"
    pub description: String,
    pub score: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchResponse {
    pub query: String,
    pub total_hits: usize,
    pub results: Vec<SearchHit>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Citation {
    pub id: String,
    pub source_id: String,
    pub publisher: String,
    pub section: String,
    pub quote: String,
    pub url: String,
    pub publication_date: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AIQueryRequest {
    pub query: String,
    pub max_citations: Option<usize>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AIQueryResponse {
    pub query: String,
    pub answer: String,
    pub citations: Vec<Citation>,
    pub grounding_score: f64,
    pub model_used: String,
    pub latency_ms: u64,
    pub disclaimer: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatMessage {
    pub role: String, // "user" | "assistant"
    pub content: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AIChatRequest {
    pub messages: Vec<ChatMessage>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AIChatResponse {
    pub response: String,
    pub citations: Vec<Citation>,
    pub grounding_score: f64,
    pub model_used: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AIMetricsResponse {
    pub total_queries_processed: i64,
    pub average_grounding_score: f64,
    pub citation_coverage_percentage: f64,
    pub average_latency_ms: f64,
    pub active_guardrails: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[allow(dead_code)]
pub struct ExecutiveKpis {
    pub total_elections_managed: i64,
    pub total_voters_registered: i64,
    pub average_turnout_percent: f64,
    pub total_constituencies: i32,
    pub total_candidates: i32,
    pub total_polling_booths: i32,
    pub ai_queries_processed: i64,
    pub platform_uptime_percent: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DataCorrection {
    pub id: String,
    pub entity_type: String,
    pub entity_id: String,
    pub field_name: String,
    pub original_value: Option<String>,
    pub proposed_value: String,
    pub source_url: String,
    pub justification: String,
    pub reporter_email: Option<String>,
    pub status: String,
    pub created_at: String,
    pub reviewed_at: Option<String>,
    pub reviewed_by: Option<String>,
    pub review_notes: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DataCorrectionSubmitRequest {
    pub entity_type: String,
    pub entity_id: String,
    pub field_name: String,
    pub original_value: Option<String>,
    pub proposed_value: String,
    pub source_url: String,
    pub justification: String,
    pub reporter_email: Option<String>,
}

impl DataCorrectionSubmitRequest {
    pub fn validate(&self) -> Result<(), String> {
        if self.entity_type.trim().is_empty() {
            return Err("entity_type is required.".into());
        }
        if self.entity_id.trim().is_empty() {
            return Err("entity_id is required.".into());
        }
        if self.field_name.trim().is_empty() {
            return Err("field_name is required.".into());
        }
        if self.proposed_value.trim().is_empty() {
            return Err("proposed_value is required.".into());
        }
        if !self.source_url.starts_with("http://") && !self.source_url.starts_with("https://") {
            return Err("source_url must be a valid HTTP or HTTPS URL.".into());
        }
        if self.justification.trim().len() < 10 {
            return Err(
                "justification must provide at least 10 characters of factual context.".into(),
            );
        }
        Ok(())
    }
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DisputedClaim {
    pub id: String,
    pub claim_id: String,
    pub dispute_type: String,
    pub contending_source_id: String,
    pub explanation: String,
    pub status: String,
    pub reported_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DataCoverageMetric {
    pub id: String,
    pub election_id: String,
    pub jurisdiction: String,
    pub total_constituencies_in_scope: i32,
    pub constituencies_indexed: i32,
    pub candidates_indexed: i32,
    pub affidavits_verified: i32,
    pub last_audit_date: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IngestionCandidateRecord {
    pub name: String,
    pub constituency_code: String,
    pub party_code: String,
    pub education: Option<String>,
    pub declared_assets_cr: f64,
    pub declared_liabilities_cr: f64,
    pub criminal_cases: i32,
    pub source_ref: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IngestionBatchPayload {
    pub source_publisher: String,
    pub source_url: String,
    pub election_id: String,
    pub dry_run: Option<bool>,
    pub candidates: Vec<IngestionCandidateRecord>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IngestionDryRunResult {
    pub batch_id: String,
    pub is_dry_run: bool,
    pub total_records_received: usize,
    pub valid_records: usize,
    pub duplicate_records: usize,
    pub invalid_records: usize,
    pub rejection_reasons: Vec<String>,
    pub preview_inserted: Vec<String>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GroundingEvaluationMetric {
    pub query: String,
    pub citations_returned: usize,
    pub grounding_score: f64,
    pub token_coverage_ratio: f64,
    pub source_authority_weight: f64,
    pub abstained: bool,
    pub latency_ms: u64,
}
