# Verification Tiers, Perspectives, and Dispositions

Reference for `verify-slice`. Keep effort proportional to failure consequences and change uncertainty rather than diff line count alone.

## 1. Operational Rigor Tiers

Each tier defines the minimum required checks. Escalate individual perspectives when a small diff touches a high-risk boundary (for example, a two-line auth or URL sanitizer change).

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
| **Commit & Evidence Hygiene** | Are commits localizable and does claimed test coverage match reality? | Check that commits separate coherent boundaries where practical and compare author self-audit claims against what unit/integration tests actually assert. |

## 3. Four-State Disposition Contract

Every required assertion ends in exactly one state:

- `PASS`: Assertion satisfied with observable proof (command output, HTTP response, DOM measurement, or screenshot).
- `FAIL`: Assertion violated with reproducible steps and observed vs. expected output.
- `BLOCKED`: Check could not run due to an environmental, fixture, or dependency problem (distinct from a product bug; diagnose the blocker before judging the implementation).
- `INCONCLUSIVE`: Check ran, but collected evidence is insufficient to prove or falsify the assertion.

### Anti-Rationalization Rules
1. **Expected values before observation**: State the exact pass/fail condition before running the check. If an assertion expects `2` and the system shows `1`, record `FAIL`, never `PASS` with a narrative excuse ("targeted reconciliation trade-off").
2. **Separate seed/fixture health from product bugs**: Avoid fragile raw SQL test seeds when domain services or API helpers exist; if a fixture mismatches schema reality, mark `BLOCKED` and fix the fixture.
3. **Unique provenance**: When comparing author self-audit, black-box QA, and diff review, label whether each confirmed defect was caught by self-audit, black-box execution, or code inspection so process value stays measurable.
