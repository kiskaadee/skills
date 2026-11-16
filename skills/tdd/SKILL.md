---
name: tdd
description: >-
  Guides test-driven development through public interface seams (Mode A: write-time
  Red-Green vertical slices) and standalone test-suite audit and hardening (Mode B)
  across Python, TypeScript, Bash, Rust, and Java. Use when the user types /tdd,
  asks for test-first implementation or bug reproduction, or requests hardening an
  existing test file, branch, or PR suite. Do not use for trivial fixes, styling,
  copy, declarative configuration, or read-only multi-axis diff review (code-review).
---

# Test-Driven Development

## Use when
- `/tdd` for Mode A (test-first implementation, red-green vertical slices, or failing bug reproduction).
- `/tdd <test-path|branch|PR>` for Mode B (active audit and hardening of existing tests against [seams-and-mocking](references/seams-and-mocking.md) and [test-quality](references/test-quality.md)).
- Not for trivial two-line fixes, copy, styling, declarative config, or pure wiring: edit directly instead.
- Not for read-only pre-merge multi-axis diff inspection (`code-review`) or live runtime/browser QA (`verify-slice`).

## Steps
1. **Check applicability and select mode.** Confirm the task tests observable logic at a testable boundary (skip and edit directly for trivial config/copy when `/tdd` was not requested). Read project domain docs (`GLOSSARY.md` or local ADRs) if present. Select **Mode A** when adding new behavior, reproducing a bug, or writing a new test; select **Mode B** when asked to audit/harden existing tests or fix `code-review` Axis 3 findings, and follow the Mode B checklist in [test-quality](references/test-quality.md).
2. **Establish the public seam.** Identify the public interface where callers observe behavior without reaching into internals (see [seams-and-mocking](references/seams-and-mocking.md)). If the seam already exists and is unambiguous, proceed directly. Pause to confirm with the human owner when introducing a new public interface, changing a production signature, or introducing test doubles.
3. **Write one failing tracer bullet (Red).** Write a focused test at the agreed seam describing *what* capability or invariant holds, not *how* internals work (see [test-quality](references/test-quality.md)). Derive expected values from independent spec literals, never by importing production value constants or mirroring implementation logic.
4. **Verify observable failure.** Run the targeted test command and confirm the test fails for the expected behavioral reason, not a syntax, import, or fixture setup error.
5. **Write the minimal implementation (Green).** Write only enough production code to make the failing test pass. Avoid speculative abstractions or untested branches.
6. **Cover negative, conflict, and boundary cases.** Once the happy-path slice passes, run red-to-green cycles for material failure modes, two-sided/one-sided boundary edges, and deterministic async/teardown behavior per [test-quality](references/test-quality.md).
7. **Clean up and hand off.** Remove duplication and clarify test names while keeping the suite green.

## Your call
- **New seams, signatures, and mock boundaries**: approve proposed public seams, external doubles vs. real lightweight fixtures, and any Mode B production signature widening (such as adding an injected timing/clock callable) before editing production interfaces.
- **Coverage depth**: decide when edge-case and negative-path slices are sufficient for the risk level of the change.

## Done when
- **Mode A**: Every targeted test was observed failing for the expected reason before passing, all tests verify public seams without tautologies, and the suite passes cleanly.
- **Mode B**: Every rewritten/hardened test is verified sensitive to its target invariant (observed failing under fault/boundary check before passing green) and the suite passes cleanly.

## Hands off to
- `code-review`: to inspect the resulting diff, smells, invariants, and Axis 3 test integrity (`Suggested Next Step: /code-review <base>..HEAD`).
- `verify-slice`: when the slice also needs live runtime, browser DOM, or multi-service verification (`Suggested Next Step: /verify-slice`).
- `diagnose`: when an unexpected test or fixture failure needs root-cause investigation (`Suggested Next Step: /diagnose <failing-test>`).
- `git-manager`: for branch isolation or committing cohesive vertical slices.
- Emit one outcome-matched `Suggested Next Step` on standalone turns; suppress when delegated (per [skeleton](../build-skill/references/skeleton.md)).
