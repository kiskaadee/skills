# Org Inventory, Issues, Milestones & Conditional Projects v2

Detailed procedure for Steps 1, 4, and 6 of `gitea-to-github`.

## 1. Segmented `--org` Dry-Run Inventory

1. **Paginated Gitea Discovery:** Query all org repositories, open PRs, and open issues using paginated Gitea API calls (`page=1..N`).
2. **Classification Taxonomy:** Classify each repository into one or more states:
   - `migratable` (clean-slate)
   - `already-pull-mirror` (`mirror: true`)
   - `sovereign-opt-out` (`forge: gitea` in `AGENTS.md`)
   - `has-lfs-blocked`
   - `has-open-prs`
   - `has-open-issues`
   - `empty` (0 commits)
   - `archived` (`archived: true`)
3. **Segmentation:** Present a single dry-run inventory table segmented into:
   - **Clean-slate:** Zero open PRs and no per-item curation needed; execute sequentially from one approval (applying any user-stated overrides such as visibility or target org).
   - **Interactive-gated:** Has open PRs (`has-open-prs`) or open issues needing curation (`has-open-issues`); prompt per repository before mutation.

## 2. Milestones & Idempotent Issue Migration

1. **Paginated GitHub Queries:** Fetch existing GitHub milestones and issues to guarantee idempotent `/diagnose` resume:
   ```bash
   gh api --paginate repos/{owner}/{repo}/milestones?state=all
   gh api --paginate repos/{owner}/{repo}/issues?state=all --jq '.[] | select(.pull_request == null)'
   ```
2. **Milestones:** Match Gitea open milestones by `title`. Create missing milestones on GitHub with `title`, `description`, and `due_on` (omitting `due_on` whenever the Gitea timestamp is null or zero).
3. **Labels & Attachments:**
   - Pre-create any missing Gitea issue labels on GitHub before creating issues (`gh label create` with color/description).
   - Scan curated open Gitea issue bodies for `/attachments/<uuid>` URLs; warn the user before archive deletion that those links will break once `<repo>-archive-YYYYMMDDHHMMSS` is removed.
4. **Immutable Deduplication Marker:** Append the following marker to the bottom of every migrated GitHub issue body (with `<gitea-host>` normalized to lowercase hostname without scheme or port):
   ```markdown
   <!-- gitea-origin: <gitea-host>/<owner>/<repo>#<number> -->
   ```
   Skip any Gitea issue whose origin marker already appears in the paginated GitHub issues list.

## 3. Conditional Projects v2 Onboarding

1. **Trigger Condition:** Create or link a 5-column Projects v2 board (`Backlog`, `Ready`, `Work in Progress`, `Review`, `Completed`) **only** when the source repo has a legacy Gitea board/contract or when the user explicitly opts in during dry-run. Leave new board creation for boardless repos to `projects` (respecting its tiered `Project Board Policy`).
2. **GraphQL Delegation:** Delegate all Projects v2 GraphQL mutations strictly to `../../projects/references/github-projects-v2.md`.
3. **Column Mapping:** Map legacy Gitea board columns case-insensitively onto the 5 canonical GitHub columns:
   - `To Do`, `Open`, `Backlog` -> `Backlog`
   - `Ready` -> `Ready`
   - `In Progress`, `Doing`, `Work in Progress` -> `Work in Progress`
   - `Review`, `In Review` -> `Review`
   - `Done`, `Closed`, `Completed` -> `Completed`
   - Unmatched column names -> fallback to `Backlog`.
