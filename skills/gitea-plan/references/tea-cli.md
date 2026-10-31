# Verified Tea CLI Subroutines

Reference for `gitea-plan` and `gitea-pr`. Canonical, verified syntax for coordinating Gitea operations via the `tea` CLI.

## Repository Context

`tea` automatically discovers the target repository and authenticated login from the active Git remote (`origin`). To verify or override:
- Check current login: `tea logins list`
- Override target repo explicitly if running outside the repository root: `-r <owner>/<repo>`

---

## 1. Issue Management

### Create an Issue
- Simple description:
  ```sh
  tea issues create --title "<title>" --description "<description>" [--milestone "<milestone>"] [--labels "<label1,label2>"]
  ```
- Multi-line description via heredoc (preferred for structured acceptance criteria):
  ```sh
  tea issues create --title "<title>" --milestone "<milestone>" --description-file - <<'EOF'
  ## Context & Problem
  ...

  ## Proposed Solution
  ...

  ## Acceptance Criteria
  1. ...
  2. ...
  EOF
  ```

### List and Inspect Issues
- List open issues:
  ```sh
  tea issues list
  ```
- Filter by milestone:
  ```sh
  tea issues list --milestone "<milestone-title>"
  ```
- View specific issue details:
  ```sh
  tea issues <index>
  ```

### Edit and Close Issues
- Update title, description, or milestone:
  ```sh
  tea issues edit <index> --title "<new-title>" --milestone "<new-milestone>"
  ```
- Close issue:
  ```sh
  tea issues close <index>
  ```

---

## 2. Milestone Management

### Create a Milestone
```sh
tea milestones create --title "<milestone-title>" --description "<overview-of-goals>"
```

### List and Inspect Milestones
```sh
tea milestones list
```

### Close a Milestone
```sh
tea milestones close "<milestone-title>"
```

---

## 3. Comments and Discussion

### Add a Comment
- Use canonical positional syntax:
  ```sh
  tea comment <index> "<comment-body>"
  ```
- Or explicit command syntax:
  ```sh
  tea comments add <index> "<comment-body>"
  ```
- **Syntax Trap**: Never use `tea comment create`. It fails with `strconv.ParseInt: parsing "create": invalid syntax`.

---

## 4. Labels
- List available labels:
  ```sh
  tea labels list
  ```
- Create repository label if missing:
  ```sh
  tea labels create --name "<name>" --color "<hex-color>" --description "<description>"
  ```
