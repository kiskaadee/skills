---
name: journal-builder
description: >-
  Turn a day's accumulated engineering history into a structured journal through
  evidence-based reconstruction, locked learning objectives, and a closed assessment loop.
---

# Journal Builder

## Use when
- `/journal-builder [YYYY-MM-DD]` or `/journal [YYYY-MM-DD]` (defaults to today).
- End of a workday or sprint to review history, test understanding, and record learning edges.
- Not for standalone changelogs; use git log directly.
- Not for deliberate coding practice drills; use `practice`.

## Steps
1. **Target the day and check history.** Establish the date window from argument or current day.
   Read events from the ledger (e.g. `commit-log.csv`) or recent repository `git log`.
   - **Provenance boundary**: A journal records the commit events incorporated into its
     reconstruction (under Decisions & Artifacts). These references serve as the durable boundary
     distinguishing previously assessed work from new ledger events.
   - **Backlog check**: If older ledger events exist that are not yet incorporated in any journal
     record, surface them and ask whether to process the older date first (preserve temporal fidelity).
   - **Incremental run**: If a journal record already exists for the target date, compare ledger
     events against incorporated commits. Only new substantive work proceeds to assessment.
2. **Reconstruct by project and domain.** Group new unassessed commits by project, then by
   technical domain (e.g. auth, deployment, architecture). Summarize what changed.
3. **Lock learning objectives.** Select the smallest useful set of independently assessable
   learning objectives from substantive work. Objectives must be atomic (one independently
   testable understanding). Formulate a hidden expected answer before asking. Skip routine work.
4. **Run the assessment loop.** Present one objective and question at a time.
   Expect either `Answer: <explanation>` or `Skip: <reason>`.
   After every answer, give concise formative feedback: what was correct, what is missing
   or imprecise, and the decision. Never pass an answer that omitted material understanding.
   - **Demonstrated**: core understanding articulated -> mark Achieved, move to next.
   - **Partially demonstrated**: material understanding missing -> targeted follow-up question.
   - **Incorrect / Unresolved**: provide smallest evidence (code line, diff, log) -> retry.
   - **Skip: I'm exhausted**: mark Deferred and move to next.
   - **Retries fail or Skip: I don't get it**: mark Unresolved (learning edge) and continue.
5. **Synthesize the candidate journal.** Structure the entry with Wins by project,
   Decisions/Artifacts, Mistakes & Learning Edges (with objective outcomes), and Technical Reflections.
6. **Hand off to `document`.** Pass the candidate journal to `document` to classify,
   author, and stage the draft. Do not choose or prompt for storage destinations.

## Your call
- **Backlog triage**: whether to process older unassessed work before today.
- **Confirm the day's scope**: whether the detected projects and domains match the day's work.
- **Respond to objectives**: provide `Answer: ...` or `Skip: <reason>`.

## Done when
- All locked learning objectives are assessed and the candidate journal is handed off to `document`.

## Hands off to
- `document`: to author and stage the candidate journal draft.
- `practice`: if an unresolved learning edge warrants an isolated deliberate practice drill.
- `diagnose`: if reflection identified an active, unexplained system failure.
