# Election Intelligence Platform — Disaster Recovery & Backup Guide

## 1. Overview
The Election Intelligence Platform utilizes an automated, zero-cost disaster recovery procedure to ensure complete data persistence and tamper-evident audit ledger preservation on free cloud hosting.

- **Storage Engine**: Neon Serverless PostgreSQL 17 (0.5 GiB SSD persistent tier).
- **Backup Mechanism**: Compressed logical SQL snapshots via `pg_dump` with SHA-256 cryptographic checksums.
- **Budget**: ₹0.00 / $0.00 per month (Utilizes native PostgreSQL client tools and local/git-safe storage).

---

## 2. Automated Backup Execution

To generate a full database snapshot with cryptographic checksum:

```bash
# Run backup script against target database (defaults to DATABASE_URL)
./scripts/backup_postgres.sh ./backups
```

### What This Does:
1. Executes `pg_dump --no-owner --clean --if-exists` to produce an idempotent restore script.
2. Pipes the output through `gzip -c` to produce a compressed archive:
   `./backups/election_intelligence_backup_YYYYMMDD_HHMMSSZ.sql.gz`.
3. Computes a SHA-256 checksum stored in:
   `./backups/election_intelligence_backup_YYYYMMDD_HHMMSSZ.sql.gz.sha256`.

---

## 3. Verified Database Restore Procedure

To restore an existing snapshot to a fresh database:

```bash
# Syntax: ./scripts/restore_postgres.sh <backup_file.sql.gz> [TARGET_DATABASE_URL]
./scripts/restore_postgres.sh ./backups/election_intelligence_backup_20261029_110000Z.sql.gz
```

### Verification Checks Performed During Restore:
1. **Archive Integrity Check**: Verifies that the SHA-256 checksum matches the archive exactly.
2. **Transaction Rollback on Error**: Executes via `psql -v ON_ERROR_STOP=1`. If any error occurs, the restore terminates without leaving corrupted tables.
3. **Table & Record Count Verification**:
   - Counts restored `elections` table rows.
   - Counts restored `candidacies` table rows.
4. **Audit Ledger Chaining Verification**:
   - Queries `audit_ledger` to verify that the cryptographic hash chain from the genesis block (`0000000000000000000000000000000000000000000000000000000000000000`) is intact.

---

## 4. Disaster Recovery Playbook (Cold Start from Zero)

If the entire cloud deployment is lost or deleted:
1. **Provision Free Neon Database**:
   - Create a new project on [neon.tech](https://neon.tech) (PostgreSQL 17).
   - Copy the new connection string: `postgresql://user:pass@ep-xyz.us-east-2.aws.neon.tech/neondb?sslmode=require`.
2. **Restore Latest Snapshot**:
   ```bash
   ./scripts/restore_postgres.sh ./backups/latest_backup.sql.gz "postgresql://user:pass@ep-xyz.../neondb?sslmode=require"
   ```
3. **Deploy Container to Render**:
   - Link repository to Render using `render.yaml`.
   - Update `DATABASE_URL` environment variable in Render dashboard.
   - The application automatically connects, verifies migrations, and begins serving traffic.
4. **Verify Health**:
   ```bash
   ./scripts/health_check.sh https://election-intelligence.onrender.com
   ```
