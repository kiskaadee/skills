#!/usr/bin/env bash
# run_regression.sh - Deterministic behavioral contract test runner for kiskaadee/skills
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

echo "=========================================================="
echo " Running Skills Ecosystem Behavioral Contract Tests"
echo " Target Root: ${REPO_ROOT}"
echo "=========================================================="

# 1. Run install.sh check on current environment
echo
echo "--- [1/3] Verifying Skills Installation & Symlinks ---"
"${REPO_ROOT}/install.sh" check

# 2. Run Python deterministic behavioral contracts suite
echo
echo "--- [2/3] Running Behavioral Contract & Invariant Tests ---"
python3 -m unittest "${SCRIPT_DIR}/test_skills_behavioral_contracts.py" "${SCRIPT_DIR}/test_build_review.py" -v

# 3. Qualitative Dogfood Protocol Verification
echo
echo "--- [3/3] Validating Clean-Room Reproducibility & Contract Protocols ---"
# Verify that projects references clean-room audit schema
grep -q "Independent Zero-Context Reproducibility Audit" "${REPO_ROOT}/skills/projects/references/tiers-and-audit.md"
grep -q "Auditor Report Schema" "${REPO_ROOT}/skills/projects/references/tiers-and-audit.md"
# Verify that implement defines preflight working-tree classification
grep -q "CLEAN_BASE" "${REPO_ROOT}/skills/implement/references/preflight.md"
# Verify that code-review defines cr-review-meta provenance marker
grep -q "cr-review-meta" "${REPO_ROOT}/skills/code-review/references/finding-schema.md"
# Verify that gt-usage defines project column move recipe
grep -q "Move issue card between columns" "${REPO_ROOT}/skills/gt-usage/references/commands.md"

echo "Clean-room reproducibility and deviation protocols verified."

echo
echo "=========================================================="
echo " All behavioral contract and regression tests PASSED (exit 0)"
echo "=========================================================="
