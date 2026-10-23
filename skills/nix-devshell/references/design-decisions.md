# Design decisions

Used at step 3. Pick each option from repository evidence; none of these is a universal default.
Evidence labels (`Established`, `Recommended`, `Contextual`, `Synthesis`, `Unresolved`) are
defined in [compatibility.md](compatibility.md#evidence-labels).

## 0. What a dev shell is

- `Established` (Nix 2.35 `nix develop` manual): `nix develop` starts Bash with an environment
  nearly identical to a derivation's build environment. Classic `nix-shell` is related but not
  identical in every detail.
- `Established`: neither command is a container or sandbox. Commands run as the user, with the
  user's filesystem, network, home directory, and host configuration.
- `Established`: `mkShell`, `stdenv`, `packages`, `buildInputs`, `nativeBuildInputs`,
  `shellHook`, and `lib.genAttrs` are nixpkgs conventions, not Nix language constructs. Language
  questions go to the Nix manual; constructor behavior goes to the pinned nixpkgs.
- `Recommended` (2025 Discourse thread "Looking for clarity on Nix developer shells"): use
  `mkShell` / `mkShellNoCC` for nixpkgs-based shells. That thread reports practical problems
  when a bare derivation bypasses setup hooks. A raw derivation is a deliberate alternative that
  must provide what its consumer expects, not something that is impossible.

## 1. Flake, classic shell.nix, or both

Inputs: existing files, Git state, contributors, CI, Nix version and enabled features, pinning
and update policy, explicit user request. An existing workflow wins unless a requirement says
otherwise.

| Workflow | Fits when | Trade-offs |
|---|---|---|
| Flake `devShells` | Flake already present; a committed input lock is wanted; contributors and CI can use the flake CLI | Lock pins the input graph. Flake features are still marked experimental upstream (Nix 2.35); distributions may enable them. Git-backed source omits untracked paths. |
| Classic `shell.nix` | Existing nix-shell workflow; flakes unavailable or disallowed; user asks for it | No flake.lock. Uses ambient `<nixpkgs>` unless an explicit pinning mechanism is added. |
| Both | Contributors need both commands and the extra maintenance is acceptable | Keep one canonical definition and have the other reuse it, to avoid drift. |

`Contextual`: the sources disagree by audience. Austin's DEV tutorial ("How I've Been Using Nix
Flakes", Feb 19, references nixos-24.11) values flake.lock. Ayats ("The Nix development
workflow", May 28 2023) recommends shell.nix when simplicity matters and you are unsure, and
shows both. Neither is the rule. Ask the user only if the choice changes how people work and
evidence gives no safe default; otherwise recommend the smallest fit and state this trade-off.

## 2. Which command does what

- `nix develop`: enter a derivation's build environment, usually the flake's devShell.
- `nix-shell`: classic shell workflow; reads `shell.nix` (or `default.nix`).
- `nix shell`: temporarily adds packages to PATH. Right for one-off tools; it does not define a
  project shell.
- `nix run`: runs an app or package's program; not an interactive dev shell.

`Synthesis`: a tool the project needs every day (build, lint, test, formatter named in CI or
docs) belongs in the devShell. A tool needed once by one person (poke an endpoint, inspect a
file) is a `nix shell nixpkgs#<pkg>` call, not a devShell edit. Exact options differ by Nix
version; check the local command reference.

## 3. nixpkgs inputs and lock policy

- `Established` (Nix 2.35 flake reference): `flake.nix` may name an unlocked reference;
  `flake.lock` records the resolved input graph.
- `Established`: a lock pins inputs. It does not pin Nix itself, host state, runtime behavior,
  package availability, or later downloads by npm, pip, cargo, and similar tools.
- `Contextual`: an indirect registry reference is a convenience choice, not automatically an
  error. For shared projects make the source and update policy visible, and follow the project's
  existing lock convention.
- `Contextual`: GitHub and channels.nixos.org tarball inputs differ in availability, caching,
  API limits, and dependency-bot support (Sep 2026 Discourse thread "PSA: Use nixos.org tarballs
  for your flake inputs!", version-specific and evolving). Locking an input, a bot updating it,
  and the binary cache having its builds are three separate questions. See
  [compatibility.md](compatibility.md#update-tooling-and-tarball-inputs).
- `Contextual`: `inputs.<name>.inputs.nixpkgs.follows = "nixpkgs"` shares one nixpkgs node when
  that is compatible and intended. It is optional; a dependency may deliberately need its own
  pin. Multiple nixpkgs nodes are not automatically wrong.
- Never add an input that the requirements do not need.

## 4. Supported systems

- Derive systems from contributors, CI, and package availability. A single-system output is
  correct for a single-system project. Do not add four systems by default.
- `Contextual`, no consensus: inline `nixpkgs.lib.genAttrs` avoids an extra input for small
  flakes (Luc Perkins, "Best practices for Nix at work", Mar 24 2025, "Split things up"
  subsection argues for fewer inputs). flake-utils is used by Austin's tutorial and several
  "NixOS in Production" templates. flake-parts fits an existing modular project. In an existing
  project, keep whatever it already uses.
- For a package that exists only on some platforms, check its `meta.platforms` in the pinned
  nixpkgs and include it conditionally (for example `lib.optionals pkgs.stdenv.isLinux [ ... ]`)
  instead of adding or dropping systems. Darwin SDK behavior is nixpkgs-version-sensitive.

## 5. Shell constructor

| Constructor | Use when | Caveats |
|---|---|---|
| `pkgs.mkShell` | A C/C++ compiler or native build support is needed | Compiler, wrapper, hardening, and SDK details vary by platform and revision. Adding another compiler package does not necessarily make it `CC`. |
| `pkgs.mkShellNoCC` | No standard compiler toolchain is needed | A package manager may later compile native extensions and need a compiler. A smaller closure is not guaranteed. |
| Custom stdenv / `mkShell.override` | The project needs a specific compiler or toolchain | Version-sensitive. See [native-deps.md](native-deps.md#selecting-a-compiler). |
| `pkgs.buildFHSEnv` | Linux software that expects FHS paths | Linux only. See [native-deps.md](native-deps.md#foreign-binaries-on-nixos). |

## 6. Where each dependency goes

- `Established` for current nixpkgs master, `Unresolved` for other revisions: `mkShell` maps
  `packages` into `nativeBuildInputs`, and merges the input lists of `inputsFrom` derivations
  (dropping those derivations themselves) and their shell hooks. Check the pinned source before
  relying on exact merge or hook order ([compatibility.md](compatibility.md#checking-the-pinned-revision)).
- `packages`: concise list for ordinary shell tools where native-input semantics fit.
- `nativeBuildInputs`: tools that run on the build platform and their setup hooks.
  `buildInputs`: libraries for the host/target. They are not interchangeable by definition,
  especially when cross-compiling.
- `inputsFrom = [ self.packages.${system}.default ]`: reuse an existing package's build inputs,
  then add only the missing developer tools. The "NixOS in Production" `cowsay` template shows
  this. Inspect what is inherited before adding duplicates. Use it only when such a package
  exists; it is not a default.
- Native libraries, outputs, `pkg-config`, hardening: [native-deps.md](native-deps.md).

## 7. Environment variables and shellHook

- `Established` for nixpkgs 24.05 (nix.dev "Declarative shell environments" tutorial, which
  pins 24.05), `Unresolved` for other revisions: flat, non-reserved, string-coercible mkShell
  attributes such as `GREETING = "hello";` become shell variables. Names must not collide with
  derivation attributes. Variables the shell protects from attribute overrides need `shellHook`
  (the tutorial's "environment variables" and "startup commands" sections).
- `Unresolved`: a nested `env = { ... }` attribute is a `mkDerivation` structured-attributes
  interface, not an established mkShell API. Do not use it unless the pinned source supports it.
- `Recommended` (Ayats 2023): `shellHook` is for runtime-dependent setup only. Keep it short,
  idempotent (safe to run twice), and quiet.
- `Synthesis`: a hook that `exec`s another shell can break `nix develop --command`, `nix-shell
  --run`, and environment capture (direnv). The idea comes from a user proposal in GitHub
  discussion #19 (AdrienLemaire, Jan 8 2025), not a recommendation. Avoid it unless required
  and tested for the actual invocation. To use your own interactive shell, prefer direnv.
- direnv / nix-direnv activate the environment in the user's existing shell (`use flake` or
  `use nix` in `.envrc`). They need direnv installed and `direnv allow` by the user.

## 8. Language toolchains

- Read `rust-toolchain.toml`, `Cargo.toml`, `go.mod`, `package.json`, `.nvmrc`,
  `pyproject.toml`, `.python-version`, and build scripts for required versions.
- Prefer the matching nixpkgs package when its version fits (check in the pinned revision). Use
  an overlay or another pinning method only when an exact version or target requires it, and
  treat that as an input-adding decision for the user.
- `Contextual`: a hybrid setup, where Nix supplies runtimes, compilers, and native libraries and
  the ecosystem lockfile manages application dependencies, is often practical. It does not make
  those later downloads Nix-reproducible. Follow the project's package-manager conventions.
