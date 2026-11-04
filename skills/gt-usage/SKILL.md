---
name: gt-usage
description: >-
  Work with Gitea repositories, issues, milestones, projects, and pull requests
  using the official gt CLI. Use when querying or mutating Gitea entities,
  extracting resource identifiers, or configuring instance remotes.
---

# Gitea CLI Usage

## Use when
- Querying, creating, or editing Gitea issues, milestones, project boards, or PRs.
- Extracting exact server identifiers and URLs via JSON output.
- Configuring instance remotes or SSH port mappings for sovereign instances.
- Not for planning or issue decomposition: use `gitea-plan`.
- Not for pull request review synthesis: use `gitea-pr`.

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
- `gitea-plan`: to decompose technical work into milestones and issues.
- `gitea-pr`: to manage pull request review and merge readiness.
