---
name: git-commit
description: >-
  Turn working-tree changes into clean, atomic Conventional Commits. Use when the user types
  /git-commit or asks to commit, split changes, or write a commit message. The diff is the
  source of truth; the user approves every commit.
---

# Git Commit

## Use when
- `/git-commit`, "commit this", "split these changes", "write the commit message".
- Rebase, squash, cherry-pick, merge or reset: read
  [references/history-editing.md](references/history-editing.md) first.

## Steps
1. **Inspect.** Repo root, branch and upstream, `git status`, `git diff`, `git diff --cached`.
   Read the repo's `AGENTS.md` for commit conventions and `git log -n 5 --oneline` for style.
   Trust the diff over anything said in the conversation.
2. **Group** changes into slices. A slice is one coherent change that could be reviewed or
   reverted on its own (e.g. refactor, then feature, then tests, then docs). Flag accidental
   additions: scratch files, unrelated formatting, debug code.
3. **Order** slices so each commit builds on the previous one.
4. **Draft messages** using the repo's types (`AGENTS.md`), otherwise Conventional Commits
   (`feat`, `fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, ...). Match depth to
   significance:
   - trivial: subject only;
   - several concrete changes: subject + bullet body;
   - non-obvious trade-off: subject + bullets + `Rationale:` line.
5. **Gate** each slice before committing:
   right repo; intended branch (not `main`/`master` unless the repo's `AGENTS.md` allows it);
   staged content is only this slice; tests/build run or explicitly waived; message matches
   the diff.
6. **Commit** the approved slice by staging exactly its files or hunks (never a blind
   `git add -A` when other changes exist), then verify: new SHA, `git log -1`, what remains
   in the working tree.
7. Repeat for the remaining slices.

In `/practice`, stop after step 4: explain the boundaries and let me run the commands.
Commit without asking only if I said so in this session, and never on `main`/`master` unless
the repo allows it.

## Your call
- **How to slice.** Offer 2-3 options, recommended first, each with its draft messages.
  Example: "1 commit" / "2 commits: refactor + feature" / "3 commits: refactor, feature, tests".
- **Approve each commit** before it is created.
- **What next** after the last commit: offer 2-3 actions (push, open PR, keep working, run `document`).

## Done when
- Every approved slice is committed, verified by SHA, and leftover changes are reported.

## Hands off to
- `document`: if a commit carries a decision or insight worth more than a commit message.
- `commit-logger`: after a verified commit, if installed.
