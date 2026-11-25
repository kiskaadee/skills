# Preflight & Branch-Scoped Checkpoint Lifecycle

Sole owner of working-tree classifications, the `--dry-run` zero-mutation
contract, and the `implement` branch-scoped checkpoint lifecycle.

---

## 1. GitHub Remote & Board Guard

Before mutating git state or moving board cards:
1. Verify GitHub repository identity with `gh repo view --json url` per
   [planning-contract.md](../../projects/references/planning-contract.md). If
   the command fails or `AGENTS.md` contains a legacy Gitea planning contract,
   halt and advise migrating to GitHub or using standalone `gt-usage`.
2. After branch/worktree preflight passes (and only when not in `--dry-run`),
   move the target issue card `Ready -> Work in Progress` using `issue.projectItems`
   per [github-projects-v2.md](../../projects/references/github-projects-v2.md).
   If the card is already in `Work in Progress` (resumed slice or rework pass),
   leave it there idempotently.

---

## 2. Working-Tree Classifications

Inspect `git status --porcelain`, `git branch --show-current`, merge/rebase
sentinel files under `$(git rev-parse --git-dir)`, and any open Draft PR or
existing checkpoint file for the target slice. Classify into exactly one state:

| Classification | Condition | Required Action |
| :--- | :--- | :--- |
| `CLEAN_BASE` | Clean working tree on the default base branch (e.g. `main`). | Create and switch to a dedicated non-`main` slice branch or worktree via `git-manager`. |
| `EXISTING_SLICE_BRANCH` | Clean working tree on the target slice's own non-`main` branch with an active checkpoint file or an open Draft PR. | Proceed directly to resume remaining tasks or execute a `code-review` rework pass without re-branching. |
| `ADOPTABLE_DIFF` | Uncommitted changes present, all scoped cleanly to the target slice, with no merge/rebase in progress. | Ask the user to confirm adopting the diff onto a dedicated non-`main` slice branch via `git-manager` before proceeding. |
| `CONFLICTING_STATE` | Unrelated dirty changes, untracked conflicting files, or an active merge, rebase, or cherry-pick. | Halt immediately. Report the exact dirty paths or operation and leave all working-tree and checkpoint files untouched. |
| `WRONG_BASE` | Current branch is neither the base branch nor the target slice's branch, or has diverged unexpectedly from the expected base. | Halt immediately. Ask the user whether to switch or re-branch via `git-manager`, leaving existing checkpoint files untouched. |

---

## 3. `--dry-run` Zero-Mutation Contract

When invoked with `--dry-run`:
- Execute read-only preflight inspection (`gh repo view --json url`, working-tree
  classification, issue acceptance criteria read) and Step 1 delta-test
  decomposition.
- Print the proposed branch name, working-tree classification, seam coverage map
  (`covered`, `partial/weak`, `missing`), execution mode (`1-worker` fast path vs.
  multi-task `test-writer`/`code-writer`), and ordered task list.
- Halt with **zero mutations**:
  - Do not create or switch branches or worktrees.
  - Do not move GitHub Projects v2 cards.
  - Do not create, modify, or delete any checkpoint file.
  - Do not spawn implementation workers, create commits, or touch Draft PRs.

---

## 4. Branch-Scoped Checkpoint Lifecycle

Multi-task slices store resume state inside the shared git common directory so
checkpoints stay isolated per branch across git worktrees and never pollute the
working tree or root `todo.txt`.

### Path & Branch Slug
```bash
git_common_dir="$(git rev-parse --git-common-dir)"
branch="$(git branch --show-current)"
branch_slug="${branch//\//__}"
state_file="${git_common_dir}/implement-state/${branch_slug}.txt"
```

### Plain-Text `todo.txt` Line Format (Direct I/O Only)
- Read and write `"$state_file"` directly (e.g., standard file/shell I/O). Never
  invoke `tuxedo` to read, append, or complete checkpoint tasks.
- Use plain-text `todo.txt` line conventions so external `todo.sh` or `tuxedo`
  can inspect the file if desired:
  - Pending task: `<task description>`
  - Completed task: `x YYYY-MM-DD <task description>`

### Lifecycle Rules
1. **Create / Resume**: Create `"$state_file"` (and its parent directory
   `implement-state/`) after Step 1 decomposition for multi-task slices. On
   `EXISTING_SLICE_BRANCH` resume, read existing pending lines and continue from
   the first uncompleted task. Auto-skipped `<= 2`-file fast-path fixes skip
   checkpoint creation unless they bail out to Step 1.
2. **Update**: After each 1:1 deliverable commit via `git-manager`, prefix the
   completed task line in `"$state_file"` with `x YYYY-MM-DD `.
3. **Delete**: Remove `"$state_file"` (`rm -f "$state_file"`) immediately after
   opening or syncing the Draft PR, or on explicit slice abort / escalation back
   to `projects`.
4. **Preserve on Halt**: Halting on `CONFLICTING_STATE`, `WRONG_BASE`, or a
   recoverable worker pause leaves any existing `"$state_file"` untouched so the
   user can resume cleanly.

---

## 5. Repo-Scoped Documentation Boundaries

- Durable engineering documentation (designs, ADRs, architecture notes, roadmaps)
  belongs in repo-scoped `docs/` (`docs/designs/*.md`, `docs/adr/`,
  `ARCHITECTURE.md`, `ROADMAP.md`).
- Ephemeral agent artifacts and personal practice notes belong in gitignored
  `.internal/` at the repository root.
- Never hardcode external vault directories or user home paths in checkpoints,
  worker prompts, or repository files.
