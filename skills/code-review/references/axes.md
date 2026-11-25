# Review Axes and Risk Tiers

Reference for `code-review`. Inspects git diffs across four distinct evaluation dimensions without allowing strength on one axis to compensate for defects on another.

Derived and adapted from Matt Pocock's skills repository (github.com/mattpocock/skills), combining the multi-axis review discipline with empirical safety and verification invariants.

## 1. The Four Review Axes

| Axis | Primary Question | Failure Mode Caught | Core Inspection Questions |
| :--- | :--- | :--- | :--- |
| **Spec & Scope** | Did we build what was requested, aligned with project direction, and only that? | Scope creep, missing requirements, architectural or roadmap drift, stale local docs | 1. Does the diff satisfy the originating GitHub issue or specification contract?<br/>2. When canonical direction docs exist (`ARCHITECTURE.md`, `ROADMAP.md`, ADRs, or active milestone scope), does the change align with long-term boundaries and trajectory?<br/>3. Is there unrequested functionality or premature generalization?<br/>4. Are changes to shared entrypoints minimal and additive, and are affected local markdown files updated when behavior or interfaces change? |
| **Standards & Smells** | Is the implementation maintainable, hygienic, and consistent? | Structural debt, missing docstrings, stale comments, lint/format regressions | 1. Does the code adhere to repo standards (`CODING_STANDARDS.md`, linter and formatter configs) with zero lint/format regressions?<br/>2. Are new or modified public symbols documented with clear docstrings, and are inline comments accurate (no stale comments contradicting the new code)?<br/>3. Are code smells present that warrant refactoring? (See [smell-heuristics](smell-heuristics.md)).<br/>4. Is naming clear and aligned with domain vocabulary? |
| **Seam & Test Integrity** | Do tests prove actual contracts at public interfaces? | Tautological tests, implementation coupling, boundary gaps, flaky waits | Audit against [seams-and-mocking](../../tdd/references/seams-and-mocking.md) and [test-quality](../../tdd/references/test-quality.md):<br/>1. Public seams only; boundary mocks only; injected timing/clock callables instead of global runtime monkeypatching; deterministic waits and guaranteed teardown.<br/>2. Non-tautological assertions with independent literals (no imported production value constants), exact+neighbor boundary points (`[min - 1, min, max, max + 1]`), and single-behavior test names (no vague buckets or `_and_` chains). |
| **Defensive Invariants** | Does the code preserve critical system properties under stress? | Injection, state desync, unhandled crashes | 1. Are untrusted inputs sanitized before reaching sinks? (See [defensive-invariants](defensive-invariants.md)).<br/>2. Does state reconcile against authoritative sources rather than local heuristic drift?<br/>3. Are failure semantics, timeouts, and resource limits explicit? |

### Non-Compensation Invariant
A strong pass on one axis never excuses a failure on another:
- Clean abstractions and zero code smells cannot excuse an unescaped HTML sink or an unhandled conflict.
- 100% test coverage cannot excuse unrequested feature drift, architectural direction drift, or broken domain invariants.
- Strict spec compliance cannot excuse fragile code structure, missing public docstrings, or lint regressions that break repository conventions.

## 2. Review Recommendations Matrix

The distinction between recommendations is clear: `Needs Rework` means an established defect requires implementation or test changes; `Blocked` means the review cannot establish sufficient confidence or scope to proceed safely.

| Condition Observed | Final Recommendation | Published `verdict` | Action Required |
| :--- | :--- | :--- | :--- |
| **Confirmed Critical or High** | `Needs Rework` | `needs_rework` | Fix confirmed defects on the branch via `implement` before `verify`. |
| **Confirmed or Unresolved Medium or Low (untriaged)** | `Pending Triage` | `needs_rework` | Do not promote or merge. Human owner chooses 1 of 3 exits per finding: Exit A (fix in-branch), Exit B (promote to a GitHub Issue), or Exit C (dismiss as invalid/false positive). |
| **Unresolved Critical or High** | `Blocked` | `needs_rework` | Resolve missing evidence or escalate to human owner before proceeding. |
| **Scope Inability or Missing Base Ref** | `Blocked` | (local halt) | Establish base commit and diff boundaries before reviewing. |
| **Zero Untriaged Findings** | `Ready` | `ready` | All findings resolved in-branch, promoted to a GitHub Issue (Exit B), or dismissed as invalid/false positive (Exit C). Route to `verify`. |

### `Ready` vs. `Pending Triage` Semantics and Downstream Reuse
- **No agent self-dismissal**: Every valid finding (including `Low` severity) starts in `Pending Triage` as `Confirmed` (or `Unresolved`), producing `Pending Triage` or `Needs Rework` (`verdict=needs_rework`) rather than `Ready`.
- **`Pending Triage` blocks `verify` promotion**: A review qualifies as `Ready` (`verdict=ready`) for `verify` only after every finding has taken one of the three explicit exits: Exit A (fixed in a new commit on the branch), Exit B (promoted to a GitHub Issue and recorded as `Promoted to #<N>` in the superseding `Ready` review's triage summary), or Exit C (dismissed as invalid/false positive and recorded as `Dismissed: <reason>` in the superseding `Ready` review's triage summary).
- A `Ready` review establishes static provenance for that exact `head_sha`; it does not substitute for runtime verification in `verify` or authorize release.

## 3. Risk-Scaled Execution Tiers

To keep review overhead proportional to risk, execution mode aligns with the risk tiers used in `verify`:

| Review Risk Tier | Typical Change | Review Execution Strategy |
| :--- | :--- | :--- |
| **Lightweight** | Small localized diffs, copy updates, styling adjustments, isolated bugfixes with no new state or untrusted data. | Single-agent sequential pass inspecting all 4 axes in order. |
| **Standard** | Multi-file feature slices, new UI components, regular API endpoints, database queries, or schema additions. | Independent review passes over the diff. Subagents may be used when helpful to prevent bias. |
| **High-Assurance** | Security, auth, permissions, payments, schema migrations, concurrent state reconciliation, destructive actions, core shared libraries, or >500-line diffs. | Assign a dedicated isolated reviewer to **Seam & Test Integrity** (Axis 3, auditing test diffs against `tdd/references/`), separate from `Spec & Scope` + `Defensive Invariants` and `Standards & Smells`, followed by independent aggregation. |

## 4. Aggregation and Anti-Silence Rules

When multiple passes or subagents inspect a change:
1. **Never silently resolve disagreements**: If Reviewer A flags a pattern as a defect and Reviewer B considers it acceptable, record the finding under `Unresolved` with both perspectives cited. The human owner adjudicates.
2. **Preserve exact evidence**: Every finding must include exact file paths, line numbers, and code snippets demonstrating the condition.
3. **Emit executable runtime checks**: Where static analysis cannot verify dynamic timing, rendering, or network failure modes, formulate runnable `RV-*` checks formatted per [finding-schema](finding-schema.md) so `verify` can execute them from the published PR review body.
