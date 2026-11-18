# Finding Schema and Review Output

Reference for `code-review`. Defines the required structure for reporting findings, ensuring every note is actionable, evidence-backed, and auditable.

Derived and adapted from Matt Pocock's review principles (github.com/mattpocock/skills), combining side-by-side axis reporting with strict defect provenance and disposition contracts.

## 1. Finding Record Schema

Every reported finding must populate all seven fields:

| Field | Description | Allowed Values / Format |
| :--- | :--- | :--- |
| **ID** | Stable identifier within this review. | `CR-01`, `CR-02`, etc. |
| **Axis** | The review axis that uncovered the finding. | `Spec & Scope`, `Standards & Smells`, `Seam & Test Integrity`, `Defensive Invariants`. |
| **Severity** | Potential failure consequence if the defect occurs. Describes impact, not reviewer confidence. | `Critical` (system security breach, data loss, fatal crash), `High` (broken invariant, missing spec requirement), `Medium` (code smell, fragile logic, missing edge test), `Low` (minor style inconsistency, naming). |
| **Evidence** | Exact location, change category, and reproducible behavior. | Distinguishes whether the code is committed, staged, or unstaged: e.g. `src/view.ts:L45 (unstaged)` with excerpt. |
| **Invariant** | The requirement, contract, or system property violated. | Clear statement of expectation (e.g., "Untrusted DOM values must be escaped before interpolation"). |
| **Impact** | Concrete failure consequence if left unaddressed. | What breaks in production, concurrency, or maintenance (e.g., "Stored XSS when name contains `<script>`"). |
| **Disposition** | Current evidentiary status of the finding. | `Confirmed` (proven defect backed by evidence), `Rejected` (disproven or false positive), `Unresolved` (open disagreement or missing evidence), `Accepted Trade-off` (conscious compromise approved by owner). |

## 2. Disposition, Severity, and the 3 Triage Exits

1. **No agent self-assigned `Accepted Trade-off`**: On a review pass, every valid finding (even `Low` severity) must be logged as `Confirmed` (or `Unresolved`). Only the human owner may assign `Accepted Trade-off`.
2. **Verdict gating (`Needs Rework` vs. `Pending Triage` vs. `Ready`)**:
   - `Confirmed Critical` or `Confirmed High` -> `Needs Rework`.
   - `Unresolved Critical` or `Unresolved High` -> `Blocked`.
   - Only `Confirmed` or `Unresolved` `Medium`/`Low` findings remain -> `Pending Triage` (never recommend merging while findings are untriaged).
   - Zero untriaged findings remain -> `Ready`.
3. **Three Mandatory Exits for `Pending Triage` Findings (No Silent Tech-Debt in Closed PRs)**:
   Because future coding agents do not read closed PR comments, an unresolved problem cannot simply be left as a closed PR comment and forgotten. Prompt the human owner to choose one exit per finding before merge:
   - **Exit A (`fix-in-branch`)**: Fix the finding on the PR branch now (`/tdd` or `/git-manager`) and re-verify.
   - **Exit B (`live-tracker`)**: Defer the work by recording it in a live tracker that future agents read before starting the next slice: append to an upcoming Gitea issue (`gt issue edit <next>`), create a follow-up Gitea issue (`gt issue create` / `gitea-plan`), or add to `todo.txt` (`tuxedo add "(B) ..."`), and link that tracker ID on the PR.
   - **Exit C (`record` / `Accepted Trade-off`, human-only)**: The human owner explicitly decides no future code change is desired and permanently accepts the trade-off as-is.
4. **Severity vs. confidence**: `Severity` describes potential impact, never reviewer confidence. A suspected high-impact flaw with incomplete evidence must be logged as `High` severity with `Unresolved` disposition, not downgraded to `Low`.

## 3. Review Report Layout

The final review summary presented to the user must follow this structure:

```markdown
# Code Review Summary: <branch or commit range>

## Overview & Scope State
- **Base Commit**: `<base-ref>` (`<base-commit-sha>`) -> `<HEAD>` (`<head-commit-sha>`)
- **Covered Working-Tree State**: `Clean` | Staged, unstaged, and relevant untracked summary plus content fingerprint (covering staged changes, unstaged changes, and relevant untracked file contents so downstream tools can verify zero state drift)
- **Assigned Risk Tier**: `Lightweight` | `Standard` | `High-Assurance`
- **Execution Mode**: `Sequential` (`Lightweight` only) | `Independent Passes` (`Standard`) | `Subagent Reviewers` (`High-Assurance` mandatory: Axes 1/2/4 subagent `<id>`, Dedicated Axis 3 Tests subagent `<id>`)

## Findings Ledger

### Confirmed Findings (Needs Rework)
| ID | Axis | Severity | State | Location | Invariant Violated | Impact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CR-01 | Defensive Invariants | Critical | Committed | `src/view.ts:L45` | Unescaped dynamic HTML sink | DOM XSS via attendee name |

### Unresolved Disagreements / Material Risks (Blocked if Critical/High)
| ID | Axis | Severity | Location | Competing Perspectives / Open Risk | Decision Needed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CR-02 | Standards & Smells | Medium | `src/api.ts:L110` | Reviewer A flags Primitive Obsession; Author notes single call site. | Accept string or introduce domain type |

### Accepted Trade-offs & Rejected Findings (Audit Traceability)
| ID | Axis | Disposition | Location | Rationale / Decision |
| :--- | :--- | :--- | :--- | :--- |
| CR-03 | Spec & Scope | Rejected | `src/main.ts:L12` | Suspected scope creep confirmed as required wiring for acceptance criterion 2. |
| CR-04 | Standards & Smells | Accepted Trade-off | `scripts/seed.py:L10` | Inlined script logic accepted to keep utility independent of core module. |

## Axis Breakdown
- **Spec & Scope**: Pass/Fail summary. Notes on scope containment and shared entrypoints across working-tree and commits.
- **Standards & Smells**: Adherence to repo conventions and Fowler smell diagnostics.
- **Seam & Test Integrity**: Evaluation of test boundaries, tautological assertions, and vertical slice evidence.
- **Defensive Invariants**: Status of trust boundaries, authority, consistency, failure semantics, and resource limits.

## Executable Runtime Checks for verify-slice
Every candidate runtime check must be directly consumable by `verify-slice` without reinterpreting narrative prose. Commands must assume execution from the repository root and use repository-relative paths (if an external path or environment dependency is genuinely required, declare that dependency and scope explicitly). Each entry requires:
- **Purpose** in the check header (`Check RV-XX: <purpose>`).
- **Scope**: `local` (safe workstation or isolated fixture execution) or `live-infra` (touches privileged permissions, host state, or external/production infrastructure; executable when the human owner explicitly authorizes the target environment and operation, otherwise recorded by `verify-slice` as `BLOCKED (out-of-bounds)`).
- **Pass Condition**: explicit observable output or state transition.
- **Failure Signal**: explicit contradiction condition.
- **Command**: copy-pasteable fenced shell block.

### Check RV-01: Out-of-band conflict handling on concurrent submission
- **Scope**: `local`
- **Pass Condition**: First request returns HTTP `200`; concurrent duplicate returns HTTP `409` with JSON code `conflict` and persisted count increments by `1`.
- **Failure Signal**: Duplicate returns `200` or `500`, unhandled traceback, or persisted count increments by `2`.
```sh
./scripts/test-concurrency-check.sh --endpoint /api/check-in
```

### Check RV-02: Privileged service reload and health verification
- **Scope**: `live-infra`
- **Pass Condition**: Target service reloads cleanly and health endpoint returns `200 OK`.
- **Failure Signal**: Non-zero exit status, permission refusal, or failed unit healthcheck.
```sh
systemctl reload app-daemon.service && systemctl is-active --quiet app-daemon.service
```

## Overall Recommendation
- **Status**: `Ready` | `Pending Triage` | `Needs Rework` | `Blocked`
- **Next Action**: When `Pending Triage` or `Needs Rework`, do not recommend merging; prompt the human owner to select Exit A (`fix-in-branch`), Exit B (`live-tracker`: Gitea issue or `todo.txt`), or Exit C (permanent `Accepted Trade-off`) for each finding. Static provenance and runtime verification remain distinct inputs; neither authorizes release on its own.
- **Suggested Next Step**: `/<skill> <args>` (emit one concrete command matched to the recommendation on standalone turns; omit when running inside a delegated subagent).
```

## 4. PR Review Block (Drafted and Auto-Published Here on Standalone Open PRs)

`code-review` is strictly read-only regarding the codebase (never modifies repository files, commits, or Gitea project boards), and automatically publishes a comment-only PR review in the same turn when invoked standalone on an open pull request. When running as a delegated subagent inside `implement-slice`, skip PR posting and return the compact report to the orchestrator.

### What goes in
- Every finding except `Rejected` ones (those stay in the local ledger only).
- Zero eligible findings on a `Ready` review: still draft and auto-publish `review-body.md` using the compact 4-axis pass template below (and omit `inline-comments.json`) so every reviewed PR head has an immutable, commit-pinned review record on Gitea.

### Per-finding routing (proposed here, decided by the owner before merge)
| Field | Values | Rule |
| :--- | :--- | :--- |
| **Placement** | `inline` or `body` | `inline` only when the location is a committed line inside a diff hunk at the reviewed head SHA. Unstaged, staged, file-level, or cross-cutting findings go in `body`. |
| **Follow-up** | `fix-in-branch`, `live-tracker`, or `record` | Proposed triage exit: `fix-in-branch` (quick fix on PR branch), `live-tracker` (defer to Gitea issue or `todo.txt` via `tuxedo add` before merge), or `record` (only after owner grants permanent `Accepted Trade-off`). A closed PR comment is never a task tracker. |

### Identity across re-reviews
Finding IDs (`CR-01`) are only unique within one review. The block header names the reviewed head SHA, and any cross-review reference uses `<short-sha>/CR-01`. `gitea-pr` uses the header SHA to avoid posting the same review twice.

### Files
Write both files to an untracked scratch location (never inside the repository tree):

`review-body.md`:
```markdown
**Code review @ `<short-head-sha>`** (`<base-ref>`..`<head-ref>`): `<Ready | Pending Triage | Needs Rework | Blocked>`

Covered state: `<Clean | fingerprint>`. Tier: `<tier>`. Static provenance only; merge authority stays with the owner.

| ID | Axis | Severity | Disposition | Placement | Proposed Exit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CR-01 | Standards & Smells | Low | Confirmed | inline | fix-in-branch (or live-tracker) |

### Body-placed findings
- **CR-02** (`<location>`): <invariant, impact, and suggested change>.
```

`review-body.md` (clean `Ready` review with zero non-rejected findings; omit `inline-comments.json`):
```markdown
**Code review @ `<short-head-sha>`** (`<base-ref>`..`<head-ref>`): `Ready`

Covered state: `<Clean | fingerprint>`. Tier: `<tier>`. Static provenance only; merge authority stays with the owner.

| Axis | Disposition |
| :--- | :--- |
| Spec & Scope | Pass |
| Standards & Smells | Pass |
| Seam & Test Integrity | Pass |
| Defensive Invariants | Pass |

No non-rejected findings.
```

`inline-comments.json` (the `gt pr review --comments-file` format; `new_position` is the line number in the new version of the file and must fall inside a diff hunk):
```json
[
  {
    "path": "src/pkg/config.py",
    "new_position": 40,
    "body": "**CR-01** (Low, Accepted Trade-off, record): <invariant and impact>. <Suggested change>."
  }
]
```

Every inline entry also appears in the body table, so the record stays complete if inline placement is rejected and the entry moves to the body.

### Auto-Publishing via `gt pr review` (Standalone Open PR Runs)
When invoked standalone on an open PR, verify guards and publish one comment-only review pinned to the reviewed commit in the same turn:

```bash
# 1. Staleness: the PR head must equal the reviewed head SHA. Mismatch: stop, re-run code-review.
gt pr view <number> --json head_sha -q .head_sha

# 2. Duplicates and pending state: stop if any review is PENDING (posting would publish its
#    inline comments too) or if a review already exists for the reviewed SHA from this block.
gt pr review list <number> --json id,state,commit,body

# 3. Auto-publish one comment-only review, pinned to the reviewed commit.
gt pr review <number> --comment --commit <reviewed-head-sha> \
  -F review-body.md --comments-file inline-comments.json --json id,url

# Body-only block (no inline entries): omit --comments-file.
```

- Never pass `--approve` or `--request-changes`: the verdict in the body is informational, and merge authority stays with the owner (Gitea also refuses approval on your own PR).
- Never pass `--yes`: it exists to publish a pending review, which step 2 already rules out.
- If Gitea rejects an inline entry (line outside a diff hunk), confirm with step 2 that no review was created, move that entry into the body, and retry once.
- Record the returned review `id` and `url`. Later fixes use `gt pr review reply` with `Fixed in <sha>` and `gt pr review resolve` via `gitea-pr`.
