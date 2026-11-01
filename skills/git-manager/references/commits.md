# Incremental Checkpoint Commits

Reference for `git-manager`. Conventions for slicing changes, formatting Conventional Commits, enforcing pre-commit hygiene, and applying session-mode commit rules.

## 1. Slice Boundaries
- One slice equals one coherent change that can be understood, reviewed, or reverted on its own (for example: contract or schema first, test + minimal fix, documentation update separately when distinct).
- Commit incrementally as each task or sub-task passes its relevant checks. Do not hoard multiple completed tasks in an uncommitted working tree.
- Order slices so every commit builds cleanly on the preceding commit.
- Flag and exclude accidental additions: scratch scripts, `.env` files, build artifacts, debug logs, or unrelated formatting churn.

## 2. Staging Discipline
- Stage explicit paths (`git add <file1> <file2>`) or specific hunks (`git add -p`).
- Never run a blind `git add -A` or `git add .` when untracked files, local worktrees, or unrelated edits exist in the repository.
- Inspect `git diff --cached --stat` and `git diff --cached` before committing to confirm that staged content matches the intended slice and nothing else.

## 3. Message Conventions and Depth Matching
- Use the repository's `AGENTS.md` commit types and scopes when defined; otherwise use Conventional Commits (`feat`, `fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `perf`, `security`).
- Match message depth to change significance:
  - **Trivial or mechanical**: concise imperative subject line only (`<= 72` characters).
  - **Multi-part slice**: subject line + concise bullet list of concrete behavioral changes.
  - **Non-obvious constraint or trade-off**: subject line + bullets + `Rationale:` line explaining why this approach was chosen over alternatives.
- Link issues (`Closes #<id>` or `Refs #<id>`) only when the commit or branch genuinely satisfies those criteria.
- Trust the staged diff over conversation claims; never overclaim untested behavior.

## 4. Deterministic Pre-Commit Gate
Verify all four checks before creating any commit:
1. **Repository and branch**: `git rev-parse --show-toplevel` matches the target repository and active branch matches intent.
2. **Scoped index**: `git diff --cached` contains only this slice.
3. **Verification**: relevant tests, linters, or builds for the touched surface have run and passed.
4. **Secret scan**: zero tokens, keys, passwords, or private connection strings appear in `git diff --cached`.

## 5. Session Modes and Exception Stops

- **`delivery` mode on a non-default working branch**:
  Once the pre-commit gate passes and none of the exception stops below apply, execute `git commit`, verify `git log -1 --oneline` and `git status --short`, and continue working without pausing for approval.

- **Exception stops (always pause for human decision per `profile/AGENTS.md`)**:
  1. Active branch is `main`, `master`, or detached `HEAD`.
  2. Relevant checks failed and cannot be resolved within current task scope (never silently waive failing checks).
  3. Working tree contains unfamiliar modifications or ambiguous untracked files not produced by the current task; present 2-3 slicing options (recommended first) exposing files and consequences.
  4. Operation involves `git revert`, `cherry-pick`, or rewriting shared history.

- **`learning` mode (`profile/learning-contract.md`)**:
  For each slice, state the facts (files, behavior changed, checks present or missing, risks) and ask 0-2 questions drawn from the diff. Pause so the user writes the commit message. Evaluate the user's draft against the diff (`correct`, `missing`, `wrong`, `unsupported` + assistance level) and let them revise. Write a message only if explicitly asked, recording `shown-solution`.

- **`/practice` active**:
  Stop after slice inspection and message calibration: explain the staging boundary and let the user run the `git add` and `git commit` commands directly.
