---
name: git-manager
description: >-
  Manage Git repository hygiene, branches, worktrees, incremental Conventional Commits,
  history integration (rebase, squash, cherry-pick, merge), conflict stops, and
  evidence-first reflog recovery. Use when creating branches or worktrees, committing
  completed task checkpoints, integrating branches, or recovering lost commits. Not for
  pull request lifecycle: use gitea-pr. Not for diff code inspection: use code-review.
---

# Git Manager

## Use when
- Creating dedicated branches or isolated worktrees before making edits.
- Recording clean, atomic Conventional Commits as coherent tasks finish, or slicing a dirty tree.
- Integrating branches (rebase, squash, merge, cherry-pick) or stopping cleanly on conflicts.
- Recovering lost commits, dangling refs, or broken working-tree state via reflog.
- Not for pull request creation or review threads: use `gitea-pr`.
- Not for multi-axis static diff evaluation: use `code-review`.

## Steps
1. **Inspect repository state.** Resolve repository root (`git rev-parse --show-toplevel`), active
   branch, upstream tracking, working-tree status (`git status --short`), repo `AGENTS.md`
   conventions, and `git log -n 5 --oneline`. Run all commands from the target repository root;
   trust the diff over conversation claims.
2. **Branch and worktree isolation.** Enforce branch-before-edits (`git switch -c <name>`). For
   parallel slices or spikes without disturbing the current working tree, manage isolated worktrees
   per [references/worktrees.md](references/worktrees.md). Never remove a worktree containing
   uncommitted or unmerged work without explicit confirmation.
3. **Incremental checkpoint commits.** Group coherent, independently revertible slices and format
   messages per [references/commits.md](references/commits.md). Enforce the pre-commit gate: right
   repo, explicit file or hunk staging (never blind `git add -A` over unrelated or scratch files),
   relevant checks passing, zero secrets, and message faithful to the diff. Follow `profile/AGENTS.md`:
   - **`delivery` mode on a non-default working branch**: commit each verified unit immediately
     without pausing for approval, unless an exception applies (`main`/`master`, failing checks,
     or unfamiliar working-tree edits).
   - **`learning` mode**: list diff facts, ask 0-2 questions, and pause so the user writes the
     commit message per `profile/learning-contract.md`. In `/practice`, let the user run the commands.
4. **Integration and history editing.** Rebase local unshared branches, squash noisy fixups, merge,
   or cherry-pick per [references/history-editing.md](references/history-editing.md). On any
   conflict: stop immediately, report conflicting files and hunks in prose, never guess resolution,
   and offer clean `--abort`.
5. **Evidence-first recovery.** For lost commits, detached `HEAD`, or botched history edits, inspect
   `git reflog` and `git fsck` before acting and restore into `recovery/<topic>` per
   [references/recovery.md](references/recovery.md). Never run speculative `--hard` resets.
6. **Verify post-operation state.** Confirm branch ref, new commit SHA (`git log -n 3 --oneline`),
   and remaining working-tree status (`git status --short`).

## Your call
- **Direct `main`/`master` commits or ambiguous dirty trees**: approve any commit on `main`/`master`
  or choose how to slice unfamiliar pre-existing working-tree edits.
- **`learning` mode commit reasoning**: write the commit message and rationale per `learning-contract.md`.
- **Integration strategy and exceptions**: choose rebase vs. merge when non-obvious, and adjudicate
  conflicts, reverts, or cherry-picks.
- **Destructive operations**: explicitly confirm with impact described first per `profile/AGENTS.md`
  before `git reset --hard`, `git restore <file>`, `git clean -fd`, force-push, or dirty worktree removal.

## Done when
- Target branch, worktree, checkpoint commit, integration, or recovery branch is verified by SHA
  and `git status --short` reflects expected leftover state.

## Hands off to
- `code-review`: when a branch or commit range is ready for multi-axis static diff review.
- `gitea-pr`: when verified commits are pushed and ready for pull request creation or update.
- `document`: when a commit or recovery surfaces a decision or insight worth recording separately.
