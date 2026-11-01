# Handoff Contracts, Failure Triage, and Final-HEAD Invariant

Reference for `implement-slice`. Every delegation uses explicit, bounded schemas so subagents execute deterministically and return compact evidence packets.

## 1. Implementation Assignment (Orchestrator -> Worker)

Provide before spawning (or messaging) an implementation worker:

- **Session Mode & Anti-Recursion**: Active mode (`mode: delivery`) plus explicit instruction: execute this task directly using `tdd` and `git-manager`; do not invoke `implement-slice` or spawn nested workers unless explicitly authorized.
- **Task ID & Objective**: Concrete deliverable outcome and linked Gitea issue (`#<id>` when applicable).
- **Assigned Workspace & Branch**: Exact repository/worktree path and non-default working branch name.
- **Scope Boundary**: In-scope files/interfaces and explicit out-of-scope exclusions (preventing opportunistic refactors).
- **Acceptance Criteria**: Numbered, falsifiable conditions this task must satisfy.
- **Checkpoint Expectation**: Expected coherent commit boundary (or boundaries) following `git-manager` Conventional Commits.
- **Required Compact Report**: Request concise structured output (no raw multi-hundred-line logs unless a check fails).

## 2. Implementation Report (Worker -> Orchestrator)

Require each worker to return:

- **Summary of Changes**: Touched files/seams and 2-5 bullet summary of what changed.
- **Criteria Coverage**: Mapping from assigned acceptance criteria to test or command proof.
- **Verification Summary**: Commands run (`pytest`, `cargo test`, typecheck, lint) with exit codes and pass counts.
- **Checkpoint Commits**: Exact commit SHA(s) and subject lines created, plus confirmation that `git status --short` is clean.
- **Scope Deviations or Open Risks**: Any unexpected constraint, untouched edge case, or blocker encountered (`None` if clean).

---

## 3. Pre-Committed QA Rubric Assignment (Orchestrator -> QA Subagent)

The rubric is written and approved during Step 3 (before implementation begins). When spawning the QA subagent:

- **Target Revision & Workspace**: Exact commit SHA (`HEAD`), base ref, and workspace path. State clearly: do not modify tracked files; leave `git status --short` clean.
- **Assurance Tier & Mode**: `Lightweight`, `Standard`, or `High-Assurance` per `verify-slice`. For `High-Assurance` black-box runs, withhold the diff narrative and worker self-audit.
- **Pre-Committed Falsifiable Checks**: Numbered checks with scope (`local` vs. `live-infra`), exact pass conditions, `FAIL if ...` signals, and any `code-review` Step 6 `RV-*` checks.
- **Authorization Boundary**: Explicitly state whether any `live-infra` check has human owner authorization for this run (default: unauthorized -> record `BLOCKED (out-of-bounds)`).

## 4. QA Report (QA Subagent -> Orchestrator)

Follows the `verify-slice` disposition contract:

- **Tested Revision**: Confirmed `HEAD` SHA and clean working-tree verification.
- **Check Dispositions**: Per-criterion result (`PASS`, `FAIL`, `BLOCKED (env/fixture)`, `BLOCKED (out-of-bounds)`, or `INCONCLUSIVE`) with concise observable evidence.
- **Confirmed Defects**: Reproducible failure steps, severity, and expected vs. actual behavior.
- **Rubric Fitness**: Explicit note if any rubric criterion proved ambiguous, untestable, or mismatched against repository reality.

---

## 5. Failure Triage and Rubric Amendment Routing

Never relay "QA failed" blindly. Classify each non-passing outcome and route to the right owner:

| Observed Outcome | Classification | Orchestrator Action |
| :--- | :--- | :--- |
| Behavioral check `FAIL` or `code-review` `Needs Rework` | **Implementation or test defect** | Send targeted actionable feedback (check ID, repro, expected contract) to the existing worker via `send_message` when live. |
| Acceptance criterion lacks public-seam test proof | **Missing seam test** | Route back to the existing worker (`tdd`) to add a non-tautological seam test and commit checkpoint. |
| `BLOCKED (env/fixture)` | **Environment or fixture blocker** | Delegate fixture/devshell repair (`nix-devshell` or worker task) or surface environment blocker to user before judging product code. |
| `BLOCKED (out-of-bounds)` | **Unauthorized `live-infra` boundary** | Preserve exact command and criteria; pause for human owner authorization, operator run, or documented deferral. |
| Symptom contradicts hypotheses across retries | **Unknown root cause** | Stop blind retries; hand off to `diagnose` for evidence-first root-cause investigation. |
| Criterion contradicts actual system architecture or tests the wrong seam | **Defective rubric** | Record an explicit **Rubric Amendment** stating what changed and why. Pause for human approval whenever an amendment relaxes an acceptance criterion or alters slice scope; never silently rewrite criteria to match worker output. |

---

## 6. Final-HEAD Evidence Invariant and Terminal Delivery

### The Invariant

> Before `gitea-pr` creates or marks a PR ready (or before terminal delivery when no PR applies), the required `code-review` and `verify-slice` evidence must identify the same final `HEAD` and applicable base revision. Any change to the reviewed diff invalidates affected evidence.

### Recovery Rules When `HEAD` Advances or Checks Emit

1. **Post-QA commit**: If `HEAD` changes after `verify-slice` (for example, to address a `code-review` finding or rebase onto base), rerun `verify-slice` against the new `HEAD`.
2. **Post-review commit**: If `HEAD` changes after `code-review`, rerun `code-review` against `<base>...HEAD`.
3. **Emitted `RV-*` runtime checks**: If `code-review` Step 6 emits executable `RV-*` checks, execute them via `verify-slice` against the final `HEAD` before packaging.
4. **Handshake reuse condition**: `verify-slice` may reuse a preceding `code-review` report for static provenance only when its recommendation is `Ready` (including `Ready (Conditional)` once open items are adjudicated by the human owner per `code-review`) and its recorded base SHA, `HEAD` SHA, and working-tree diff fingerprint still match exactly.

### Conditional Terminal Paths

- **PR applies**: Once `code-review` (`Ready`) and `verify-slice` (zero unhandled `FAIL`) match final `HEAD`, hand off both packets to `gitea-pr` to draft the PR description, pause for human PR approval, create/update the PR, and report merge readiness.
- **No PR applies** (local repo, approved solo-branch workflow, or bounded spike): Enforce the identical final-`HEAD` evidence invariant, then present the commit range (`<base>..HEAD`), static review disposition, runtime verification ledger, and any open residual-risk decisions directly to the user.
