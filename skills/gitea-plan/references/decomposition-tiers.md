# Project Sizing and Task Decomposition Tiers

Reference for `gitea-plan`. Guidelines for scaling planning ceremony to risk and scope, preserving momentum while keeping architecture traceable.

## Core Axiom: Issues vs. Commits

- An **Issue** represents an **independently deliverable outcome** (what is built, verified, and closed by a pull request). It defines falsifiable acceptance criteria and expected behavior.
- A **Commit** represents an **atomic, reversible implementation checkpoint** (a step within that issue's branch). Commits must compile and pass tests, but do not need to represent an entire closed issue on their own.
- **Anti-pattern**: Never create 1:1 Gitea issues for micro-commits (such as "fix typo", "add helper function", or "clean up lint"). Group cohesive checkpoints under a single deliverable issue.

---

## Planning Ceremony Tiers

| Tier | Typical Work | Planning Primitives Used | Decomposition Rule |
| :--- | :--- | :--- | :--- |
| **Small** | Single-step bugfix, documentation tweak, dependency bump, routine chore | 1 Gitea Issue directly linked to 1 PR | Zero milestones. Zero project boards. Keep issue description concise (Context, Solution, Acceptance Criteria). |
| **Medium** | New user-facing feature, vertical slice, multi-step refactor, performance spike | 1 Milestone + 2 to 5 Deliverable Issues | Each issue has its own branch and PR. Every issue includes explicit numbered acceptance criteria and verification notes. |
| **Large** | Architectural redesign, multi-service cutover, major platform evolution | Repository Plan Document + Rolling Gitea Milestones | Technical source of truth remains in repository documentation (`ARCHITECTURE.md`, `docs/plans/`, or ADRs). Gitea coordinates rolling execution horizons. |

---

## Rolling Horizons for Large Projects

When planning large epics, avoid waterfall decomposition where every future task is pre-created as an issue weeks before implementation:

1. **Active Milestone (Immediate Horizon)**:
   - Decomposed into 2 to 5 concrete deliverable issues with falsifiable acceptance criteria.
   - Actively assigned, scheduled, and implemented via dedicated branches.
2. **Future Milestones (Deferred Horizons)**:
   - Represented as high-level milestones or single coarse placeholder issues in Gitea.
   - Decomposed into concrete issues only when the active milestone is completed and its lessons are verified.
3. **Architecture Synchronization**:
   - As decisions are made during active implementation, update repository docs (`reconcile-docs`) before decomposing the next rolling milestone.
