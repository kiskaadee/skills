# History Editing

Rules for rewriting or combining history. Read before any of these operations.

## Squash
- Do it to collapse noise (checkpoint or fixup commits) into one coherent change.
- Don't squash a meaningful sequence (foundation, feature, tests, docs) into one giant commit.

## Rebase
- Fine on local, unshared branches, to keep history linear and tidy before integrating.
- Never rebase or force-push a branch others may have pulled without my explicit OK.
- On conflicts: stop immediately. Inspect `git status --short` and conflicting hunks. Never guess resolution. Offer `git rebase --abort` to return cleanly to prior state if resolution is uncertain.

## Cherry-pick
1. Inspect the source commit and what it depends on, and confirm approval with the user per `profile/AGENTS.md` before executing.
2. Confirm the target working tree is clean.
3. Cherry-pick, inspect the resulting diff, run validation.
4. On conflicts or hidden dependencies: stop and report. Offer `git cherry-pick --abort`.

## Revert
- Confirm target SHA, blast radius, and user approval per `profile/AGENTS.md` before running `git revert`.
- Run validation after creating the revert commit; on conflicts, stop and offer `git revert --abort`.

## Merge
- Follow the repo's integration policy (merge commit vs fast-forward vs rebase).
- Keep merge commits when the branch shape tells a useful story (long-running feature work).
- On conflicts: stop and report. Offer `git merge --abort` before attempting resolution.

## Reset and restore
- **Safe** (keeps file contents): `git restore --staged <file>`, `git reset --soft <ref>`.
- **Destructive** (discards work): `git restore <file>`, `git reset --hard`, `git clean -fd`,
  `git push --force`.
- Never run a destructive command without telling me exactly what would be lost and getting an
  explicit yes.
