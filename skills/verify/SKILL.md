---
name: verify
description: >-
  Run risk-proportional black-box runtime QA, inspect remote CI checks, promote
  verified GitHub Draft PRs, and execute human-gated merge closeout with
  Projects v2 board transitions. Use when verifying a ready-reviewed GitHub PR
  or aborting an abandoned Draft PR. Not for static diff review (use
  code-review), debugging (use diagnose), or implementation (use implement).
---

# Verify

## Use when
- Verifying a GitHub PR whose latest `code-review` passed with `verdict=ready`.
- Promoting a verified Draft PR to ready-for-review and running merge closeout.
- Explicitly aborting an abandoned or superseded Draft PR.
- Not for static diff review (`code-review`), debugging (`diagnose`), or writing
  code / managing `todo.txt` state (`implement`).

## Steps
Precondition: an existing open GitHub PR verified via `gh repo view --json url`
per [planning-contract.md](../projects/references/planning-contract.md) (no
manual PR fallback; route to `implement` if none exists). `verify` has zero
`todo.txt` cleanup responsibility (`implement` owns its checkpoint file).

1. **Phase 1: Read-Only Runtime QA and CI.** Before running QA checks, read
   [references/qa-dispositions.md](references/qa-dispositions.md). Confirm the
   latest `cr-review-meta` matches exact current `head_sha` with
   `verdict=ready`; if missing, stale, or `needs_rework`, halt and route to
   `code-review`. Execute `RV-*` checks (sized by risk tier) with explicit
   dispositions (`PASS`, `FAIL`, `BLOCKED (env/fixture)`,
   `BLOCKED (out-of-bounds)`, `INCONCLUSIVE`), and inspect `gh pr checks`. On
   red CI, inspect `gh run view --log-failed` and route to `diagnose` or
   `implement`.
2. **Phase 2: Promotion.** Before posting the ledger, promoting, closing out,
   or aborting, read
   [references/closeout-and-abort.md](references/closeout-and-abort.md). When
   Phase 1 passes (zero `FAIL`, zero unresolved `BLOCKED (env/fixture)` or
   `INCONCLUSIVE`, green CI), post the final Verification Ledger comment,
   promote the PR (`gh pr ready`), and move the board card
   `Work in Progress -> Review` per
   [github-projects-v2.md](../projects/references/github-projects-v2.md).
3. **Phase 3: Human Merge Gate and Closeout.** Present the verification packet
   (static provenance, runtime dispositions, CI, and `Contract Drift` per
   [pr-and-drift.md](../implement/references/pr-and-drift.md)) for human merge
   authorization. On approval: merge the PR, execute `Review -> Completed`
   directly via `issue.projectItems` per
   [github-projects-v2.md](../projects/references/github-projects-v2.md), and
   chain `reconcile-docs` + `projects` when `Contract Drift` != `none`. On
   rejection: run `gh pr ready --undo` and move `Review -> Work in Progress`.
4. **Explicit Draft PR Abort (on request only).** Only when explicitly invoked
   to close an abandoned/superseded Draft PR, skip Steps 1-3 and follow the
   abort path in
   [references/closeout-and-abort.md](references/closeout-and-abort.md)
   (`gh pr close` + revert board card to `Backlog`).

## Your call
- **`live-infra` authorization**: approve before running `live-infra` checks.
- **Non-passing checks**: decide repair, fixture fix, or operator window for
  `FAIL`, `BLOCKED`, or `INCONCLUSIVE` dispositions.
- **Merge or abort authorization**: approve/reject merge at Phase 3, or confirm
  before aborting a Draft PR (`gh pr close` + `Backlog`).

## Done when
- Merged: PR merged, card in `Completed`, and drift handoff emitted if needed.
- Rejected/blocked: PR stays Draft, card in `Work in Progress`, handoff stated.
- Aborted: Draft PR closed and card reverted to `Backlog`.

## Hands off to
- `code-review`: missing, stale, or `needs_rework` `cr-review-meta` (`Suggested Next Step: /code-review`).
- `implement`: QA or CI requires code fixes (`Suggested Next Step: /implement #<issue>`).
- `diagnose`: opaque CI or runtime failure (`Suggested Next Step: /diagnose`).
- `reconcile-docs` and `projects`: post-merge when `Contract Drift` != `none` (`Suggested Next Step: /reconcile-docs`).
- Emit one outcome-matched `Suggested Next Step:` on standalone turns; suppress
  when delegated per [skeleton.md](../build-skill/references/skeleton.md).
