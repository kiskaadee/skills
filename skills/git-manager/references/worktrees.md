# Git Worktrees

Reference for `git-manager`. Manage isolated working trees linked to the same underlying Git repository without cloning or stashing.

## Use Cases
- Working on a quick fix or spike without stashing or switching branches in your main working tree.
- Running parallel test suites or builds in separate checkouts.
- Evaluating a PR branch while keeping current development intact.

## Path Conventions
- Place worktrees outside the primary repository directory (for example, `../<repo>-<feature>` or in a dedicated sibling directory), or under an ignored `.worktrees/` directory.
- Never nest a worktree inside a tracked source directory.

## Core Operations

### 1. Add Worktree
- For an existing branch:
  ```sh
  git worktree add ../<repo>-<branch> <branch>
  ```
- For a new branch off current base:
  ```sh
  git worktree add -b feat/<name> ../<repo>-<feature> <base-ref>
  ```

### 2. Inspect Worktrees
- List all active worktree paths and their checked-out branches/SHAs:
  ```sh
  git worktree list
  ```

### 3. Pinning / Locking
- Prevent accidental pruning when a worktree sits on removable or shared storage:
  ```sh
  git worktree lock <path> --reason "active long-running test build"
  git worktree unlock <path>
  ```

### 4. Safe Removal
- Confirm working-tree status inside the worktree first:
  ```sh
  git -C <path> status --short
  ```
- If clean, remove cleanly:
  ```sh
  git worktree remove <path>
  ```
- If dirty, **never run `git worktree remove --force`** without explicit confirmation from the human owner describing what uncommitted edits will be discarded.
- If a worktree directory was deleted manually, clean up administrative metadata:
  ```sh
  git worktree prune
  ```
