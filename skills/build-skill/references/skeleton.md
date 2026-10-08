# Skill Skeleton

Every `skills/*/SKILL.md` uses this shape. `build-skill` owns this file; other skills follow it and do not restate it.

## Canonical Directory Structure

```text
skills/<skill-name>/
├── SKILL.md          # Required: Root instructions with YAML frontmatter
├── references/       # Optional: Deep documentation, schemas, and manuals
├── scripts/          # Optional: Deterministic executable scripts
├── resources/        # Optional: Templates, assets, or static data
└── examples/         # Optional: Reference cases and sample inputs/outputs
```

## SKILL.md Skeleton

```markdown
---
name: <command-name>          # Regex ^[a-z0-9-]+$ (lowercase alphanumeric and hyphens; slash command: /<command-name>)
description: >-
  <What it does in 3rd person. When to use it: concrete triggers for semantic routing.>
# disable-model-invocation: true   # Optional boolean: true prevents automatic model invocation (manual slash command only)
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

- **80 lines max** for `SKILL.md`. Templates, long formats, and branch rules go in `references/`.
- **Extra sections** are allowed only for a format used across several steps (e.g. `diagnose`'s checkpoint).
- **One owner per rule.** If another file already defines it (AGENTS.md, another skill), point to it.
- **Deletion test.** If removing a sentence would not change what the agent does, remove it.
- **Plain words.** No invented vocabulary. Prefer "decision" over "epistemic commitment".
- **No diagrams that repeat a list.** A numbered list is already the flow.
- **No em-dashes** in skill text.
- **The `name` is the slash command.** Must match `^[a-z0-9-]+$`. Never use underscores (`_`) or uppercase; never create a separate wrapper skill to expose a command.
- **Public repo hygiene.** Never hardcode user home paths (`/home/...`) or secrets.
