// Election Intelligence Platform - Cryptographic Audit Log & Tamper Detection
// Computes and verifies SHA-256 hash chaining across administrative actions

use crate::domain::AuditLog;
use sha2::{Digest, Sha256};

pub const GENESIS_HASH: &str = "0000000000000000000000000000000000000000000000000000000000000000";

#[allow(clippy::too_many_arguments)]
pub fn compute_event_hash(
    previous_hash: &str,
    sequence_number: i64,
    timestamp: &str,
    actor: &str,
    action: &str,
    resource: &str,
    status: &str,
    ip_address: &str,
    metadata_json: &str,
) -> String {
    let mut hasher = Sha256::new();
    hasher.update(previous_hash.as_bytes());
    hasher.update(b"|");
    hasher.update(sequence_number.to_string().as_bytes());
    hasher.update(b"|");
    hasher.update(timestamp.as_bytes());
    hasher.update(b"|");
    hasher.update(actor.as_bytes());
    hasher.update(b"|");
    hasher.update(action.as_bytes());
    hasher.update(b"|");
    hasher.update(resource.as_bytes());
    hasher.update(b"|");
    hasher.update(status.as_bytes());
    hasher.update(b"|");
    hasher.update(ip_address.as_bytes());
    hasher.update(b"|");
    hasher.update(metadata_json.as_bytes());

    let result = hasher.finalize();
    hex::encode(result)
}

/// Verifies whether an ordered sequence of audit log entries maintains unbroken SHA-256 hash chaining.
pub fn verify_audit_chain(logs: &[AuditLog]) -> Result<(), String> {
    if logs.is_empty() {
        return Ok(());
    }

    let mut sorted = logs.to_vec();
    sorted.sort_by_key(|l| l.sequence_number);

    for (i, log) in sorted.iter().enumerate() {
        if i == 0 {
            // Genesis entry or start of chain
            if log.previous_hash.is_empty() {
                return Err(format!("Entry {} has empty previous_hash", log.id));
            }
        } else {
            let prev = &sorted[i - 1];
            // 1. Strict contiguous sequence check
            if log.sequence_number != prev.sequence_number + 1 {
                return Err(format!(
                    "Tampering detected at log id {}: non-contiguous sequence_number {} following prior sequence_number {}",
                    log.id, log.sequence_number, prev.sequence_number
                ));
            }

            // 2. Hash link continuity check
            if log.previous_hash != prev.current_hash {
                return Err(format!(
                    "Tampering detected at log id {}: previous_hash '{}' does not match prior entry current_hash '{}'",
                    log.id, log.previous_hash, prev.current_hash
                ));
            }
        }

        if log.current_hash.is_empty() {
            return Err(format!("Entry {} has empty current_hash", log.id));
        }
    }

    Ok(())
}

/// Verifies that an individual entry's current_hash matches its exact canonical payload.
#[allow(dead_code)]
pub fn verify_single_entry_hash(log: &AuditLog) -> Result<(), String> {
    let meta_str = serde_json::to_string(&log.metadata).unwrap_or_else(|_| "{}".to_string());
    let expected = compute_event_hash(
        &log.previous_hash,
        log.sequence_number,
        &log.timestamp,
        &log.actor,
        &log.action,
        &log.resource,
        &log.status,
        &log.ip_address,
        &meta_str,
    );

    if log.current_hash != expected {
        return Err(format!(
            "Tampering detected at log id {}: current_hash '{}' does not match recomputed hash '{}'",
            log.id, log.current_hash, expected
        ));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compute_event_hash_deterministic() {
        let hash1 = compute_event_hash(
            GENESIS_HASH,
            1,
            "2026-07-23T12:00:00Z",
            "admin",
            "UPDATE_FLAG",
            "feature_flags/enable_rag",
            "SUCCESS",
            "127.0.0.1",
            "{}",
        );
        let hash2 = compute_event_hash(
            GENESIS_HASH,
            1,
            "2026-07-23T12:00:00Z",
            "admin",
            "UPDATE_FLAG",
            "feature_flags/enable_rag",
            "SUCCESS",
            "127.0.0.1",
            "{}",
        );
        assert_eq!(hash1, hash2);
        assert_eq!(hash1.len(), 64);
    }

    #[test]
    fn test_verify_audit_chain_tamper_detection() {
        let meta = serde_json::json!({});
        let hash1 = compute_event_hash(
            GENESIS_HASH,
            1,
            "t1",
            "user",
            "ACT1",
            "res1",
            "OK",
            "1.1.1.1",
            "{}",
        );
        let hash2 = compute_event_hash(
            &hash1, 2, "t2", "user", "ACT2", "res2", "OK", "1.1.1.1", "{}",
        );

        let valid_chain = vec![
            AuditLog {
                id: "1".into(),
                sequence_number: 1,
                timestamp: "t1".into(),
                actor: "user".into(),
                action: "ACT1".into(),
                resource: "res1".into(),
                status: "OK".into(),
                ip_address: "1.1.1.1".into(),
                previous_hash: GENESIS_HASH.into(),
                current_hash: hash1.clone(),
                metadata: meta.clone(),
            },
            AuditLog {
                id: "2".into(),
                sequence_number: 2,
                timestamp: "t2".into(),
                actor: "user".into(),
                action: "ACT2".into(),
                resource: "res2".into(),
                status: "OK".into(),
                ip_address: "1.1.1.1".into(),
                previous_hash: hash1.clone(),
                current_hash: hash2.clone(),
                metadata: meta.clone(),
            },
        ];

        assert!(verify_audit_chain(&valid_chain).is_ok());

        // Tamper with previous_hash in second entry
        let mut tampered_chain = valid_chain.clone();
        tampered_chain[1].previous_hash = "deadbeefdeadbeef".into();
        assert!(verify_audit_chain(&tampered_chain).is_err());
    }

    #[test]
    fn test_verify_single_entry_hash() {
        let meta = serde_json::json!({});
        let hash = compute_event_hash(
            GENESIS_HASH,
            1,
            "t1",
            "user",
            "ACT1",
            "res1",
            "OK",
            "1.1.1.1",
            "{}",
        );

        let mut entry = AuditLog {
            id: "1".into(),
            sequence_number: 1,
            timestamp: "t1".into(),
            actor: "user".into(),
            action: "ACT1".into(),
            resource: "res1".into(),
            status: "OK".into(),
            ip_address: "1.1.1.1".into(),
            previous_hash: GENESIS_HASH.into(),
            current_hash: hash,
            metadata: meta,
        };

        assert!(verify_single_entry_hash(&entry).is_ok());

        // Corrupt current_hash
        entry.current_hash = "corrupted_hash".into();
        assert!(verify_single_entry_hash(&entry).is_err());
    }
}
