---
name: gt-usage
description: >-
  Standalone ad-hoc utility for working with Gitea repositories, issues,
  milestones, projects, and pull requests using the official gt CLI outside the
  GitHub core delivery loop. Use when querying or mutating Gitea entities,
  extracting resource identifiers, or configuring Gitea instance remotes.
---

# Gitea CLI Usage

## Use when
- Ad-hoc querying, creating, or editing Gitea issues, milestones, project boards, or PRs on Gitea-hosted repos or mirrors.
- Extracting exact server identifiers and URLs via JSON output.
- Configuring instance remotes or SSH port mappings for sovereign Gitea instances.
- Standalone utility outside the GitHub core delivery loop (`projects`, `implement`, `code-review`, `verify`).

## Steps
1. **Verify CLI availability and auth.** Run `gt auth status`. If unauthenticated,
   guide the user to run `gt auth login` with their instance host and token.
2. **Discover flags and subcommands.** Run `gt <command> --help` to verify local
   flag availability before running mutations.
3. **Query with structured JSON.** Always pass `--json <fields>` (or `--jq <filter>`)
   when reading or creating entities. Never scrape plain terminal tables or guess IDs.
4. **Extract verified server identifiers.**
   - Milestones: Query `gt milestone list --json id,title,url` or extract from creation.
   - Issues: Query `gt issue list --json number,title,url`.
   - Projects: Query `gt project list --json id,title,url`.
   - PRs: Query `gt pr list --json number,title,url`.
5. **Format multi-line bodies via files.** Pass issue or PR descriptions via
   `-F <file>` or `-F -` to preserve formatting without shell escaping issues.
6. **Apply instance remotes.** For non-standard SSH ports, configure host mapping
   via `gt config set ssh_host <host>:<port> --host <instance-url>`. See
   [references/instance-conventions.md](references/instance-conventions.md).

## Your call
- **Instance authentication**: prompt user if `gt auth status` indicates missing credentials.
- **Entity deletion or closure**: confirm before closing or deleting remote resources.

## Done when
- Target Gitea entity is created, queried, or updated with confirmed server JSON output.

## Hands off to
- `gitea-to-github`: when migrating a Gitea repository or org to GitHub primary with a Gitea pull mirror.
- `git-manager`: for local branch, commit, or remote configuration work.
- `projects`: when planning active delivery workflows on GitHub instead of ad-hoc Gitea usage.
