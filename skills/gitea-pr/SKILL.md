---
name: gitea-pr
description: >-
  Manage pull request lifecycle on Gitea: verify branch readiness, synthesize structured PR
  descriptions from code-review and verify-slice evidence packets, link issues, digest review
  feedback, and report merge readiness. Not for code inspection: use code-review. Not for
  runtime QA: use verify-slice. Not for Git branch, commit, or merge mechanics: use git-manager.
---

# Gitea PR

## Use when
- Opening or updating a pull request on Gitea after implementing an issue or feature.
- Synthesizing static code review and runtime verification evidence into a reviewable PR.
- Tracking review comments, requested changes, and CI checks toward merge readiness.
- Not for static code inspection or publishing PR review blocks: use `code-review`.
- Not for runtime behavioral verification: use `verify-slice`.
- Not for branch creation, committing, rebasing, or local history integration: use `git-manager`.

## Steps
1. **Verify branch readiness.** Confirm the local working tree is clean (`git status --short`),
   the branch tracks an upstream remote (`git rev-parse @{u}`), unpushed commits are pushed,
   and the target base branch exists on the remote.
2. **Collect review and verification evidence.** Inspect outputs from preceding skills:
   - `code-review`: Static provenance, covered commits/diff fingerprint, findings disposition,
     and overall recommendation (`Ready`).
   - `verify-slice`: Runtime evidence ledger across behavioral, security, and state checks,
     confirming zero unhandled `FAIL` outcomes.
   If either packet is missing or stale relative to current `HEAD`, stop and run that skill first.
3. **Draft structured PR description.** Compose the PR body following
   [references/pr-lifecycle.md](references/pr-lifecycle.md):
   - Issue Linkage: `Closes #<issue-index>`.
   - Summary of Changes: Problem, solution, and scope boundary.
   - Static Review Provenance: Base/head SHAs, diff SHA256, and 4-axis disposition.
   - Runtime Verification Ledger: Markdown table of executed checks and outcomes.
   - Residual Risks and Rollback: Operational considerations and reversibility.
4. **Present for human approval.** Present proposed title, target base branch, milestone,
   and description body to the user per `profile/AGENTS.md`. Stop for confirmation before
   creating or editing the pull request.
5. **Create or update pull request via `gt pr` and move card to `Review`.** Run verified
   commands from [references/gt-pulls.md](references/gt-pulls.md):
   `gt pr create -t "<title>" -B "<base>" -H "<branch>" -F <body-file> --json number,url`.
   Pass `--draft` if work remains in progress. Extract verified PR number and URL, and ensure
   the linked issue card is in `Review` (`Work in Progress -> Review`) on the project board.
6. **Track review feedback, merge on owner approval, and move card `Review -> Completed`.**
   Inspect status checks (`gt pr checks <number>`), mergeability
   (`gt pr view <number> --json mergeable,review_decision`), and review comments
   (`gt pr review comments <number>`). If the current PR head lacks a published `code-review`
   comment, hand off to `code-review`. When checks pass and feedback is resolved, report
   `Ready for Merge`. Once the owner explicitly authorizes merge, run `gt pr merge <number>`
   and move the linked issue card `Review -> Completed`.

## Your call
- **PR title and description approval**: review and approve the draft PR content and issue linkage.
- **Review feedback triage**: decide how to address review comments (rework, clarification, deferral).
- **Merge and release authorization**: decide when to merge the PR into the target base branch.

## Done when
- Pull request is created or updated in Gitea with complete evidence provenance, and its current
  review and mergeability status is reported to the user.

## Hands off to
- `code-review`: if the PR head lacks a static review comment or the diff changed (`Suggested Next Step: /code-review <pr-number>`).
- `verify-slice`: if new code requires runtime verification (`Suggested Next Step: /verify-slice`).
- `reconcile-docs`: after merge when docs/milestones shift (`Suggested Next Step: /reconcile-docs`).
- `implement-slice`: after merge when next issue is queued (`Suggested Next Step: /implement-slice #<next-issue>`).
- `git-manager`: to commit review fixes, rebase, or update against base.
- Emit one outcome-matched `Suggested Next Step` on every standalone turn (including when CI is pending after PR creation: `/code-review <pr-number>` or `/gitea-pr <pr-number>`) per [skeleton](../build-skill/references/skeleton.md).
