---
name: implement-slice
description: >-
  Orchestrates end-to-end delivery of a Gitea issue or vertical feature slice
  across delegated implementation and QA subagents, checkpoint commits, static
  review, and pull request packaging. Never edits implementation code or
  self-certifies QA. Not for decomposing epics into issues (use gitea-plan) or
  executing a single already-delegated worker task (use tdd and git-manager).
---

# Implement Slice

## Use when
- Delivering an approved Gitea issue or bounded feature slice end to end via coordinated subagents.
- Coordinating multi-task checkpoints, pre-committed QA rubrics, and final review gates.
- Not for decomposing raw epics into milestones and issues: use `gitea-plan`.
- Not inside an already-delegated implementation worker task: follow the assigned worker contract (`tdd`, `git-manager`) without re-invoking `implement-slice`.

## Steps
1. **Preflight branch check, readiness audit, and `Backlog -> Ready`.** Check session mode per `profile/AGENTS.md`. Classify working tree per [handoff-contracts](references/handoff-contracts.md) (`CLEAN_BASE`, `ADOPTABLE_DIFF`, `CONFLICTING_STATE`, `WRONG_BASE`). Stop on conflicts. Read target Gitea issue/milestone/board state via `gt issue`, `gt milestone`, direction docs (`ARCHITECTURE.md`, `ROADMAP.md`, `docs/designs/*.md`, `AGENTS.md`), and `git status --short`. Reconcile issue acceptance criteria against current `HEAD` (handing off to `reconcile-docs` if canonical design docs drifted during upstream slices, or updating the Gitea issue after owner approval) and, when `--dry-run` is not active, move the issue card `Backlog -> Ready` on the project board. Hand off to `gitea-plan` if tracking issues must be created first.
2. **Select orchestration topology (`complexity x risk`).** Combine planning size with assurance risk per [orchestration-tiers](references/orchestration-tiers.md). Keep pure-orchestrator invariants: retain plan, status, commit SHAs, QA dispositions, blockers; never edit implementation files, repair Git via code edits, self-certify QA, or ingest full test logs unless resolving a failure.
3. **Lock Planned Workflow and pre-committed rubrics.** Formulate the Planned Workflow using the Canonical Node Schema (5-tuples: `node_id`, `claim`, `method`, `executor`, `pass_condition`). Project a dynamic Mermaid diagram deriving directly from node IDs with visible rework edges. If `--dry-run` is active, halt after displaying the plan (enforce 0 file changes, 0 commits, 0 remote calls). Hard gate: pause for human approval.
4. **Move card `Ready -> Work in Progress`, assign workspaces, and delegate.** Once the human approves Step 3, move the issue card `Ready -> Work in Progress` on the project board per [handoff-contracts](references/handoff-contracts.md). Govern branch/worktree lifecycle through `git-manager` per [orchestration-tiers](references/orchestration-tiers.md). Dispatch worker subagent(s) with the Implementation Assignment in [handoff-contracts](references/handoff-contracts.md). Never run concurrent workers in the same working tree. Update the runtime Execution Record table as nodes change state.
5. **Audit worker reports and run rubric QA.** Verify worker reports via read-only Git checks. Spawn read-only QA subagents running `verify-slice` against pre-committed rubrics. Update Execution Record with concrete evidence (SHA, exit codes).
6. **Triage outcomes and route rework.** Classify failures using [handoff-contracts](references/handoff-contracts.md): route code defects to existing worker via `send_message`; record justified rubric amendments if criteria change. Loop Steps 4-6 until all nodes pass.
7. **Enforce final-HEAD evidence, move card `Work in Progress -> Review`, and integrate.** Confirm `code-review` (`Ready`) and `verify-slice` match the exact final `HEAD` and base, then move the issue card `Work in Progress -> Review` on the project board. Present the Execution Deviation Report (skipped/added checks, rework iterations, scope drift; if scope drift evolved a contract in `docs/designs/*.md` or `ARCHITECTURE.md`, prompt to run `reconcile-docs` before the next slice). Integrate per [orchestration-tiers](references/orchestration-tiers.md) Policy Matrix: fast-forward merge (and move card `Review -> Completed`) if repo `AGENTS.md` permits and user approves, else hand off to `gitea-pr`.

## Your call
- **Session mode**: decide whether to switch from `learning` to `delivery` before autonomous delegation.
- **Planned workflow and rubrics**: approve task breakdown, node 5-tuples, assurance tier, and QA rubrics before workers spawn.
- **Rubric amendments, live-infra, and trade-offs**: approve rubric criteria changes, authorize `live-infra` checks, and adjudicate review conflicts.
- **Integration authorization**: authorize direct merge to main or PR creation and merge.

## Done when
- All slice checkpoints are committed on a clean target branch, `code-review` (`Ready`) and `verify-slice` match the same final `HEAD`, the Execution Deviation Report is recorded, and the branch is integrated per policy.

## Hands off to
- `gitea-plan`: when goals or epics require milestone and issue decomposition before slice execution.
- `git-manager`: to create/integrate slice branches and worktrees, commit worker checkpoints, or stop on conflicts.
- `tdd`: inside implementation workers for seam-level red-green development.
- `verify-slice`: inside QA subagents for pre-committed chunk and final-`HEAD` runtime verification.
- `code-review`: for final-slice 4-axis static and strategic alignment inspection.
- `diagnose`: when an unexpected failure requires evidence-first root-cause investigation.
- `gitea-pr`: when policy or remote CI mandates a pull request and final-`HEAD` packets are ready.
- `reconcile-docs`: when upstream slices or approved scope drift leave canonical docs or design specs out of sync with `HEAD`.
