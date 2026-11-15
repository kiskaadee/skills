# Reconciliation Matrix

This guide governs how the agent correlates historical records, present implementation, and future intent during Step 4 of `reconcile-docs`.

## 1. Epistemic Authority Model

Treat each source according to its temporal role and authority:

| Source | Temporal role | Epistemic authority |
| :--- | :--- | :--- |
| Chronological records (vault notes, logs, discussions) | Past | Historical evidence. Explains how the system arrived here. |
| Merged PRs & published `code-review` comments (`gt pr`) | Past -> Present | Primary record of slice-level contract evolutions, accepted trade-offs, and deferred nits. |
| Repository implementation (code, tests, configuration, `AGENTS.md`) | Present | Canonical technical truth. Determines what the system is right now. |
| Existing repository documentation (`ARCHITECTURE.md`, `docs/designs/*.md`) | Present | Canonical unless contradicted by current implementation. |
| Gitea Milestones & Project Board (`Completed` vs. `Backlog`/`Ready`) | Present -> Future | Read-only delivery state: `Completed` cards are present truth; `Backlog`/`Ready` cards are future intent. |
| Active plans (roadmaps, proposals, pending designs) | Future | Planned intent. Describes where the system may go next. |
| ADRs | Past -> Present | Historical decision record that remains valid until superseded. |
| ROADMAP | Future | Intended technical trajectory. |

**Guiding Rule**: Historical records explain how the system arrived here; the repository determines what the system is now; active plans describe where it may go next.

Never allow an old note or obsolete plan to overwrite the actual implementation reality.

## 2. Reconciliation Mapping

For every concept, architectural choice, or component candidate, correlate its status across all three temporal domains:

| Historical state | Current implementation | Future state | Documentation consequence |
| :--- | :--- | :--- | :--- |
| Decision still relevant | Implemented | No change | ADR (why) + ARCHITECTURE (what exists now) |
| Decision changed | New implementation | Migration complete | Supersede old ADR + ARCHITECTURE (current state) |
| Old proposal | Never implemented | Still planned | ROADMAP (planned item) |
| Old proposal | Never implemented | Abandoned | Omit from docs; preserve in discussion archive only |
| Current implementation | No historical rationale | No known change | ARCHITECTURE (document current reality) + consider ADR candidate |
| Current implementation | Important rationale exists | No known change | ADR (record rationale) + ARCHITECTURE |
| Current implementation | Planned replacement | Future migration | ARCHITECTURE (current) + ROADMAP (planned migration) |
| Contradictory records | Repository resolves it | Stable | Document current code truth; record supersession in ADR if needed |

## 3. Conflict Typology

Flag contradictions explicitly during reconciliation rather than quietly smoothing them over:

### Historical Contradiction
- *Symptom*: Notes claim component X is used (e.g. PostgreSQL), but repository code uses Y (e.g. SQLite WAL).
- *Resolution*: Repository code wins for present-state docs. Check chronological records for a pivot or migration. If found, mark the original decision superseded and document the migration in an ADR.

### Premature Promotion
- *Symptom*: A roadmap, RFC, or discussion note describes a feature or architecture as if it exists, but the codebase does not contain it.
- *Resolution*: Do not include in `ARCHITECTURE.md` or `README.md`. Place into `ROADMAP.md` under the appropriate planning horizon (Near Term, Medium Term, or Exploratory).

### Zombie Architecture
- *Symptom*: Existing repository documentation references modules, subsystems, or dependencies that were deleted or refactored away.
- *Resolution*: Mark for removal in `ARCHITECTURE.md` and `README.md`. If the removal was a major architectural pivot, record a superseding ADR.

### Amnesiac Implementation
- *Symptom*: The codebase contains complex boundaries, non-standard conventions, or unusual workarounds, but history contains no explanation.
- *Resolution*: Document the current reality in `ARCHITECTURE.md` and surface an ADR candidate during the Step 5 human checkpoint so the engineer can supply the missing rationale.


### Mid-Slice Spec Drift
- *Symptom*: A merged slice intentionally evolved a shared type, configuration model, error class, or boundary (documented in `AGENTS.md` or PR review comments), leaving an active design specification (`docs/designs/*.md`) or `ARCHITECTURE.md` referencing the pre-slice contract.
- *Resolution*: Reconcile the affected sections of `docs/designs/*.md` and `ARCHITECTURE.md` to match the merged implementation on `main` before downstream slices execute.
