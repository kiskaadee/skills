---
name: journal-builder
description: >-
  Turn a day's accumulated engineering history into a structured journal through
  collaborative reconstruction, locked learning objectives, and a closed assessment loop.
---

# Journal Builder

## Use when
- `/journal-builder [YYYY-MM-DD]` or `/journal [YYYY-MM-DD]` (defaults to today).
- End of a workday or sprint to review history, test understanding, and record learning edges.
- Not for standalone changelogs; use git log directly.
- Not for deliberate coding practice drills; use `practice`.

## Steps
1. **Target the day and check history.** Establish the date window from argument or today.
   Read events from the ledger (e.g. `commit-log.csv`) or recent repository `git log`.
   - **Provenance check**: Read `assessed_commits` frontmatter across existing journals.
     Only events whose full 40-character SHA is absent proceed as unassessed work.
   - **Backlog check**: If unassessed events exist from prior dates, surface them and ask
     whether to process the older backlog chronologically first.
   - **Resolve locations**: Resolve project identities to local paths using the agent profile.
2. **Reconstruct collaboratively.** Inspect resolved repositories (diffs, tests, docs).
   Formulate the reconstruction checkpoint (sources, narrative, domains, uncertainties).
   Pause and confirm the context before formulating any questions.
3. **Lock learning objectives.** Once reconstruction is confirmed, select the smallest useful
   set of atomic learning objectives from substantive work. Formulate a hidden expected answer
   and rubric before asking. Skip routine work.
4. **Run the assessment loop.** Present one objective and question at a time.
   Expect either `Answer: <explanation>` or `Skip: <reason>`.
   After every answer, give concise formative feedback: what was correct, what is missing
   or imprecise, and the decision. Never pass an answer that omitted material understanding.
   - **Demonstrated**: core understanding articulated -> mark Achieved, move to next.
   - **Partially demonstrated**: material understanding missing -> targeted follow-up question.
   - **Incorrect / Unresolved**: provide smallest evidence (code line, diff, log) -> retry.
   - **Skip: I'm exhausted**: mark Deferred and move to next.
   - **Retries fail or Skip: I don't get it**: mark Unresolved (learning edge) and continue.
5. **Synthesize the candidate journal.** Include `assessed_commits` in YAML frontmatter.
   Structure body with Wins by project, Decisions/Artifacts, Mistakes & Learning Edges
   (with objective outcomes), and Technical Reflections.
6. **Hand off to `document`.** Pass the candidate journal to `document` to classify,
   author, and stage the draft. Do not choose or prompt for storage destinations.

## Reconstruction checkpoint
Before locking objectives, present the reconstructed context:
- **Sources**: Inspected repos, commit SHAs, related docs or notes.
- **Narrative**: What was built, refactored, or tested, and observed results.
- **Domains**: Technical concepts involved (e.g. auth flows, token dynamics).
- **Uncertainties**: Missing context, unstated rationale, or ambiguous intent.
Pause for confirmation: "Does this reconstruction match the work you want to review?"

## Your call
- **Backlog triage**: whether to process older unassessed work before today.
- **Confirm reconstruction**: whether sources, narrative, and domains match your actual work.
- **Respond to objectives**: provide `Answer: ...` or `Skip: <reason>`.

## Done when
- All locked learning objectives are assessed and candidate journal is handed off to `document`.

## Hands off to
- `document`: to author and stage the candidate journal draft.
- `practice`: if an unresolved learning edge warrants an isolated deliberate practice drill.
- `diagnose`: if reflection identified an active, unexplained system failure.
