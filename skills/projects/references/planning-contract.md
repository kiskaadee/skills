# Planning Contract & Canonical Board State Machine

Sole owner of the repository `AGENTS.md` planning contract schema, the canonical
5-column GitHub Projects v2 board state machine, transition ownership, and the
scoped GitHub remote guard. Other delivery skills (`implement`, `verify`,
`code-review`, `reconcile-docs`) reference this file rather than duplicating it.

---

## 1. Repository `AGENTS.md` Planning Contract Schema

Each GitHub-managed repository stores minimal, human-readable planning
coordinates in its `AGENTS.md`:

```yaml
# Planning Contract (owned by projects)
project_number: <int>
```

### Contract Invariants
- **State-free coordinates only**: Store only `project_number: <int>`. Never
  hardcode rotating sprint state (active milestone numbers, open issue lists,
  sprint names).
- **Zero brittle Node IDs**: Never store GraphQL Node IDs (`PVT_...`,
  `PVTSSF_...`, `PVTI_...`, or single-select option IDs) in `AGENTS.md`. Skills
  resolve all IDs dynamically at runtime via
  [github-projects-v2.md](github-projects-v2.md).
- **Repo-scoped documentation paths**: Durable engineering specs, architecture
  notes, and roadmaps live in repository-scoped `docs/` (`docs/designs/*.md`,
  `docs/adr/`, `ARCHITECTURE.md`, `ROADMAP.md`). Ephemeral agent artifacts and
  personal practice records live in gitignored `.internal/` at the repository
  root. Never encode user home paths or external vault directories in a
  repository planning contract.

---

## 2. Canonical 5-Column Board State Machine

All GitHub Projects v2 boards managed by the delivery loop use 5 canonical
`Status` column names paired with fixed GitHub `ProjectV2SingleSelectFieldOptionColor`
enums:

```text
Backlog -> Ready -> Work in Progress -> Review -> Completed
```

| Order | Column | Fixed GitHub Color Enum | Entering Transition Owner | Trigger Event |
| :--- | :--- | :--- | :--- | :--- |
| `0` | `Backlog` | `GRAY` | `projects` (or `verify` on abort) | Issue created and onboarded, or abandoned/superseded Draft PR closed |
| `1` | `Ready` | `BLUE` | `projects` | Slice prioritized and ready for execution |
| `2` | `Work in Progress` | `YELLOW` | `implement` (or `verify` on merge rejection) | `implement` preflight passes (`Ready -> Work in Progress`); card stays here through Draft PR open, `code-review`, and rework; human merge rejection at `verify` Phase 3 runs `gh pr ready --undo` and moves `Review -> Work in Progress` |
| `3` | `Review` | `PURPLE` | `verify` | `verify` Phase 2 passes runtime QA + CI + `verdict=ready` gate and promotes the Draft PR (`gh pr ready`), moving `Work in Progress -> Review` |
| `4` | `Completed` | `GREEN` | `verify` | `verify` Phase 3 merges the PR on human approval and executes `Review -> Completed` directly |

### Read-Only Skill Boundaries
- **`code-review`**: Strictly read-only regarding project boards. Never executes
  board card moves.
- **`reconcile-docs`**: Strictly read-only regarding GitHub state. Never mutates
  GitHub issues, pull requests, milestones, or project boards.

---

## 3. Scoped GitHub Remote Guard

Forge-dependent operations across the delivery loop (`projects`, `implement`,
`verify`, PR review publishing in `code-review`, and optional GitHub-state reads
in `reconcile-docs`) must verify GitHub repository identity before issuing forge
commands:

```bash
gh repo view --json url
```

- **Why `gh repo view --json url`**: Resolves the active GitHub repository even
  when using custom SSH host aliases or non-`origin` remotes.
- **Local-only exception**: Local diff reviews in `code-review` (when no open PR
  exists or local-only mode is requested) and local git/doc reconciliation in
  `reconcile-docs` run without requiring a GitHub remote.
- **Legacy Gitea contract detection**: If `gh repo view --json url` fails, or if
  the repository's `AGENTS.md` contains a legacy Gitea planning contract (such
  as Gitea `project_id`, `{Backlog..Completed -> column_id}` maps, or
  `gitea-plan` sync rules), fail fast and advise the user to either migrate the
  repository to GitHub or use standalone `gt-usage` outside the core delivery
  loop.

---

## 4. Meaningful Conflict Reconciliation

When reconciling specs, roadmaps, and GitHub state in Step 2, never mechanically
mirror or silently mutate conflicting state. Detect and report semantic
conflicts before planning new work:

- **Zombie In-Progress**: Issue or linked PR is closed on GitHub, but its card
  still sits in `Backlog`, `Ready`, `Work in Progress`, or `Review`.
- **Premature Completed**: Card sits in `Completed`, but the issue remains open
  or lacks a merged PR / commit on the default branch.
- **Review Orphan**: Card sits in `Review`, but no open ready-for-review PR
  exists.
- **Horizon Divergence**: An open issue is assigned to a closed milestone or
  diverges from the active milestone in `ROADMAP.md`.
- **Doc Lag**: `ARCHITECTURE.md`, `ROADMAP.md`, or `docs/designs/*.md` lags
  behind `Completed` board cards. Hand off to `reconcile-docs` before
  decomposing the next rolling milestone.
