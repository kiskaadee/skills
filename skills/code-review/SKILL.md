---
name: code-review
description: >-
  Inspects git diffs, GitHub pull requests, and commit ranges across four
  independent axes: Spec & Scope, Standards & Smells, Seam & Test Integrity,
  and Defensive Invariants. Use when reviewing code changes before merge or
  verifying diff quality. Not for live runtime QA: use verify.
---

# Code Review

## Use when
- Reviewing a branch, open GitHub PR, work-in-progress diff, or commit range.
- Evaluating code structure, hygiene, defensive invariants, and test seams.
- Not for live runtime QA, CI promotion, or merge: use `verify`.
- Not for debugging an unknown symptom: use `diagnose`.

## Steps
Keep the codebase strictly read-only: never edit repository files, create
commits, or mutate GitHub Projects v2 board cards.

1. **Pin the fixed point and scope.** Resolve `<base>` and `HEAD` SHAs
   (`git rev-parse <base> HEAD`). Inspect working-tree state (`git status --short`,
   unstaged `git diff`, staged `git diff --cached`, relevant untracked files)
   and committed history (`git diff <base>...HEAD`, `git log <base>..HEAD --oneline`).
2. **Select execution tier.** Before inspecting, read [axes](references/axes.md)
   and assign `Lightweight`, `Standard`, or `High-Assurance`. For `High-Assurance`,
   never run `Sequential` or a single combined subagent: spawn a dedicated isolated
   Axis 3 (`Seam & Test Integrity`) subagent separate from Axes 1/2/4 and record
   both subagent IDs in `Execution Mode`.
3. **Inspect the four axes independently.**
   - **Spec & Scope**: issue/spec satisfaction, alignment with canonical docs
     (`ARCHITECTURE.md`, `ROADMAP.md`, ADRs), minimal shared-file footprint,
     and affected local markdown accuracy.
   - **Standards & Smells**: repo rules, [smell-heuristics](references/smell-heuristics.md),
     missing docstrings on new/modified public symbols, stale inline comments,
     and lint/format regressions.
   - **Seam & Test Integrity**: audit test diffs against
     [seams-and-mocking](../tdd/references/seams-and-mocking.md) and
     [test-quality](../tdd/references/test-quality.md).
   - **Defensive Invariants**: [defensive-invariants](references/defensive-invariants.md)
     (trust boundaries, authority, consistency, failure semantics, resource limits).
4. **Record findings and executable runtime checks.** Before formatting output
   or publishing, read [finding-schema](references/finding-schema.md). Valid
   findings start in `Pending Triage` (never self-dismiss). Keep disagreements
   under `Unresolved`. Emit runnable `RV-*` checks (`local` vs. `live-infra`,
   explicit `FAIL if ...` signals) for stateful or high-risk paths.
5. **Determine verdict and publish on open GitHub PRs.** Apply [axes](references/axes.md)
   (`Needs Rework`, `Blocked`, `Pending Triage`, `Ready`). Verify GitHub repo via
   `gh repo view --json url` and check for an open PR on `HEAD`. Whenever an open
   GitHub PR exists (standalone or delegated), build the payload via
   `skills/code-review/scripts/build_review.py --input ... --diff ... --reviews ... --comments ... --head-sha <sha> --verdict <ready|needs_rework>`
   and pipe stdout to `gh api repos/{owner}/{repo}/pulls/{n}/reviews --input -`.
   Handle exit `2` (duplicate `(head_sha, verdict)` skip) and exit `1`
   (`3-rework-cycle cap` escalation). When no open PR exists or in local-only mode,
   skip publishing and explicitly state in output that no open PR was found and
   findings are reported locally.

## Your call
- **Triaging findings (3 exits before `Ready`)**: choose Exit A (fix in-branch),
  Exit B (promote to a GitHub Issue), or Exit C (dismiss as invalid/false positive).
- **Escalations and disagreements**: adjudicate `Unresolved` findings or a
  `3-rework-cycle cap` halt.
- **Release authority**: static provenance never authorizes merge or release.

## Done when
- All four axes are inspected, findings and `RV-*` checks are recorded, and the
  review is published to the open GitHub PR (or explicitly reported locally when
  no open PR exists).

## Hands off to
- `implement`: on `Needs Rework` (`<= 2`-file localized fixes take the fast path;
  complex rework enters Step 1; `Suggested Next Step: /implement #<issue>`).
- `verify`: on `Ready` (`Suggested Next Step: /verify`).
- `tdd`: when Axis 3 fails (`Suggested Next Step: /tdd <affected-test-files>`).
- `diagnose`: when a finding exposes an unknown root cause (`Suggested Next Step: /diagnose`).
- Emit one outcome-matched `Suggested Next Step:` on standalone turns; suppress
  when delegated per [skeleton](../build-skill/references/skeleton.md).
