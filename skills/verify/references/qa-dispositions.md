# Runtime QA Perspectives, Tiers, and Dispositions

Reference for `verify` Phase 1 (Read-Only Runtime QA and CI). Keep verification
effort proportional to failure consequences and change uncertainty rather than
diff line count alone.

---

## 1. Static Provenance Gate (`cr-review-meta` Check)

Before running runtime checks, confirm that `code-review` has already audited
the exact current PR commit with `verdict=ready`:

1. Fetch the PR's current head commit SHA:
   ```bash
   gh pr view <pr-number> --json headRefOid,isDraft,url,body
   ```
2. Inspect paginated PR reviews for the latest `cr-review-meta` HTML comment:
   ```bash
   gh api --paginate --slurp repos/{owner}/{repo}/pulls/<pr-number>/reviews \
     --jq '[add[] | select((.body // "") | contains("cr-review-meta:"))] | last | .body'
   ```
   Expected marker format:
   ```html
   <!-- cr-review-meta: max_id=NN head_sha=<sha> verdict=ready|needs_rework -->
   ```
3. **Hard Block Rule**:
   - If `cr-review-meta` is **missing**, halt Phase 1 and route to `code-review`.
   - If `head_sha` does **not** match `headRefOid` (stale review after new
     commits), halt Phase 1 and route to `code-review`.
   - If `verdict` is `needs_rework` (anything other than `ready`), halt Phase 1
     and route to `code-review` or `implement`.
   - Never substitute runtime QA for static code review, and never waive a
     missing or stale `verdict=ready` marker.

---

## 2. Operational Rigor Tiers

Select the minimum tier matching the slice's risk profile. Escalate individual
perspectives whenever a small diff touches a high-risk boundary (for example,
a two-line auth, permission, or URL sanitizer change).

| Tier | Typical Slice | Minimum Required Runtime & CI Checks | Execution Mode |
| :--- | :--- | :--- | :--- |
| **Lightweight** | Copy updates, styling tweaks, isolated low-risk fixes with no new state or untrusted inputs | 1. Execute `RV-*` checks from the `code-review` body (if present).<br/>2. Run relevant existing automated tests and a targeted smoke/regression check on the touched view or CLI path.<br/>3. Verify `gh pr checks` is green. | Direct execution in current session. |
| **Standard** | New UI component, ordinary API integration, or modification to an established workflow | 1. Execute all `RV-*` checks plus falsifiable assertions for every acceptance criterion.<br/>2. Run automated test suite, typecheck, and lint.<br/>3. Verify happy, empty, and error states plus persistence across reload.<br/>4. Run targeted regression checks on shared entrypoints.<br/>5. Verify `gh pr checks` is green. | Direct execution by default. Use an isolated black-box subagent (withholding diff and author self-audit) only if multi-step workflow bias warrants independence. |
| **High-Assurance** | Auth, permissions, payments, destructive actions, sensitive data, concurrent/conflict state, or cross-cutting architecture | All `Standard` checks, plus:<br/>1. Explicit conflict, duplicate-submission, and aggregate-state reconciliation assertions.<br/>2. Adversarial input checks against security boundaries.<br/>3. Secondary backend/API reads confirming persisted truth after mutations. | Independent black-box subagent for behavioral scenarios paired with `gh pr checks` verification. |

---

## 3. Selectable Black-Box QA Perspectives

Select only the perspectives warranted by the slice's risk profile. Convert
every selected perspective and every `RV-*` item into concrete falsifiable
checks rather than vague instructions ("check security").

| Perspective | Core Question | Concrete Runtime Checks to Construct |
| :--- | :--- | :--- |
| **Behavioral & Workflow** | Can the user complete the intended end-to-end task across real states? | Verify each required user journey across loading, empty, error/retry, partial, and success states; confirm state survives reload and matches authoritative backend reads. |
| **State & Concurrency** | Do local UI elements, sibling rows, and aggregate counters stay aligned with authoritative state? | Check duplicate-click guards, timeout/retry recovery, and conflict responses (such as `409`); assert that aggregate counters and sibling items reconcile with authoritative server state rather than drifting via partial local heuristics. |
| **Security Boundaries** | Can untrusted data execute code, break attributes, or route to unsafe destinations? | Exercise dynamic values across DOM/template and URL sinks with at least one adversarial payload; verify safe escaping, context-appropriate URL validation (`href`/`src`/`action`), and auth/permission enforcement. |
| **Ergonomics & Accessibility** | Is the slice usable on narrow screens, with touch, and via keyboard/assistive tech? | Check narrow mobile viewport (`375px`) for overflow, `>= 44x44px` touch targets, sequential keyboard `Tab` focus, visible `:focus-visible` outlines, and `aria-live` announcements for dynamic feedback. |
| **Scope & Regression** | Did the slice disturb adjacent features or shared entrypoints? | Run targeted smoke checks on neighboring views, routes, or CLI subcommands that share modified modules, routers, or schemas. |

---

## 4. Falsifiable Check Format & Scope Boundaries

Every check must declare its exact failure condition and scope before execution.
Never use open-ended observational prompts ("run the command and see what
happens").

```text
ID: RV-01 (or QA-01)
Scope: local | live-infra
Command / Action: <exact reproducible command or UI steps>
Assertion: PASS if <observable signal>; FAIL if <contradictory signal>
```

### `local` vs. `live-infra` Boundaries
- **`local`**: Runs against local builds, unit/integration suites, ephemeral
  test fixtures, local dev servers, or sandboxed mocks. Execute directly during
  Phase 1.
- **`live-infra`**: Requires privileged access, host rebuilds, production or
  staging migrations, live external APIs with side effects, or homelab/cloud
  infrastructure changes.
  - Execute `live-infra` checks **only** when the human owner has explicitly
    authorized the target environment and operation.
  - Without explicit authorization, do **not** fabricate execution or mark
    `PASS`; record `BLOCKED (out-of-bounds)` and preserve the exact command and
    `FAIL if ...` criteria for an authorized operator window.

---

## 5. Five-State Disposition Contract

Every required check ends in exactly one disposition. `BLOCKED` records an
honest execution boundary, never permission to assume correctness or count an
unexecuted check as `PASS`.

| Situation | Disposition | Required Action |
| :--- | :--- | :--- |
| Check executes (`local`, or explicitly authorized `live-infra`) and satisfies the expected condition | `PASS` | Attach observable proof (exit code, command output, HTTP status, DOM measurement, or screenshot). |
| Check executes and triggers its `FAIL if ...` condition | `FAIL` | Record reproducible steps and observed vs. expected output; block Phase 2 promotion. |
| Local fixture, seed, dependency, or tool setup prevents execution | `BLOCKED (env/fixture)` | Diagnose and repair the local blocker before judging the implementation (distinct from a product bug); block Phase 2 promotion until resolved. |
| `live-infra` check requires permissions or infrastructure unavailable or not explicitly authorized for this run | `BLOCKED (out-of-bounds)` | Preserve exact command and `FAIL if ...` criteria for the human owner; surface explicitly in the Phase 3 packet. |
| Check executes, but available evidence cannot prove or falsify the assertion | `INCONCLUSIVE` | State what signal is missing and how to make the check deterministically falsifiable; block Phase 2 promotion until resolved or explicitly decided by the human owner. |

---

## 6. Remote CI Inspection (`gh pr checks`)

1. Inspect remote CI status for the PR:
   ```bash
   gh pr checks <pr-number>
   ```
2. If all required checks pass, record CI as `PASS` in the Verification Ledger.
3. If any check is pending, wait or report pending status before Phase 2
   promotion.
4. If any check fails (red CI):
   - Fetch failed job logs directly:
     ```bash
     gh run view <run-id> --log-failed
     ```
   - Block Phase 2 promotion.
   - Route root-cause investigation of opaque CI failures to `diagnose`, or
     clear code/test regressions to `implement`.

---

## 7. Authority Separation & Anti-Rationalization Rules

- **Authority separation**: `code-review` establishes **static provenance** for
  a specific `head_sha`; `verify` establishes **runtime behavioral and CI
  evidence**; neither substitutes for the other, and only the human owner
  authorizes merge/release.
- **Expected values before observation**: State the exact `FAIL if ...`
  condition before running the check. If an assertion expects `2` and the
  system returns `1`, record `FAIL`, never `PASS` with a narrative excuse.
- **Separate fixture health from product bugs**: If a test seed or fixture
  mismatches schema reality, mark `BLOCKED (env/fixture)` and fix the fixture
  rather than misclassifying it as a passing check or a product regression.
