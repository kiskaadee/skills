# Orchestration Topology, Boundaries, and Workspace Ownership

Reference for `implement-slice`. Defines how the orchestrator combines existing planning and assurance tiers without redefining them, preserves context efficiency, and prevents workspace contention.

## 1. Pure-Orchestrator and Context-Budget Invariants

These boundaries hold across every slice size and risk tier:

1. **No implementation or self-certified QA**: The orchestrator never edits product or test files, creates ad-hoc fixup commits, executes mutations to repair broken code, or declares runtime QA passing without worker/QA evidence. Read-only inspection (`tea`, `git status`, `git log`, `git diff --stat`, targeted file reads to check a contradiction) is allowed.
2. **Context-budget discipline**:
   - **Retain in orchestrator context**: approved slice plan, task dependency status, assigned workspace/branch refs, checkpoint commit SHAs, QA check dispositions, active blockers, and open human decisions.
   - **Delegate out of orchestrator context**: full test suite transcripts, build logs, browser traces, and line-by-line edit narratives. Require concise structured reports with exact references (commit SHAs, `path:line` locations, check IDs, or log/artifact paths) and inspect raw output only when resolving a discrepancy or failure.

---

## 2. Combining `Complexity x Risk` (Single-Owner Tier Mapping)

`implement-slice` does not define new sizing or risk vocabularies; it composes the canonical tiers owned by sibling skills:

- **Planning size (`Small`, `Medium`, `Large`)**: owned by [`gitea-plan`](../../gitea-plan/references/decomposition-tiers.md). Governs Gitea planning ceremony and task decomposition granularity.
- **Assurance rigor (`Lightweight`, `Standard`, `High-Assurance`)**: owned by [`code-review`](../../code-review/references/axes.md) and [`verify-slice`](../../verify-slice/references/perspectives.md). Governs worker independence, runtime check depth, and static review isolation.

**Risk override rule**: Always compute assurance rigor from failure consequences, never diff line count alone. Touching authentication, permissions, secrets, payments, concurrent state, data migrations, deployment/infrastructure, destructive operations, or core shared libraries elevates even a `Small` slice to `High-Assurance` verification and review while keeping `Small` planning ceremony.

| Planning Size x Assurance Rigor | Worker Delegation | Mid-Slice QA (`verify-slice`) | Final Slice Gate (`<base>...HEAD`) |
| :--- | :--- | :--- | :--- |
| **`Small` x `Lightweight`** | 1 implementation worker subagent on slice branch (`tdd` where applicable + `git-manager` checkpoint commit + self-audit). | Skip separate mid-slice QA subagent if deterministic worker evidence satisfies the pre-committed rubric; run final-`HEAD` `verify-slice` Lightweight checks. | Single-pass `code-review` (`Lightweight`) + final-`HEAD` `verify-slice` confirmation. |
| **`Small`/`Medium` x `Standard`** | Sequential worker subagent(s) per task/chunk on slice branch (or isolated worktrees only if tasks are genuinely independent). | Spawn independent rubric QA subagent (`verify-slice` `Standard`) at chunk boundary or slice completion when stateful/UI/API behavior warrants separation. | Independent `code-review` (`Standard`, including strategic alignment) + final-`HEAD` `verify-slice` packet. |
| **Any Size x `High-Assurance`** (or `Large` multi-chunk slice) | Sequential tasks on slice branch or isolated per-task worktrees for independent tracks; strict checkpoint boundaries. | Spawn clean black-box QA subagent (`verify-slice` `High-Assurance`), withholding diff narrative and worker self-audit per `verify-slice` Step 3. | Isolated multi-axis `code-review` (`High-Assurance`) + final-`HEAD` `verify-slice` packet (including any emitted `RV-*` checks). |

---

## 3. Branch, Worktree, and QA Ownership Boundaries

Explicit ownership prevents concurrent working-tree corruption and keeps Git recovery out of the orchestrator:

| Role | Exact Responsibility |
| :--- | :--- |
| **Orchestrator (`implement-slice`)** | Decides branch/worktree topology in the approved plan, assigns each worker an explicit workspace path and target branch, and verifies resulting refs/SHAs read-only. Never repairs broken Git state by editing files or committing directly. |
| **`git-manager`** | Owns and governs branch creation, `.worktrees/<task>` creation/removal, branch integration (`rebase`, `merge`, `cherry-pick`), conflict stops, and evidence-first `reflog` recovery. On any merge/rebase conflict or unfamiliar dirty tree, `git-manager` stops immediately for human decision. |
| **Implementation Worker** | Modifies code and tests only inside its assigned workspace and scope boundary; runs local checks via `tdd` and commits verified checkpoints autonomously on the non-default working branch per `git-manager`. |
| **QA Subagent (`verify-slice`)** | Evaluates a pinned commit SHA (`HEAD`) without modifying tracked repository files. Writes temporary fixtures or scratch state only in isolated temp directories (such as `mktemp -d`), leaving `git status --short` clean. |

### Contention and Worker Reuse Rules

1. **Sequential default**: Prefer sequential task delegation on a single slice branch when tasks touch related modules or take minutes rather than hours; parallel worktrees pay an integration cost.
2. **Mandatory isolation for concurrency**: Never run two implementation subagents concurrently in the same working directory. Concurrent implementation tasks require separate `git-manager` worktrees and an explicit integration step before final-`HEAD` review.
3. **Stateful worker reuse**: Retain each worker's subagent `conversationId`. When QA or `code-review` routes actionable rework back on a task, message that existing worker (`send_message`) so it retains design context instead of spawning a cold worker. Spawn a fresh worker only for a distinct new task or when the original worker session is unavailable.
