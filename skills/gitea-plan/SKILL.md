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
   state for contradictions. Flag zombie in-progress, premature completed, or horizon
   divergence conflicts before planning new work. When closing a milestone or before
   decomposing the next rolling milestone, if `ARCHITECTURE.md`, `ROADMAP.md`, or
   `docs/designs/*.md` lag behind `Completed` board cards, hand off to `reconcile-docs`
   first. See [references/decomposition-tiers.md](references/decomposition-tiers.md).
2. **Assess scope and select tier.** Assign `Small`, `Medium`, or `Large`.
   Emit explicit `### Project Board Policy: <Omitted|Recommended|Required> (Rationale)`.
3. **Decompose into deliverable outcome slices.** Map work into verifiable issues
   with test seams and falsifiable acceptance criteria (Context, Solution, Criteria),
   grouping TDD test seams vertically by submodule or capability rather than a single
   monolithic upfront test block across all modules.
4. **Run independent reproducibility audit.** Spawn clean-room subagent with raw
   input manifest (commit SHA, specs, proposed issue markdown). Review 5-section
   evaluation to resolve material ambiguities before human gate.
5. **Present decomposition for approval.** Present proposed milestone, board,
   issues, and any proposed repository `AGENTS.md` planning-contract diff with
   audit disposition. Stop for approval before mutating Gitea entities or `AGENTS.md`.
6. **Execute Gitea operations via `gt` CLI.** Use verified commands from `gt-usage`:
   - Milestones: `gt milestone create "<title>" -d "<desc>" --json id,url`.
   - Projects: create with `gt project create "<title>" --template none --json id,url` if
     missing (with `--org <org>` for multi-repo orgs), or reconcile an existing board in
     place (`PATCH` matched role aliases, `POST` missing columns, set `Backlog` default,
     and apply the Deep Signal hex colors per [decomposition-tiers](references/decomposition-tiers.md)).
   - Issues: `gt issue create -t "<title>" -F <file> -m <id> -p <id> --json id,number,url`
     (or attach to org board: `gt issue edit <number> -R <repo> --add-project <id>`).
   Extract server IDs directly; never guess sequence numbers or construct `/milestone/1`.
7. **Verify created state.** Inspect `gt issue list`, `gt milestone list`, and board
   columns to confirm server IDs, column colors/order, and non-hallucinated canonical URLs.
8. **Formalize repo planning contract in `AGENTS.md`.** When establishing or changing
   `Medium`/`Large` planning structure, record or reconcile a concise sync rule in the
   repository's `AGENTS.md` so day-to-day coding agents keep trackers updated without
   reloading `gitea-plan`:
   - Pin **stable structural coordinates only**: canonical roadmap/checklist paths
     (e.g., `docs/roadmap.md`, `todo.txt`), authoritative Gitea repo + Project Board ID
     + `{Backlog, Ready, Work in Progress, Review, Completed -> column_id}` map,
     remote mirror policy (e.g., GitHub code-only), and the escalation trigger to
     re-run `gitea-plan` on scope shifts or epic Readiness Gates.
   - **Never** hardcode rotating sprint state (active milestone numbers or open issue
     lists) inside `AGENTS.md`; let `docs/roadmap.md`, `todo.txt`, and `gt` hold state.

## Your call
- **Planning tier selection**: confirm Small vs. Medium vs. Large ceremony level.
- **Issue decomposition boundaries**: approve or revise proposed issue slices.
- **Batch entity creation**: approve structured batch creation and `AGENTS.md` contract edits per `profile/AGENTS.md`.

## Done when
- Target milestone, board, and issues exist on Gitea with verified server IDs,
  canonical URLs, and falsifiable acceptance criteria.
- Repository `AGENTS.md` contains an accurate, state-free planning sync contract
  whenever `Medium`/`Large` planning structure is created or updated.

## Hands off to
- `implement-slice`: to orchestrate end-to-end delivery of an approved issue or slice.
- `git-manager`: to create dedicated branches or worktrees for decomposed issues.
- `gitea-pr`: to link, review, and close issues via pull requests.
- `reconcile-docs`: when canonical docs or design specs lag behind completed slices or milestone boundaries.
