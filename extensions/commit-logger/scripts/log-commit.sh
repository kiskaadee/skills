#!/usr/bin/env bash
# log-commit.sh - Deterministic Git commit event capture for structured knowledge vaults
# Appends verified commit metadata into 00-inbox/commit-log.csv

set -euo pipefail

VAULT_ROOT="${VAULT_ROOT:-${BRAIN_ROOT:-$HOME/Brain}}"
LEDGER_FILE="${LEDGER_FILE:-${VAULT_ROOT}/00-inbox/commit-log.csv}"

TARGET_REF="HEAD"
FORCE_ALLOW_BRAIN=false

for arg in "$@"; do
    if [[ "$arg" == "--force" ]] || [[ "$arg" == "--allow-brain" ]]; then
        FORCE_ALLOW_BRAIN=true
    elif [[ "$arg" != -* ]]; then
        TARGET_REF="$arg"
    fi
done

# 1. Verify Git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "commit-logger: not inside a git repository. Exiting." >&2
    exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "${REPO_ROOT}")"

# 2. Anti-Recursion Invariant: Vault repo is non-loggable unless explicitly forced
if [[ "${REPO_ROOT}" == "${VAULT_ROOT}" ]] || [[ "${REPO_NAME}" == "Brain" ]] || [[ "${REPO_NAME}" == "$(basename "${VAULT_ROOT}")" ]]; then
    if [[ "${FORCE_ALLOW_BRAIN}" != "true" ]]; then
        # Silent exit as a no-op to prevent recursion
        exit 0
    fi
fi

# 3. Extract Immutable Git Metadata
COMMIT_SHA="$(git rev-parse "${TARGET_REF}")"
PARENT_SHA="$(git rev-parse --verify "${COMMIT_SHA}^" 2>/dev/null || echo "")"
COMMITTED_AT="$(git show -s --format=%cI "${COMMIT_SHA}")"
SUBJECT="$(git show -s --format=%s "${COMMIT_SHA}")"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")"

# 4. Authoritative Project Mapping
PROJECT=""
if [[ "${REPO_ROOT}" == "${VAULT_ROOT}" ]] || [[ "${REPO_NAME}" == "Brain" ]] || [[ "${REPO_NAME}" == "$(basename "${VAULT_ROOT}")" ]]; then
    PROJECT="brain"
elif [[ -d "${VAULT_ROOT}/06-projects/${REPO_NAME}" ]]; then
    PROJECT="${REPO_NAME}"
elif [[ -d "${VAULT_ROOT}/06-projects/${REPO_NAME,,}" ]]; then
    PROJECT="${REPO_NAME,,}"
elif [[ -d "${VAULT_ROOT}/06-projects" ]]; then
    # Resolve workstation path relative to $HOME (e.g. ~/Homelab/Core, ~/Config)
    if [[ "${REPO_ROOT}" == "${HOME}"* ]]; then
        REL_REPO_PATH="~${REPO_ROOT#$HOME}"
    else
        REL_REPO_PATH="${REPO_ROOT}"
    fi

    if [[ "${REL_REPO_PATH}" != "~" && -n "${REL_REPO_PATH}" ]]; then
        ESCAPED_PATH="${REL_REPO_PATH//./\\.}"
        # Look for matching project directory referencing authoritative workstation path in README.md
        for proj_dir in "${VAULT_ROOT}/06-projects"/*; do
            if [[ -f "${proj_dir}/README.md" ]]; then
                if grep -Eq "(^|[^a-zA-Z0-9_/-])${ESCAPED_PATH}([^a-zA-Z0-9_/-]|$)" "${proj_dir}/README.md"; then
                    PROJECT="$(basename "${proj_dir}")"
                    break
                fi
            fi
        done
    fi
fi

# 5. CSV Formatting (RFC 4180 Escaping)
escape_csv() {
    local val="$1"
    # Double existing double quotes
    val="${val//\"/\"\"}"
    # Quote if string contains comma, quote, or newline
    if [[ "${val}" =~ [,\"\n\r] ]]; then
        echo "\"${val}\""
    else
        echo "${val}"
    fi
}

ESCAPED_SUBJECT="$(escape_csv "${SUBJECT}")"

# 6. Ensure Ledger File and Header Exist
mkdir -p "$(dirname "${LEDGER_FILE}")"
if [[ ! -f "${LEDGER_FILE}" ]]; then
    echo "committed_at,repository,project,branch,commit_sha,parent_sha,subject" > "${LEDGER_FILE}"
fi

# 7. Idempotency Barrier: Full 40-char SHA deduplication
if grep -q ",${COMMIT_SHA}," "${LEDGER_FILE}" 2>/dev/null; then
    # Commit already recorded
    exit 0
fi

# 8. Atomic Append
echo "${COMMITTED_AT},${REPO_NAME},${PROJECT},${BRANCH},${COMMIT_SHA},${PARENT_SHA},${ESCAPED_SUBJECT}" >> "${LEDGER_FILE}"
