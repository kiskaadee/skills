# Review Axes and Risk Tiers

Reference for `code-review`. Inspects git diffs across four distinct evaluation dimensions without allowing strength on one axis to compensate for defects on another.

Derived and adapted from Matt Pocock's skills repository (github.com/mattpocock/skills), combining the multi-axis review discipline with empirical safety and verification invariants.

## 1. The Four Review Axes

| Axis | Primary Question | Failure Mode Caught | Core Inspection Questions |
| :--- | :--- | :--- | :--- |
| **Spec & Scope** | Did we build what was requested, aligned with project direction, and only that? | Scope creep, missing requirements, architectural or roadmap drift, leaky abstractions | 1. Does the diff satisfy the originating issue or specification contract?<br/>2. When canonical direction docs exist (`ARCHITECTURE.md`, `ROADMAP.md`, ADRs, or active milestone scope), does the change align with long-term boundaries and trajectory?<br/>3. Is there unrequested functionality or premature generalization?<br/>4. Are changes to shared entrypoints (e.g., routers, base config) minimal and additive? |
| **Standards & Smells** | Is the implementation maintainable and consistent? | Structural debt, friction with conventions | 1. Does the code adhere to repo standards (`CODING_STANDARDS.md`, linter configs)?<br/>2. Are code smells present that warrant refactoring? (See [smell-heuristics](smell-heuristics.md)).<br/>3. Is naming clear and aligned with domain vocabulary? |
| **Seam & Test Integrity** | Do tests prove actual contracts at public interfaces? | Tautological tests, implementation coupling, boundary gaps, flaky waits | Audit against [seams-and-mocking](../../tdd/references/seams-and-mocking.md) and [test-quality](../../tdd/references/test-quality.md):<br/>1. Public seams only; boundary mocks only; injected timing/clock callables instead of global runtime monkeypatching; deterministic waits and guaranteed teardown.<br/>2. Non-tautological assertions with independent literals (no imported production value constants), exact+neighbor boundary points (`[min-1, min, max, max+1]`), and single-behavior test names (no vague buckets or `_and_` chains). |
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
| **Confirmed Critical or High** | `Needs Rework` | Fix confirmed defects on the branch before release review. |
| **Confirmed or Unresolved Medium or Low (untriaged)** | `Pending Triage` | Do not recommend merge. Human owner chooses 1 of 3 exits per finding: (A) fix in-branch, (B) promote to live tracker (Gitea issue or `todo.txt`), or (C) grant permanent `Accepted Trade-off`. |
| **Unresolved Critical or High** | `Blocked` | Resolve missing evidence or escalate to human owner before proceeding. |
| **Scope Inability or Missing Base Ref** | `Blocked` | Establish base commit and diff boundaries before reviewing. |
| **Zero Untriaged Findings** | `Ready` | All findings resolved, tracked in a live tracker, or explicitly granted `Accepted Trade-off` by the owner. |

### `Ready` vs. `Pending Triage` Semantics and Downstream Reuse
- **No agent self-adjudication**: Reviewer agents must never self-assign `Accepted Trade-off` on a review pass. Every valid observation (including `Low` nits) starts as `Confirmed` (or `Unresolved`), producing `Pending Triage` (or `Needs Rework`) rather than `Ready`.
- **`Pending Triage` blocks merge recommendations**: A review in `Pending Triage` qualifies as `Ready` for `gitea-pr` merge readiness only after every finding has taken one of the three explicit exits: (A) fixed in a new commit on the branch, (B) recorded in a live tracker that future agents read (an open Gitea issue or `todo.txt` via `tuxedo add`), or (C) explicitly approved by the human owner as a permanent `Accepted Trade-off` (no future action needed).
- A `Ready` review establishes static provenance for that exact diff; it does not substitute for runtime verification or authorize release.

## 3. Risk-Scaled Execution Tiers

To keep review overhead proportional to risk, execution mode reuses the tiers established in `verify-slice`:

| Review Risk Tier | Typical Change | Review Execution Strategy |
| :--- | :--- | :--- |
| **Lightweight** | Copy updates, styling adjustments, isolated bugfixes with no new state or untrusted data. | Single-agent sequential pass inspecting all 4 axes in order. |
| **Standard** | New UI components, regular API endpoints, database queries, or schema additions. | Independent review passes over the diff. Subagents may be used when helpful to prevent bias. |
| **High-Assurance** | Auth, permissions, payments, concurrent state reconciliation, destructive actions, or core shared libraries. | Assign a dedicated isolated reviewer to **Seam & Test Integrity** (Axis 3, auditing test diffs against `tdd/references/`), separate from `Spec & Scope` + `Defensive Invariants` and `Standards & Smells`, followed by independent aggregation. |

## 4. Aggregation and Anti-Silence Rules

When multiple passes or subagents inspect a change:
1. **Never silently resolve disagreements**: If Reviewer A flags a pattern as a defect and Reviewer B considers it acceptable, record the finding under `Unresolved` with both perspectives cited. The human owner adjudicates.
2. **Preserve exact evidence**: Every finding must include exact file paths, line numbers, and code snippets demonstrating the condition.
3. **Emit executable runtime checks**: Where static analysis cannot verify dynamic timing, rendering, or network failure modes, formulate runnable Step 6 checks formatted per [finding-schema](finding-schema.md) and pass them to `verify-slice`.
