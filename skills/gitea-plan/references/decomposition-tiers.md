# Project Sizing, Ceremony Tiers, and Artifact Contracts

Reference for `gitea-plan`. Guidelines for scaling planning ceremony to risk and scope, preserving momentum while keeping architecture traceable and reproducible.

## 1. Core Axiom: Issues vs. Commits

- An **Issue** represents an **independently deliverable outcome** (what is built, verified, and closed by a pull request). It defines falsifiable acceptance criteria and expected behavior.
- A **Commit** represents an **atomic, reversible implementation checkpoint** (a step within that issue's branch). Commits must compile and pass tests, but do not need to represent an entire closed issue on their own.
- **Anti-pattern**: Never create 1:1 Gitea issues for micro-commits (such as "fix typo", "add helper function", or "clean up lint"). Group cohesive checkpoints under a single deliverable issue.

---

## 2. Entity Semantics: Issues, Boards, and Milestones

Each Gitea planning primitive tracks a distinct dimension of engineering reality:
- **Issue State (`Open` vs. `Closed`)**: Deliverable completion on `main`.
- **Board State (Columns: *Backlog*, *Ready*, *In Progress*, *Review*, *Done*)**: Spatial workflow stage in the active pipeline.
- **Milestone**: Strategic delivery horizon (capacity-driven or time-bounded release boundary).

### Meaningful Conflict Reconciliation
Never mechanically mirror or silently mutate state. Instead, detect and report semantic conflicts:
- **Zombie In-Progress**: Issue is closed on Gitea, but its card still sits in *Backlog*, *Ready*, or *In Progress* on the board.
- **Premature Done**: Card is moved to *Done*, but the issue remains open or lacks a merged PR / commit on `main`.
- **Review Orphan**: Card sits in *Review*, but no active PR or static review packet exists.
- **Horizon Divergence**: Open issue is assigned to a milestone that is closed or diverges from the active milestone in `ROADMAP.md`.

---

## 3. Planning Ceremony Tiers & Project Board Policy

| Tier | Typical Work | Gitea Primitives | Project Board Policy | Decomposition Rule |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | Single-step bugfix, documentation tweak, dependency bump, routine chore | 1 Issue linked directly to 1 PR / Commit | **Omitted by Policy** (issue tracker suffices) | Zero milestones. Zero project boards. Keep description concise (Context, Solution, Acceptance Criteria). |
| **Medium** | Vertical feature slice, multi-step refactor, performance spike (2 to 5 issues) | 1 Milestone + 2 to 5 Issues | **Recommended** (Basic Kanban: *Backlog*, *Ready*, *In Progress*, *Review*, *Done*) | Each issue has its own branch and PR. All issues include explicit numbered acceptance criteria and test seams. |
| **Large** | Architectural epic, platform cutover, multi-service evolution | Roadmap Doc + Rolling Milestones + Deliverable Issues | **Required** (Board coordinates rolling horizons) | Source of truth remains in repo docs (`ARCHITECTURE.md`, `ROADMAP.md`, ADRs). Gitea coordinates rolling execution. |

**Deterministic Output Header**: Every planning proposal must explicitly state:
```markdown
### Project Board Policy: <Omitted|Recommended|Required> (Rationale)
```

---

## 4. Independent Zero-Context Reproducibility Audit

Before finalizing decomposition for approval, run a clean-room audit subagent to verify plan reproducibility without conversational context:

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
