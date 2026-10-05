# Skill Skeleton

Every `skills/*/SKILL.md` uses this shape. `build-skill` owns this file; other skills follow it and do not restate it.

```markdown
---
name: <command-name>          # what the user types: /<command-name>
description: >-
  <What it does, in one sentence. When to use it: concrete triggers.>
# disable-model-invocation: true   # only for skills that must never auto-trigger
---

# <Title>

## Use when
- Triggers (and one "not for X, use Y" line if confusion is likely).

## Steps
1. Numbered, imperative, in the order the agent should act.

## Your call
- Decisions the agent hands to the human instead of making them.
  Asked the way the global AGENTS.md "Your call" rule describes.

## Done when
- The observable signal that the skill is finished.

## Hands off to
- `<skill>`: when and why.
```

## Rules

- **80 lines max** for `SKILL.md`. Templates, long formats and branch rules go in `references/`.
- **Extra sections** are allowed only for a format used across several steps (e.g. `diagnose`'s checkpoint).
- **One owner per rule.** If another file already defines it (AGENTS.md, another skill), point to it.
- **Deletion test.** If removing a sentence would not change what the agent does, remove it.
- **Plain words.** No invented vocabulary. Prefer "decision" over "epistemic commitment".
- **No diagrams that repeat a list.** A numbered list is already the flow.
- **No em-dashes** in skill text.
- **The `name` is the slash command.** Never create a separate wrapper skill to expose a command.
