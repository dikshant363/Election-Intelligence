# Backup and Recovery Guide

This document defines the disaster recovery (DR) and backup protocols for the Election Intelligence Platform.

## 1. Backup Strategy Overview

- **Database (PostgreSQL)**: Daily full backups, continuous WAL (Write-Ahead Log) archiving.
- **Cache (Redis)**: Snapshots every 6 hours (AOF enabled).
- **Environment State**: Infrastructure as Code (Terraform) and Secrets (managed in cloud provider).
- **Retention Policy**:
  - Daily backups kept for 30 days.
  - Weekly backups kept for 12 weeks.
  - Monthly backups kept for 1 year.

## 2. Database Backup Procedures

### PostgreSQL `pg_dump` Commands
Manual backup of the database:
```bash
pg_dump -U postgres -h localhost -F c -d election_intelligence -f backup_$(date +%Y%m%d).dump
```

### Automated Scheduling
Backups are automated via a cron job running on a secure utility server, executed daily at 02:00 AM UTC. Logs are routed to monitoring services.

### Storage and Encryption
Backups are encrypted using AES-256 before transit and stored in an off-site AWS S3 bucket (or equivalent) with versioning enabled and strict IAM access controls.

## 3. Application State Backup

- **Configuration**: All app config is stored in Git (version controlled).
- **Secrets**: Stored in AWS Secrets Manager / Azure Key Vault. Backed up implicitly via provider redundancy.
- **Environment**: Docker images are pushed to a container registry, enabling instant rollout of specific versions.

## 4. Backup Integrity Verification

- **Checksums**: SHA-256 checksums are generated upon backup creation and verified upon transfer to S3.
- **Snapshot Module**: The internal module at `backend/app/production/backup/` continuously monitors backup health and alerts via Slack/Email if a checksum fails or a backup is missed.

## 5. Recovery Procedures

### Database Restore from Backup
1. Stop application traffic to prevent partial state writes.
2. Drop existing schema (if corrupted).
3. Restore using `pg_restore`:
   ```bash
   pg_restore -U postgres -h localhost -d election_intelligence -1 backup_file.dump
   ```
4. Run Alembic migrations to ensure schema consistency.
5. Resume application traffic.

### Point-in-Time Recovery (PITR)
Using WAL archives (e.g., via WAL-E or pgBackRest), the DB can be restored to a specific timestamp just before the disaster event occurred.

### Full System Restore
1. Provision new database instance.
2. Restore latest DB backup.
3. Deploy latest Docker container for Backend API.
4. Update DNS/Load Balancers to point to new API instances.

## 6. RTO and RPO Targets

- **Recovery Time Objective (RTO)**: 2 hours. (Time to restore full functionality).
- **Recovery Point Objective (RPO)**: 5 minutes. (Maximum acceptable data loss, mitigated by WAL streaming).

## 7. Disaster Recovery Scenarios

- **Database Server Failure**: Failover to hot-standby replica. RTO < 5 minutes.
- **Application Server Failure**: Load balancer automatically routes to healthy instances. Auto-scaling spins up new instances.
- **Complete Data Center Failure**: Traffic routed to multi-region secondary deployment. Infrastructure redeployed via Terraform.
- **Accidental Data Deletion**: Execute Point-in-Time Recovery (PITR) to restore state prior to the deletion event.

## 8. Restore Testing Schedule

- **Monthly**: Automated script tests restoring the database to a sandbox environment to verify data integrity.
- **Quarterly**: Full manual DR drill (Game Day) executed by the DevOps team to test end-to-end system recovery.

## 9. Backup Monitoring

Monitoring is configured via Prometheus/Grafana. Alerts trigger if:
- Backup job fails or doesn't run within the scheduled window.
- Backup file size is anomalies (e.g., significantly smaller than previous days).
- Checksum verification fails.
