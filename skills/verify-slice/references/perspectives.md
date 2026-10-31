# Verification Tiers, Perspectives, and Dispositions

Reference for `verify-slice`. Keep effort proportional to failure consequences and change uncertainty rather than diff line count alone.

## 1. Operational Rigor Tiers

Each tier defines the minimum required checks. Escalate individual perspectives when a small diff touches a high-risk boundary (for example, a two-line auth or URL sanitizer change). When a reusable `Ready` `code-review` handshake covers the exact unchanged base, head, and working-tree diff (see `SKILL.md` Steps 1 and 4), that review satisfies the tier's static diff audit as static provenance while `verify-slice` supplies runtime behavioral evidence; if any relevant file changed post-review, audit at least the changed delta.

| Tier | Typical Slice | Minimum Required Checks | Execution Mode |
| :--- | :--- | :--- | :--- |
| **Lightweight** | Copy updates, styling tweaks, isolated low-risk fixes with no new state or untrusted inputs | 1. Run relevant existing automated tests.<br/>2. Targeted smoke/regression check on the touched view.<br/>3. Concise diff check for scope containment. | Direct execution in current session. |
| **Standard** | New UI component, ordinary API integration, or modification to an established workflow | 1. Falsifiable assertions for every acceptance criterion.<br/>2. Automated test suite, typecheck, and lint.<br/>3. Runtime check of happy, empty, and error states plus persistence reload.<br/>4. Targeted regression check on shared entrypoints.<br/>5. White-box diff review of untrusted sinks and state updates. | Direct execution by default. Use an isolated black-box subagent only if multi-step workflow bias or author self-audit independence warrants the cost. |
| **High-Assurance** | Auth, permissions, payments, destructive actions, sensitive data, concurrent/conflict state, or cross-cutting architecture | All `Standard` checks, plus:<br/>1. Explicit conflict, duplicate-submission, and aggregate-state reconciliation assertions.<br/>2. Source-to-sink security audit with adversarial input tests.<br/>3. Secondary backend/API reads confirming persisted truth after mutations. | Independent black-box subagent for behavioral scenarios paired with separate white-box diff review. |

## 2. Selectable Review Perspectives

Select only the perspectives relevant to the slice's risk profile. Give each selected perspective concrete assertions rather than vague instructions ("review security").

| Perspective | Core Question | Concrete Checks to Construct |
| :--- | :--- | :--- |
| **Behavioral & Workflow** | Can the user complete the intended end-to-end task across real states? | Verify each required user journey across loading, empty, error/retry, partial, and success states; confirm state survives reload and matches backend reads. |
| **State & Concurrency** | Do local UI elements, sibling rows, and aggregate counters stay aligned with authoritative state? | Check duplicate-click guards, timeout/retry recovery, and conflict responses (such as `409`); assert that aggregate counters and sibling items reconcile with authoritative server state rather than drifting via partial local heuristics. |
| **Security Boundaries** | Can untrusted data execute code, break attributes, or route to unsafe destinations? | Trace every dynamic value into DOM/template sinks: verify safe DOM APIs or HTML escaping for text and quoted attributes, context-appropriate URL validation for `href`/`src`/`action` (never relying on HTML escaping alone for URLs), and at least one adversarial payload check. |
| **Ergonomics & Accessibility** | Is the slice usable on narrow screens, with touch, and via keyboard/assistive tech? | Check narrow mobile viewport (`375px`) for overflow, `>= 44x44px` touch targets, sequential keyboard `Tab` focus, visible `:focus-visible` outlines, and `aria-live` announcements for dynamic feedback. |
| **Scope & Regression** | Did the slice disturb adjacent features or smuggle unrelated refactors? | Inspect shared files (`main`, routers, shared types/styles) for minimal additive footprint; run targeted smoke checks on neighboring views/endpoints. |
| **Commit & Evidence Hygiene** | Are commits localizable and does claimed test coverage match reality? | Separates two distinct responsibilities: (1) **Static review** (commit structure, diff scope, source and test inspection) is covered by a matching `Ready` review handshake. (2) **Runtime evidence reconciliation** verifies that reported outcomes are supported by executed checks and relevant test assertions substantiate claimed contracts. |

## 3. Four-State Disposition Contract and Boundary Matrix

Every required assertion ends in exactly one disposition. `BLOCKED` records an honest execution boundary, never permission to assume correctness or count an unexecuted check as `PASS`:

| Situation | Disposition | Required Action |
| :--- | :--- | :--- |
| Check executes (`local`, or `live-infra` explicitly authorized by the human owner) and satisfies expected condition | `PASS` | Attach observable proof (command output, HTTP status, DOM measurement, or screenshot). |
| Check executes and contradicts expected behavior | `FAIL` | Record reproducible steps and observed vs. expected output. |
| Local fixture, seed, or tool setup prevents execution | `BLOCKED (env/fixture)` | Diagnose and repair the local blocker before judging the implementation (distinct from a product bug). |
| `live-infra` check requires permissions or infrastructure (host rebuilds, production migrations, privileged network changes) unavailable or not explicitly authorized for this run | `BLOCKED (out-of-bounds)` | Do not fabricate execution or mark `PASS`; preserve the exact command and pass/fail criteria for an authorized operator run or maintenance window. |
| Check executes, but available evidence cannot prove or falsify the assertion | `INCONCLUSIVE` | State what signal is missing and how to make the check deterministically falsifiable. |

### Authority Separation Invariant
- `code-review` establishes **static provenance** for a specific revision range and working-tree diff.
- `verify-slice` establishes **runtime behavioral evidence** for selected assertions.
- Neither substitutes for the other, and neither grants release approval; only the human owner authorizes release.

### Anti-Rationalization Rules
1. **Expected values before observation**: State the exact pass/fail condition before running the check. If an assertion expects `2` and the system shows `1`, record `FAIL`, never `PASS` with a narrative excuse ("targeted reconciliation trade-off").
2. **Separate seed/fixture health from product bugs**: Avoid fragile raw SQL test seeds when domain services or API helpers exist; if a fixture mismatches schema reality, mark `BLOCKED` and fix the fixture.
3. **Unique provenance**: When comparing author self-audit, black-box QA, and diff review, label whether each confirmed defect was caught by self-audit, black-box execution, or code inspection so process value stays measurable.
