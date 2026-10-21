---
name: practice
description: >-
  Socratic tutoring and delayed retrieval practice. Use when typing /practice or
  /practice review to learn concepts, solve LeetCode algorithms, or review due topics.
---

# Practice

## Use when
- `/practice [topic or problem]`, `/practice review`, LeetCode practice, "teach me".
- Works in any repo or as a pure concept question. No curriculum needed.
- Not for urgent production failures: use `diagnose`.
- Socratic practice procedure. If session mode is `delivery`, suggest switching
  to `learning` mode rather than changing it silently (see profile's "Session mode").

## Steps
1. **Check overdue revisits.** If invoked as `/practice review` or with no topic given, scan
   for practice records with `revisit_after <= today` (inbox, learning, docs). If any exist,
   surface up to 3 and ask whether to review one or start a new topic. When reviewing,
   execute recall-before-reveal per [references/revisit-protocol.md](references/revisit-protocol.md).
2. **Establish target.** For a new topic or algorithm problem, ask what I want to understand
   or build, and what my current mental model is.
3. **Help at lowest level that works**, moving up only when I am stuck:
   1. A question that makes me check my own assumption.
   2. Where to look: file/line range, docs section, or inspection tool.
   3. A short first-principles explanation of the missing concept, then hand control back.
   4. A minimal demo in an unrelated example (never in working code).
4. **Let me attempt it**: code, prediction, explanation, diagnosis, or algorithm approach.
   Ask me to read my own result before you comment.
5. **Review what I produced**: report calibration (rubric checklist + assistance level),
   label points (`correct`, `missing`, `wrong`, `unsupported`), then point at gaps.
6. **Direct answer on request**: give without resistance, then check with one follow-up.
7. **Wrap up and schedule**: what changed in understanding, primary sources, and offer
   a practice record with `revisit_after` interval per protocol.

Never edit files in working repo or run implementation commands unless explicitly asked.

## Your call
- **Revisit choice**: whether to review an overdue topic or start a new one.
- **Did I understand it?**: solve one transfer challenge or unaided re-solve before calling done.
- **Save a practice record?**: template [references/practice-record.md](references/practice-record.md)
  with computed `revisit_after`.

## Done when
- I solve the transfer challenge, complete the unaided revisit, or close the topic.

## Hands off to
- `document`: when a durable insight came out of the session.
- `git-commit`: it proposes slices and lists facts; I write the message and type the commit.
