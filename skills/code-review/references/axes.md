# Review Axes and Risk Tiers

Reference for `code-review`. Inspects git diffs across four distinct evaluation dimensions without allowing strength on one axis to compensate for defects on another.

Derived and adapted from Matt Pocock's skills repository (github.com/mattpocock/skills), combining the multi-axis review discipline with empirical safety and verification invariants.

## 1. The Four Review Axes

| Axis | Primary Question | Failure Mode Caught | Core Inspection Questions |
| :--- | :--- | :--- | :--- |
| **Spec & Scope** | Did we build what was requested, aligned with project direction, and only that? | Scope creep, missing requirements, architectural or roadmap drift, leaky abstractions | 1. Does the diff satisfy the originating issue or specification contract?<br/>2. When canonical direction docs exist (`ARCHITECTURE.md`, `ROADMAP.md`, ADRs, or active milestone scope), does the change align with long-term boundaries and trajectory?<br/>3. Is there unrequested functionality or premature generalization?<br/>4. Are changes to shared entrypoints (e.g., routers, base config) minimal and additive? |
| **Standards & Smells** | Is the implementation maintainable and consistent? | Structural debt, friction with conventions | 1. Does the code adhere to repo standards (`CODING_STANDARDS.md`, linter configs)?<br/>2. Are code smells present that warrant refactoring? (See [smell-heuristics](smell-heuristics.md)).<br/>3. Is naming clear and aligned with domain vocabulary? |
| **Seam & Test Integrity** | Do tests prove actual contracts at public interfaces? | Tautological tests, implementation coupling | 1. Are tests verifying public interfaces (seams) rather than mocking private internals?<br/>2. Are assertions non-tautological (do not mirror code logic or pass by construction)?<br/>3. Prefer tests establishing observable behavior through meaningful vertical slices. Batch independent cases when doing so preserves clear contracts and does not substitute test quantity for behavioral evidence. |
| **Defensive Invariants** | Does the code preserve critical system properties under stress? | Injection, state desync, unhandled crashes | 1. Are untrusted inputs sanitized before reaching sinks? (See [defensive-invariants](defensive-invariants.md)).<br/>2. Does state reconcile against authoritative sources rather than local heuristic drift?<br/>3. Are failure semantics, timeouts, and resource limits explicit? |

### Non-Compensation Invariant
A strong pass on one axis never excuses a failure on another:
- Clean abstractions and zero code smells cannot excuse an unescaped HTML sink or an unhandled conflict.
- 100% test coverage cannot excuse unrequested feature drift, architectural direction drift, or broken domain invariants.
- Strict spec compliance cannot excuse fragile code structure that breaks repository conventions.

## 2. Review Recommendations Matrix

The distinction between recommendations is clear: `Needs Rework` means an established defect requires implementation or test changes; `Blocked` means the review cannot establish sufficient confidence or scope to proceed safely.

| Condition Observed | Final Recommendation | Action Required |
| :--- | :--- | :--- |
| **Confirmed Critical or High** | `Needs Rework` | Fix confirmed defects before release review. |
| **Confirmed Medium or Low requiring changes** | `Needs Rework` | Apply requested refactoring or test coverage fixes. |
| **Unresolved Critical or High** | `Blocked` | Resolve missing evidence or escalate to human owner before proceeding. |
| **Unresolved Medium or Low** | `Ready` (Conditional) | Human owner may adjudicate and accept trade-offs without blocking. |
| **Scope Inability or Missing Base Ref** | `Blocked` | Establish base commit and diff boundaries before reviewing. |
| **No Blocking Findings** | `Ready` | Implementation is structurally sound; proceed to `verify-slice` or release. |

### `Ready` Semantics and Downstream Reuse
`Ready` means the review completed across all four axes, no confirmed or unresolved blocking findings remain (`Needs Rework` or `Blocked`), and the report explicitly identifies the base revision, head revision, and relevant working-tree state it covered. `Ready (Conditional)` qualifies as `Ready` for downstream handshake reuse only after the human owner adjudicates the open Medium/Low items (`Accepted Trade-off` or `Rejected`). A `Ready` review establishes static provenance for that exact diff; it does not substitute for runtime verification or authorize release.

### Documented Trade-Off Acceptance
When a human owner accepts a documented trade-off for a Medium or Low finding, record the finding disposition as `Accepted Trade-off` (distinct from `Rejected`). This preserves audit traceability without misclassifying an intentional compromise as a disproven defect.

## 3. Risk-Scaled Execution Tiers

To keep review overhead proportional to risk, execution mode reuses the tiers established in `verify-slice`:

| Review Risk Tier | Typical Change | Review Execution Strategy |
| :--- | :--- | :--- |
| **Lightweight** | Copy updates, styling adjustments, isolated bugfixes with no new state or untrusted data. | Single-agent sequential pass inspecting all 4 axes in order. |
| **Standard** | New UI components, regular API endpoints, database queries, or schema additions. | Independent review passes over the diff. Subagents may be used when helpful to prevent bias. |
| **High-Assurance** | Auth, permissions, payments, concurrent state reconciliation, destructive actions, or core shared libraries. | Fully isolated reviewers for separate axes (e.g., Subagent 1 on Spec, Invariants, and Tests; Subagent 2 on Standards and Smells), followed by independent aggregation. |

## 4. Aggregation and Anti-Silence Rules

When multiple passes or subagents inspect a change:
1. **Never silently resolve disagreements**: If Reviewer A flags a pattern as a defect and Reviewer B considers it acceptable, record the finding under `Unresolved` with both perspectives cited. The human owner adjudicates.
2. **Preserve exact evidence**: Every finding must include exact file paths, line numbers, and code snippets demonstrating the condition.
3. **Emit executable runtime checks**: Where static analysis cannot verify dynamic timing, rendering, or network failure modes, formulate runnable Step 6 checks formatted per [finding-schema](finding-schema.md) and pass them to `verify-slice`.
