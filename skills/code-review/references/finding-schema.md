# Finding Schema and GitHub PR Review Output

Reference for `code-review`. Sole owner of the `CR-XX` finding lifecycle, the `build_review.py` payload contract, and GitHub PR review publishing.

Derived and adapted from Matt Pocock's review principles (github.com/mattpocock/skills), combining side-by-side axis reporting with strict defect provenance and disposition contracts.

## 1. Finding Record Schema

Every reported finding must populate all seven fields:

| Field | Description | Allowed Values / Format |
| :--- | :--- | :--- |
| **ID** | Monotonic per-PR identifier across all review passes. | `CR-01`..`CR-99`, `CR-100`, etc. (assigned deterministically by `build_review.py`). |
| **Axis** | The review axis that uncovered the finding. | `Spec & Scope`, `Standards & Smells`, `Seam & Test Integrity`, `Defensive Invariants`. |
| **Severity** | Potential failure consequence if the defect occurs. Describes impact, not reviewer confidence. | `Critical` (security breach, data loss, fatal crash), `High` (broken invariant, missing spec requirement), `Medium` (code smell, fragile logic, missing edge test), `Low` (minor style, docstring, or naming issue). |
| **Evidence** | Exact location, change category, and reproducible behavior. | Distinguishes committed, staged, or unstaged state: e.g. `src/view.ts:L45 (committed)` with excerpt. |
| **Invariant** | The requirement, contract, or system property violated. | Clear statement of expectation (e.g., "Untrusted DOM values must be escaped before interpolation"). |
| **Impact** | Concrete failure consequence if left unaddressed. | What breaks in production, concurrency, or maintenance (e.g., "Stored XSS when name contains `<script>`"). |
| **Disposition** | Current evidentiary status of the finding. | `Pending Triage` / `Confirmed` (proven defect backed by evidence), `Unresolved` (open disagreement or missing evidence), `Dismissed` (invalid or false positive, Exit C). |

## 2. Disposition, Severity, and the 3 Triage Exits

1. **Every valid finding starts in `Pending Triage`**: On a review pass, every valid finding (even `Low` severity) must be logged as `Confirmed` (or `Unresolved`) in `Pending Triage`. Never silently waive findings or self-dismiss defects.
2. **Verdict gating (`Needs Rework` vs. `Blocked` vs. `Pending Triage` vs. `Ready`)**:
   - `Confirmed Critical` or `Confirmed High` -> `Needs Rework` (`verdict=needs_rework`).
   - `Unresolved Critical` or `Unresolved High` -> `Blocked` (`verdict=needs_rework`).
   - Only `Confirmed` or `Unresolved` `Medium`/`Low` findings remain -> `Pending Triage` (`verdict=needs_rework`; never promote or merge while untriaged findings remain).
   - Zero unresolved `Pending Triage` findings remain -> `Ready` (`verdict=ready`).
3. **Three Mandatory Exits for `Pending Triage` Findings (No Silent Tech-Debt in Closed PRs)**:
   Because future coding agents do not read closed PR comments, an unresolved finding cannot be left behind in a closed PR thread. Prompt the human owner to choose one exit per finding before `Ready`:
   - **Exit A (`fix-in-branch`)**: Fix the finding on the PR branch (`implement` fast path for `<= 2`-file localized fixes, `implement` Step 1 for complex rework, or `tdd` + `git-manager`) and re-run `code-review`.
   - **Exit B (`github-issue`)**: Promote the finding to a GitHub Issue (`gh issue create` or `projects`), optionally paired with `TODO(#<N>): ...` or a `Why:` comment + ADR link in `docs/decisions/`. Record `Promoted to #<N>` in the superseding `Ready` review body's `triage_closures[]` summary.
   - **Exit C (`dismiss`)**: Dismiss the finding as invalid or a false positive. Record `Dismissed: <reason>` in the superseding `Ready` review body's `triage_closures[]` summary.
4. **Severity vs. confidence**: `Severity` describes potential impact, never reviewer confidence. A suspected high-impact flaw with incomplete evidence must be logged as `High` severity with `Unresolved` disposition, not downgraded to `Low`.

## 3. Review Report Layout

The review summary presented to the user must follow this structure:

```markdown
# Code Review Summary: <branch or commit range>

## Overview & Scope State
- **Base Commit**: `<base-ref>` (`<base-commit-sha>`) -> `<HEAD>` (`<head-commit-sha>`)
- **Covered Working-Tree State**: `Clean` | Staged, unstaged, and relevant untracked summary plus content fingerprint
- **Assigned Risk Tier**: `Lightweight` | `Standard` | `High-Assurance`
- **Execution Mode**: `Sequential` (`Lightweight` only) | `Independent Passes` (`Standard`) | `Subagent Reviewers` (`High-Assurance` mandatory: Axes 1/2/4 subagent `<id>`, Dedicated Axis 3 Tests subagent `<id>`)

## Findings Ledger

### Confirmed Findings (Pending Triage / Needs Rework)
| ID | Axis | Severity | State | Location | Invariant Violated | Impact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CR-01 | Defensive Invariants | Critical | Committed | `src/view.ts:L45` | Unescaped dynamic HTML sink | DOM XSS via attendee name |

### Unresolved Disagreements / Material Risks (Blocked if Critical/High)
| ID | Axis | Severity | Location | Competing Perspectives / Open Risk | Decision Needed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CR-02 | Standards & Smells | Medium | `src/api.ts:L110` | Reviewer A flags Primitive Obsession; Author notes single call site. | Fix in-branch, promote to GitHub Issue, or dismiss |

### Triage Closures (Exit B / Exit C Audit Trail)
| ID | Exit | Resolution |
| :--- | :--- | :--- |
| CR-03 | Exit B | Promoted to #45 |
| CR-04 | Exit C | Dismissed: false positive on test fixture |

## Axis Breakdown
- **Spec & Scope**: Pass/Fail summary, scope containment, shared entrypoints, and affected local markdown.
- **Standards & Smells**: Repo conventions, docstrings on new/modified public symbols, inline comment accuracy, lint/format hygiene, and Fowler smell diagnostics.
- **Seam & Test Integrity**: Evaluation of test boundaries, tautological assertions, and vertical slice evidence.
- **Defensive Invariants**: Status of trust boundaries, authority, consistency, failure semantics, and resource limits.

## Executable Runtime Checks for verify
Every candidate runtime check must be directly consumable by `verify` from the published PR review body without reinterpreting narrative prose. Commands assume execution from the repository root with repository-relative paths. Each entry requires:
- **Purpose** in the check header (`Check RV-XX: <purpose>`).
- **Scope**: `local` (safe workstation or isolated fixture execution) or `live-infra` (touches privileged permissions, host state, or external/production infrastructure; requires explicit human owner authorization in `verify`, otherwise recorded as `BLOCKED (out-of-bounds)`).
- **Pass Condition**: explicit observable output or state transition.
- **Failure Signal**: explicit `FAIL if ...` contradiction condition.
- **Command**: copy-pasteable fenced shell block.

### Check RV-01: Out-of-band conflict handling on concurrent submission
- **Scope**: `local`
- **Pass Condition**: First request returns HTTP `200`; concurrent duplicate returns HTTP `409` with JSON code `conflict` and persisted count increments by `1`.
- **Failure Signal**: `FAIL if` duplicate returns `200` or `500`, unhandled traceback occurs, or persisted count increments by `2`.
```sh
./scripts/test-concurrency-check.sh --endpoint /api/check-in
```

## Overall Recommendation
- **Status**: `Ready` | `Pending Triage` | `Needs Rework` | `Blocked`
- **PR Publishing**: Published review URL (or explicit notice: `No open GitHub PR found; findings reported locally.`)
- **Next Action**: Route `Needs Rework` to `implement` (`<= 2`-file fast path or Step 1), `Pending Triage` to owner triage (Exit A / Exit B / Exit C), or `Ready` to `verify`. Static provenance never authorizes release on its own.
- **Suggested Next Step**: `/<skill> <args>` (emit one concrete command matched to the recommendation on standalone turns; omit when running inside a delegated subagent).
```

## 4. GitHub PR Review Publishing via `build_review.py`

`code-review` is strictly read-only regarding the codebase (never modifies repository files, commits, or GitHub Projects v2 boards). Whenever invoked on an open GitHub PR (verified via `gh repo view --json url`), whether standalone or delegated, build the review payload deterministically with `skills/code-review/scripts/build_review.py` and publish one comment-only review pinned to `head_sha`.

If no open PR exists for `HEAD` (or when running in local-only mode), skip PR publishing and explicitly state in the report that no open PR was found and findings are reported locally.

### Input Schema (`--input <findings.json>`)

Write temporary scratch files outside the repository tree (for example under `/tmp/cr-review-$$/`):

```json
{
  "base_ref": "main",
  "head_ref": "feat/example",
  "covered_state": "Clean",
  "tier": "Standard",
  "findings": [
    {
      "path": "src/pkg/config.py",
      "line": 40,
      "side": "RIGHT",
      "severity": "Medium",
      "axis": "Standards & Smells",
      "title": "Missing public docstring",
      "body": "Invariant, impact, and suggested change."
    }
  ],
  "rv_checks": [
    {
      "id": "RV-01",
      "purpose": "Out-of-band conflict handling",
      "scope": "local",
      "pass_condition": "Duplicate returns HTTP 409",
      "fail_signal": "FAIL if duplicate returns 200 or 500",
      "command": "./scripts/test-concurrency-check.sh"
    }
  ],
  "triage_closures": [
    {
      "id": "CR-01",
      "exit": "B",
      "resolution": "Promoted to #45"
    }
  ]
}
```

- `findings[]` is required (may be `[]` on a clean `Ready` pass). Each finding requires non-empty strings `severity`, `title`, and `body`.
- `path`, `line`, and `side` (`"LEFT"` for deleted lines in the diff, `"RIGHT"` for added, modified, or context lines) are validated against `--diff`. Any finding that is cross-file (`path: null`), targets a missing file, or falls outside a diff hunk is automatically moved into `### Findings (Unanchored / Cross-File)` in the review `body` to prevent GitHub `422 Unprocessable Entity` errors.
- `rv_checks[]` (optional) renders inside a collapsible `<details>` block in the review `body` so `verify` can recover all `RV-*` checks in a fresh session.
- `triage_closures[]` (optional) renders a `### Triage Summary` section recording Exit B (`Promoted to #<N>`) and Exit C (`Dismissed: <reason>`) closures on a superseding `Ready` review.

### Monotonic `CR-XX`, Guards, and `cr-review-meta`

`skills/code-review/scripts/build_review.py` parses paginated prior reviews and inline comments outside LLM context:
1. **Pagination flattening**: Consumes `gh api --paginate --slurp` (`[[...]]`) or flat (`[...]`) JSON arrays for both `--reviews` and `--comments`.
2. **Monotonic `max_id`**: Extracts the maximum integer across every `<!-- cr-review-meta: max_id=NN ... -->` marker and `^### CR-(\d+)` heading in prior reviews and inline comments. New findings start at `max_id + 1` (`CR-01`..`CR-99`, `CR-100`).
3. **Duplicate `(head_sha, verdict)` guard**: If a prior review already has the exact same `(head_sha, verdict)`, `build_review.py` exits `2` with no stdout JSON (skip re-posting). A `verdict=ready` review on the same `head_sha` is allowed to supersede an earlier `verdict=needs_rework` review after Exit B/C triage.
4. **3-rework-cycle cap**: Counts prior `cr-review-meta` entries with `verdict=needs_rework`. If 3 or more already exist and `--verdict needs_rework` is requested, `build_review.py` exits `1` with an escalation message on stderr; halt and escalate to the human owner.
5. **Metadata stamp**: Appends `<!-- cr-review-meta: max_id=NN head_sha=<sha> verdict=ready|needs_rework -->` to the emitted review `body`. `verify` reads this marker to confirm `verdict=ready` matches the current PR `head_sha`.

### Publishing Workflow (`gh api`)

```bash
# 1. Verify GitHub repository identity and resolve open PR number + head_sha
gh repo view --json url -q .url
pr_num=$(gh pr view --json number -q .number)
head_sha=$(gh pr view "$pr_num" --json headRefOid -q .headRefOid)
repo=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# 2. Fetch PR diff and paginated review/comment history to scratch files
scratch=$(mktemp -d)
gh pr diff "$pr_num" > "$scratch/pr.diff"
gh api --paginate --slurp "repos/${repo}/pulls/${pr_num}/reviews" > "$scratch/reviews.json"
gh api --paginate --slurp "repos/${repo}/pulls/${pr_num}/comments" > "$scratch/comments.json"

# 3. Build validated GitHub PR review JSON (exits 0=post, 2=duplicate skip, 1=error/3-cycle cap)
if payload=$(python3 skills/code-review/scripts/build_review.py \
  --input "$scratch/findings.json" \
  --diff "$scratch/pr.diff" \
  --reviews "$scratch/reviews.json" \
  --comments "$scratch/comments.json" \
  --head-sha "$head_sha" \
  --verdict "$verdict"); then
  printf '%s\n' "$payload" | gh api "repos/${repo}/pulls/${pr_num}/reviews" --input - --jq '{id, html_url}'
else
  rc=$?
  # rc == 2: duplicate (head_sha, verdict) already published; skip cleanly
  # rc == 1: invalid input or 3-rework-cycle cap reached; escalate to human owner
fi
rm -rf "$scratch"
```

- `build_review.py` always emits `"event": "COMMENT"` pinned to `"commit_id": "<head_sha>"`. Never emit `APPROVE` or `REQUEST_CHANGES`: merge authority stays with the human owner.
- Record the returned review `id` and `html_url` in the final review summary.
