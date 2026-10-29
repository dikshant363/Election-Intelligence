#!/usr/bin/env bash
# Election Intelligence Platform — Autopilot Automated Health Probing Script
# Probes readiness, system status, API routes, and schema integrity without leaking secrets

set -euo pipefail

TARGET_URL="${1:-${DEPLOYMENT_URL:-http://127.0.0.1:3000}}"
TARGET_URL="${TARGET_URL%/}" # Strip trailing slash

echo "=========================================================="
echo "  Election Intelligence Platform — Autopilot Health Check"
echo "=========================================================="
echo "Target Host: ${TARGET_URL}"
echo "Timestamp:   $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "----------------------------------------------------------"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

FAILED_CHECKS=0
TOTAL_CHECKS=0

check_endpoint() {
    local name="$1"
    local endpoint="$2"
    local expected_code="${3:-200}"
    local required_str="${4:-}"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    local out_file="${TMP_DIR}/res_${TOTAL_CHECKS}.json"
    
    echo -n "Checking ${name} (${endpoint})... "
    
    local http_code
    http_code=$(curl -s -L -o "${out_file}" -w "%{http_code}" --connect-timeout 10 --max-time 30 "${TARGET_URL}${endpoint}" || echo "000")

    if [ "${http_code}" != "${expected_code}" ]; then
        echo "FAILED (HTTP ${http_code}, Expected ${expected_code})"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi

    if [ -n "${required_str}" ]; then
        if ! grep -q "${required_str}" "${out_file}"; then
            echo "FAILED (Content mismatch: Missing '${required_str}')"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        fi
    fi

    echo "OK (HTTP ${http_code})"
    return 0
}

# 1. Readiness Probe (Checks PostgreSQL live connection)
check_endpoint "Readiness Probe" "/ready" "200" '"status":"READY"'

# 2. Liveness & Component Health Probe
check_endpoint "Liveness & Health Probe" "/health" "200" '"status":"UP"'

# 3. Comprehensive System & Autopilot Status
check_endpoint "Autopilot Status" "/status" "200" '"tier":"FREE_TIER_PERMANENT"'

# 4. Essential Public API - Elections
check_endpoint "Elections API" "/api/v1/elections" "200" "elec-2024-ls"

# 5. Essential Public API - Candidates
check_endpoint "Candidates API" "/api/v1/candidates" "200" "success"

# 6. Essential Public API - Coverage Inventory
check_endpoint "Coverage Inventory API" "/api/v1/coverage" "200" "constituencies_indexed"

# 7. Frontend Landing Page
check_endpoint "Web Landing Page" "/" "200" "<!DOCTYPE html>"

echo "----------------------------------------------------------"
if [ "${FAILED_CHECKS}" -eq 0 ]; then
    echo "Result: ALL ${TOTAL_CHECKS} HEALTH CHECKS PASSED (100% HEALTHY)"
    echo "=========================================================="
    exit 0
else
    echo "Result: ${FAILED_CHECKS} OF ${TOTAL_CHECKS} CHECKS FAILED"
    echo "=========================================================="
    exit 1
fi
