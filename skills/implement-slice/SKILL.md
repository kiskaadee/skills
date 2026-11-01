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
1. **Verify session mode and read slice context.** Check active session mode per `profile/AGENTS.md`: if `learning` is active, pause so the user can decide whether to switch to `delivery`. Read target Gitea issue/milestone state (`tea issues`, `tea milestones`), canonical direction docs (`ARCHITECTURE.md`, `ROADMAP.md`, ADRs when present), and `git status --short`. Clarify ambiguous intent with the user; hand off to `gitea-plan` if tracking issues must be created first.
2. **Select orchestration topology (`complexity x risk`).** Combine planning size (`Small`, `Medium`, `Large` from `gitea-plan`) with assurance risk (`Lightweight`, `Standard`, `High-Assurance` from `code-review` and `verify-slice`) per [orchestration-tiers](references/orchestration-tiers.md), letting high-risk surfaces override size upward. Keep pure-orchestrator and context-budget invariants at every tier: retain only the plan, task status, commit SHAs, QA dispositions, blockers, and decisions; never edit implementation files, repair Git via code edits, self-certify QA, or ingest full test logs unless resolving a failure.
3. **Lock plan, workspace topology, and pre-committed QA rubrics.** Decompose the slice into ordered tasks/chunks with explicit scope boundaries, expected `git-manager` checkpoint boundaries, workspace assignment (sequential shared branch vs. isolated `.worktrees/<task>` for concurrent workers), whether a PR applies, and falsifiable QA rubrics written before any worker spawns. Hard gate: pause for human approval before implementation begins.
4. **Assign workspaces and delegate implementation.** Govern branch and worktree lifecycle through `git-manager` per [orchestration-tiers](references/orchestration-tiers.md) (orchestrator decides topology and assigns workspaces; `git-manager` executes branch/worktree operations; workers edit and commit checkpoints inside their assigned workspace). Dispatch worker subagent(s) with the Implementation Assignment in [handoff-contracts](references/handoff-contracts.md). Never run concurrent implementation workers in the same working tree.
5. **Audit worker reports and run rubric QA.** Verify returned Implementation Reports via concise read-only Git checks (`git status --short`, `git log`, `git show --stat`) to confirm clean trees, commit SHAs, and scope containment. When the tier or chunk boundary requires independent QA, spawn a read-only/isolated QA subagent running `verify-slice` against the pre-committed rubric (withholding author narrative for `High-Assurance` black-box runs).
6. **Triage outcomes and route rework.** Classify non-passing outcomes using [handoff-contracts](references/handoff-contracts.md): send code defects or missing seam tests back to the existing worker subagent (`send_message`) when its context remains live; repair or escalate `BLOCKED (env/fixture)`; pause for human authorization on `BLOCKED (out-of-bounds)` (`live-infra`); and if a rubric proves defective, record an explicit justified amendment (pausing for human approval if acceptance criteria or scope change). Loop Steps 4-6 until all slice tasks pass.
7. **Enforce final-`HEAD` evidence invariant and finish.** Run `code-review` across `<base>...HEAD` (including strategic project alignment). Enforce the final-`HEAD` invariant in [handoff-contracts](references/handoff-contracts.md): required `code-review` (`Ready`) and `verify-slice` (zero unhandled `FAIL`) evidence must identify the same final `HEAD` and applicable base revision; any diff change invalidates affected evidence and triggers re-verification (completing any new `RV-*` checks on final `HEAD` via valid handshake reuse). Hard gate: never package a ready PR or declare completion until final-`HEAD` evidence is current. If a PR applies, hand off to `gitea-pr`; otherwise present the final-`HEAD` evidence summary, commit range, and open decisions to the user.

## Your call
- **Session mode**: decide whether to switch from `learning` to `delivery` before autonomous delegation.
- **Plan and pre-committed rubrics**: approve task decomposition, assurance tier, workspace topology, and QA rubrics before any implementation worker spawns.
- **Rubric amendments, `live-infra`, and trade-offs**: approve any rubric change that relaxes criteria or alters scope, authorize `live-infra` checks, and adjudicate unresolved conflicts or review disagreements.
- **PR packaging and release**: approve PR creation/updates and authorize merge (or accept local slice delivery when no PR applies).

## Done when
- All slice checkpoints are committed on a clean target branch, `code-review` (`Ready`) and `verify-slice` (zero unhandled `FAIL`) match the same final `HEAD` and base revision, and either `gitea-pr` has packaged the PR or final evidence has been delivered directly when no PR applies.

## Hands off to
- `gitea-plan`: when goals or epics require milestone and issue decomposition before slice execution.
- `git-manager`: to create/integrate slice branches and worktrees, commit worker checkpoints, or stop on conflicts.
- `tdd`: inside implementation workers for seam-level red-green development.
- `verify-slice`: inside QA subagents for pre-committed chunk and final-`HEAD` runtime verification.
- `code-review`: for final-slice 4-axis static and strategic alignment inspection.
- `diagnose`: when an unexpected failure requires evidence-first root-cause investigation.
- `gitea-pr`: when a PR applies and final-`HEAD` review plus verification packets are ready.
