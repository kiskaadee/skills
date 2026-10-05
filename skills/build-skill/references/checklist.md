# Skill Checklist

Used by `build-skill` at step 6 (writing) and step 7 (dogfooding).

## Before calling a skill done

| Check | Question |
| :--- | :--- |
| One job | Is there one recurring problem this skill owns? |
| Clear edges | Does "Hands off to" say where it stops? Does "Use when" say what it is not for? |
| One owner per rule | Is any rule here already defined elsewhere (AGENTS.md, another skill)? Point to it instead. |
| Deletion test | Would removing each sentence change what the agent does? If not, remove it. |
| Observable finish | Does "Done when" name a concrete signal (test passes, file exists, user approved)? |
| Human decisions | Does "Your call" list the decisions that must stay with the user? |
| Size | Is `SKILL.md` 80 lines or less, with bulky material in `references/`? |
| Invocation | Should this ever auto-trigger? If not, set `disable-model-invocation: true`. |
| Description | Does it say what the skill does and name concrete triggers? (The agent decides from this alone.) |
| Public repo | No absolute home paths, no secrets. |

Add extra controls (hard gates, state files, checkpoints) only for a failure you have actually
seen. If you can't name the failure, don't add the control.

## Refining after a dogfood run

Change the smallest thing that explains what went wrong:

| Observed                                 | Smallest fix                                                                 |
| :--------------------------------------- | :--------------------------------------------------------------------------- |
| Skipped a verification step              | Make the step's proof observable and gate the next step on it.               |
| Ignored an important rule                | Move the rule into the numbered steps, where it is read at the right moment. |
| Procedure lost in detail                 | Move the detail to `references/`.                                            |
| Wandered into another skill's job        | Tighten "Use when" and "Hands off to".                                       |
| Repeated boilerplate                     | Cut the instruction or shorten it.                                           |
| Behaved correctly without an instruction | Delete the instruction.                                                      |

Then re-run a scenario that used to work, to confirm nothing regressed.

## Writing style

- Write like a developer explaining to another developer, not like an authority issuing orders.
- Explain the mechanism directly; skip pep talks and long lists of bans.
- Clean GitHub-flavored markdown. No em-dashes.
