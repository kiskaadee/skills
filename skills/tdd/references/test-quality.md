# Test Quality and Anti-Patterns

Reference for `tdd`. Keeps red-to-green cycles anchored to observable behavior, independent truth, and real failure semantics.

Derived and adapted from Matt Pocock's `tdd` skill (`github.com/mattpocock/skills`), combined with empirical state-reconciliation and input-safety lessons.

## 1. Four Test Anti-Patterns to Reject

### A. Implementation-Coupled Tests
- **Smell**: Asserting `toHaveBeenCalledWith` on internal helpers, testing private functions, or verifying state through a side channel (raw table query) when a public read interface exists.
- **Tell**: The test breaks during an internal refactor even though caller-observable behavior is unchanged.
- **Fix**: Act through the public write seam and assert through the public read seam or rendered output.

### B. Tautological Assertions
- **Smell**: Recomputing the expected value with the same logic as production code, importing production value constants (`PERMISSIONS`, `DEFAULT_PORT`, `ALLOWLIST`, error templates) to construct the expected value, or mocking a boundary to return `X` and only asserting `result == X`.
- **Tell**: A bug in the formula or a typo/accidental change to the production constant keeps the test green.
- **Fix**: Use independent hardcoded literals, worked domain examples, or specification tables as the expected value (importing public *types* or *exception classes* such as `pytest.raises(ConfigError)` is valid).

```python
# BAD: Recomputes expected value or imports the production constant under test
def test_calculate_total_and_port():
    assert calculate_total([Item(price=10), Item(price=5)]) == sum(i.price for i in items)
    assert client.port == DEFAULT_PORT

# GOOD: Independent literals from worked example and spec
def test_calculate_total_sums_item_prices():
    assert calculate_total([Item(price=10), Item(price=5)]) == 15
```

### C. Optimistic Local-State Illusions
- **Smell**: Testing conflict or error recovery (such as HTTP `409 Conflict`) by asserting only that the clicked row changed locally, ignoring sibling records or aggregate counters that changed out-of-band on the server.
- **Fix**: Simulate authoritative server state where multiple records diverged out-of-band, and assert that both item state and aggregate counters reconcile with the authoritative read.

### D. Premature Horizontal Batching
- **Smell**: Writing twenty parameterized tests upfront against an imagined interface before one vertical slice works end-to-end.
- **Fix**: Drive one tracer-bullet test from Red to Green first so the real contract settles. Once the vertical slice works, batch independent boundary/edge cases (`pytest.mark.parametrize`, `test.each`, Rust table slices) where they clarify the contract without padding test count.

## 2. Negative and Defensive Slices Worth Adding

After the primary capability turns green, add focused red-to-green tests for the failure modes present in the slice:
- **Conflict and retry paths**: Duplicate submissions, `409` responses, network errors, and idempotent retries.
- **Untrusted input boundaries**: Special characters or HTML payloads (`<img src=x onerror=...>`) rendered safely as literal text rather than executable markup.
- **Empty and boundary values (Boundary Value Analysis)**: For any closed range `[min, max]` or length/capacity limit, test all four boundary neighbors `[min - 1, min, max, max + 1]` (accepting `min` and `max`; rejecting `min - 1` and `max + 1`). For one-sided lower bounds (`>= min` or non-empty length), test `[min - 1, min]`; for one-sided upper bounds (`<= max`), test `[max, max + 1]` (adapting to `<` / `>` exclusive boundaries). Parametrize cleanly (`@pytest.mark.parametrize`, `test.each`, Bash loops, Rust test tables, JUnit `@ParameterizedTest`).

## 3. Single-Behavior Test Naming and Focus

Name every test `<unit> + <observable behavior under condition>` so failures identify the exact broken contract without reading the test body:
- **Python (`pytest`) / Bash (`bats`) / Rust (`#[test]`)**: `test_<unit>_<behavior>` (for example, `test_set_volume_rejects_above_max`).
- **TypeScript (`vitest`/`jest`)**: `describe("<unit>", () => it("<behavior under condition>"))`.
- **Java (`JUnit 5`)**: `@Test void <unit>_<behavior>()` (or `@DisplayName("<unit> <behavior under condition>")`).
- **Ban vague bucket names**: Never name tests `test_validation`, `test_defaults`, `test_edge_cases`, or `test_helpers`.
- **Ban multi-behavior `_and_` chains**: Split compound tests (`test_wake_coalesces_and_handles_connected_and_pairing`) into focused single-behavior tests or parameterized cases so an early assertion failure never hides sibling behaviors. Atomic domain terms (such as `search_and_replace`) remain valid.

## 4. Mode B Audit and Hardening Checklist

When `/tdd` is invoked in **Mode B** on existing tests, a branch, or `code-review` Axis 3 findings:
1. **Inventory test defects** against [seams-and-mocking](seams-and-mocking.md) (global timer monkeypatching, fixed sleeps/silent loops, missing teardown, internal collaborator mocks) and Sections 1-3 above (tautological constant imports, missing `[min-1, min, max, max+1]` boundary points, vague or `_and_` names).
2. **Gate signature changes**: Pause at `## Your call` before adding an injected timing/clock parameter or changing any production signature; rewrite test-only fixes directly.
3. **Harden and verify sensitivity**: Apply fixes one seam at a time, confirm each rewritten test fails when its target invariant or boundary is violated (via temporary/reverted fault check or explicit invalid-input assertion), and verify the full test suite passes green.
