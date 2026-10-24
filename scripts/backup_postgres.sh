#!/usr/bin/env bash
# Election Intelligence Platform - PostgreSQL Disaster Recovery Backup Script
# Creates a timestamped, gzip-compressed snapshot of the database with SHA-256 checksum

set -euo pipefail

DB_URL="${DATABASE_URL:-postgres://localhost:5432/election_intelligence}"
BACKUP_DIR="${1:-./backups}"
TIMESTAMP="$(date -u +"%Y%m%d_%H%M%SZ")"
BACKUP_FILE="${BACKUP_DIR}/election_intelligence_backup_${TIMESTAMP}.sql.gz"
CHECKSUM_FILE="${BACKUP_FILE}.sha256"

mkdir -p "${BACKUP_DIR}"

echo "=========================================================="
echo "  Election Intelligence Platform — Database Backup"
echo "=========================================================="
echo "Target DB: ${DB_URL}"
echo "Destination: ${BACKUP_FILE}"
echo "Timestamp: ${TIMESTAMP}"
echo "----------------------------------------------------------"

if ! command -v pg_dump >/dev/null 2>&1; then
    echo "ERROR: 'pg_dump' utility not found on PATH." >&2
    exit 1
fi

echo "==> Exporting database snapshot via pg_dump..."
pg_dump --no-owner --clean --if-exists "${DB_URL}" | gzip -c > "${BACKUP_FILE}"

echo "==> Computing SHA-256 checksum..."
if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "${BACKUP_FILE}" > "${CHECKSUM_FILE}"
elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum "${BACKUP_FILE}" > "${CHECKSUM_FILE}"
fi

FILESIZE="$(du -h "${BACKUP_FILE}" | cut -f1)"
echo "==> Backup completed successfully!"
echo "    Archive:  ${BACKUP_FILE} (${FILESIZE})"
echo "    Checksum: $(cat "${CHECKSUM_FILE}")"
echo "=========================================================="
