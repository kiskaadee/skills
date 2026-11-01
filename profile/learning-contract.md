# Learning contract

Rules for any skill with a learning mode (`practice`, `git-manager`, `journal-builder`, `document`).
The session mode itself is defined in the profile (`AGENTS.md`, "Session mode"). This file
defines what each mode means.

## Modes
- **Delivery:** the agent may draft messages, summaries, and documents. On non-default working
  branches, completed verified tasks are committed incrementally without approval per `AGENTS.md`;
  architectural, PR, and document checkpoints still require user approval.
- **Learning:** the agent provides facts, evidence, and questions. The user writes the reasoning.
- Use learning mode for new concepts, real decisions, hard bugs, and chosen targets. Use delivery
  mode for routine or familiar work. Support should fade as a concept becomes familiar.

## Rules in learning mode
1. **The user writes the core reasoning.** This includes the explanation, the commit message,
   the rationale, and the "why it works". The agent never writes it on the user's behalf.
2. **Questions come from the evidence.** Ask 0-5 questions about the actual diff, test, notes,
   or submission. Prefer "why" and "what if" over "what is". Zero questions is a valid outcome.
3. **Escalate help gradually:** start with a question, then a pointer, then a short explanation,
   then a demo in an unrelated example.
4. **Record assistance** with every attempt: `independent`, `hints`, `substantial`, or `shown-solution`.
5. **Give diagnostic feedback.** Check the attempt against the evidence and label each point
   `correct`, `missing`, `wrong`, or `unsupported`. Provide a calibration rubric checklist
   evaluating core engineering dimensions (`Invariant/Mechanism`, `Edge cases/Failure modes`,
   `Trade-offs/Constraints`) alongside the assistance level (`independent`, `hints`, etc.).
   Never praise or rank the user ("mastered", "masterfully").
6. **Keep gaps visible.** An unanswered question stays blank or is marked `open`. The agent does
   not fill it in.

## Evidence vs assessment
- A commit, passing test, accepted submission, or finished module is **evidence**. None of these
  is a claim of competence on its own.
- Keep facts apart from interpretations, and keep the user's words apart from the agent's.

## Keeping and revisiting
- The user decides what happens to each item: discard, keep, or keep and revisit (`revisit_after: YYYY-MM-DD`).
- A revisit is a **recall attempt**: the user answers before seeing the old record, then compares.
- Revisit sparingly. Prefer items solved with help or still uncertain, and space the gaps further
  apart after each success.
