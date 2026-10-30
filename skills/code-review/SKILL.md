---
name: code-review
description: >-
  Inspects git diffs, pull requests, and commit ranges across four independent
  axes: Spec & Scope, Standards & Smells, Seam & Test Integrity, and Defensive
  Invariants. Use when reviewing code changes before merge or verifying diff
  quality. Not for live runtime QA: use verify-slice.
---

# Code Review

## Use when
- Reviewing a branch, pull request, work-in-progress diff, or commit range before merge.
- Evaluating code structure, defensive invariants, and test seam integrity.
- Not for live runtime browser or deployment testing: use `verify-slice`.
- Not for debugging an unknown symptom: use `diagnose`.

## Steps
1. **Pin the fixed point and scope.** Resolve the base ref and record its commit SHA via `git rev-parse <base>`. Inspect working-tree state (`git status --short`, unstaged `git diff`, staged `git diff --cached`) alongside committed history (`git diff <base>...HEAD` and `git log <base>..HEAD --oneline`). Report findings distinguished across committed, staged, and unstaged changes.
2. **Select execution tier.** Match the change to the risk tiers from [axes](references/axes.md) (`Lightweight`, `Standard`, or `High-Assurance`). Single-agent sequential pass for Lightweight; independent review passes for Standard; isolated subagents per axis for High-Assurance.
3. **Inspect the four axes.** Evaluate the diff against each axis independently using [axes](references/axes.md):
   - **Spec & Scope**: originating requirements satisfied, minimal shared-file footprint, zero scope creep.
   - **Standards & Smells**: repository rules and Fowler smell diagnostics from [smell-heuristics](references/smell-heuristics.md) (evaluated as confirmed violations, potential smells, or contextual trade-offs).
   - **Seam & Test Integrity**: tests verify public interface seams, assertions are non-tautological, negative/boundary paths covered, vertical slices prioritized over bulk imagined tests.
   - **Defensive Invariants**: system properties from [defensive-invariants](references/defensive-invariants.md) (trust boundaries, authority, consistency, failure semantics, resource limits).
4. **Record structured findings.** Record every finding using the schema in [finding-schema](references/finding-schema.md) (`ID`, `Axis`, `Severity`, `Evidence`, `Invariant`, `Impact`, `Disposition`). A strong pass on one axis never compensates for a failure on another.
5. **Aggregate without silent resolution.** When multiple reviewers or passes disagree, keep the disagreement visible under `Unresolved` until evidence settles it.
6. **Recommend runtime verification scenarios.** Identify stateful or high-risk paths that static inspection cannot prove and list them as suggested scenarios for `verify-slice`.
7. **Present the review summary.** Group findings by axis and apply the decision matrix from [axes](references/axes.md): `Needs Rework` (confirmed defects require changes), `Blocked` (unresolved Critical/High risks or unestablished scope), or `Ready` (no blocking defects; documented trade-offs accepted by owner). Never authorize release: the human owner decides release.

## Your call
- **Handling findings**: decide whether confirmed findings block merge, trigger a rework loop, or become tracked follow-up issues.
- **Adjudicating unresolved disagreements**: resolve conflicting reviewer perspectives or accepted architectural trade-offs.
- **Authorizing release**: verification and review evidence inform decisions, but the human owner remains the sole release authority.

## Done when
- All four axes have been inspected across working-tree and committed changes, every finding is recorded with evidence and disposition, candidate runtime scenarios are passed to `verify-slice` if needed, and the human owner has reviewed the findings.

## Hands off to
- `diagnose`: when a finding exposes a root cause that requires deeper troubleshooting.
- `verify-slice`: to execute behavioral and runtime verification scenarios.
- `git-commit`: when committing review fixes or test adjustments.
