# Evidence-First Git Recovery

Reference for `git-workspace`. Procedures for diagnosing and recovering lost commits, detached heads, botched rebases, or corrupted refs using observable evidence.

## Core Invariant
Never propose a destructive command (`git reset --hard`, `git checkout -f`, `git clean -fd`) as a speculative remedy. Destructive commands discard uncommitted files permanently. Always inspect evidence first, locate candidate commit SHAs, and restore state into a new named branch.

## 1. Inspect Current State Before Acting

Check working-tree and ref state:
```sh
git status --short
git branch -v
git log -n 5 --oneline
```
If working-tree changes exist, stash or commit them before attempting ref recovery:
```sh
git stash push -m "WIP before reflog recovery"
```

## 2. Reflog Inspection

The reflog records every update to local branch tips and `HEAD`.

- Inspect recent `HEAD` movements:
  ```sh
  git reflog -n 20 --date=iso
  ```
- Look for state transitions:
  - `rebase (finish)` / `rebase (start)`: find the commit immediately preceding `rebase (start)`.
  - `reset: moving to ...`: find the SHA prior to the reset.
  - `commit: ...`: locate orphaned commits from deleted or moved branches.

- Inspect branch-specific reflog:
  ```sh
  git reflog show <branch-name>
  ```

## 3. Verify Candidate Commit

Inspect the candidate SHA before restoring:
```sh
git show <candidate-sha> --stat
git log -1 -p <candidate-sha>
```
Confirm that the commit contains the expected changes and history.

## 4. Non-Destructive Restoration

Never mutate current branch in place with `--hard` reset. Instead, point a dedicated recovery branch at the discovered SHA:
```sh
git branch recovery/<topic> <candidate-sha>
```
Verify the recovered branch:
```sh
git log -n 3 --oneline recovery/<topic>
```
Then switch to the recovery branch cleanly:
```sh
git switch recovery/<topic>
```

## 5. Dangling and Unreachable Objects (Last Resort)

If a commit was not captured in the reflog (e.g. reflog expired or repository corruption):
```sh
git fsck --lost-found
```
Dangling commits appear in `.git/lost-found/commit/`. Inspect each candidate:
```sh
git log -1 -p <dangling-sha>
```
Once found, create a branch off it:
```sh
git branch recovery/<topic> <dangling-sha>
```
