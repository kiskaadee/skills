---
name: commit-logger
description: >-
  Record verified Git commit events as lossless, immutable records in a machine-readable
  commit ledger (00-inbox/commit-log.csv). Use when git-commit completes or to log commits.
---

# Commit Logger

## Use when
- Recording a verified Git commit event into the vault ledger (`00-inbox/commit-log.csv`).
- Automatic handoff from `git-commit` after a commit is created.
- Catch-up capture of unlogged commits (`/commit-logger [COMMIT_SHA]`).
- Not for daily reflection or learning assessment: use `journal-builder`.
- Not for triaging notes: use `draft-curation`.

## Steps
1. **Pre-condition and recursion check.** Inspect the target repository root:
   `git rev-parse --show-toplevel`.
   If inside the vault repository itself or named `Brain`, terminate immediately unless
   `--force` or `--allow-brain` is explicitly provided.
2. **Idempotency check.** Verify if the full 40-character commit SHA already exists in
   `00-inbox/commit-log.csv`. If present, exit silently.
3. **Capture via deterministic script.** Run the capture script:
   `bash scripts/log-commit.sh [COMMIT_SHA]` (defaults to `HEAD` if omitted).
   Consult [references/ledger-schema.md](references/ledger-schema.md) for field definitions.
4. **Verify row.** Inspect `00-inbox/commit-log.csv` to confirm the row exists and complies
   with RFC 4180 format.

## Your call
- Whether to force logging a vault commit when operating inside the vault (`--force`).

## Done when
- The verified commit event row exists in `00-inbox/commit-log.csv`, or duplicate was safely skipped.

## Hands off to
- `journal-builder`: at day end to reconstruct history and assess learning objectives from the ledger.
