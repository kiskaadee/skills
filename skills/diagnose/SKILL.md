---
name: diagnose
description: >-
  Evidence-first troubleshooting. Use when the user types /diagnose or reports a bug,
  regression, failing build, or unexpected system behavior. Works from raw evidence to a
  proven root cause and a minimal, reversible fix, pausing at risky transitions.
---

# Diagnose

## Use when
- `/diagnose [symptom or error]`, or any "why is this broken / behaving strangely?" request.
- If I want to find the cause myself, switch to `practice`.

## Steps
1. **Observe.** Collect raw evidence first: exact error, logs, exit codes, a reproduction,
   what changed recently, how far the failure spreads. If no symptom was given, ask for it.
2. **Hypothesize.** List the plausible causes. Keep what the system reported separate from
   what you infer.
3. **Check, with a stated purpose.** Before each inspection command, say what it tests and
   which result would confirm or rule out a hypothesis.
4. **Narrow** until one cause is proven by evidence, not just plausible.
5. **Fix** with the smallest reversible change.
6. **Validate** locally (tests, linters, build), then **verify** in the environment where it
   actually failed.
7. **Clean up** every temporary probe (debug logs, env overrides, fixtures, test records)
   and confirm it's gone.

Scale the effort to the problem: a typo gets one line, not a ceremony.
Redact secrets (tokens, keys, connection strings) from anything you print or save.

## Checkpoints
At risky or multi-system transitions (domain narrowed, hypothesis ruled out, change applied,
ready to commit or deploy), pause and report in six short parts:
**Current state** (known vs unknown), **Reasoning**, **Changes**, **Validation**
(expected vs actual), **Next action**, **Recovery** (how to roll back).
For trivial issues, a one-sentence status is enough.

## Your call
- Which hypothesis to chase when the evidence is ambiguous.
- Approving any step that changes state: commit, push, deploy, data change.
- Whether the root cause taught something worth recording.

## Done when
- The fix is verified where the failure happened, and all temporary probes are removed.

## Hands off to
- `git-commit`: to package the fix once recovery is verified.
- `document`: when the investigation revealed a non-obvious failure mode or design flaw.
