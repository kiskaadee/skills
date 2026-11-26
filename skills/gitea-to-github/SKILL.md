---
name: gitea-to-github
description: >-
  Migrates standalone repositories or Gitea organizations from self-hosted Gitea
  to GitHub, converting each Gitea repo into a pull mirror. Use when migrating
  a Gitea repo or org, translating .gitea/workflows/ CI to GitHub Actions, or
  updating legacy Gitea AGENTS.md contracts to GitHub Projects v2.
disable-model-invocation: true
---

# Gitea to GitHub

## Use when
- Migrating a standalone Gitea repository or `--org <gitea-org>` to GitHub primary with a Gitea pull mirror.
- Translating `.gitea/workflows/` to `.github/workflows/` and legacy `AGENTS.md` contracts to `project_number: <int>`.
- Not for ad-hoc Gitea operations outside migration: use `gt-usage`.
- Not for ongoing GitHub planning or slice execution: use `projects` or `implement`.

## Steps
1. **Preflight and dry-run plan.** Read [references/remote-and-mirror.md](references/remote-and-mirror.md) and [references/entity-migration.md](references/entity-migration.md). Run read-only discovery first (dry-run is default; `--dry-run` optional). Verify `gt`/`gh` auth, `new-repo --empty --no-mirror --no-clone`, live `mirror: true` skip, `git lfs ls-files` fail-fast, `empty`/`archived` state, and dirty `AGENTS.md`/`.gitea/workflows/` paths. Halt after printing the segmented inventory/plan unless `--execute` or explicit approval is given (`interactive-gated` repos still pause per item).
2. **Snapshot and resolve open PRs.** Export Gitea JSON metadata (issues, PRs, milestones, releases, webhooks) to `$XDG_STATE_HOME/gitea-to-github-backup/<repo>/` under `umask 077`. Require an explicit per-PR choice (`merge`, `push branch + recreate PR`, `close`, or `abort`) for every open Gitea PR.
3. **Provision GitHub and push refs.** Invoke `new-repo <target> --empty --no-mirror --no-clone` from a fresh `mktemp -d` non-git directory (skip if target GitHub repo exists). Push explicit `refs/heads/*:refs/heads/*` and `refs/tags/*:refs/tags/*` refspecs from a temp bare clone after verifying branch ancestry on resume.
4. **Conditional Projects v2 onboarding.** Only if a legacy Gitea board or contract exists (or user opts in during dry-run), create or link the 5-column Projects v2 board via `../projects/references/github-projects-v2.md`.
5. **Translate CI and `AGENTS.md` in `/tmp/`.** Read [references/ci-and-contracts.md](references/ci-and-contracts.md). Skip if planned updates already exist on GitHub; otherwise translate `.gitea/workflows/` to `.github/workflows/`, rewrite `README.md` badges, warn on non-`GITEA_TOKEN` secrets, and rewrite legacy `AGENTS.md` to `project_number: <int>` in an ephemeral `/tmp/` clone and push.
6. **Migrate milestones and open issues.** Sync open milestones and curated open issues idempotently using `<!-- gitea-origin: <gitea-host>/<owner>/<repo>#<number> -->` markers.
7. **Flip local `origin`, archive, and mirror.** If a local checkout exists, delegate `origin` flip and `git pull` to `git-manager`. Rename Gitea repo to `<repo>-archive-YYYYMMDDHHMMSS` (`<= 77`-char base), attach pull mirror via `new-repo --gitea-mirror`, verify SHA parity within `60s`, and delete the archive only after explicit confirmation.

## Your call
- Dry-run approval, `--org` selection/overrides, and any `archived: true` unarchive decision.
- Per-PR resolution for open Gitea PRs and per-issue curation.
- Opt-in to `self-hosted` runners (`private` repos only) or conditional Projects v2 board creation.
- Explicit confirmation before deleting `<repo>-archive-YYYYMMDDHHMMSS`.

## Done when
- GitHub has all refs, planned `.github/workflows/` and `AGENTS.md` updates, and curated issues/milestones, and Gitea pull-mirror SHA parity is verified.

## Hands off to
- `git-manager`: local `origin` remote flip, dirty working-tree resolution, and `git pull`.
- `projects`: new Projects v2 board setup or roadmap decomposition after migration.
- `diagnose`: mid-flight API or network failures before resuming idempotently.
- `gt-usage`: standalone Gitea queries outside migration.
- Standalone turns end with `Suggested Next Step: /projects` (if planning work) or `Suggested Next Step: /implement` (suppressed when delegated).
