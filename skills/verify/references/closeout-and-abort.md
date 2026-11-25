# Verification Ledger, Promotion, Closeout, and Abort

Reference for `verify` Phase 2 (Promotion), Phase 3 (Human Merge Gate and
Closeout), human rejection rollback, and explicit Draft PR abort.

> **Zero `todo.txt` responsibility**: `verify` never reads, edits, or deletes
> `todo.txt` or `implement-state` checkpoint files. `implement` solely owns
> checkpoint lifecycle and cleanup.

---

## 1. Verification Ledger Comment Template (Phase 2)

Post one Verification Ledger comment on the PR only after Phase 1 passes
(verified `cr-review-meta` `head_sha` + `verdict=ready`, zero `FAIL`, zero
unresolved `BLOCKED (env/fixture)` or `INCONCLUSIVE`, and green CI):

```bash
gh pr comment <pr-number> --body-file <verification-ledger.md>
```

### Ledger Template
```markdown
## Verification Ledger

- **Reviewed Head SHA**: `<head_sha>`
- **Static Provenance**: `code-review` (`verdict=ready`)
- **Rigor Tier**: `<Lightweight | Standard | High-Assurance>`
- **Remote CI (`gh pr checks`)**: `PASS`
- **Contract Drift**: `<none | summary from PR body>`

### Runtime QA Dispositions

| Check ID | Scope | Disposition | Evidence |
| :--- | :--- | :--- | :--- |
| `RV-01` | `local` | `PASS` | `<command / observable proof>` |
| `RV-02` | `live-infra` | `BLOCKED (out-of-bounds)` | `<preserved command & criteria>` |

### Notes / Operator Follow-ups
- `<None, or list any BLOCKED (out-of-bounds) checks awaiting operator window>`
```

---

## 2. Phase 2: Draft PR Promotion (`Work in Progress -> Review`)

1. Confirm the Verification Ledger comment is posted on `<pr-number>`.
2. Promote the Draft PR to ready-for-review:
   ```bash
   gh pr ready <pr-number>
   ```
3. Move the linked issue card `Work in Progress -> Review` using the
   `issue.projectItems` single-query resolution and `SINGLE_SELECT` mutation in
   [github-projects-v2.md](../../projects/references/github-projects-v2.md)
   (Section 4). Confirm the transition ownership matches
   [planning-contract.md](../../projects/references/planning-contract.md).

---

## 3. Phase 3: Human Merge Gate and Post-Merge Closeout

Present the verification packet to the human owner (static provenance, runtime
dispositions, CI status, any `BLOCKED (out-of-bounds)` operator items, and the
PR body's `Contract Drift` value per
[pr-and-drift.md](../../implement/references/pr-and-drift.md)) and wait for
explicit merge authorization.

### 3a. On Human Approval (Merge + `Review -> Completed`)
1. Merge the pull request using the repository's configured merge strategy (for
   example, squash merge):
   ```bash
   gh pr merge <pr-number> --squash --delete-branch
   ```
2. Move the linked issue card `Review -> Completed` directly via
   `issue.projectItems` per
   [github-projects-v2.md](../../projects/references/github-projects-v2.md)
   (Section 4):
   - Query `issue.projectItems(first: 20)` filtered by
     `project.number == $project_number` (from `AGENTS.md`).
   - Resolve `project_id`, `item_id` (`PVTI_...`), `status_field_id`
     (`PVTSSF_...`), and the `Completed` `option_id`.
   - Execute `updateProjectV2ItemFieldValue` with
     `value: { singleSelectOptionId: $completed_option_id }`.
3. **Partial-failure idempotency**: If the PR merge succeeds but the Projects v2
   mutation fails (network/API error), report the partial state clearly.
   Re-running `verify` Phase 3 board closeout or `projects` reconciliation
   safely moves the stranded card `Review -> Completed` without re-merging.
4. **Contract Drift chaining**: Read the fixed-format `Contract Drift:` line
   from the PR body per
   [pr-and-drift.md](../../implement/references/pr-and-drift.md):
   - If `Contract Drift: none`: closeout is complete; recommend next ready slice
     via `projects` or `implement` if applicable.
   - If `Contract Drift` != `none`: chain `reconcile-docs` first to update
     canonical docs (`ARCHITECTURE.md`, `ROADMAP.md`, `docs/designs/*.md`),
     followed by `projects` to align downstream issues and milestones.

### 3b. On Human Rejection Rollback (`Review -> Work in Progress`)
If the human owner rejects the merge or requests rework:
1. Convert the PR back to Draft:
   ```bash
   gh pr ready --undo <pr-number>
   ```
2. Move the linked issue card `Review -> Work in Progress` via
   `issue.projectItems` per
   [github-projects-v2.md](../../projects/references/github-projects-v2.md)
   (Section 4).
3. Record the human owner's requested changes and route back to `implement`
   (or `code-review` if only review triage is needed).

---

## 4. Abandoned / Superseded Draft PR Abort Path

> **Explicit invocation only**: Enter this path ONLY when the user explicitly
> asks to abort or close an abandoned/superseded Draft PR. Never trigger this
> path automatically from a failed Phase 1 check or Phase 3 rejection.

1. Verify GitHub repository identity via `gh repo view --json url` and confirm
   the target PR is an open Draft PR (`gh pr view <pr-number> --json state,isDraft,url`).
2. Confirm explicit user approval stating the PR to close and the linked issue
   card that will revert to `Backlog`.
3. Close the Draft PR with an explicit reason comment:
   ```bash
   gh pr close <pr-number> --comment "Closing abandoned/superseded Draft PR: <reason>"
   ```
4. Move the linked issue card back to `Backlog` via `issue.projectItems` per
   [github-projects-v2.md](../../projects/references/github-projects-v2.md)
   (Section 4).
5. Do not touch `todo.txt` or `implement-state` files; if an orphaned branch
   checkpoint exists locally, `implement` owns its cleanup.
