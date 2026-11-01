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
1. **Size checks to risk and evaluate review handshake.** Inspect touched files, boundaries, and failure consequences, then apply the matching minimum check set in [perspectives](references/perspectives.md) (`Lightweight`, `Standard`, or `High-Assurance`) plus only the perspectives warranted by the diff. Reuse a preceding `code-review` report for static provenance only when its status is `Ready` (completed across all four axes, no unresolved blocking findings remain, and covered scope is identified), the reviewed base and head revisions match, and the current relevant working-tree diff is unchanged from the reviewed diff. Proceed directly on routine checks within authorized scope; pause for confirmation only when verification would materially expand scope, require `live-infra` authorization, incur substantial setup or subagent cost, or introduce a trade-off.
2. **Write falsifiable assertions.** Convert acceptance criteria, `code-review` Step 6 fenced checks (when present), and selected perspectives into concrete checks with explicit failure conditions (`FAIL if ...`), scope classification (`local` vs. `live-infra`), and required evidence. Never use open-ended observational prompts ("record what happens").
3. **Verify runtime behavior.** Execute `local` behavioral, state, and persistence checks against the live system when the tier requires it, confirming mutations via both UI state and authoritative backend reads. Execute `live-infra` checks only when the human owner has explicitly authorized the target environment and operation; otherwise record `BLOCKED (out-of-bounds)` with the preserved command and criteria. Execute directly by default; use a clean subagent (withholding the diff, PR narrative, and author self-audit) only when independent execution is likely to expose blind spots in stateful workflows or `High-Assurance` changes.
4. **Inspect the diff (unless handshake invariant holds).** When Step 1 verified a reusable `Ready` review on the exact unchanged diff, bypass static diff re-inspection and cite that review as static provenance (runtime verification provides behavioral evidence and never substitutes for static review). Otherwise (standalone run, non-`Ready` review, revision mismatch, or changed working-tree diff), audit the changed delta or full diff against the selected code-level perspectives (untrusted data and URL sinks, authoritative state reconciliation, scope containment, and test coverage claims).
5. **Record dispositions honestly.** Score every check as `PASS`, `FAIL`, `BLOCKED` (`env/fixture` vs. `out-of-bounds`), or `INCONCLUSIVE` with evidence (see [perspectives](references/perspectives.md)). Never rationalize an unexpected result as a design trade-off, treat a missing or `BLOCKED` check as passing, or treat either static provenance or runtime evidence as release approval.
6. **Present the evidence packet.** Distinguish static provenance (`diff` audit vs. `code-review` handshake) from runtime evidence, note discrepancies against the implementer's self-audit, separate `BLOCKED (env/fixture)` repairs from `BLOCKED (out-of-bounds)` operator checks, and recommend a disposition without waiving failed criteria.

## Your call
- **Expanded verification scope and `live-infra` authorization**: approve before running `live-infra` operations against privileged or external environments, spinning up costly test setups, or launching isolated subagents outside previously authorized boundaries.
- **Handling non-passing checks**: decide whether a `FAIL`, `BLOCKED`, or `INCONCLUSIVE` check triggers a repair loop, an environment fix, an authorized operator window, a tracked follow-up issue, or an explicit waiver.
- **Release decision**: decide whether to accept residual risks and merge; neither static review nor runtime verification authorizes release on its own.

## Done when
- Every required check has an evidence-backed disposition (`PASS`, `FAIL`, `BLOCKED (env/fixture)`, `BLOCKED (out-of-bounds)`, or `INCONCLUSIVE`), static provenance and runtime evidence are clearly distinguished, and the human owner has reviewed the packet to decide release or rework.

## Hands off to
- `diagnose`: when a failed or blocked check needs root-cause investigation.
- `git-manager`: when committing verified repair changes or managing test branches.
- `document`: when verification uncovers a durable architectural insight or decision.
