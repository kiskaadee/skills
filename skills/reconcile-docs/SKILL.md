---
name: reconcile-docs
description: >-
  Audit, reconcile, and generate canonical repository documentation (README.md,
  ARCHITECTURE.md, docs/adr/, ROADMAP.md, docs/designs/*.md) against commit
  history, code reality, Gitea delivery state, and active plans. Use when
  updating a repository's official documentation. For capturing a single
  session's decision, debug record, or insight into repo docs, use document.
---

# Reconcile Docs

## Use when
- `/reconcile-docs [history-path]`: audit or reconcile repository documentation against history, Gitea state, and active plans.
- Closing a milestone or resolving mid-milestone design spec drift flagged by `code-review` or `implement-slice`.
- Not for capturing a single session's insight or incident record (use `/document`).

## Steps
1. **Discover Present State.** Inspect working-tree status, repository source, tests, configuration, `AGENTS.md`, and existing docs. Build a present-state inventory of components, responsibilities, boundaries, and dependencies.
2. **Reconstruct History.** Read chronological notes and commit history from the repository (`git log`, `docs/discussions/`, `docs/debug/`, `docs/adr/`, or an optional history path) and, when a Gitea remote exists, read merged PRs and published `code-review` PR comments/reviews via `gt` (using `gt-usage` read-only queries). Extract decisions, accepted trade-offs, mid-slice contract pivots, rejected alternatives, migrations, and incidents.
3. **Extract Future Intent.** Identify active plans, roadmaps (`ROADMAP.md`, `docs/designs/*.md`), and, when a Gitea remote exists, read open/closed Gitea milestones, issues, and Project Board column placement (`Completed` vs. `Backlog`, `Ready`, `Work in Progress`, `Review`) read-only via `gt`. Classify each item as committed, planned, exploratory, or superseded. Never mutate Gitea issues, PRs, or board cards.
4. **Reconcile and Detect Conflicts.** Correlate past claims, present code reality, and future plans using [references/reconciliation-matrix.md](references/reconciliation-matrix.md). Flag contradictions (historical claims contradicted by code, mid-slice spec drift in `docs/designs/*.md`, or `Backlog` plans masquerading as current implementation).
5. **Human Checkpoint.** Present a Reconciliation Report following [references/checkpoint-format.md](references/checkpoint-format.md) listing present architecture, recovered decisions, resolved and unresolved conflicts, and proposed document mutations. Stop for user approval.
6. **Draft or Update Canonical Docs.** Once approved, generate or update target artifacts following [references/doc-contracts.md](references/doc-contracts.md) in order:
   - `README.md` (identity, purpose, high-level navigation)
   - `ARCHITECTURE.md` (canonical present-state system model only)
   - `docs/adr/` (accepted or superseded decision records with context)
   - `ROADMAP.md` (intentional future direction and completed milestones)
   - `docs/designs/*.md` (when an active multi-slice design spec has drifted behind merged slices)
7. **Verify Consistency.** Run cross-document consistency checks: verify no future claims in ARCHITECTURE, no obsolete claims in README or active design specs, consistent terminology, and valid links.

## Your call
- History source location if not specified or ambiguous.
- Reconciliation conflict resolutions: whether to supersede, document migration, or drop stale claims.
- Approval of the Reconciliation Report before writing any documentation file.
- Which suggested ADR candidates warrant writing.

## Done when
- The Reconciliation Report is approved by the user, canonical documentation files are written or updated, and consistency validation passes cleanly.

## Hands off to
- `git-manager`: for branch setup or committing updated documentation (`Suggested Next Step: /git-manager`).
- `gitea-plan`: when reconciled `ROADMAP.md` or `docs/designs/*.md` require new or updated Gitea milestones, issues, or board reconciliation (`Suggested Next Step: /gitea-plan`).
- Emit one outcome-matched `Suggested Next Step` on standalone turns per [skeleton](../build-skill/references/skeleton.md).
