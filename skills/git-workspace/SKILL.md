---
name: git-workspace
description: >-
  Manage Git branches, worktrees, history integration (rebase, squash, cherry-pick),
  conflict stops, and evidence-first reflog recovery. Use when creating branches or
  worktrees, synchronizing branches, editing history, or recovering lost commits.
  Not for slicing checkpoint commits: use git-commit.
---

# Git Workspace

## Use when
- Creating dedicated feature branches or isolated worktrees before making edits.
- Integrating branches (rebase, squash, merge, cherry-pick) or resolving conflicts.
- Recovering lost commits, dangling refs, or broken working-tree state via reflog.
- Not for slicing uncommitted diffs into checkpoint commits: use `git-commit`.

## Steps
1. **Inspect state.** Resolve target repository root (`git rev-parse --show-toplevel`), active branch,
   upstream tracking, clean vs. dirty status (`git status --short`), and reflog head. All commands execute
   strictly from the target repository root.
2. **Branch and worktree management.** Enforce the branch-before-edits invariant. Create dedicated feature
   branches (`git switch -c <name>`). When working across parallel tasks or spikes without disturbing current
   working-tree state, create an isolated worktree following [references/worktrees.md](references/worktrees.md).
   Never remove a worktree containing uncommitted or unmerged work without explicit confirmation.
3. **Integration and history editing.** Rebase local unshared branches onto upstream base; collapse fixup
   checkpoints via squash; cherry-pick with dependency checks. On any merge or rebase conflict: stop immediately,
   report conflicting files and hunks in prose, never guess resolution, and offer clean abort (`git rebase --abort`).
   Follow [references/history-editing.md](references/history-editing.md).
4. **Evidence-first recovery.** When a commit, branch, or working-tree state appears lost or corrupted, inspect
   evidence first (`git reflog`, `git fsck`, `git branch -v`) to identify exact candidate SHAs and timestamps
   before proposing any fix. Never run destructive resets (`git reset --hard`) as a speculative remedy. Restore
   discovered state into a dedicated recovery branch. Follow [references/recovery.md](references/recovery.md).
5. **Verify post-operation state.** Confirm target ref, commit log (`git log -n 3 --oneline`), and clean working
   tree before concluding.

## Your call
- **Branch and worktree naming and target paths**: choose names and locations for new branches or worktrees.
- **Integration strategy**: choose rebase vs. merge when an architectural choice exists.
- **Conflict resolution**: adjudicate conflicting hunks when git stops during integration.
- **Consequential and destructive actions**: require explicit confirmation with impact described first per
  `profile/AGENTS.md` before running destructive commands (`git reset --hard`, force-push, worktree removal).

## Done when
- Target branch or worktree is created, integrated, or safely cleaned up; or lost ref is restored to a named
  branch with observable verification evidence.

## Hands off to
- `git-commit`: when code changes are ready to be sliced, reviewed, and committed.
- `code-review`: when a branch or PR diff is ready for multi-axis static review before integration.
