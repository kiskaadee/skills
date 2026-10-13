---
name: inspect-flake-update
description: >-
  Inspect changes when flake.lock is updated. Reviews updated input revisions
  one by one, surfaces upstream changelogs, verifies with nix flake check,
  summarizes modifications, and suggests a commit message.
---

# Inspect Flake Update

## Use when
- `flake.lock` has uncommitted modifications after updating inputs.
- Inspecting, auditing, or reviewing revisions introduced by flake updates.
- Not for general git diff inspections (use `/git-commit`).
- Not for troubleshooting unrelated NixOS build failures (use `/diagnose`).

## Steps
1. **Detect lock changes.** Run `git diff flake.lock` to identify all changed inputs.
   Parse each input node: input name, previous revision, and new revision.
   If `flake.lock` is clean, ask which input the user wants to update.
2. **Review revisions one by one.** For each updated input:
   - Identify repository host and commit comparison range (e.g. `owner/repo@old...new`).
   - Retrieve commit log, PR list, or release notes between the two revisions.
   - Present the changes to the user, highlighting breaking changes, major updates,
     security fixes, or deprecated options.
   - Wait for the user confirmation before proceeding to the next input.
3. **Validate the flake.** Run `nix flake check` to ensure metadata, inputs, and derivations
   evaluate cleanly. If the repository defines host or package builds, optionally run
   dry builds without switching or activating.
4. **Synthesize changes and suggest commit message.** Summarize all inspected inputs,
   noting their updated versions and key upstream changes. Suggest a Conventional Commit
   message (e.g. `chore(flake): bump <input> to <rev>` or `chore(deps): update inputs`).
5. **Hand off.** Hand off to `git-commit` to stage `flake.lock` and execute the commit.

## Your call
- Deciding whether to accept an input update or roll it back.
- Choosing whether to run additional dry builds beyond `nix flake check`.
- Approving the suggested commit message.

## Done when
- All updated inputs have been reviewed, `nix flake check` passes cleanly, the change
  summary and commit message are produced, and handoff to `git-commit` is ready.

## Hands off to
- `git-commit`: to review staged changes and create the commit.
- `diagnose`: if `nix flake check` or derivation evaluation fails.
