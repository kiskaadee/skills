# Test Quality and Anti-Patterns

Reference for `tdd`. Keeps red-to-green cycles anchored to observable behavior, independent truth, and real failure semantics.

Derived and adapted from Matt Pocock's `tdd` skill (`github.com/mattpocock/skills`), combined with empirical state-reconciliation and input-safety lessons.

## 1. Four Test Anti-Patterns to Reject

### A. Implementation-Coupled Tests
- **Smell**: Asserting `toHaveBeenCalledWith` on internal helpers, testing private functions, or verifying state through a side channel (raw table query) when a public read interface exists.
- **Tell**: The test breaks during an internal refactor even though caller-observable behavior is unchanged.
- **Fix**: Act through the public write seam and assert through the public read seam or rendered output.

### B. Tautological Assertions
- **Smell**: Recomputing the expected value with the same logic as production code, asserting a constant equals itself, or mocking a boundary to return `X` and only asserting `result == X`.
- **Tell**: A bug in the formula or contract would change both the code and the expected expression identically, keeping the test green.
- **Fix**: Use concrete literals, worked domain examples, or specification tables as an independent source of truth.

```python
# BAD: Recomputes expected value using the same arithmetic
def test_calculate_total():
    items = [Item(price=10), Item(price=5)]
    assert calculate_total(items) == sum(i.price for i in items)

# GOOD: Independent literal from worked example
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
- **Empty and boundary values**: Zero items, maximum capacity limits, missing optional fields, and unauthorized callers.
