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
- Not for general Git operations or history management (use `/git-manager`).
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
4. **Synthesize changes and prepare commit.** Summarize all inspected inputs, noting their
   updated versions and key upstream changes. In `delivery` mode, draft a Conventional Commit
   message (e.g. `chore(flake): bump <input> to <rev>`); in `learning` mode, let the user write it.
5. **Hand off.** Hand off to `git-manager` to stage `flake.lock` and commit per session-mode rules.

## Your call
- Deciding whether to accept an input update or roll it back.
- Choosing whether to run additional dry builds beyond `nix flake check`.
- Approving the commit on `main`/`master`, or writing the message in `learning` mode per `profile/AGENTS.md`.

## Done when
- All updated inputs have been reviewed, `nix flake check` passes cleanly, the change
  summary is produced, and handoff to `git-manager` is ready.

## Hands off to
- `git-manager`: to stage `flake.lock` and record the commit.
- `diagnose`: if `nix flake check` or derivation evaluation fails.
