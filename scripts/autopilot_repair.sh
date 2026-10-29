#!/usr/bin/env bash
# Election Intelligence Platform — Bounded Self-Repair Orchestrator
# Enforces bounds, path allowlists, regression tests, quality gates, and automated PR generation

set -euo pipefail

ISSUE_ID="${1:-}"
ATTEMPT_COUNT="${2:-1}"
MAX_ALLOWED_ATTEMPTS=3

if [ -z "${ISSUE_ID}" ]; then
    echo "Usage: $0 <issue_id> [attempt_count]" >&2
    exit 1
fi

echo "=========================================================="
echo "  Election Intelligence Platform — Bounded Self-Repair"
echo "=========================================================="
echo "Target Issue:  #${ISSUE_ID}"
echo "Attempt:       ${ATTEMPT_COUNT} of ${MAX_ALLOWED_ATTEMPTS}"
echo "Branch:        autopilot/repair-issue-${ISSUE_ID}"
echo "Timestamp:     $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "----------------------------------------------------------"

# 1. Enforce Maximum Repair Attempt Limit
if [ "${ATTEMPT_COUNT}" -gt "${MAX_ALLOWED_ATTEMPTS}" ]; then
    echo "ERROR: Exceeded maximum allowed repair attempts (${MAX_ALLOWED_ATTEMPTS})." >&2
    echo "Self-repair halted to prevent runaway cycles. Escalating for manual review." >&2
    exit 2
fi

# 2. Inspect Working Tree & Enforce Safe Path Allowlist
echo "==> Inspecting modified files against safety boundaries..."
MODIFIED_FILES=$(git diff --name-only HEAD)

if [ -z "${MODIFIED_FILES}" ]; then
    echo "NOTICE: No working tree modifications detected to evaluate."
    exit 0
fi

for file in ${MODIFIED_FILES}; do
    echo "  Checking file: ${file}"
    # Explicit Denylist Check
    if [[ "${file}" =~ ^migrations/ ]] || \
       [[ "${file}" =~ ^\.github/ ]] || \
       [[ "${file}" =~ ^\.env ]] || \
       [[ "${file}" =~ ^backups/ ]] || \
       [[ "${file}" == "render.yaml" ]] || \
       [[ "${file}" == "Dockerfile" ]] || \
       [[ "${file}" == "docker-compose.yml" ]] || \
       [[ "${file}" == "Cargo.lock" ]] || \
       [[ "${file}" == "LICENSE" ]]; then
        echo "SECURITY VIOLATION: Path '${file}' is protected and cannot be mutated by autopilot." >&2
        exit 3
    fi

    # Explicit Allowlist Check
    if [[ ! "${file}" =~ ^src/ ]] && [[ ! "${file}" =~ ^tests/ ]] && [[ "${file}" != "Cargo.toml" ]]; then
        echo "SECURITY VIOLATION: Path '${file}' is outside the bounded repair allowlist (src/, tests/, Cargo.toml)." >&2
        exit 3
    fi
done

# 3. Check for Destructive SQL Patterns
echo "==> Scanning diff for destructive SQL patterns..."
DIFF_CONTENT="$(git diff HEAD)"
if echo "${DIFF_CONTENT}" | grep -Ei "DROP TABLE|TRUNCATE|DROP DATABASE|DROP SCHEMA|ALTER TABLE.*DROP COLUMN|DELETE FROM ELECTIONS|DELETE FROM AUDIT_LEDGER"; then
    echo "SECURITY VIOLATION: Destructive database deletion pattern detected in patch." >&2
    exit 4
fi

# 4. Enforce Quality Gates
echo "==> Running Quality Gate 1: Code Formatting Check..."
cargo fmt --all -- --check

echo "==> Running Quality Gate 2: Clippy Linter Check..."
cargo clippy --all-targets --all-features -- -D warnings

echo "==> Running Quality Gate 3: Automated Test Suite (Must Pass 100%)..."
cargo test --all-targets

echo "==> Running Quality Gate 4: Production Release Build..."
cargo build --release

# 5. Check Diff Bounds
DIFF_LINES=$(echo "${DIFF_CONTENT}" | wc -l | tr -d ' ')
echo "==> Patch size: ${DIFF_LINES} lines of diff."
if [ "${DIFF_LINES}" -gt 500 ]; then
    echo "WARNING: Patch diff exceeds 500 lines. Flagged for required manual maintainer review."
fi

# 6. Branch and Pull Request Creation
BRANCH_NAME="autopilot/repair-issue-${ISSUE_ID}"
echo "==> Preparing repair branch: ${BRANCH_NAME}..."

if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
    git checkout "${BRANCH_NAME}"
else
    git checkout -b "${BRANCH_NAME}"
fi

git add -A
git commit -m "fix(autopilot): bounded automated repair for issue #${ISSUE_ID} (attempt ${ATTEMPT_COUNT})" || echo "No new commit needed."

if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    echo "==> Pushing repair branch to origin..."
    git push -u origin "${BRANCH_NAME}" --force-with-lease

    echo "==> Opening Pull Request for maintainer review..."
    PR_BODY=$(cat <<EOF
## 🤖 Autopilot Bounded Self-Repair

### Overview
- **Fixes Issue:** #${ISSUE_ID}
- **Attempt:** ${ATTEMPT_COUNT} of ${MAX_ALLOWED_ATTEMPTS}
- **Safety Policy:** Bounded repair paths enforced (\`src/\`, \`tests/\`, \`Cargo.toml\`)
- **Budget Compliance:** ₹0/month Free Tier strictly preserved

### Verification & Quality Gates
- [x] Code Formatting (\`cargo fmt\`) Passed
- [x] Strict Clippy Linter (\`cargo clippy -D warnings\`) Passed (0 warnings)
- [x] Complete Automated Test Suite Passed (100%)
- [x] Production Release Build (\`cargo build --release\`) Passed
- [x] Zero Destructive Schema Changes

### Files Modified
\`\`\`text
${MODIFIED_FILES}
\`\`\`

---
*Created by the Election Intelligence Platform Autopilot Governance System.*
EOF
)
    gh pr create \
        --title "fix(autopilot): bounded automated repair for issue #${ISSUE_ID}" \
        --label "autopilot,automated-repair,needs-review" \
        --body "${PR_BODY}" || echo "PR already exists or created."
fi

echo "==> Bounded self-repair workflow completed successfully!"
echo "=========================================================="
