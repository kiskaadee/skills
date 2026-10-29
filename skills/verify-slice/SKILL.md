---
name: verify-slice
description: >-
  Runs risk-proportional verification and pull request review across behavioral,
  state, security, ergonomic, and regression perspectives using falsifiable
  assertions. Use when verifying a vertical feature slice, reviewing a pull
  request before merge, or planning QA checks. Not for root-cause debugging;
  use diagnose.
---

# Verify Slice

## Use when
- Verifying a vertical feature slice or pull request before human release review.
- Building or executing risk-proportional QA checks against acceptance criteria.
- Not for investigating an unknown failure from raw symptoms: use `diagnose`.

## Steps
1. **Size checks to risk.** Inspect touched files, boundaries, and failure consequences, then apply the matching minimum check set in [perspectives](references/perspectives.md) (`Lightweight`, `Standard`, or `High-Assurance`) plus only the perspectives warranted by the diff. Proceed directly on routine checks within authorized scope; pause for confirmation only when verification would materially expand scope, incur substantial setup or subagent cost, or introduce a trade-off.
2. **Write falsifiable assertions.** Convert acceptance criteria and selected perspectives into concrete checks with explicit failure conditions (`FAIL if ...`) and required evidence. Never use open-ended observational prompts ("record what happens").
3. **Verify runtime behavior.** Run required behavioral, state, and persistence checks against the live system when the tier requires it, confirming mutations via both UI state and authoritative backend reads. Execute directly by default; use a clean subagent (withholding the diff, PR narrative, and author self-audit) only when independent execution is likely to expose blind spots in stateful workflows or `High-Assurance` changes.
4. **Inspect the diff.** Audit the actual code diff and commit history against the selected code-level perspectives (untrusted data and URL sinks, authoritative state reconciliation, scope containment, and test coverage claims).
5. **Record dispositions honestly.** Score every check as `PASS`, `FAIL`, `BLOCKED`, or `INCONCLUSIVE` with evidence (see [perspectives](references/perspectives.md)). Never rationalize an unexpected result as a design trade-off, treat a missing check as passing, or convert an aggregate score into release approval.
6. **Present the evidence packet.** Group confirmed findings by source (runtime vs. diff), note discrepancies against the implementer's self-audit, surface blocked or unverified areas, and recommend a disposition without waiving failed criteria.

## Your call
- **Expanded verification scope**: approve before spinning up costly test environments, isolated subagents, or checks outside previously authorized boundaries.
- **Handling non-passing checks**: decide whether a `FAIL`, `BLOCKED`, or `INCONCLUSIVE` check triggers a repair loop, an environment fix, a tracked follow-up issue, or an explicit waiver.
- **Release decision**: decide whether to accept residual risks and merge; verification evidence never authorizes release on its own.

## Done when
- Every required check has an evidence-backed state (`PASS`, `FAIL`, `BLOCKED`, or `INCONCLUSIVE`) and the human owner has reviewed the evidence packet to decide release or rework.

## Hands off to
- `diagnose`: when a failed or blocked check needs root-cause investigation.
- `git-commit`: when packaging approved verification or repair changes.
- `document`: when verification uncovers a durable architectural insight or decision.
