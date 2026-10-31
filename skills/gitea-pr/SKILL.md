---
name: gitea-pr
description: >-
  Manage pull request lifecycle on Gitea: verify branch readiness, synthesize structured PR
  descriptions from code-review and verify-slice evidence packets, link issues, digest review
  feedback, and report merge readiness. Not for code inspection: use code-review. Not for
  runtime QA: use verify-slice. Not for Git branch or merge mechanics: use git-workspace.
---

# Gitea PR

## Use when
- Opening or updating a pull request on Gitea after implementing an issue or feature.
- Synthesizing static code review and runtime verification evidence into a reviewable PR.
- Tracking review comments, requested changes, and CI checks toward merge readiness.
- Not for static code inspection: use `code-review`.
- Not for runtime behavioral verification: use `verify-slice`.
- Not for branch creation, rebasing, or local history integration: use `git-workspace`.

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
4. **Present for human approval.** Present the proposed title, target base branch, milestone,
   and description body to the user per `profile/AGENTS.md`. Stop for confirmation before
   creating or editing the pull request.
5. **Create or update pull request via `tea`.** Run verified commands from
   [references/tea-pulls.md](references/tea-pulls.md) (`tea pulls create --description-file -`).
   Pass `--draft` if work remains in progress.
6. **Track review feedback and merge readiness.** Inspect incoming review comments
   (`tea pulls review-comments <index>`) and mergeability status. Synthesize actionable
   feedback. When all checks pass and review feedback is resolved, report `Ready for Merge`.
   Release and merge authority belongs exclusively to the human owner: never merge automatically.

## Your call
- **PR title and description approval**: review and approve the draft PR content and issue linkage.
- **Review feedback triage**: decide how to address review comments (rework, clarification, deferral).
- **Merge and release authorization**: decide when to merge the PR into the target base branch.

## Done when
- Pull request is created or updated in Gitea with complete evidence provenance, and its current
  review and mergeability status is reported to the user.

## Hands off to
- `code-review`: if the diff changes and needs renewed static inspection.
- `verify-slice`: if new code requires runtime verification.
- `git-commit`: to package review fixes into atomic commits.
- `git-workspace`: to rebase or update the branch against upstream base.
