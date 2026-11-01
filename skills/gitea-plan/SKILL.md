---
name: gitea-plan
description: >-
  Translate technical goals, user requests, and architecture plans into Gitea planning
  primitives (issues, milestones, labels, dependencies) with tiered complexity scaling.
  Use when decomposing work, creating or updating Gitea issues, or establishing planning
  milestones. Not for managing pull requests: use gitea-pr.
---

# Gitea Plan

## Use when
- Decomposing a project, feature request, or technical plan into trackable Gitea units.
- Creating or editing milestones and issues with falsifiable acceptance criteria.
- Setting rolling planning horizons for multi-phase epics.
- Not for orchestrating slice implementation across subagents: use `implement-slice`.
- Not for branch or worktree management: use `git-manager`.
- Not for pull request lifecycle or review tracking: use `gitea-pr`.

## Steps
1. **Assess scope and select tier.** Inspect repository context, documentation plans, or user
   request to assign a planning tier (`Small`, `Medium`, or `Large`) per
   [references/decomposition-tiers.md](references/decomposition-tiers.md). Enforce minimum
   ceremony: small tasks never get milestones or board overhead.
2. **Decompose into deliverable outcome slices.** Map work items into verifiable issues.
   Ensure each issue represents an independently deliverable outcome with a defined testing
   seam, rather than a micro-commit. For large projects, decompose only the active milestone
   and leave future horizons coarse.
3. **Draft falsifiable acceptance criteria.** For each planned issue, formulate:
   - Context and problem: what motivates the change.
   - Proposed solution and scope: boundary of what is in and out of scope.
   - Acceptance criteria: numbered, observable pass/fail conditions.
4. **Present decomposition for approval.** Present the proposed milestone and issues for human
   review following the operational checkpoint rules in `profile/AGENTS.md`. Stop for approval
   before creating any Gitea entities.
5. **Execute Gitea operations via `tea` CLI.** Use verified commands from
   [references/tea-cli.md](references/tea-cli.md) (`tea milestones create`, `tea issues create`).
   Pass multi-line descriptions via `--description-file -` to preserve formatting.
6. **Verify created state.** Inspect `tea issues list` or `tea milestones list` to confirm index
   numbers and report the created entities to the user.

## Your call
- **Planning tier selection**: confirm Small vs. Medium vs. Large ceremony level.
- **Issue decomposition boundaries**: approve or revise the proposed issue slices.
- **Batch issue creation**: approve structured batch issue creation per `profile/AGENTS.md`.

## Done when
- Target milestone and issues are created in Gitea with verifiable index numbers and falsifiable
  acceptance criteria.

## Hands off to
- `implement-slice`: to orchestrate end-to-end delivery of an approved issue or slice.
- `git-manager`: to create dedicated branches or worktrees for the decomposed issues.
- `gitea-pr`: to link, review, and close issues via pull requests.
