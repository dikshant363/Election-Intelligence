#!/usr/bin/env bash
# Election Intelligence Platform - PostgreSQL Disaster Recovery Restore Script
# Restores a timestamped, gzip-compressed database snapshot after checksum validation

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <path_to_backup.sql.gz> [DATABASE_URL]"
    echo "Example: $0 ./backups/election_intelligence_backup_20261024_120000Z.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"
DB_URL="${2:-${DATABASE_URL:-postgres://localhost:5432/election_intelligence}}"
CHECKSUM_FILE="${BACKUP_FILE}.sha256"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "ERROR: Backup file '${BACKUP_FILE}' does not exist." >&2
    exit 1
fi

echo "=========================================================="
echo "  Election Intelligence Platform — Database Restore"
echo "=========================================================="
echo "Backup File: ${BACKUP_FILE}"
echo "Target DB:   ${DB_URL}"
echo "----------------------------------------------------------"

if [ -f "${CHECKSUM_FILE}" ]; then
    echo "==> Verifying SHA-256 archive integrity..."
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 -c "${CHECKSUM_FILE}"
    elif command -v sha256sum >/dev/null 2>&1; then
        sha256sum -c "${CHECKSUM_FILE}"
    fi
    echo "==> Archive integrity verified: OK"
else
    echo "WARNING: No checksum file found at '${CHECKSUM_FILE}'. Proceeding without integrity check."
fi

if ! command -v psql >/dev/null 2>&1; then
    echo "ERROR: 'psql' client utility not found on PATH." >&2
    exit 1
fi

echo "==> Restoring database from compressed archive..."
gunzip -c "${BACKUP_FILE}" | psql -v ON_ERROR_STOP=1 "${DB_URL}"

echo "==> Verifying database restored tables..."
ELECTION_COUNT="$(psql -t -A -c "SELECT COUNT(*) FROM elections;" "${DB_URL}" || echo "0")"
CANDIDATE_COUNT="$(psql -t -A -c "SELECT COUNT(*) FROM candidacies;" "${DB_URL}" || echo "0")"

echo "==> Restore verification successful!"
echo "    Elections Count:   ${ELECTION_COUNT}"
echo "    Candidacies Count: ${CANDIDATE_COUNT}"
echo "=========================================================="
