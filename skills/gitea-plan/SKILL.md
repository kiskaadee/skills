---
name: gitea-plan
description: >-
  Translate technical goals, user requests, and architecture plans into Gitea planning
  primitives (issues, milestones, project boards) with tiered complexity scaling.
  Use when decomposing work, creating or updating Gitea issues, or establishing planning
  milestones. Not for managing pull requests: use gitea-pr.
---

# Gitea Plan

## Use when
- Decomposing a project, feature request, or technical plan into trackable Gitea units.
- Creating or editing milestones, project boards, and issues with falsifiable criteria.
- Setting rolling planning horizons for multi-phase epics.
- Not for orchestrating slice implementation across subagents: use `implement-slice`.
- Not for branch or worktree management: use `git-manager`.
- Not for pull request lifecycle or review tracking: use `gitea-pr`.

## Steps
1. **Reconcile artifacts bidirectionally.** Check specs, roadmaps, assets, and Gitea
   state for contradictions. Flag zombie in-progress, premature done, or horizon
   divergence conflicts before planning new work. See
   [references/decomposition-tiers.md](references/decomposition-tiers.md).
2. **Assess scope and select tier.** Assign `Small`, `Medium`, or `Large`.
   Emit explicit `### Project Board Policy: <Omitted|Recommended|Required> (Rationale)`.
3. **Decompose into deliverable outcome slices.** Map work into verifiable issues
   with test seams and falsifiable acceptance criteria (Context, Solution, Criteria).
4. **Run independent reproducibility audit.** Spawn clean-room subagent with raw
   input manifest (commit SHA, specs, proposed issue markdown). Review 5-section
   evaluation to resolve material ambiguities before human gate.
5. **Present decomposition for approval.** Present proposed milestone, board, and
   issues with audit disposition. Stop for approval before creating Gitea entities.
6. **Execute Gitea operations via `gt` CLI.** Use verified commands from `gt-usage`:
   - Milestones: `gt milestone create "<title>" -d "<desc>" --json id,url`.
   - Projects: `gt project create "<title>" --template basic_kanban --json id,url`.
   - Issues: `gt issue create -t "<title>" -F <file> -m <id> -p <id> --json number,url`.
   Extract server IDs directly; never guess sequence numbers or construct `/milestone/1`.
7. **Verify created state.** Inspect `gt issue list` and `gt milestone list` to
   confirm server IDs, board cards, and non-hallucinated canonical URLs.

## Your call
- **Planning tier selection**: confirm Small vs. Medium vs. Large ceremony level.
- **Issue decomposition boundaries**: approve or revise proposed issue slices.
- **Batch entity creation**: approve structured batch creation per `profile/AGENTS.md`.

## Done when
- Target milestone, board, and issues exist on Gitea with verified server IDs,
  canonical URLs, and falsifiable acceptance criteria.

## Hands off to
- `implement-slice`: to orchestrate end-to-end delivery of an approved issue or slice.
- `git-manager`: to create dedicated branches or worktrees for decomposed issues.
- `gitea-pr`: to link, review, and close issues via pull requests.
