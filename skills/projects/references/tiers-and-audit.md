# Project Sizing, Ceremony Tiers, and Reproducibility Audit

Reference for `projects`. Guidelines for scaling planning ceremony to risk and
scope, structuring vertical-slice issues, and running clean-room reproducibility
audits on GitHub Issues and Projects v2.

---

## 1. Core Axiom: Issues vs. Commits

- An **Issue** represents an **independently deliverable outcome** (what is
  built, verified, and closed by a pull request). It defines test seams and
  falsifiable acceptance criteria (`Context`, `Solution`, `Acceptance Criteria`).
- A **Commit** represents an **atomic, reversible implementation checkpoint**
  within an issue's branch. Commits compile and pass tests, but do not need to
  close an entire issue on their own.
- **Anti-pattern**: Never create 1:1 GitHub issues for micro-commits (such as
  "fix typo", "add helper function", or "clean up lint"). Group cohesive
  checkpoints under one deliverable issue.
- **Vertical Submodule TDD Grouping**: Inside a multi-module issue, organize
  acceptance criteria and TDD test seams vertically by submodule or capability
  layer (for example, `parser` -> `validator` -> `cli`) rather than a single
  horizontal "write all tests for the entire issue first" block, so `implement`
  executes incremental Red-Green cycles per submodule.

---

## 2. GitHub Planning Primitives

Each GitHub primitive tracks a distinct dimension of delivery:

- **Issue State (`OPEN` vs. `CLOSED`)**: Deliverable completion on the default branch.
- **Projects v2 `Status` Column (`Backlog`, `Ready`, `Work in Progress`, `Review`, `Completed`)**:
  Active workflow stage. See [planning-contract.md](planning-contract.md) for
  canonical colors and transition ownership, and
  [github-projects-v2.md](github-projects-v2.md) for GraphQL recipes.
- **Milestone & Projects v2 `DATE` Fields**: Strategic delivery horizon and
  target/due dates.

---

## 3. Planning Ceremony Tiers & Project Board Policy

| Tier | Typical Work | GitHub Primitives | Project Board Policy | Decomposition Rule |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | Localized bugfix, doc update, dependency bump, routine chore (1 to 3 issues) | 1 to 3 Issues, single optional Milestone | **Omitted** by policy (issue tracker suffices) | Keep each issue concise (`Context`, `Solution`, `Acceptance Criteria`). Clean-room audit omitted. |
| **Medium** | Vertical feature slice, multi-step refactor, capability buildout (4 to 8 vertical slices) | 1 Milestone + 4 to 8 Issues | **Recommended** (5-column Projects v2 board) | Each issue has its own branch and Draft PR. Explicit numbered acceptance criteria and test seams. Mandatory clean-room audit. |
| **Large** | Architectural epic, platform cutover, multi-service evolution | Roadmap doc + Phased Rolling Milestones + Cross-Slice Dependency Map + Deliverable Issues | **Required** (5-column Projects v2 board coordinates rolling horizons) | Source of truth stays in repo docs (`ARCHITECTURE.md`, `ROADMAP.md`, `docs/designs/*.md`, `docs/adr/`). Mandatory clean-room audit. |

### Deterministic Output Headers (Subagent Provenance Guard)
Every planning proposal must emit both headers verbatim before asking for
approval:

```markdown
### Project Board Policy: <Omitted|Recommended|Required> (Rationale)
### Reproducibility Audit: <Passed | Remediated> (Subagent: `<conversation-id>` | `Omitted: Small tier`)
```

- For `Medium` and `Large` tiers, `Subagent: <conversation-id>` must record the
  real conversation ID returned by the clean-room auditor subagent. Never
  fabricate a placeholder ID or claim `Passed` without running the subagent.
- `Omitted: Small tier` is valid only when the selected tier is `Small`.

---

## 4. Independent Zero-Context Reproducibility Audit

Mandatory for `Medium` and `Large` plans before presenting the decomposition for
approval (Step 5). Spawn a fresh-context subagent with zero prior conversation
history to verify that every proposed slice is executable without guesswork.

### Input Manifest (Strict Clean-Room)
Pass strictly raw artifacts and pinned repository state to the auditor:
1. Pinned repository root and commit SHA (`git rev-parse HEAD`).
2. Canonical specifications (`ARCHITECTURE.md`, `ROADMAP.md`, `docs/designs/*.md`, `docs/adr/*.md`).
3. Proposed raw issue titles, descriptions, test seams, and acceptance criteria markdown.
4. Proposed milestone titles, due dates, and Projects v2 board specifications.
5. Declared asset paths and prerequisite environment variables.

### Auditor Report Schema
The clean-room auditor must report directly from the manifest across five
explicit sections, without inventing missing requirements or fabricating
unchecked claims:

1. **Reconstructed from Source Artifacts**: Scope and sequence directly supported by source text.
2. **Inferred Requirements**: Deductions made from titles or conventions lacking explicit spec text.
3. **Undetermined Seams**: Gaps or ambiguities that cannot be resolved without guessing.
4. **Materiality Classification**:
   - *Material*: Forces an implementer to guess about scope, behavior, acceptance criteria, or prerequisites.
   - *Non-Material*: Cosmetic or self-evident convention.
5. **Concrete Remediation Plan**: Specific edits to specs, assets, or issue criteria needed to resolve every *Material* ambiguity.

Resolve all *Material* findings before requesting human approval. Record the
auditor's exact outcome (`Passed` if zero material findings, `Remediated` after
applying fixes) and `<conversation-id>` in the `### Reproducibility Audit:`
header.

---

## 5. Rolling Horizons for Large Projects

Avoid waterfall decomposition where distant work is pre-created weeks before
execution:

1. **Active Milestone (Immediate Horizon)**: Decompose into concrete vertical
   slice issues with falsifiable acceptance criteria and a cross-slice
   dependency map.
2. **Future Milestones (Deferred Horizons)**: Represent as high-level milestones
   with target due dates or single coarse placeholder issues.
3. **Architecture Synchronization**: Run `reconcile-docs` to sync canonical docs
   against completed work before decomposing the next rolling milestone.

---

## 6. Organization-Level Shared Projects v2 Boards

For multi-repository architectures coordinated under one GitHub organization:
- Create one shared Projects v2 board at the organization level and record its
  `project_number` in each participating repository's `AGENTS.md`.
- Onboard issues from child repositories onto that shared board using
  `organization(login: $owner).projectV2(number: $project_number)` and
  `addProjectV2ItemById` (see [github-projects-v2.md](github-projects-v2.md)).
- Keep architectural strategy and cross-repo roadmaps in the hub repository's
  `docs/` directory while the shared board tracks unified delivery status.
