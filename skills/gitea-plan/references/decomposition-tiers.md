# Project Sizing, Ceremony Tiers, and Artifact Contracts

Reference for `gitea-plan`. Guidelines for scaling planning ceremony to risk and scope, preserving momentum while keeping architecture traceable and reproducible.

## 1. Core Axiom: Issues vs. Commits

- An **Issue** represents an **independently deliverable outcome** (what is built, verified, and closed by a pull request). It defines falsifiable acceptance criteria and expected behavior.
- A **Commit** represents an **atomic, reversible implementation checkpoint** (a step within that issue's branch). Commits must compile and pass tests, but do not need to represent an entire closed issue on their own.
- **Anti-pattern**: Never create 1:1 Gitea issues for micro-commits (such as "fix typo", "add helper function", or "clean up lint"). Group cohesive checkpoints under a single deliverable issue.
- **Vertical Submodule TDD Grouping**: Inside a multi-module issue, organize acceptance criteria and TDD test drafts vertically by submodule or dependency layer (e.g. `protocols` -> `ssap` -> `pointer` -> `manager`) rather than a single horizontal "write all tests for the entire issue first" section, so `implement-slice` executes incremental Red->Green cycles per submodule.

---

## 2. Entity Semantics: Issues, Boards, and Milestones

Each Gitea planning primitive tracks a distinct dimension of engineering reality:
- **Issue State (`Open` vs. `Closed`)**: Deliverable completion on `main`.
- **Board State (Columns: *Backlog*, *Ready*, *Work in Progress*, *Review*, *Completed*)**: Spatial workflow stage in the active pipeline.
- **Milestone**: Strategic delivery horizon (capacity-driven or time-bounded release boundary).

### Canonical 5-Column Pipeline & Semantic Colors (Deep Signal Palette)

| Sorting | Canonical Title | Role Aliases (Matched Case-Insensitively) | Hex Color | Default | Transition Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | **Backlog** | `backlog`, `to-do`, `todo`, `icebox`, `triage` | `#475569` (Slate Gray) | `true` | `gitea-plan` (default placement for dependent issues) |
| `1` | **Ready** | `ready`, `next`, `up next`, `queued`, `groomed` | `#1d76db` (Signal Blue) | `false` | `implement-slice` (Step 1 preflight readiness check) |
| `2` | **Work in Progress** | `work in progress`, `in progress`, `wip`, `doing`, `active` | `#d97706` (Warm Amber) | `false` | `implement-slice` (Step 4 worker start) |
| `3` | **Review** | `review`, `in review`, `qa`, `testing`, `verification` | `#6d28d9` (Royal Purple) | `false` | `implement-slice` (Step 7 final-HEAD pass) / `gitea-pr` |
| `4` | **Completed** | `completed`, `done`, `closed`, `shipped` | `#15803d` (Forest Green) | `false` | `gitea-pr` (on owner-authorized merge) / `implement-slice` |

### Board Provisioning & Non-Destructive Reconciliation (`gitea-plan`)
1. **Create if missing**: When `Project Board Policy` is `Recommended` or `Required` and no open board exists, create one with `gt project create "<title>" --template none -d "<desc>" --json id,title,url`, then `POST` the 5 canonical columns (`sorting: 0..4`) with their Deep Signal hex colors and set `Backlog` as `default: true` (using the recipes in `gt-usage`).
2. **Reconcile in place if existing**: Never assume an existing board already adheres to the convention, and never delete columns that hold cards. Query `/projects/<id>/columns`, match existing columns to the 5 roles by their case-insensitive aliases, and `PATCH` matched columns in place (`title`, `color`, `sorting`) so attached cards stay intact. Create only the missing canonical columns via `POST`, and ensure `Backlog` is marked `default: true`.
3. **Pin column IDs in `AGENTS.md`**: Record the resolved Project Board ID and `{Backlog, Ready, Work in Progress, Review, Completed -> column_id}` map in the repository's `AGENTS.md` planning contract so `implement-slice` and `gitea-pr` move cards without guessing names.

### Meaningful Conflict Reconciliation
Never mechanically mirror or silently mutate state. Instead, detect and report semantic conflicts:
- **Zombie In-Progress**: Issue or PR is closed on Gitea, but its card still sits in *Backlog*, *Ready*, *Work in Progress*, or *Review* on the board.
- **Premature Completed**: Card is moved to *Completed*, but the issue remains open or lacks a merged PR / commit on `main`.
- **Review Orphan**: Card sits in *Review*, but no active PR or static review packet exists.
- **Horizon Divergence**: Open issue is assigned to a milestone that is closed or diverges from the active milestone in `ROADMAP.md`.

---

## 3. Planning Ceremony Tiers & Project Board Policy

| Tier | Typical Work | Gitea Primitives | Project Board Policy | Decomposition Rule |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | Single-step bugfix, documentation tweak, dependency bump, routine chore | 1 Issue linked directly to 1 PR / Commit | **Omitted by Policy** (issue tracker suffices) | Zero milestones. Zero project boards. Keep description concise (Context, Solution, Acceptance Criteria). |
| **Medium** | Vertical feature slice, multi-step refactor, performance spike (2 to 5 issues) | 1 Milestone + 2 to 5 Issues | **Recommended** (5-column Kanban: *Backlog*, *Ready*, *Work in Progress*, *Review*, *Completed*) | Each issue has its own branch and PR. All issues include explicit numbered acceptance criteria and test seams. |
| **Large** | Architectural epic, platform cutover, multi-service evolution | Roadmap Doc + Rolling Milestones + Deliverable Issues | **Required** (Board coordinates rolling horizons) | Source of truth remains in repo docs (`ARCHITECTURE.md`, `ROADMAP.md`, ADRs). Gitea coordinates rolling execution. |

**Deterministic Output Headers**: Every planning proposal must explicitly state both headers before asking for approval:
```markdown
### Project Board Policy: <Omitted|Recommended|Required> (Rationale)
### Reproducibility Audit: <Passed | Remediated> (Subagent: `<conversation-id>` | `Omitted: Small tier`)
```

---

## 4. Independent Zero-Context Reproducibility Audit (`Medium` and `Large` Mandatory)

Before presenting a `Medium` or `Large` decomposition for approval (Step 5), spawn a clean-room audit subagent to verify plan reproducibility without conversational context and record its `<conversation-id>` in the `### Reproducibility Audit:` header:

### Input Manifest (Strict Clean-Room)
The auditor receives strictly raw artifacts and pinned repository state:
1. Pinned repository root and commit SHA.
2. Canonical specifications (`docs/specs/*.md`) and `ROADMAP.md`.
3. Proposed raw issue titles, descriptions, and acceptance criteria markdown.
4. Proposed milestone and board specifications.
5. Declared asset paths and prerequisite environment variables.

### Auditor Report Schema
The auditor reports across five explicit sections:
1. **Reconstructed from Source Artifacts**: Scope and sequence directly supported by source text.
2. **Inferred Requirements**: Deductions made from titles or conventions lacking explicit spec text.
3. **Undetermined Seams**: Gaps or ambiguities that could not be resolved without guessing.
4. **Materiality Classification**:
   - *Material*: Forces an implementer to guess about scope, behavior, acceptance, or prerequisites.
   - *Non-Material*: Cosmetic or self-evident convention.
5. **Concrete Remediation Plan**: Specific edits to specs, assets, or criteria to resolve material ambiguities.

---

## 5. Rolling Horizons for Large Projects

When planning large epics, avoid waterfall decomposition where every future task is pre-created as an issue weeks before implementation:
1. **Active Milestone (Immediate Horizon)**: Decomposed into 2 to 5 concrete deliverable issues with falsifiable acceptance criteria.
2. **Future Milestones (Deferred Horizons)**: Represented as high-level milestones or single coarse placeholder issues in Gitea.
3. **Architecture Synchronization**: Update repository docs (`reconcile-docs`) before decomposing the next rolling milestone.

---

## 6. Multi-Repository Organizations and Shared Boards

When planning across multi-repository architectures (where an organization hub coordinates multiple deliverable repositories or services):
- **Root Kanban at Organization Level**: Create the shared board at the organization level (`gt project create "<title>" --org <org> --template none`) and reconcile the 5 canonical columns. Do not isolate tracking into separate child repository boards.
- **Attach Child Issues to Org Board**: Deliverable issues and pull requests created in child repositories attach to the organization board via `gt issue create ... -p <project-id>` or `gt issue edit <number> -R <owner/repo> --add-project <project-id>`.
- **Hub Documentation Alignment**: Architectural strategy, shared documentation, and roadmaps remain centralized in the hub repository, while the organization-level Kanban board coordinates unified cross-repo delivery status.
