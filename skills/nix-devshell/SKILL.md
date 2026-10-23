---
name: nix-devshell
description: >-
  Authors, extends, validates, and troubleshoots project Nix development shells (flake
  devShells or classic shell.nix) from repository evidence. Use when creating or editing a
  devShell, adding tools or native libraries to one, choosing between a flake and shell.nix,
  or when nix develop or nix-shell fails to evaluate, build, start, or compile the project.
---

# Nix Dev Shell

## Use when
- Creating, extending, or repairing a project's development shell, or diagnosing why it fails.
- Not for NixOS or Home Manager configuration, packaging the project itself, production
  containers, or devenv/devbox/flox. Lock updates go to `inspect-flake-update`.

## Steps
1. **Inspect before deciding.** Read the Nix files, `flake.lock` (pinned nixpkgs revision,
   or record that none is present), `.envrc`, language manifests, build scripts, CI,
   contributor docs, `git status`, and `nix --version` with enabled features. Write a short
   inventory of what exists and which conventions (workflow, helper library, systems,
   constructor, input policy) you will keep.
2. **Establish requirements** from that evidence: tools, runtimes, native libraries, compiler,
   env vars, startup behavior, project commands, target systems. Ask only about gaps that
   change the design and cannot be read from the repo.
3. **Choose the design** with [references/design-decisions.md](references/design-decisions.md):
   keep the existing workflow, add only required systems and inputs, pick the smallest option
   that meets the requirements. If anything is compiled or linked, also read
   [references/native-deps.md](references/native-deps.md) before adding libraries or flags.
4. **Check version-sensitive mechanisms** (compiler overrides, env attributes, output selection,
   hooks, platform metadata) against the pinned revision using
   [references/compatibility.md](references/compatibility.md). If you cannot check, say so and
   either take a route that does not depend on it or ask.
5. **Implement** in the project's existing style; syntax pitfalls and illustrative (unexecuted)
   patterns are in [references/authoring-patterns.md](references/authoring-patterns.md).
   Create and edit files only. Never run `git add`, `git commit`, `git stash`, or anything else
   that changes the index or history. A new untracked file in a Git-backed flake is invisible
   to flake evaluation: say so and record it as a required user action.
6. **Validate progressively** with the four levels in
   [references/validation-troubleshooting.md](references/validation-troubleshooting.md):
   evaluation, realization and shell start, environment check, project command. Run the
   levels that apply, in order. A passing level is never evidence for a later one.
7. **Troubleshoot** by first naming the failing phase (evaluation, fetching, realization, shell
   start, compilation, runtime) from the actual error, using the symptom table in the same
   reference. Then follow `diagnose` for hypotheses and checks. Try the smallest justified fix;
   do not rewrite working parts (for example a whole `shellHook`) to fix one line.
8. **Report** in the format below.

## Report
- **Changes**: files created or edited, and the design choice with its evidence.
- **Validation**: one row per level: `passed` or `failed` with the exact command and the
  observed output excerpt; `blocked` with the exact cause (for example "`flake.nix` untracked,
  Git-filtered evaluation cannot see it"); or `not run` with the reason. Never list a command
  you did not run in this session. Checks that do not depend on the blocked files still run,
  but are not presented as proof that the shell works.
- **Unverified**: version-sensitive behavior not checked against the pinned revision,
  platforms not tested, and anything inferred rather than observed.
- **User actions**: for example, track new files (by hand or with `git-commit`) and rerun
  the blocked checks.

## Your call
- Flake, classic shell.nix, or both, when the repo shows no preference and the choice changes
  how people work. Otherwise recommend the smallest fit and state the trade-off.
- Adding systems, flake inputs, or helper libraries (flake-utils, flake-parts).
- Enabling unfree packages.
- Host-level fixes (nix-ld, NixOS configuration): recommend, never apply.
- Relying on a version-sensitive mechanism you could not verify for the pinned revision.

## Done when
- The agreed files exist or are changed, the Git index and history are untouched, and the
  report has a row for every validation level.

## Hands off to
- `git-commit`: to track or commit the new and changed files.
- `diagnose`: when the root cause lies outside Nix (application bug, host fault).
- `inspect-flake-update`: to review a lock update.
