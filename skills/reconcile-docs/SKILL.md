---
name: reconcile-docs
description: >-
  Reconcile historical evidence, present code reality, and future plans into canonical repository documentation. Use when typing /reconcile-docs to audit, update, or generate README, ARCHITECTURE, ROADMAP, or ADRs.
---

# Reconcile Docs

## Use when
- `/reconcile-docs [history-path]`: audit or reconcile repository documentation against history and active plans.
- Not for capturing a single session's insight (use `/document`).
- Not for triaging inbox notes into vault directories (use `draft-curation`).

## Steps
1. **Discover Present State.** Inspect working-tree status, repository source, tests, configuration, and existing docs. Build a present-state inventory of components, responsibilities, boundaries, and dependencies.
2. **Reconstruct History.** Read chronological notes and commit history from the provided history source (vault records, discussions, previous ADRs). Extract decisions, rejected alternatives, migrations, constraints, and incidents. Classify each observation.
3. **Extract Future Intent.** Identify active plans, roadmaps, and open proposals. Classify each as committed, planned, exploratory, or superseded.
4. **Reconcile and Detect Conflicts.** Correlate past claims, present code reality, and future plans using [references/reconciliation-matrix.md](references/reconciliation-matrix.md). Flag contradictions (such as historical claims contradicted by code, or plans masquerading as current implementation).
5. **Human Checkpoint.** Present a Reconciliation Report following [references/checkpoint-format.md](references/checkpoint-format.md) listing present architecture, recovered decisions, resolved and unresolved conflicts, and proposed document mutations. Stop for user approval.
6. **Draft or Update Canonical Docs.** Once approved, generate or update target artifacts following [references/doc-contracts.md](references/doc-contracts.md) in order:
   - `README.md` (identity, purpose, high-level navigation)
   - `ARCHITECTURE.md` (canonical present-state system model only)
   - `docs/adr/` (accepted or superseded decision records with context)
   - `ROADMAP.md` (intentional future direction only)
7. **Verify Consistency.** Run cross-document consistency checks: verify no future claims in ARCHITECTURE, no obsolete claims in README, consistent terminology, and valid links.

## Your call
- History source location if not specified or ambiguous.
- Reconciliation conflict resolutions: whether to supersede, document migration, or drop stale claims.
- Approval of the Reconciliation Report before writing any documentation file.
- Which suggested ADR candidates warrant writing.

## Done when
- The Reconciliation Report is approved by the user, canonical documentation files are written or updated, and consistency validation passes cleanly.

## Hands off to
- `git-commit`: to review diffs and commit updated documentation files.
