---
name: draft-curation
description: >-
  Triage, classify, format, validate, and move raw notes and drafts from an inbox or staging
  directory into canonical knowledge lifecycle directories. Use when triaging 00-inbox/ drafts.
---

# Draft Curation

## Use when
- `/draft-curation`: triaging, classifying, and ingesting raw notes from `00-inbox/` into canonical vault lifecycle directories.
- Handoff from `document` after drafting notes into staging inbox.
- Not for capturing git commits into ledger: use `commit-logger`.
- Not for authoring fresh documents from conversation: use `document`.

## Steps
1. **Preflight verification.** Verify repository health before moving files (run vault validator if present, e.g. `python scripts/validate-brain.py`).
2. **Inventory staging.** Scan `00-inbox/` for pending drafts, ignoring system ledgers (`commit-log.csv`), `.keep`, or `README.md`. Identify project context and note scope.
3. **Classify and format.** Determine target directory, frontmatter type, and filename slug using [references/curation-matrix.md](references/curation-matrix.md). Ensure H1 heading, relative links, and clean markdown.
4. **Checkpoint.** Present source path, proposed destination, proposed frontmatter, and epistemic rationale. Stop for confirmation before moving files.
5. **Relocate and reconcile.** Write transformed file to destination (reconciling with existing daily journal if applicable, preserving existing edits and unioning `assessed_commits`). Delete original draft from `00-inbox/`.
6. **Validate integrity.** Re-run repository validation suite to verify frontmatter, links, and syntax pass cleanly.

## Your call
- **Confirm destination and frontmatter**: approve target path, frontmatter type, and rationale.
- **Decomposition**: whether to split a draft covering multiple distinct concerns.
- **Reconciliation edits**: approving changes when merging into an existing daily journal.

## Done when
- Staged draft is relocated, removed from `00-inbox/`, and repository validation passes cleanly.

## Hands off to
- `git-commit`: to inspect working-tree diff and commit curated documents with semantic commit types.
