# Remote, Git Push, and Mirror Swap

Detailed procedure for Steps 1, 2, 3, and 7 of `gitea-to-github`.

## 1. Preflight Checks

1. **Tool & Auth Verification:** Verify `gt auth status` (or active Gitea token), `gh auth status`, and `command -v new-repo`.
2. **Host Discovery (No Hardcoded Domains):** Derive `<gitea-host>` dynamically from the repository's `origin` remote URL or the active `gt` CLI host configuration, normalized to lowercase hostname without scheme or port.
3. **Live Mirror & Sovereign Checks:** Query Gitea repo metadata (`GET /api/v1/repos/{owner}/{repo}`):
   - If `mirror: true`, skip migration (already a pull mirror).
   - If `archived: true`, classify as `archived`; Gitea blocks renames and visibility updates on archived repos, so unarchive only with explicit user approval.
   - If `empty: true` (0 commits), classify as `empty` and skip git ref pushes and `/tmp/` clone commits.
4. **Git LFS Fail-Fast:** Check `git lfs ls-files` (or `.gitattributes` `filter=lfs`). If LFS objects exist, fail fast and skip migration.
5. **Dirty Local Path Check:** If a local checkout exists, run `git status --porcelain -- AGENTS.md .gitea/workflows/`. If uncommitted edits exist on those paths, prompt the user to commit or stash them via `git-manager` first, or continue via the `/tmp/` clone and skip the post-swap local `git pull`.
6. **Visibility Mapping:** Map Gitea `public` -> GitHub `public`, `private` -> GitHub `private`, and `internal` -> GitHub `private` (emitting an explicit warning). If the target GitHub repo already exists as `private`, update the Gitea repo to `private` before mirroring.

## 2. Pre-Migration Backup & Open PR Gate

1. **Secure JSON Snapshot:** Create `$XDG_STATE_HOME/gitea-to-github-backup/<repo>/` (falling back to `~/.local/state/gitea-to-github-backup/<repo>/`) with `umask 077` (`0700` dir, `0600` files). Export paginated Gitea JSON snapshots for open/closed issues, PRs, milestones, releases, and webhooks.
2. **Open PR Gate:** Never auto-merge conflicting or unreviewed Gitea PRs. List every open PR with draft, mergeable, and CI status and require an explicit per-PR choice before proceeding:
   - `merge`: merge on Gitea before cloning refs.
   - `push branch + recreate PR`: push head/base branches to GitHub and recreate the PR on GitHub.
   - `close`: close on Gitea (preserved in JSON snapshot).
   - `abort`: halt migration for this repository.

## 3. Empty GitHub Provisioning & Idempotent Ref Push

1. **Check Existing GitHub Repo (Resume Guard):** Run `gh repo view <gh-owner>/<repo> --json name,defaultBranchRef`. If it already exists, skip `new-repo` creation.
2. **Non-Git Temp Directory Creation:** Otherwise, **always invoke `new-repo` from a fresh non-git temporary directory (`mktemp -d`)** so `new_repo.py`'s `determine_target()` never sees `.git` and never triggers `link_and_push_existing()` to overwrite local `origin`:
   ```bash
   (cd "$(mktemp -d)" && new-repo <target> --empty --no-mirror --no-clone [-o <gh-org>] [-p])
   ```
3. **Explicit Refspec Push & Ancestry Guard:** Clone Gitea into a temp bare directory (`git clone --bare <gitea-url> <tmp-bare>`). Before pushing, if the target GitHub repo already has branches (e.g., on `/diagnose` resume), verify whether each Gitea branch tip is already an ancestor of the corresponding GitHub branch; never force-push over Step 5 `/tmp/` commits. Push explicit refspecs only (avoiding Gitea internal refs such as `refs/pull/*`):
   ```bash
   git push <github-url> 'refs/heads/*:refs/heads/*' 'refs/tags/*:refs/tags/*'
   ```
   Set GitHub's default branch to match Gitea's and verify `HEAD`, branch list, and tag list align.

## 4. Ephemeral `/tmp/` Commit, Archive Rename & Pull Mirror Swap

1. **Ephemeral `/tmp/` Clone:** Apply planned `.github/workflows/`, `README.md` badge updates, and `AGENTS.md` rewrites inside a fresh `/tmp/` clone of `<github-url>`, commit, and push to GitHub before touching Gitea. On resume, skip if the planned updates are already present on GitHub.
2. **Local Checkout Update:** If a local checkout exists, delegate flipping `origin` to `<github-url>`, resolving any dirty working-tree state, and pulling the migration commit (unless skipped due to colliding local edits) to `git-manager`.
3. **Archive Rename (100-Char Limit):** Compute UTC timestamp `YYYYMMDDHHMMSS` (`-archive-YYYYMMDDHHMMSS` is 23 chars). Truncate the `<repo>` base name to `<= 77` chars if needed so `<base>-archive-YYYYMMDDHHMMSS` stays within Gitea's 100-char limit, then rename via `PATCH /api/v1/repos/{owner}/{repo}`.
4. **Pull Mirror Attachment & Sync Verification:** Attach the Gitea pull mirror (passing private-repo credentials per `new-repo`'s mirror auth contract):
   ```bash
   (cd "$(mktemp -d)" && new-repo --gitea-mirror <github-url> [-p] [--gitea-org <gitea-org>])
   ```
   Trigger `POST /api/v1/repos/{owner}/{repo}/mirror-sync`, then poll `GET /api/v1/repos/{owner}/{repo}` and compare Gitea's default-branch commit SHA against GitHub's default-branch SHA every `3s` up to a `60s` timeout.
5. **Destructive Archive Deletion Gate:** Only after SHA parity is confirmed, ask for explicit user confirmation before deleting `<base>-archive-YYYYMMDDHHMMSS`.
