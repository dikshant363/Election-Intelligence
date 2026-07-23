# Data Retention Policy — Election Intelligence Platform v1.0.0

## 1. Policy Overview

Election data is a matter of public record and historical significance. This policy defines how long each data category is retained, when it is archived vs deleted, and what processes govern retention decisions.

> [!IMPORTANT]
> Election data in India is subject to Representation of the People Act and Election Commission of India guidelines. This policy is designed to comply with Indian election data governance requirements.

---

## 2. Data Categories and Retention Periods

| Data Category | Retention Period | Disposition | Notes |
| :--- | :--- | :--- | :--- |
| **Election Results** | Indefinite | Archive | Public record; never delete |
| **Candidate Records** | Indefinite | Archive | Public accountability record |
| **Party Records** | Indefinite | Archive | Historical party data |
| **Constituency Records** | Indefinite | Archive | Boundary changes versioned |
| **Polling Booth Data** | 10 years minimum | Archive then review | Granular booth data |
| **ETL Ingestion Logs** | 3 years | Archive then delete | Operational log |
| **ETL Provenance Records** | Indefinite | Archive | Data lineage requires permanent retention |
| **Access Logs (API)** | 1 year | Delete | Security and audit |
| **Authentication Logs** | 2 years | Archive then delete | Security compliance |
| **Audit Logs** | 7 years | Archive | Regulatory requirement |
| **AI Query Logs** | 90 days | Delete | Privacy consideration |
| **AI Response Cache** | 24 hours | Evict automatically | Redis TTL |
| **Search Query Logs** | 30 days | Aggregate then delete | Analytics aggregated |
| **Performance Metrics** | 90 days (raw) / 2 years (aggregated) | Rollup | Prometheus retention |
| **Backup Snapshots** | 30 days (daily), 1 year (monthly) | Delete per schedule | Offsite for monthly |
| **JWT Tokens** | Token expiry | Expire automatically | Stateless; no DB storage |
| **User Session Data** | Session duration | Expire automatically | No persistent storage |

---

## 3. Archival Process

### Primary Data (Election, Candidate, Party, Constituency, Result)
- Never hard-deleted from the primary database.
- Soft deletion via `is_active` / `deleted_at` flag where applicable.
- Historical records accessible via API with appropriate filters.
- Archived to cold storage (S3/GCS) annually for records older than 10 years.

### Operational Data (Logs, ETL records)
- Automated deletion job runs weekly.
- Deletion confirmed with a checksum log entry before removal.
- Aggregated analytics preserved even after raw deletion.

---

## 4. Right to Correction

Election data corrections follow this process:
1. Correction request submitted with source evidence.
2. Data steward reviews against official ECI records.
3. If approved: original record updated; provenance log records the correction, who approved it, and source.
4. Corrected records are audit-trailed — the change history is never erased.

---

## 5. Data Deletion Procedures

```bash
# Soft delete an election record (preferred)
UPDATE elections SET is_active = false, deleted_at = NOW() WHERE id = '<id>';

# Hard delete operational logs older than retention limit
DELETE FROM etl_ingestion_logs WHERE created_at < NOW() - INTERVAL '3 years';

# Archive before deletion (always backup first)
pg_dump --table=etl_ingestion_logs election_intelligence > etl_logs_archive_$(date +%Y%m).sql
```

---

## 6. Backup Retention

| Backup Type | Frequency | Retention | Storage |
| :--- | :--- | :--- | :--- |
| Daily full backup | Every day at 02:00 IST | 30 days | Local + encrypted offsite |
| Weekly backup | Every Sunday | 12 weeks | Encrypted offsite |
| Monthly backup | 1st of month | 12 months | Cold storage (encrypted) |
| Pre-release snapshot | Before every deployment | Until next release | Local |

---

## 7. Compliance References

- **Information Technology Act 2000** (India): Data security obligations.
- **Representation of the People Act 1950/1951**: Election data as public record.
- **Election Commission of India Guidelines**: Data accuracy and correction procedures.
- **Personal Data Protection Bill** (India, pending): Handles any personal data within candidate profiles.

---

## 8. Retention Review

This policy is reviewed annually or when:
- New regulations come into effect.
- Storage costs require re-evaluation.
- A new data category is introduced to the platform.

All changes to retention periods must be approved by the Principal Architect and documented in `DECISION_LOG.md`.
