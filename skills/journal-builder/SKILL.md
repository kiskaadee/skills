---
name: journal-builder
description: >-
  Turn a day's engineering history into a factual journal and learning scaffold.
  Produces facts and question blanks for the user to answer, then evaluates them.
---

# Journal Builder

## Use when
- `/journal-builder [YYYY-MM-DD]` or `/journal [YYYY-MM-DD]` (defaults to today).
- End of a workday or sprint to record facts and practice recalling key reasoning.
- Not for standalone changelogs: use git log directly.
- Not for deliberate coding practice drills: use `practice`.

## Steps
1. **Target the day and check history.** Establish date from argument or today.
   Check if a draft scaffold exists for that date with filled answers; if so, skip to step 5.
   Read events from repository `git log` or session history.
   - **Provenance check**: Read `assessed_commits` across existing journals. Only events
     whose full 40-character SHA is absent proceed as unassessed work.
   - **Backlog check**: If unassessed events exist from prior dates, surface them and ask
     whether to process the older backlog chronologically first.
   - **Resolve locations**: Resolve project identities to local paths using agent profile.
2. **Reconstruct facts.** Inspect repositories (diffs, tests, docs). Group by project:
   commit SHAs, files touched, passing/failing tests, and links to ADRs or plans.
3. **Formulate learning questions.** Follow the learning contract. Select 0-3 questions
   from substantive work (architectural decisions, invariants, trade-offs, hard bugs).
   Skip routine work. Prepare hidden expected answers grounded in the diffs. Zero questions
   is a valid outcome if work was routine.
4. **Author scaffold draft.**
   - **Learning mode** (session mode, see profile): write draft with `status: draft`. Include
     `assessed_commits`, `## Facts (Agent)` grouping commits and artifacts, `## Learning & Reasoning (User)`
     with question headers and blanks (`[Your answer / explanation]`), and an empty `## Open / Gaps`.
     Stage draft in configured notes inbox (e.g. `00-inbox/`) and prompt me to fill the blanks.
   - **Delivery mode**: draft concise facts and brief summary without blanks, avoiding promotional
     praise ("masterfully", "expert").
5. **Review completed scaffold.** When evaluating a filled draft:
   - Check answers against code evidence and invariants.
   - Fill `## Feedback & Calibration (Agent)`: label points (`correct`, `missing`, `wrong`,
     `unsupported`) and provide calibration rubric checklist (Invariant, Edge cases, Trade-offs)
     with assistance level.
   - Keep my original wording intact; never overwrite my answers with AI summaries.
   - Move unresolved points to `## Open / Gaps`. Set `status: completed`.
6. **Hand off to `document` or `draft-curation`.** Pass completed journal to stage or relocate.

## Your call
- **Backlog triage**: whether to process older unassessed work before today.
- **Review questions**: whether questions target the right decisions, or to skip any question.
- **Save destination**: confirm final journal location (default: `03-records/journal/YYYY-MM-DD.md`).

## Done when
- Scaffold draft is staged with blanks (Phase 1), or filled scaffold is evaluated and completed (Phase 2).

## Hands off to
- `draft-curation`: to curate and relocate completed journal from inbox to canonical archive.
- `practice`: if an unresolved gap warrants an isolated deliberate practice drill.
- `diagnose`: if reflection identified an active, unexplained system failure.
