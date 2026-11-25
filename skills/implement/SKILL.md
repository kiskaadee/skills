---
name: implement
description: >-
  Execute a GitHub vertical-slice issue end-to-end with preflight checks,
  delta-test decomposition, adaptive test-writer/code-writer subagents, 1:1
  commits, and Draft PR publishing. Use when implementing a ready GitHub issue
  or addressing code-review rework. Not for planning (use projects), static
  review (use code-review), or runtime QA and merge (use verify).
---

# Implement

## Use when
- Delivering a ready GitHub issue slice on a non-default branch or worktree.
- Executing rework passes routed back from `code-review` on an open Draft PR.
- Not for decomposing epics or creating issues: use `projects`.
- Not for static diff review or PR review publishing: use `code-review`.
- Not for black-box runtime QA, PR promotion, or merge: use `verify`.

## Steps
Pure orchestrator invariant: mutate only your branch-scoped checkpoint file
directly. Never write production code, never write tests, never perform code
review, and never publish PR review comments (`code-review` owns review
publishing).

1. **Preflight and board transition.** Before preflight or checkpointing, read
   [references/preflight.md](references/preflight.md). Verify GitHub repo
   identity via `gh repo view --json url` per
   [planning-contract.md](../projects/references/planning-contract.md).
   Classify the working tree (`CLEAN_BASE`, `EXISTING_SLICE_BRANCH`,
   `ADOPTABLE_DIFF`, `CONFLICTING_STATE`, `WRONG_BASE`). Halt immediately on
   `CONFLICTING_STATE` or `WRONG_BASE`. Otherwise create or switch to a
   non-`main` branch or worktree via `git-manager`, and move the issue card
   `Ready -> Work in Progress` per
   [github-projects-v2.md](../projects/references/github-projects-v2.md).
2. **Step 1 delta-test decomposition.** Before decomposing tasks or spawning
   workers, read
   [references/decomposition-and-roles.md](references/decomposition-and-roles.md).
   Inspect existing tests on affected seams (`covered`, `partial/weak`,
   `missing`). Auto-skip Step 1 for trivial `<= 2`-file localized fixes with no
   new test seam. If `--dry-run`, print the plan and halt with zero mutations.
   Otherwise write slice tasks directly in plain `todo.txt` format inside
   `$(git rev-parse --git-common-dir)/implement-state/<branch_slug>.txt`
   without invoking `tuxedo`.
3. **Adaptive execution loop.** Dispatch subagents with embedded OS-level
   non-interactive timeout wrapping (`1-worker` fast path for auto-skipped
   trivial fixes, or `test-writer` -> `code-writer` with 3-4 task worker
   recycling and a 2-turn deadlock breaker). Commit 1:1 per completed
   deliverable via `git-manager`, and mark completed tasks done in
   `"$state_file"`.
4. **Draft PR and state cleanup.** Before opening or syncing a Draft PR, read
   [references/pr-and-drift.md](references/pr-and-drift.md). Push via
   `git-manager`, open or sync a Draft PR (`gh pr create --draft`, `Closes #<N>`,
   `Contract Drift: none | <summary>`), delete `"$state_file"`, and keep the
   board card in `Work in Progress`.

## Your call
- **Branch adoption (`ADOPTABLE_DIFF`) or re-branching (`WRONG_BASE`)**: confirm
  how to handle existing working-tree changes or diverged branches.
- **Deadlock escalation**: resolve 2-turn `test-writer`/`code-writer` deadlocks
  or approve routing to `diagnose`.
- **Scope or contract drift**: confirm whether unexpected contract changes stay
  in-slice or split into a follow-up issue via `projects`.

## Done when
- Every slice task is implemented, tested, and committed 1:1 on a non-`main`
  branch.
- A Draft PR is open or synced with `Closes #<N>` and `Contract Drift: ...`.
- The branch-scoped `"$state_file"` is deleted and the board card remains in
  `Work in Progress`.

## Hands off to
- `code-review`: to audit the Draft PR (`Suggested Next Step: /code-review`).
- `diagnose`: when a 2-turn deadlock or unexpected failure needs root-cause
  debugging (`Suggested Next Step: /diagnose`).
- `projects`: when scope splits or an explicit abort requires replanning.
- Emit one outcome-matched `Suggested Next Step:` on standalone turns; suppress
  when delegated to a subagent per [skeleton.md](../build-skill/references/skeleton.md).
