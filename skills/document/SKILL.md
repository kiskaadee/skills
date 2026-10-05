---
name: document
description: >-
  Decide whether a session produced knowledge worth keeping, pick the right document type
  (Discussion, ADR, Plan, Debug Record, Knowledge), and draft it. Use when the user types
  /document, or when another skill hands off a decision, root cause, or insight.
---

# Document

## Use when
- `/document` at the end of a session, or a handoff from `diagnose`, `practice`, `git-commit`.
- Routine fixes and chores need no document: a good commit message is enough.

## Steps
1. **Is it worth writing?** Default is no. Continue only if the session produced something
   non-obvious that someone (me, in six months) would benefit from reading: a decision, a
   surprising failure, a reusable insight.
2. **Classify by the kind of knowledge, not by the activity that produced it:**

| Knowledge                                             | Type         | Spec                                             |
| ----------------------------------------------------- | ------------ | :----------------------------------------------- |
| Why: exploration, alternatives, trade-offs            | Discussion   | [discussion](references/discussion-authoring.md) |
| What we decided (architecture)                        | ADR          | [adr](references/adr-authoring.md)               |
| How to build it: phases, constraints, done-definition | Plan         | [plan](references/plan-authoring.md)             |
| What broke and why (root cause)                       | Debug Record | [debug](references/debug-record-authoring.md)    |
| A general mental model or technique                   | Knowledge    | [knowledge](references/knowledge-authoring.md)   |

A rich session may justify more than one (e.g. Debug Record + Discussion). Split them; don't write one hybrid document.

3. **Draft** each document following its spec. Read the spec before writing.
4. **Avoid overlap.**  Each fact has one owning document: the Discussion owns the reasoning,
   the ADR the decision, the Plan the steps, the Debug Record the evidence, Knowledge the
   general lesson. Others link to it instead of repeating it. 
5. **Keep references portable**: Use relative paths or context-defined placeholders. Never write absolute file-system paths into documentation. 
6. **Save** to the location I choose (see below). Discussions and Debug Records are
   historical and never rewritten later. ADRs and Plans get `status: superseded` when replaced.

## Your call
- **Type(s)**: confirm the classification from step 2.
- **The key sentence**: before drafting, ask me to state the core in my own words: the
  decision, the root cause, or the insight. Build the draft around my sentence.
- **Insights:** when the core insight is unclear, ask about the intent behind important choices, rejected alternatives, and relevant trade-offs. Use these questions to validate the user's understanding, not to expand the scope of the session.
- **Where it goes**: offer 2-3 options, recommended first, e.g.
  default notes inbox (from profile) / the project's `docs/` / typed record folder.

## Done when
- The file exists at the chosen location, or we agreed no document is needed.

## Hands off to
- `git-commit`: to commit the document if it lives in a repo.
