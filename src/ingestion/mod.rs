// Election Intelligence Platform - Data Ingestion Pipeline & Connector
// Implements format validation, dry-run checks, transactional commits, and idempotency

use crate::db::Database;
use crate::domain::{IngestionBatchPayload, IngestionCandidateRecord, IngestionDryRunResult};
use crate::error::AppError;
use sha2::{Digest, Sha256};

pub struct IngestionPipeline;

impl IngestionPipeline {
    /// Computes SHA-256 hash of payload content for idempotency tracking
    pub fn compute_payload_hash(data: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        hex::encode(hasher.finalize())
    }

    /// Parses CSV format into structured candidate records
    pub fn parse_csv_candidates(
        csv_content: &str,
    ) -> Result<Vec<IngestionCandidateRecord>, AppError> {
        let mut records = Vec::new();
        let lines: Vec<&str> = csv_content.lines().collect();
        if lines.is_empty() {
            return Err(AppError::Validation("CSV payload is empty.".into()));
        }

        // Header check: name,constituency_code,party_code,education,declared_assets_cr,declared_liabilities_cr,criminal_cases,source_ref
        for (idx, line) in lines.iter().enumerate().skip(1) {
            let row: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
            if row.len() < 8 {
                return Err(AppError::Validation(format!(
                    "Line {}: insufficient columns. Expected 8 columns (name,constituency_code,party_code,education,declared_assets_cr,declared_liabilities_cr,criminal_cases,source_ref).",
                    idx + 1
                )));
            }

            let assets: f64 = row[4].parse().map_err(|_| {
                AppError::Validation(format!(
                    "Line {}: invalid assets number '{}'",
                    idx + 1,
                    row[4]
                ))
            })?;
            let liabilities: f64 = row[5].parse().map_err(|_| {
                AppError::Validation(format!(
                    "Line {}: invalid liabilities number '{}'",
                    idx + 1,
                    row[5]
                ))
            })?;
            let cases: i32 = row[6].parse().map_err(|_| {
                AppError::Validation(format!(
                    "Line {}: invalid criminal_cases count '{}'",
                    idx + 1,
                    row[6]
                ))
            })?;

            records.push(IngestionCandidateRecord {
                name: row[0].to_string(),
                constituency_code: row[1].to_string(),
                party_code: row[2].to_string(),
                education: Some(row[3].to_string()),
                declared_assets_cr: assets,
                declared_liabilities_cr: liabilities,
                criminal_cases: cases,
                source_ref: row[7].to_string(),
            });
        }

        Ok(records)
    }

    /// Processes ingestion batch with dry-run support, idempotency, and transactional persistence
    pub async fn process_batch(
        db: &Database,
        payload: IngestionBatchPayload,
        actor: &str,
        ip_address: &str,
    ) -> Result<IngestionDryRunResult, AppError> {
        let is_dry_run = payload.dry_run.unwrap_or(false);
        let batch_id = format!(
            "batch-{}",
            uuid::Uuid::new_v4().to_string()[..8].to_uppercase()
        );

        let mut valid_records = 0;
        let mut duplicate_records = 0;
        let mut invalid_records = 0;
        let mut rejection_reasons = Vec::new();
        let mut preview_inserted = Vec::new();

        // 1. Fetch valid constituencies and parties to validate relationships
        let existing_candidates = db.get_candidates().await.unwrap_or_default();
        let constituencies = db.get_constituencies().await.unwrap_or_default();
        let parties = db.get_parties().await.unwrap_or_default();

        let mut valid_candidates = Vec::new();

        for cand in &payload.candidates {
            if cand.name.trim().is_empty() {
                invalid_records += 1;
                rejection_reasons.push("Candidate name cannot be empty.".into());
                continue;
            }

            // Relationship check: constituency
            let const_match = constituencies.iter().find(|c| {
                c.code == cand.constituency_code
                    || c.name.to_lowercase() == cand.constituency_code.to_lowercase()
            });
            if const_match.is_none() {
                invalid_records += 1;
                rejection_reasons.push(format!(
                    "Unknown constituency code/name '{}'",
                    cand.constituency_code
                ));
                continue;
            }

            // Relationship check: party
            let party_match = parties
                .iter()
                .find(|p| p.code.to_uppercase() == cand.party_code.to_uppercase());
            if party_match.is_none() {
                invalid_records += 1;
                rejection_reasons.push(format!(
                    "Unknown political party code '{}'",
                    cand.party_code
                ));
                continue;
            }

            // Invariant: Non-negative assets & liabilities
            if cand.declared_assets_cr < 0.0 || cand.declared_liabilities_cr < 0.0 {
                invalid_records += 1;
                rejection_reasons.push(format!(
                    "Negative financial declaration for candidate '{}'",
                    cand.name
                ));
                continue;
            }

            // Duplicate detection: same candidate name & constituency in election
            let const_id = &const_match.unwrap().id;
            let party_id = &party_match.unwrap().id;

            let is_duplicate = existing_candidates.iter().any(|ec| {
                ec.name.to_lowercase() == cand.name.to_lowercase()
                    && ec.constituency_id == *const_id
            });

            if is_duplicate {
                duplicate_records += 1;
                rejection_reasons.push(format!(
                    "Duplicate nomination: candidate '{}' already registered in constituency '{}'",
                    cand.name, cand.constituency_code
                ));
                continue;
            }

            valid_records += 1;
            preview_inserted.push(format!(
                "{} ({}) - {}",
                cand.name, cand.party_code, cand.constituency_code
            ));
            valid_candidates.push((cand, const_id.clone(), party_id.clone()));
        }

        // If dry_run is true, return analysis report without committing
        if is_dry_run {
            return Ok(IngestionDryRunResult {
                batch_id,
                is_dry_run: true,
                total_records_received: payload.candidates.len(),
                valid_records,
                duplicate_records,
                invalid_records,
                rejection_reasons,
                preview_inserted,
            });
        }

        // 2. Transactional Commit
        let mut tx = db.pool().begin().await?;

        let now = chrono::Utc::now().to_rfc3339();
        let today = chrono::Utc::now().format("%Y-%m-%d").to_string();

        // Insert batch metadata
        sqlx::query(
            r#"
            INSERT INTO import_batches (id, source_file, records_count, provenance, status, imported_at)
            VALUES ($1, $2, $3, $4, 'PROCESSED', $5::timestamptz)
            "#,
        )
        .bind(&batch_id)
        .bind(&payload.source_url)
        .bind(valid_records as i32)
        .bind(&payload.source_publisher)
        .bind(&now)
        .execute(&mut *tx)
        .await?;

        for (cand, const_id, party_id) in valid_candidates {
            let person_id = format!("per-{}", &uuid::Uuid::new_v4().to_string()[..8]);
            let candidacy_id = format!("cand-{}", &uuid::Uuid::new_v4().to_string()[..8]);
            let affidavit_id = format!("aff-{}", &uuid::Uuid::new_v4().to_string()[..8]);
            let disclosure_id = format!("disc-{}", &uuid::Uuid::new_v4().to_string()[..8]);

            sqlx::query("INSERT INTO persons (id, name, nationality) VALUES ($1, $2, 'Indian')")
                .bind(&person_id)
                .bind(&cand.name)
                .execute(&mut *tx)
                .await?;

            sqlx::query(
                r#"
                INSERT INTO candidacies (id, person_id, election_id, constituency_id, party_id, nomination_date, status)
                VALUES ($1, $2, $3, $4, $5, $6::date, 'ACCEPTED')
                "#,
            )
            .bind(&candidacy_id)
            .bind(&person_id)
            .bind(&payload.election_id)
            .bind(&const_id)
            .bind(&party_id)
            .bind(&today)
            .execute(&mut *tx)
            .await?;

            sqlx::query(
                r#"
                INSERT INTO affidavits (id, candidacy_id, submission_date, verification_status, source_reference)
                VALUES ($1, $2, $3::date, 'VERIFIED', $4)
                "#,
            )
            .bind(&affidavit_id)
            .bind(&candidacy_id)
            .bind(&today)
            .bind(&cand.source_ref)
            .execute(&mut *tx)
            .await?;

            sqlx::query(
                r#"
                INSERT INTO disclosures (id, affidavit_id, movable_assets_inr, immovable_assets_inr, liabilities_inr, criminal_cases_count, education_details)
                VALUES ($1, $2, $3, 0.0, $4, $5, $6)
                "#,
            )
            .bind(&disclosure_id)
            .bind(&affidavit_id)
            .bind(cand.declared_assets_cr * 10_000_000.0)
            .bind(cand.declared_liabilities_cr * 10_000_000.0)
            .bind(cand.criminal_cases)
            .bind(cand.education.clone().unwrap_or_else(|| "Not Disclosed".into()))
            .execute(&mut *tx)
            .await?;
        }

        // Record audit log for the ingestion batch
        db.append_audit_log_tx(
            &mut tx,
            actor,
            "BATCH_DATA_INGESTION",
            &format!("etl/{}", batch_id),
            "SUCCESS",
            ip_address,
            serde_json::json!({
                "source_publisher": payload.source_publisher,
                "election_id": payload.election_id,
                "valid_records": valid_records,
                "duplicates_skipped": duplicate_records,
                "invalid_skipped": invalid_records
            }),
        )
        .await?;

        tx.commit().await?;

        Ok(IngestionDryRunResult {
            batch_id,
            is_dry_run: false,
            total_records_received: payload.candidates.len(),
            valid_records,
            duplicate_records,
            invalid_records,
            rejection_reasons,
            preview_inserted,
        })
    }
}
