# Verified `gt pr` Pull Request Subroutines

Reference for `gitea-pr`. Canonical, verified syntax for managing pull requests, status checks, and review threads via `gt`.

## 1. Inspecting Pull Requests

### List Pull Requests
```bash
# List open PRs with structured fields
gt pr list --json number,title,state,url

# List all PRs including closed/merged
gt pr list --state all --json number,title,state,url
```

### View Pull Request Details & Status Checks
```bash
# View basic PR details
gt pr view <number>

# Inspect mergeability and review decision
gt pr view <number> --json number,title,state,mergeable,review_decision,url

# Show status of CI checks on the head commit
gt pr checks <number>

# Wait for CI checks to complete
gt pr checks <number> --watch
```

---

## 2. Creating and Updating Pull Requests

### Create a Pull Request
- Create standard PR with multi-line body from file:
  ```bash
  gt pr create -t "<title>" -B "<base-branch>" -H "<feature-branch>" -F <body-file> --json number,url
  ```
- Create as a Draft / WIP PR:
  ```bash
  gt pr create -t "WIP: <title>" --draft -B "<base-branch>" -H "<feature-branch>" -F <body-file> --json number,url
  ```
- Assign milestone and project:
  ```bash
  gt pr create -t "<title>" -B "<base>" -H "<branch>" -m <milestone-id> -p <project-id> -F <body-file> --json number,url
  ```

### Edit a Pull Request
```bash
# Update title or base branch
gt pr edit <number> --title "<new-title>"

# Mark a draft PR as ready for review
gt pr ready <number>
```

---

## 3. Review Comments and Discussions

### List Review Comments
```bash
# List inline review comments
gt pr review comments <number>

# View PR activity and top-level comments
gt pr timeline <number>
```

### Reply to Review Comments
```bash
# Reply to an inline comment
gt pr review reply <number> <comment-id> "Fixed in <sha>"

# Add top-level comment
gt pr comment <number> -b "<comment-text>"
```

### Resolve Review Comments
```bash
# Mark an inline thread as resolved
gt pr review resolve <comment-id>

# Reopen an inline thread
gt pr review unresolve <comment-id>
```

### Publish a `code-review` Comment Block
Input: `review-body.md` and `inline-comments.json` drafted by `code-review` (section 4 of its `finding-schema.md`), plus the reviewed head SHA from the block header.

```bash
# 1. Staleness: the PR head must equal the reviewed head SHA. Mismatch: stop, re-run code-review.
gt pr view <number> --json head_sha -q .head_sha

# 2. Duplicates and pending state: stop if any review is PENDING (posting would publish its
#    inline comments too) or if a review already exists for the reviewed SHA from this block.
gt pr review list <number> --json id,state,commit,body

# 3. After owner approval: one comment-only review, pinned to the reviewed commit.
gt pr review <number> --comment --commit <reviewed-head-sha> \
  -F review-body.md --comments-file inline-comments.json --json id,url

# Body-only block (no inline entries): omit --comments-file.
```

- Never pass `--approve` or `--request-changes`: the verdict in the body is informational, and merge authority stays with the owner (Gitea also refuses approval on your own PR).
- Never pass `--yes`: it exists to publish a pending review, which step 2 already rules out.
- If Gitea rejects an inline entry (line outside a diff hunk), confirm with step 2 that no review was created, move that entry into the body, and retry once.
- Record the returned review `id` and `url`. Later fixes use `gt pr review reply` with `Fixed in <sha>` and `gt pr review resolve`, per the triage workflow in `pr-lifecycle.md`.

---

## 4. Closing and Merging Pull Requests

### Close or Reopen PR
```bash
gt pr close <number>
gt pr reopen <number>
```

### Merge Pull Request (Requires Explicit Human Authorization)
Release and merge authority belongs exclusively to the human owner.
```bash
# Fast-forward / merge commit
gt pr merge <number>

# Squash and merge
gt pr merge <number> --squash --delete-branch
```
