# Verified `gt` CLI Commands & JSON Recipes

All commands require official `gt` CLI (v1.0.0+). Never guess numeric server identifiers or scrape terminal formatting tables; always query with `--json`.

## 1. Authentication & Status

```bash
# Check logged-in status
gt auth status

# Authenticate with an instance
gt auth login --host <https-instance-url>
```

## 2. Milestones

Gitea assigns instance-wide auto-incrementing integer IDs to milestones. A repository's first milestone is almost never ID `1`. Always extract `.id` and `.url`.

```bash
# Create milestone and print server ID and canonical URL
gt milestone create "<title>" -d "<description>" --json id,title,url

# Create milestone with deadline (format: YYYY-MM-DD)
gt milestone create "<title>" --deadline 2026-12-31 -d "<description>" --json id,title,url

# List open milestones with verified IDs
gt milestone list --json id,title,state,url

# View milestone details
gt milestone view <id>
```

## 3. Project Boards

Projects provide spatial Kanban workflow stages.

```bash
# Create project board with basic kanban columns
gt project create "<title>" --template basic_kanban -d "<description>" --json id,title,url

# List open projects
gt project list --json id,title,state,url

# View project cards and columns
gt project view <id>

# List board columns with IDs
gt api /repos/{owner}/{repo}/projects/<project-id>/columns --jq '.[].id, .[].title'

# Move issue card between columns (requires global issue ID, e.g. from `gt issue list --json id,number`)
gt api -X POST /repos/{owner}/{repo}/projects/<project-id>/issues/<global-issue-id>/move -F column_id=<target-col-id>
```

## 4. Issues

```bash
# Create issue attached to milestone and project
gt issue create -t "<title>" -F <body-file> -m <milestone-id> -p <project-id> --json number,title,url

# List open issues with global IDs and numbers
gt issue list --json id,number,title,state,url

# List open issues in a milestone
gt issue list -m <milestone-id> --json number,title,state,url

# Edit issue title, milestone, or body
gt issue edit <number> --title "<new-title>" -m <milestone-id>

# Close an issue
gt issue close <number>
```

## 5. Pull Requests

```bash
# Create pull request targeting base branch
gt pr create -t "<title>" -F <body-file> --base main --head <branch> --json number,title,url

# List open PRs
gt pr list --json number,title,state,url

# View PR details and review status
gt pr view <number>

# Checkout PR branch locally
gt pr checkout <number>
```

## 6. Output Extraction Discipline

When consuming `gt` output in scripts or skills:
- Use `--json <fields>` to guarantee structured key-value output.
- Use `--jq <expression>` to extract specific scalars without external `jq` dependencies:
  ```bash
  milestone_id=$(gt milestone create "v1.0" --jq '.id')
  issue_url=$(gt issue create -t "Fix bug" -b "Details" --jq '.url')
  ```
