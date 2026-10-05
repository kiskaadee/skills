---
name: build-skill
description: >-
  Interactive design and refinement of agent skills. Use when the user types /build-skill
  to create a new skill or fix one that misbehaves.
disable-model-invocation: true
---

# Build Skill

## Use when
- `/build-skill [capability]`: turning a recurring workflow or failure into a skill.
- Fixing an existing skill after watching it misbehave on a real task.

## Steps
1. **Find the friction.** Ask what recurring workflow, pain point, or failure this addresses.
   If no capability was given, ask: "What keeps going wrong, or what do you keep repeating?"
2. **Pick the right tool.** Before writing a skill, check whether it is really:
   - a rule that always applies: one line in `AGENTS.md`;
   - a fixed command with no judgment: a script;
   - a human procedure: a guide in your docs or vault;
   - a procedure that needs agent judgment: a skill. Continue.
3. **Check overlap.** List the skills in this repo (`skills/`, `extensions/`). Ask where the new
   skill stops and which existing skill it hands off to.
4. **Size it.** Decide the shape: reference (facts consulted on demand), transformation
   (input to output), procedure (steps with checks between them), or interview (rounds of
   questions). Add gates or checkpoints only for a failure you can name.
5. **Write a short spec:** name (= slash command), description, steps, "Your call" items,
   done-when signal, hand-offs, files in `references/` or `scripts/` if any.
6. **Write it** in this repo following [references/skeleton.md](references/skeleton.md),
   then run the checks in [references/checklist.md](references/checklist.md).
7. **Dogfood.** Run it on a real task, read the agent's actual turns, and fix the smallest
   thing that went wrong (see the checklist's refinement table). Re-run a case that worked
   before to make sure nothing regressed.

Write only in this repo. Never create copies elsewhere or wrapper skills for slash commands.

## Your call
- Rule, script, guide, or skill? (step 2)
- What the skill refuses to own. (step 3)
- **Approve the spec before any file is written.** (step 5)
- Whether a dogfood failure is worth a fix, or acceptable.

## Done when
- The skill passes the checklist and one real dogfood run behaves as the spec says.

## Hands off to
- `git-commit`: to commit the new or changed skill.
