# Draft PR Publishing & Contract Drift Marker

Sole owner of the Draft PR body template, rework sync rules, and the fixed-format
`Contract Drift` marker read by `verify`.

---

## 1. Board & Review Publishing Boundaries

- **Card stays in `Work in Progress`**: After opening or syncing a Draft PR,
  `implement` leaves the GitHub Projects v2 card in `Work in Progress`. Never
  move the card to `Review` here; `verify` owns `Work in Progress -> Review`
  when promoting the PR with `gh pr ready` per
  [planning-contract.md](../../projects/references/planning-contract.md).
- **No PR review comments**: `implement` never publishes PR reviews or inline
  review comments. `code-review` is the sole owner of PR review publishing.
- **Checkpoint cleanup**: Immediately after the Draft PR is opened or synced,
  delete `"$state_file"`
  (`$(git rev-parse --git-common-dir)/implement-state/<branch_slug>.txt`) per
  [preflight.md](preflight.md).

---

## 2. Draft PR Open & Rework Sync Rules

1. Push the non-`main` slice branch via `git-manager` (`git push -u origin <branch>`).
2. Check for an existing PR on the current branch (`gh pr view --json number,url,isDraft`).
3. **New Draft PR** (no PR exists yet):
   ```bash
   gh pr create --draft --title "<Conventional PR Title>" --body-file <pr-body.md>
   ```
   - Never open a ready-for-review PR directly from `implement`; always pass
     `--draft`.
4. **Rework Sync** (an open Draft PR already exists):
   - Push the new 1:1 rework commits to the existing branch.
   - Update the Draft PR body with `gh pr edit <pr-number> --body-file <pr-body.md>`
     whenever scope, verification commands, linked issues, or the
     `Contract Drift` status changed.
   - If the rework pass resolved localized findings with no change to scope or
     `Contract Drift`, pushing the commits is sufficient.

---

## 3. Draft PR Body Template

Use this structure when creating or syncing a Draft PR body:

```markdown
Closes #<N>

## Scope Summary
- <Deliverable 1 and key files touched>
- <Deliverable 2 and key files touched>

## Verification
- `<targeted test command>` (exit 0)
- `<lint / typecheck command>` (exit 0)

Contract Drift: none
```

*(Replace `none` with a concise single-line summary when drift occurred.)*

---

## 4. Fixed-Format `Contract Drift` Marker

`verify` parses the Draft PR body during Phase 3 closeout to decide whether to
chain `reconcile-docs` and `projects` after merge.

### Format
```text
Contract Drift: none
```
or
```text
Contract Drift: <concise summary of deviation and affected interfaces or docs>
```

### What Counts as Contract Drift
Record non-`none` drift whenever implementation deviates from any of:
- Target GitHub issue acceptance criteria.
- Public interfaces, CLI flags, API payloads, or data schemas.
- Canonical architecture or planning documents (`ARCHITECTURE.md`, `ROADMAP.md`,
  or active `docs/designs/*.md` specs).

### Rules
- Include exactly one `Contract Drift:` line at the bottom of the PR body.
- Do not invent alternate labels (such as `Drift:` or `Spec Deviations:`).
- Keep the value on the same line (`Contract Drift: none` or
  `Contract Drift: <summary>`) so downstream tooling and `verify` can read it
  unambiguously.
