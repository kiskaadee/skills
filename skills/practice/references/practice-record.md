# Practice Record Template

Default location: configured notes inbox (or project `docs/`) as `practice-YYYY-MM-DD-<topic>.md`.
Before saving, ask where it goes (2-3 options, configured notes inbox recommended).

```markdown
---
type: practice
date: YYYY-MM-DD
project: <project-name or none>
topics: [<topic-1>, <topic-2>]
status: completed | active
assistance: independent | hints | substantial | shown-solution
revisit_after: YYYY-MM-DD
---

# Practice: <topic or problem>

## Calibration
- **Assistance**: independent | hints | substantial | shown-solution
- **Rubric**:
  - Invariant / Mechanism: [✓ | ✗ | ~] <note>
  - Edge cases / Failure modes: [✓ | ✗ | ~] <note>
  - Trade-offs / Constraints: [✓ | ✗ | ~] <note>

## Starting point
The question, bug, or mechanism I set out to understand.

## How my mental model changed
- Before: what I assumed.
- After: the mechanism, invariant, or rule that clicked.

## Evidence I understood it
Transfer challenges, predictions, or explanations I got right without direct help.

## Still open
- Concepts to revisit.
- Primary references (official docs, specs, source paths).
```
