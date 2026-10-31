# Pull Request Lifecycle and Evidence Synthesis

Reference for `gitea-pr`. Defines PR states, evidence synthesis template, and feedback triage workflow.

## 1. Pull Request Lifecycle States

```text
Draft (WIP) -> Review -> Changes Requested -> Ready for Merge -> Merged
                                 |                    |
                                 +-- [Rework/Fix] ----+
```

1. **Draft (WIP)**: PR opened early for visibility. In Gitea, prefixed with `WIP:` or flagged `--draft`. CI may run; reviews are informal.
2. **Review**: Feature complete, working tree clean, static `code-review` and runtime `verify-slice` evidence packets attached. Ready for formal audit.
3. **Changes Requested**: Reviewer identified defects, missing tests, or security concerns. Agent addresses feedback via `git-commit` and refreshes evidence.
4. **Ready for Merge**: All review threads resolved, static review confirms `Ready`, runtime checks pass, and mergeability is green.
5. **Merged**: Merged into target base branch by the human owner. Associated issues are closed automatically by Gitea.

---

## 2. Standard PR Description Template

Every PR description synthesizes static provenance and runtime evidence into a transparent record:

```markdown
Closes #<issue-index>

## Summary of Changes
<Concise overview of what was built, why, and what architectural decisions were made.>

## Scope & Non-Goals
- **In Scope**: <Itemized list of changes included in this PR>
- **Out of Scope**: <Explicitly deferred items or non-goals>

## Static Review Provenance (`code-review`)
- **Base Commit**: `<base-sha>` -> **Head Commit**: `<head-sha>`
- **Committed Diff Fingerprint**: `sha256:<hash>`
- **Axes Breakdown**:
  - Spec & Scope: Pass
  - Standards & Smells: Pass
  - Seam & Test Integrity: Pass
  - Defensive Invariants: Pass
- **Review Status**: `Ready`

## Runtime Verification Ledger (`verify-slice`)
| Check ID | Perspective | Scope | Description | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| RV-01 | Behavioral / Seam | local | Unit & integration suite execution | PASS |
| RV-02 | State & Concurrency | local | Race condition & lock invariant check | PASS |
| RV-03 | Security / Host Boundary | local | Host socket validation boundary | PASS |

## Residual Risks & Operational Considerations
- **Environment Prerequisites**: <Any required environment variables, sockets, or permissions>
- **Reversibility**: <How to cleanly revert this slice if unexpected regressions occur>
```

---

## 3. Review Feedback Triage Workflow

When comments or change requests arrive on a PR:

1. **Extract review comments**:
   ```sh
   tea pulls review-comments <index>
   ```
2. **Categorize comments**:
   - *Defects & Invariants*: Logic errors, broken tests, edge-case crashes (require code fix).
   - *Spec & Scope Clarifications*: Questions about intent or architectural fit (require response or doc update).
   - *Nits / Polish*: Minor style preferences that do not violate repo standards (human owner decides priority).
3. **Implement fixes on the feature branch**:
   - Use `tdd` or direct edits.
   - Commit fixes using `git-commit` with conventional commit scope (e.g. `fix(gitea-pr): address review feedback`).
4. **Re-verify after changes**:
   - Run `code-review` to confirm the updated diff fingerprint is clean.
   - Run `verify-slice` to substantiate runtime assertions.
5. **Reply and resolve threads via `tea`**:
   - Reply to comment: `tea pulls reply <index> <comment-id> "Fixed in <sha>"`
   - Resolve thread: `tea pulls resolve <comment-id>`
6. **Push updates to remote**:
   - `git push origin <branch>`

---

## 4. Release Authority Guardrail

Automated skills and checks inform the human owner; they never make the merge decision independently:
- Neither passing unit tests nor a `Ready` code review implies permission to execute `tea pulls merge`.
- The human owner reviews the consolidated ledger, assesses residual risks, and explicitly authorizes merge execution.
