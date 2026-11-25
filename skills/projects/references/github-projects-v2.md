# GitHub Projects v2 & Milestone Recipes

Sole owner of GitHub Projects v2 GraphQL recipes and REST milestone commands.
Referenced by `projects` (onboarding, milestones, due dates), `implement`
(`Ready -> Work in Progress`), and `verify` (`Work in Progress -> Review`,
`Review -> Completed`, and abort/rejection reverts).

---

## 1. Prerequisites & Anti-Hallucination Rules

- Verify GitHub repository identity first: `gh repo view --json url`.
- Confirm `gh auth status` includes `repo` and `project` scopes before running
  Projects v2 GraphQL mutations.
- **Never hardcode or guess IDs**: Never guess milestone sequence numbers, never
  construct `/milestone/1` URLs, and never hardcode GraphQL Node IDs
  (`PVT_...`, `PVTSSF_...`, `PVTI_...`, or single-select option IDs). Always
  resolve IDs dynamically from live `gh api` responses.

---

## 2. Fixed 5-Column Color Enum Map

GitHub Projects v2 `Status` single-select options use fixed enum names
(`ProjectV2SingleSelectFieldOptionColor`), not hex codes:

| Order | Column Name | GitHub Color Enum |
| :--- | :--- | :--- |
| `0` | `Backlog` | `GRAY` |
| `1` | `Ready` | `BLUE` |
| `2` | `Work in Progress` | `YELLOW` |
| `3` | `Review` | `PURPLE` |
| `4` | `Completed` | `GREEN` |

When reconciling an existing board's `Status` field via `updateProjectV2Field`,
match existing options case-insensitively and preserve their option IDs where
possible so attached cards stay intact. Ensure all 5 canonical column names and
color enums above exist before moving cards.

---

## 3. Onboarding New Issues onto a Board (`projects`)

Use `owner.projectV2(number: $project_number)` when creating or onboarding an
issue that is not yet attached to the board. Replace `organization` with `user`
for user-owned projects.

### Step 3a: Resolve `project_id` and Issue Global Node ID
```bash
gh api graphql \
  -F owner="<owner>" \
  -F repo="<repo>" \
  -F project_number=<project_number> \
  -F issue_number=<issue_number> \
  -f query='
    query($owner: String!, $repo: String!, $project_number: Int!, $issue_number: Int!) {
      organization(login: $owner) {
        projectV2(number: $project_number) { id }
      }
      repository(owner: $owner, name: $repo) {
        issue(number: $issue_number) { id url }
      }
    }'
```

*(For personal repositories, replace `organization(login: $owner)` with
`user(login: $owner)`.)*

### Step 3b: Add Issue to Project (`addProjectV2ItemById`)
```bash
gh api graphql \
  -f project_id="<PVT_...>" \
  -f content_id="<I_...>" \
  -f query='
    mutation($project_id: ID!, $content_id: ID!) {
      addProjectV2ItemById(input: {projectId: $project_id, contentId: $content_id}) {
        item { id }
      }
    }'
```

---

## 4. Card Transitions via `issue.projectItems` (`implement`, `verify`)

For board card moves, query `issue.projectItems` directly instead of scanning
`projectV2.items`. This avoids 100-item board pagination limits and resolves
`project_id`, `status_field_id`, the `PVTI_...` item ID, and all target column
`option_id`s in a single GraphQL request.

### Step 4a: Single-Query Dynamic Resolution
```bash
gh api graphql \
  -F owner="<owner>" \
  -F repo="<repo>" \
  -F issue_number=<issue_number> \
  -f query='
    query($owner: String!, $repo: String!, $issue_number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $issue_number) {
          projectItems(first: 20) {
            nodes {
              id
              project {
                id
                number
                field(name: "Status") {
                  ... on ProjectV2SingleSelectField {
                    id
                    options { id name color }
                  }
                }
              }
            }
          }
        }
      }
    }'
```

Filter `.data.repository.issue.projectItems.nodes[]` by
`select(.project.number == $project_number)` (using `project_number` from
`AGENTS.md`):
- If no matching node exists, halt and onboard the issue via Section 3 first.
- Verify the resolved `Status` field options include the target canonical column
  name (`Backlog`, `Ready`, `Work in Progress`, `Review`, or `Completed`).
  **Fail fast** with a clear column-name mismatch error if the target option is
  missing; never fall back to a guessed option ID.

### Step 4b: Move Card (`SINGLE_SELECT` Status Mutation)
```bash
gh api graphql \
  -f project_id="<PVT_...>" \
  -f item_id="<PVTI_...>" \
  -f field_id="<PVTSSF_...>" \
  -f option_id="<option_id>" \
  -f query='
    mutation($project_id: ID!, $item_id: ID!, $field_id: ID!, $option_id: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $project_id
        itemId: $item_id
        fieldId: $field_id
        value: { singleSelectOptionId: $option_id }
      }) {
        projectV2Item { id }
      }
    }'
```

---

## 5. Updating Projects v2 `DATE` Fields

Resolve the `DATE` field ID dynamically from `project.fields(first: 50)` (or
`project.field(name: "<Field Name>")`), then run `updateProjectV2ItemFieldValue`
with an ISO-8601 `YYYY-MM-DD` string:

```bash
gh api graphql \
  -f project_id="<PVT_...>" \
  -f item_id="<PVTI_...>" \
  -f field_id="<PVTF_...>" \
  -f date="YYYY-MM-DD" \
  -f query='
    mutation($project_id: ID!, $item_id: ID!, $field_id: ID!, $date: Date!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $project_id
        itemId: $item_id
        fieldId: $field_id
        value: { date: $date }
      }) {
        projectV2Item { id }
      }
    }'
```

---

## 6. REST Milestone & Issue Operations

GitHub CLI does not expose a native `gh milestone` subcommand; manage milestones
through REST via `gh api repos/{owner}/{repo}/milestones`:

```bash
# List open milestones (extract number, title, due_on, html_url)
gh api repos/{owner}/{repo}/milestones --paginate \
  --jq '.[] | {number, title, state, due_on, html_url}'

# Create a milestone (due_on is optional ISO-8601 UTC)
gh api repos/{owner}/{repo}/milestones -X POST \
  -f title="<Milestone Title>" \
  -f description="<Scope summary>" \
  -f due_on="YYYY-MM-DDTHH:MM:SSZ"

# Update or close a milestone (use dynamically queried milestone number)
gh api repos/{owner}/{repo}/milestones/<milestone_number> -X PATCH \
  -f state="closed"

# Create an issue attached to a milestone and verify returned URL
gh issue create \
  --title "<Issue Title>" \
  --body-file <issue-body.md> \
  --milestone "<Milestone Title>"
```
