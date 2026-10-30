# Finding Schema and Review Output

Reference for `code-review`. Defines the required structure for reporting findings, ensuring every note is actionable, evidence-backed, and auditable.

Derived and adapted from Matt Pocock's review principles (github.com/mattpocock/skills), combining side-by-side axis reporting with strict defect provenance and disposition contracts.

## 1. Finding Record Schema

Every reported finding must populate all seven fields:

| Field | Description | Allowed Values / Format |
| :--- | :--- | :--- |
| **ID** | Stable identifier within this review. | `CR-01`, `CR-02`, etc. |
| **Axis** | The review axis that uncovered the finding. | `Spec & Scope`, `Standards & Smells`, `Seam & Test Integrity`, `Defensive Invariants`. |
| **Severity** | Potential failure consequence if the defect occurs. Describes impact, not reviewer confidence. | `Critical` (system security breach, data loss, fatal crash), `High` (broken invariant, missing spec requirement), `Medium` (code smell, fragile logic, missing edge test), `Low` (minor style inconsistency, naming). |
| **Evidence** | Exact location, change category, and reproducible behavior. | Distinguishes whether the code is committed, staged, or unstaged: e.g. `src/view.ts:L45 (unstaged)` with excerpt. |
| **Invariant** | The requirement, contract, or system property violated. | Clear statement of expectation (e.g., "Untrusted DOM values must be escaped before interpolation"). |
| **Impact** | Concrete failure consequence if left unaddressed. | What breaks in production, concurrency, or maintenance (e.g., "Stored XSS when name contains `<script>`"). |
| **Disposition** | Current evidentiary status of the finding. | `Confirmed` (proven defect backed by evidence), `Rejected` (disproven or false positive), `Unresolved` (open disagreement or missing evidence), `Accepted Trade-off` (conscious compromise approved by owner). |

## 2. Disposition and Severity Rules

1. **Blocking status**: Only `Confirmed` findings (Critical, High, or changes-required Medium/Low) trigger a `Needs Rework` verdict.
2. **Unresolved findings**: `Unresolved Critical` or `Unresolved High` findings result in a `Blocked` verdict until resolved with evidence or owner adjudication. `Unresolved Medium` or `Low` findings can remain `Ready` if the owner accepts the trade-off.
3. **Rejected vs. Accepted Trade-off**:
   - `Rejected`: The finding was an invalid concern or disproven by facts.
   - `Accepted Trade-off`: The finding identifies a genuine compromise where the owner explicitly accepts the local cost for an engineering reason.
   Both remain in the ledger for full audit traceability.
4. **Severity vs. confidence**: `Severity` describes potential impact, never reviewer confidence. A suspected high-impact flaw with incomplete evidence must be logged as `High` severity with `Unresolved` disposition, not downgraded to `Low`.

## 3. Review Report Layout

The final review summary presented to the user must follow this structure:

```markdown
# Code Review Summary: <branch or commit range>

## Overview & Scope State
- **Base Commit**: `<base-ref>` (`<base-commit-sha>`) -> `<HEAD>` (`<head-commit-sha>`)
- **Working Tree State**: Clean / Staged Changes / Unstaged Changes (`git status --short`)
- **Assigned Risk Tier**: `Lightweight` | `Standard` | `High-Assurance`
- **Execution Mode**: `Sequential` | `Independent Passes` | `Subagent Reviewers`

## Findings Ledger

### Confirmed Findings (Needs Rework)
| ID | Axis | Severity | State | Location | Invariant Violated | Impact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CR-01 | Defensive Invariants | Critical | Committed | `src/view.ts:L45` | Unescaped dynamic HTML sink | DOM XSS via attendee name |

### Unresolved Disagreements / Material Risks (Blocked if Critical/High)
| ID | Axis | Severity | Location | Competing Perspectives / Open Risk | Decision Needed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CR-02 | Standards & Smells | Medium | `src/api.ts:L110` | Reviewer A flags Primitive Obsession; Author notes single call site. | Accept string or introduce domain type |

### Accepted Trade-offs & Rejected Findings (Audit Traceability)
| ID | Axis | Disposition | Location | Rationale / Decision |
| :--- | :--- | :--- | :--- | :--- |
| CR-03 | Spec & Scope | Rejected | `src/main.ts:L12` | Suspected scope creep confirmed as required wiring for acceptance criterion 2. |
| CR-04 | Standards & Smells | Accepted Trade-off | `scripts/seed.py:L10` | Inlined script logic accepted to keep utility independent of core module. |

## Axis Breakdown
- **Spec & Scope**: Pass/Fail summary. Notes on scope containment and shared entrypoints across working-tree and commits.
- **Standards & Smells**: Adherence to repo conventions and Fowler smell diagnostics.
- **Seam & Test Integrity**: Evaluation of test boundaries, tautological assertions, and vertical slice evidence.
- **Defensive Invariants**: Status of trust boundaries, authority, consistency, failure semantics, and resource limits.

## Recommended Runtime Scenarios for verify-slice
List concrete runtime checks or adversarial test cases that static inspection identified as necessary for runtime verification:
1. Scenario: Verify out-of-band 409 conflict handling with simultaneous check-in attempts.
2. Scenario: Verify input sanitization with payload `<img src=x onerror=alert(1)>`.

## Overall Recommendation
- **Status**: `Ready` | `Needs Rework` | `Blocked`
- **Next Action**: State whether to hand off to `verify-slice` for runtime verification, `diagnose` for root-cause fixes, or present to human owner for adjudication.
```
