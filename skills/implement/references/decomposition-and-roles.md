# Step 1 Delta-Test Decomposition & Worker Roles

Defines Step 1 delta-test classification, the `<= 2`-file fast path, worker role
contracts, recycling and deadlock circuit breakers, and mandatory OS-level
non-interactive command wrapping.

---

## 1. Step 1 Delta-Test Decomposition

Before writing tasks or spawning workers, inspect the repository's existing test
suite on every seam affected by the target issue or rework finding. Classify
each affected seam into one of three states:

| Seam State | Meaning | Required Task Ordering |
| :--- | :--- | :--- |
| `covered (keep green)` | Existing tests already assert the target behavior and edge cases. | Do not add redundant tests; keep existing tests green after production edits. |
| `partial/weak (harden)` | Tests touch the seam but miss edge cases, error paths, or falsifiable assertions. | `test-writer` hardens tests first (observing failure on missing behavior), then `code-writer` satisfies them. |
| `missing (new Red test)` | No test covers the new behavior or bug reproduction. | `test-writer` writes a new failing Red test first, then `code-writer` implements the minimal Green fix. |

Record the resulting ordered deliverables directly in
`$(git rev-parse --git-common-dir)/implement-state/<branch_slug>.txt` per
[preflight.md](preflight.md) (unless `--dry-run` is active or the fast path
applies).

---

## 2. `<= 2`-File Fast-Path Criteria & Bailout

Auto-skip Step 1 decomposition and checkpoint file creation when **all** of the
following hold:
- The change is a localized fix or localized `code-review` rework item touching
  `<= 2` files.
- No new test seam is introduced (existing tests cover the behavior or a single
  localized assertion suffices).
- No public interface, schema, or architecture contract changes.

### Fast-Path Bailout Rule
If execution reveals that scope exceeds 2 files, requires a new test seam, or
impacts a public contract, stop the `1-worker` fast path immediately, run Step 1
delta-test decomposition, initialize `"$state_file"`, and switch to the
multi-task `test-writer` -> `code-writer` loop.

---

## 3. Worker Role Contracts

`implement` is a pure orchestrator: it never edits production code, never edits
tests, never performs code review, and never publishes PR review comments.

### Shared Invariants (All Workers)
- **Anti-recursion**: Never invoke `implement` or spawn nested workers.
- **Footer suppression**: Suppress any standalone `Suggested Next Step:` footer;
  return only a compact handoff summary (touched files, verification commands
  and exit codes, observed contract drift or blockers).
- **Mandatory non-interactive wrapping**: Execute all shell commands using the
  Section 5 wrapper and tiered timeouts.
- **No git history rewrites**: Leave commits and branch management to the
  orchestrator (`git-manager`), unless explicitly instructed to run read-only
  `git diff` / `git status`.

### `test-writer` Contract
- Owns Red tests and seam hardening for `missing` and `partial/weak` seams.
- Never implements production logic beyond minimal type/compilation stubs when a
  statically typed language requires them to compile the Red test.
- Runs targeted test commands to confirm the new or hardened test fails for the
  expected reason (Red) before returning.
- Runs repository lint/typecheck on touched test files and adds brief `Why:`
  comments for non-obvious test invariants or fixtures.

### `code-writer` Contract
- Owns the minimal production implementation that turns Red tests Green while
  keeping `covered` seams green.
- **Per-task hygiene** (mandatory before returning):
  - Run repository lint, formatter check, and typecheck on touched files.
  - Add or update docstrings on all new or modified public symbols.
  - Add concise `Why:` comments for non-obvious invariants, edge-case guards, or
    trade-offs (never narrating obvious code mechanics).
  - Update directly affected local markdown (such as adjacent module READMEs or
    inline usage docs impacted by the change).
- Report any detected Contract Drift (deviation from issue acceptance criteria,
  public interfaces/schemas, `ARCHITECTURE.md`, or `ROADMAP.md`) in the handoff
  packet so the orchestrator can record it in the Draft PR.

### `1-worker` Fast-Path Contract
- Used only when Section 2 fast-path criteria hold.
- Applies the localized fix and targeted verification in a single worker turn,
  enforcing all `code-writer` hygiene rules (lint/typecheck, docstrings, `Why:`
  comments, affected local markdown) and shared invariants.

---

## 4. Worker Recycling & Deadlock Circuit Breaker

- **3-4 Task Worker Recycling**: After every 3-4 completed tasks in a multi-task
  slice, retire the current `test-writer` and `code-writer` instances and spawn
  fresh workers. This prevents quadratic context growth and stale-file
  assumptions across long slices.
- **2-Turn Deadlock Circuit Breaker**: If `test-writer` and `code-writer` fail
  to converge on a single task after 2 back-and-forth turns (for example,
  disputed test seam, flaky environment, or ambiguous specification):
  1. Stop dispatching further retries on that task.
  2. Preserve `"$state_file"` untouched.
  3. Escalate to the human owner with the exact failure output and options to
     clarify the spec or hand off to `diagnose`.

---

## 5. Mandatory OS-Level Non-Interactive Command Wrapping

Embed this execution rule verbatim in every `test-writer`, `code-writer`, and
`1-worker` prompt:

```bash
CI=true GIT_TERMINAL_PROMPT=0 PAGER=cat setsid timeout -k 10 <N>s <cmd> < /dev/null
```

### Why This Wrapper Is Required
- `setsid` detaches the command from any controlling `/dev/tty` so interactive
  prompts cannot hang waiting for terminal input.
- `< /dev/null` closes stdin immediately.
- `CI=true`, `GIT_TERMINAL_PROMPT=0`, and `PAGER=cat` disable interactive CLI
  wizards, credential prompts, and pagers.
- `timeout -k 10 <N>s` sends `SIGTERM` after `<N>` seconds and escalates to
  `SIGKILL` 10 seconds later if the process ignores `SIGTERM`.

### Tiered Timeouts (`<N>`)
| Tier | Timeout | Applies To |
| :--- | :--- | :--- |
| Fast CLI | `60s` | Git commands, `gh` CLI queries, linters, formatters, typecheckers, quick scripts |
| Unit Tests | `180s` | Targeted unit test runs and local test suites |
| Cold Builds | `600s` | Cold compilation, container/Nix builds, and heavy fixture builds |
