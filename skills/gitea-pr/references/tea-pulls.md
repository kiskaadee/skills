# Verified Tea CLI Pull Request Subroutines

Reference for `gitea-pr`. Canonical, verified syntax for managing pull requests and review threads via `tea`.

## 1. Inspecting Pull Requests

### List Pull Requests
- List open PRs:
  ```sh
  tea pulls list
  ```
- List all PRs including closed:
  ```sh
  tea pulls list --state all
  ```

### View Pull Request Details
- View basic PR details:
  ```sh
  tea pulls <index>
  ```
- Inspect mergeability and CI status:
  ```sh
  tea pulls <index> --fields index,title,state,mergeable,ci,base,head
  ```

---

## 2. Creating and Updating Pull Requests

### Create a Pull Request
- Create standard PR with multi-line description via heredoc:
  ```sh
  tea pulls create --title "<title>" --base "<base-branch>" --head "<feature-branch>" --description-file - <<'EOF'
  Closes #<issue-index>

  ## Summary of Changes
  ...
  EOF
  ```
- Create as a Draft / WIP PR:
  ```sh
  tea pulls create --title "WIP: <title>" --draft --base "<base-branch>" --head "<feature-branch>" --description-file - <<'EOF'
  ...
  EOF
  ```
- Assign milestone or labels:
  ```sh
  tea pulls create --title "<title>" --base "<base>" --milestone "<milestone-name>" --labels "<label1,label2>" --description-file -
  ```

### Edit a Pull Request
- Update title or milestone:
  ```sh
  tea pulls edit <index> --title "<new-title>" --milestone "<milestone-name>"
  ```

---

## 3. Review Comments and Discussions

### List Review Comments
- View all inline review comments:
  ```sh
  tea pulls review-comments <index>
  ```
- View general PR comments:
  ```sh
  tea comments list <index>
  ```

### Reply to Review Comments
- Reply to an inline review comment:
  ```sh
  tea pulls reply <index> <comment-id> "<reply-text>"
  ```
- Add a top-level comment to the PR:
  ```sh
  tea comment <index> "<comment-text>"
  ```

### Resolve Review Comments
- Mark an inline review comment as resolved:
  ```sh
  tea pulls resolve <comment-id>
  ```
- Unresolve a comment if follow-up is needed:
  ```sh
  tea pulls unresolve <comment-id>
  ```

---

## 4. Closing and Merging Pull Requests

### Close or Reopen PR
- Close without merging:
  ```sh
  tea pulls close <index>
  ```
- Reopen closed PR:
  ```sh
  tea pulls reopen <index>
  ```

### Merge Pull Request (Human Release Authorization Required)
- Merge using specified merge style (`merge`, `rebase`, `squash`, `rebase-merge`):
  ```sh
  tea pulls merge <index> --style rebase --title "<commit-title>" --message "<commit-body>"
  ```
- **Operator Safety Rule**: Skills report merge readiness. Only execute `tea pulls merge` when the human owner has explicitly authorized merging.
