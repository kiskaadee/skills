---
name: tdd
description: >-
  Guides test-driven development through public interface seams using red-green
  vertical slices, boundary-only mocking, and non-tautological assertions. Use
  when the user types /tdd, asks for test-first implementation, requests a
  failing reproduction test for a bug, or writes unit and integration tests. Do
  not use for trivial fixes, styling, copy, declarative configuration, or
  routine edits where test-first was not requested.
---

# Test-Driven Development

## Use when
- `/tdd`, or explicit requests for test-first implementation, red-green loops, or bug reproduction tests.
- Authoring or refactoring unit and integration tests around behavioral contracts.
- Not for trivial two-line fixes, copy, styling, declarative config, or pure wiring: edit directly instead.
- Not for pre-merge diff inspection (`code-review`) or live browser/deployment QA (`verify-slice`).

## Steps
1. **Check applicability.** Confirm the task introduces or changes observable logic at a testable boundary. If the change is trivial (typo, styling, static config, pure wiring) and `/tdd` was not explicitly requested, skip this skill and apply the change directly. Read project domain docs (`GLOSSARY.md` or local ADRs) if present so test and interface names match domain terms.
2. **Establish the public seam.** Identify the public interface where callers observe behavior without reaching into internals (see [seams-and-mocking](references/seams-and-mocking.md)). If the seam already exists and is unambiguous (such as adding a regression test to an established endpoint or function), proceed directly. Pause to confirm with the human owner only when introducing a new public interface, choosing between multiple candidate seams, or introducing test doubles.
3. **Write one failing tracer bullet (Red).** Write a focused test at the agreed seam describing *what* capability or invariant holds, not *how* internals work (see [test-quality](references/test-quality.md)). Derive expected values from an independent source of truth (known literals, worked domain examples, specification rules), never by mirroring the implementation's formula.
4. **Verify observable failure.** Run the targeted test command and confirm the test fails for the expected behavioral reason, not a syntax, import, or fixture setup error.
5. **Write the minimal implementation (Green).** Write only enough production code to make the failing test pass. Avoid speculative abstractions or untested branches.
6. **Cover negative, conflict, and boundary cases.** Once the happy-path slice passes, run additional red-to-green cycles for material failure modes (invalid inputs, conflict states such as `409`, timeouts, or state reconciliation invariants). Batch independent table-driven cases only after a vertical slice establishes the real contract.
7. **Clean up and hand off.** Remove duplication and clarify names while keeping the suite green, or defer broader structural cleanup to `code-review`.

## Your call
- **New seams and mock boundaries**: approve proposed public seams and any external mocks vs. real lightweight fixtures (such as an in-memory or temporary test database) before test authoring begins on new interfaces.
- **Coverage depth**: decide when edge-case and negative-path slices are sufficient for the risk level of the change.

## Done when
- Every targeted test was observed failing for the expected reason before passing, all tests verify public seams without tautological assertions, and the relevant test suite passes cleanly.

## Hands off to
- `code-review`: to inspect the resulting diff, code smells, defensive invariants, and test seam integrity.
- `verify-slice`: when the slice also needs live runtime, browser DOM, or multi-service verification.
- `diagnose`: when an unexpected test or fixture failure needs root-cause investigation.
- `git-commit`: to commit cohesive vertical slices.
