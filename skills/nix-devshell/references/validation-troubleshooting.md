# Validation and troubleshooting

Used at step 6 (validation), step 7 (troubleshooting), and step 8 (reporting).
Labels: [compatibility.md](compatibility.md#evidence-labels).

## 1. Execution phases (`Established`)

Every failure happens in a specific phase. Name the phase from the error output before proposing
a fix:

| Phase | Typical work | Boundary and common failures |
|---|---|---|
| Evaluation | Parse and evaluate Nix expressions; produce `.drv` descriptions | Syntax errors, missing attributes, type errors ("cannot coerce a function to a string"), unfree rejection, missing local files omitted from a Git-backed flake source. Flake purity restricts mutable evaluator state; classic expressions may read `<nixpkgs>` from `NIX_PATH`. |
| Source / dependency acquisition | Fetch flake inputs, tarballs, and source trees | even a locked input may still need to be fetched if not in the local store. Network, authentication, or substituter errors happen here, not in pure evaluation. |
| Realization / build | Substitute from binary cache or build required derivations | Unavailable substitutes, unsupported system/package (`meta.platforms`), upstream build failures. |
| Shell initialization | Populate environment variables, run package setup hooks, run `shellHook` | Broken `shellHook` quoting, non-zero exit in a hook, `exec` replacing the shell and breaking `--command` / direnv capture. |
| Compilation / build inside shell | Run the project's compiler, linker, or build tool inside the realized shell | Missing headers (`.dev` output not selected), missing libraries, missing `pkg-config` when build queries `.pc`, compiler hardening flags rejecting code, wrong compiler/stdenv. |
| Runtime inside shell | Run compiled binaries, tests, or downloaded tools | Dynamic linker / ELF interpreter missing on NixOS for prebuilt Linux binaries, missing runtime shared libraries, host state differences. |

`Established`: evaluation success does not prove realization, shell startup, compilation, or
runtime behavior.

## 2. Progressive validation levels

Pick the commands that match the project's workflow (`nix develop` for a flake, `nix-shell` for
`shell.nix`). Run applicable levels in order:

| Level | Example commands | What it proves | What it does NOT prove |
|---|---|---|---|
| 1. Evaluation | `nix flake show`; `nix eval .#devShells.<system>.default.drvPath`; `nix-instantiate shell.nix` | Expression parses and produces a derivation for that system | That inputs can be fetched/built, that the shell starts, or that other systems evaluate |
| 2. Realization + shell start | `nix develop --command true`; `nix-shell --run true` | Required store paths exist on this host and the shell initializes for command mode | That tools have expected versions, that interactive prompts work, or that the project builds |
| 3. Environment check | `nix develop --command sh -c 'command -v <tool> && <tool> --version'`; `nix develop --command printenv <VAR>`; `pkg-config --modversion <lib>` (only if the build uses `pkg-config`) | Named tools, versions, and variables are present in the shell on this host | That compilation, linking, or project commands succeed |
| 4. Project command | `nix develop --command <build/test/lint command>` (or `nix-shell --run ...`) | That specific command succeeded on this host with current inputs | Other commands, other target systems, or unpinned ecosystem downloads |

### Where `nix flake check` fits

`Established` (Nix 2.35 `nix flake check` manual): `nix flake check` evaluates recognized flake
outputs and builds derivations in `checks.<system>`. It does **not** enter `devShells` or run
project build commands unless a check derivation explicitly does so. Report it as an output/check
validation, never as proof that the devShell starts or compiles the project.

### Reporting rules and blocked checks

- Report every level as `passed`, `failed`, `blocked`, or `not run`.
- For `passed` and `failed`, include the exact command run and a concise excerpt of the observed
  output. Never report a command that was not executed in this session.
- **Untracked files in Git-backed flakes**: when a newly created `flake.nix` or imported local
  file is untracked, Git-filtered flake evaluation cannot see it.
  - Do **not** run `git add` (staging belongs to the user / `git-commit`).
  - Do **not** substitute `path:.` by default (it bypasses Git source filtering, copies the whole
    directory including untracked files into the Nix store, and does not test what contributors
    will run).
  - Mark the flake-dependent levels as `blocked: <file> is untracked, so Git-filtered flake
    evaluation omits it`.
  - Still run any check that does not depend on the untracked flake (static review of the file,
    syntax check with `nix-instantiate --parse <file>`, or validation of an existing `shell.nix`),
    and state clearly that parsing does not prove evaluation, realization, or runtime.
  - Under **User actions**, ask the user to track the file (manually or via `git-commit`) and
    rerun the blocked levels.

## 3. Symptom-to-evidence table

Treat symptoms as hypotheses. Inspect first, then make the smallest justified change.

| Symptom | Phase | What to inspect first | Smallest next step |
|---|---|---|---|
| Flake says a visible local file does not exist | Evaluation | `git status` (is the path untracked?) | Explain Git source filtering; do not stage; ask user to track the path (or use `git-commit`). |
| `experimental Nix feature 'nix-command' / 'flakes' is disabled` | CLI / Evaluation | `nix --version`, `/etc/nix/nix.conf`, `~/.config/nix/nix.conf`, project docs | Follow the project's documented invocation or use classic `shell.nix` if supported. |
| `attribute 'devShells.<sys>.default' missing` or unsupported system | Evaluation / Realization | Flake outputs and package `meta.platforms` in pinned nixpkgs | Add only required systems; wrap OS-specific packages in `lib.optionals`. |
| `cannot coerce a function to a string` in package list | Evaluation | Error trace and the `packages` / `buildInputs` list syntax | Parenthesize function application inside lists (`(pkgs.foo.withPackages ...)`), or pass required args. |
| Unfree package rejected | Evaluation | Exact package name in trace and repo unfree policy | Ask the user or follow existing repo config; never enable `allowUnfree` silently. |
| Header (`.h`) or library (`-l...`) not found | Compilation | Build log, compiler command, package `outputs` in pinned nixpkgs, whether build calls `pkg-config` or CMake | See [native-deps.md](native-deps.md): add the missing library to `buildInputs`, select `.dev` if required, and add `pkg-config` to `nativeBuildInputs` only if the build queries `.pc` files. |
| Build fails with `-Werror=format-security` or similar wrapper flag | Compilation | Exact compiler error and active hardening flags | Narrowly disable the specific flag (for example `hardeningDisable = [ "format" ];` after checking pinned nixpkgs), not `all`. |
| `clang` added to `packages` but `cc` is still GCC | Compilation | `nix develop --command which cc` and `echo $CC` | Standard `mkShell` stdenv supplies `CC`; see compiler override in [native-deps.md](native-deps.md#selecting-a-compiler). |
| Prebuilt Linux binary fails with `No such file or directory` or missing `.so` on NixOS | Runtime | `file <bin>`, `patchelf --print-interpreter <bin>`, `ldd <bin>` | Diagnose interpreter vs shared libs vs FHS paths using [native-deps.md](native-deps.md#foreign-binaries-on-nixos). |
| `nix develop --command <cmd>` opens an interactive shell or ignores `<cmd>`, or direnv fails | Shell initialization | `shellHook` contents (especially `exec <shell>` or unconditional stdout noise) | Remove `exec` or guard interactive-only commands; keep existing working hook lines intact. |
| Slow evaluation or multiple `nixpkgs` copies in `flake.lock` | Evaluation | `nix flake metadata` input graph | Remove unused inputs; add `.follows = "nixpkgs"` only where sharing the root pin is compatible and intended. |
| `nix develop` fails on a custom raw derivation | Shell initialization | Derivation attributes and expected builder environment | Prefer `pkgs.mkShell` / `pkgs.mkShellNoCC` for nixpkgs packages. |
