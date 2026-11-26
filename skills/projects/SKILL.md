---
name: projects
description: >-
  Translate technical goals, user requests, and architecture plans into GitHub
  Issues, Milestones, and Projects v2 boards with tiered complexity scaling.
  Use when decomposing work, creating or updating GitHub issues or milestones,
  or managing rolling planning horizons. Not for slice implementation (use
  implement) or PR verification (use verify).
---

# Projects

## Use when
- Decomposing a project, feature request, or technical plan into trackable GitHub units.
- Creating or updating GitHub Milestones, Projects v2 boards, and vertical-slice issues.
- Setting rolling planning horizons for multi-phase epics.
- Not for executing an approved issue slice: use `implement`.
- Not for black-box QA, PR promotion, or merge closeout: use `verify`.
- Not for standalone Git branch or worktree mechanics: use `git-manager`.

## Steps
1. **Verify GitHub identity and contract.** Before checking remotes or editing
   `AGENTS.md`, read [references/planning-contract.md](references/planning-contract.md).
   Run `gh repo view --json url` to confirm a GitHub repository. If it fails or
   `AGENTS.md` holds a legacy Gitea planning contract, halt and advise migrating
   to GitHub via `/gitea-to-github` or using standalone `gt-usage`.
2. **Reconcile specs and GitHub state.** Compare `ARCHITECTURE.md`, `ROADMAP.md`,
   `docs/designs/*.md`, GitHub Issues, Milestones, and Projects v2 cards for
   contradictions (zombie in-progress, premature completed, review orphan,
   horizon divergence). If canonical docs lag behind `Completed` board cards,
   hand off to `reconcile-docs` first.
3. **Select tier and decompose into vertical slices.** Before sizing,
   decomposing, or auditing, read
   [references/tiers-and-audit.md](references/tiers-and-audit.md). Assign
   `Small`, `Medium`, or `Large` and emit
   `### Project Board Policy: <Omitted|Recommended|Required> (Rationale)`. Map
   work into deliverable outcome issues with test seams, Vertical Submodule TDD
   Grouping, and falsifiable acceptance criteria (Context, Solution, Criteria).
4. **Run Independent Zero-Context Reproducibility Audit (`Medium`/`Large`).**
   Spawn a clean-room subagent with the raw input manifest (pinned commit SHA,
   specs, proposed issue markdown, milestone/board plan) to surface and resolve
   material ambiguities before the human gate.
5. **Present plan for approval.** Emit
   `### Reproducibility Audit: <Passed | Remediated> (Subagent: <id> | Omitted: Small tier)`
   alongside proposed milestones, due dates, board updates, issues, and any
   `AGENTS.md` contract diff. Stop for approval before mutating GitHub or `AGENTS.md`.
6. **Execute GitHub operations.** Before running Projects v2 or milestone
   mutations, read
   [references/github-projects-v2.md](references/github-projects-v2.md). Use
   `gh issue`, REST `gh api repos/{owner}/{repo}/milestones`, and `gh api graphql`
   (`owner.projectV2` onboarding, `issue.projectItems` status updates, `DATE`
   fields). Resolve all IDs dynamically; never hardcode or guess Node IDs or
   construct `/milestone/1`.
7. **Verify state and formalize `AGENTS.md`.** Confirm created issue numbers,
   canonical URLs, milestone due dates, and board columns. For `Medium`/`Large`
   planning structure, record only the state-free `project_number: <int>`
   contract in `AGENTS.md` (never rotating sprint state or GraphQL Node IDs).

## Your call
- **Planning tier selection**: confirm `Small`, `Medium`, or `Large` ceremony.
- **Slice boundaries and milestones**: approve or revise proposed issues and due dates.
- **Batch mutations**: approve GitHub entity creation and `AGENTS.md` contract edits.

## Done when
- Target milestones, board columns, and issues exist on GitHub with dynamically
  verified IDs, canonical URLs, and falsifiable acceptance criteria.
- `AGENTS.md` holds an accurate, state-free `project_number` contract whenever
  `Medium`/`Large` planning structure is created or updated.

## Hands off to
- `implement`: to deliver a ready issue (`Suggested Next Step: /implement #<first-ready-issue>`).
- `reconcile-docs`: when canonical docs lag behind completed cards (`Suggested Next Step: /reconcile-docs`).
- `git-manager`: for standalone branch or worktree operations.
- Emit one outcome-matched `Suggested Next Step:` on standalone turns; suppress
  when delegated per [skeleton.md](../build-skill/references/skeleton.md).
