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
1. **Pin the fixed point and scope.** Resolve the base ref and record exact base and head commit SHAs (`git rev-parse <base> HEAD`). Inspect working-tree state (`git status --short`, unstaged `git diff`, staged `git diff --cached`, and relevant untracked files) alongside committed history (`git diff <base>...HEAD` and `git log <base>..HEAD --oneline`). Record the covered revisions and working-tree diff state (for example, clean tree or diff fingerprint) so downstream tools can verify whether the reviewed diff remained unchanged, and distinguish findings across committed, staged, and unstaged changes.
2. **Select execution tier.** Match the change to the risk tiers from [axes](references/axes.md) (`Lightweight`, `Standard`, or `High-Assurance`). Single-agent sequential pass for `Lightweight`; independent review passes for `Standard`; for `High-Assurance`, never run `Sequential` or a single combined subagent: spawn a dedicated isolated Axis 3 (`Seam & Test Integrity`) subagent separate from Axes 1/2/4 and record both subagent IDs in `Execution Mode`.
3. **Inspect the four axes.** Evaluate the diff against each axis independently using [axes](references/axes.md):
   - **Spec & Scope**: originating requirements satisfied, aligned with canonical project direction (`ARCHITECTURE.md`, `ROADMAP.md`, ADRs, active milestone) when present, minimal shared-file footprint, zero scope creep.
   - **Standards & Smells**: repository rules and Fowler smell diagnostics from [smell-heuristics](references/smell-heuristics.md) (evaluated as confirmed violations, potential smells, or contextual trade-offs).
   - **Seam & Test Integrity**: audit test diffs against [seams-and-mocking](../tdd/references/seams-and-mocking.md) and [test-quality](../tdd/references/test-quality.md) (public seams, injected timing callables, deterministic waits/teardown, non-tautological literals, boundary coverage, single-behavior naming).
   - **Defensive Invariants**: system properties from [defensive-invariants](references/defensive-invariants.md) (trust boundaries, authority, consistency, failure semantics, resource limits).
4. **Record structured findings.** Record every finding using the schema in [finding-schema](references/finding-schema.md) (`ID`, `Axis`, `Severity`, `Evidence`, `Invariant`, `Impact`, `Disposition`). Never self-assign `Accepted Trade-off` on a review pass: all valid findings start as `Confirmed` (or `Unresolved`); only the human owner may grant `Accepted Trade-off`. A strong pass on one axis never compensates for a failure on another.
5. **Aggregate without silent resolution.** When multiple reviewers or passes disagree, keep the disagreement visible under `Unresolved` until evidence settles it.
6. **Emit executable runtime checks.** For stateful or high-risk paths that static inspection cannot prove, emit runnable fenced shell commands for `verify-slice` following the Step 6 contract in [finding-schema](references/finding-schema.md) (stating purpose, `local` vs. `live-infra` scope classification, explicit pass condition, and explicit failure signal).
7. **Present the review summary.** Group findings by axis and apply the decision matrix from [axes](references/axes.md): `Needs Rework` (confirmed defects require changes), `Blocked` (unresolved Critical/High risks or unestablished scope), `Pending Triage` (only untriaged Medium/Low findings remain; never recommend merging until each takes one of the 3 triage exits in [finding-schema](references/finding-schema.md)), or `Ready` (all four axes completed and zero untriaged findings remain). Static review establishes static provenance for that diff only; never authorize release.
8. **Auto-publish the PR review block (standalone open PR only).** Keep the codebase strictly read-only (never edit repo files or mutate project boards). When invoked standalone on an open PR, draft `review-body.md` (and `inline-comments.json` when inline findings exist) per section 4 of [finding-schema](references/finding-schema.md), including the compact 4-axis pass block on clean `Ready` reviews, verify `head_sha` and duplicate/pending guards, and automatically publish one `--comment` review pinned with `--commit <reviewed-head-sha>` in the same turn. Skip PR publishing when delegated inside `implement-slice`.

## Your call
- **Triaging findings (3 exits before merge)**: for each `Confirmed` or `Unresolved` finding, decide whether to (A) fix in-branch now, (B) promote to a live tracker (append/create Gitea issue or `todo.txt` via `tuxedo add`), or (C) grant permanent `Accepted Trade-off` (`record`).
- **Adjudicating unresolved disagreements**: resolve conflicting reviewer perspectives.
- **Authorizing release**: verification and review evidence inform decisions, but the human owner remains the sole release authority.

## Done when
- All four axes have been inspected across working-tree and committed changes, every finding is recorded with evidence and disposition, executable Step 6 runtime checks are emitted for `verify-slice` if needed, and the human owner has reviewed the findings.

## Hands off to
- `tdd`: when Axis 3 fails (`Suggested Next Step: /tdd <affected-test-files>`) or production rework needs test-first fixes (`Suggested Next Step: /tdd <module-or-test-path>`).
- `diagnose`: when a finding exposes an unknown root cause (`Suggested Next Step: /diagnose`).
- `verify-slice`: when `Ready` and runtime/`RV-*` checks are needed (`Suggested Next Step: /verify-slice`).
- `git-manager`: when branching, committing review fixes, or rebasing.
- `gitea-pr`: when `Ready` on an open PR with clean runtime checks (`Suggested Next Step: /gitea-pr <pr-or-issue>`).
- Emit one outcome-matched `Suggested Next Step` on standalone turns; suppress when delegated (per [skeleton](../build-skill/references/skeleton.md)).
