# Compatibility, verification, and source boundaries

Used at step 4 (checking version-sensitive behavior) and step 8 (reporting unverified items).

## Evidence labels

Every claim in this skill's references carries one of five labels:

- `Established`: directly supported by official Nix / Nixpkgs reference manuals or inspected
  source code for the stated version.
- `Recommended`: supported by practical reports in the corpus (such as `mkShell` over naked
  derivations, or modest `shellHook`s), not a hard language rule.
- `Contextual`: depends on project workflow, team, or tooling; sources in the corpus legitimately
  disagree (for example flake vs `shell.nix`, `flake-utils` vs `lib.genAttrs`).
- `Synthesis`: operational agent policy derived to prevent common mistakes (inspect first,
  preserve conventions, never stage files silently, separate validation levels).
- `Unresolved`: behavior that varies across Nix or nixpkgs versions, platforms, or external tools
  and was not verified across all target revisions. Must be checked against the target project's
  pinned revision before relying on it.

## Compatibility baseline policy

Do not assume a numeric minimum Nix version or a universal supported nixpkgs release range:

1. **Use the target project's lock and baseline.** Read `flake.lock` (or classic pin in
   `shell.nix` / `npins` / `niv`) for the exact nixpkgs commit, and check `nix --version` plus
   enabled features on the host or CI config.
2. **Verify version-sensitive APIs against that pin.** If a project has no lock or declared
   baseline, state the evidence version you are drawing from and make the pin an explicit
   project decision.
3. **Never promise broader compatibility than you have verified.**

## Checking the pinned revision

When a task touches a version-sensitive mechanism, check the project's locked nixpkgs before
relying on it:

1. **Find the pinned commit** from `flake.lock` (`nodes.nixpkgs.locked.rev`) or `nix flake metadata`.
2. **Inspect via local evaluation against the locked input** when Nix is available:
   - Check package existence or outputs:
     `nix eval .#devShells.<system>.default` or
     `nix eval --inputs-from . nixpkgs#<pkg>.outputs`
   - Check platform support:
     `nix eval --inputs-from . nixpkgs#<pkg>.meta.platforms`
   - Locate or read nixpkgs source files in the local store if already fetched:
     `nix eval --inputs-from . --raw nixpkgs#outPath` (then read `pkgs/build-support/mkshell/default.nix`
     under that store path if present locally).
3. **If the locked source is not available locally and cannot be fetched**:
   - State clearly in the report what could not be verified against the pinned revision.
   - Prefer a conservative pattern that does not depend on the unverified detail, or ask the user
     before relying on it.

## Version-sensitive items (`Unresolved` unless checked on the target pin)

- **Experimental feature flags**: Nix 2.35 documentation still marks `nix-command` and `flakes`
  experimental upstream, though some distributions enable them by default. Check the host.
- **Output attribute names**: current manuals use `devShells.<system>.default` and warn on legacy
  `devShell.<system>`. Check the project's existing outputs and target Nix version.
- **`mkShell` internals**: current mutable nixpkgs `master` (`pkgs/build-support/mkshell/default.nix`)
  maps `packages` into `nativeBuildInputs`, merges selected `inputsFrom` attributes, drops the
  `inputsFrom` derivations themselves from the merged list, and concatenates their shell hooks.
  An immutable reference example is nixpkgs 23.11 commit `057f9aecfb71c4437d2b27d3323df7f93c010b7e`
  (used by the workspace's `cowsay` template), linked at:
  - `https://github.com/NixOS/nixpkgs/blob/057f9aecfb71c4437d2b27d3323df7f93c010b7e/pkgs/build-support/mkshell/default.nix`
  - `https://github.com/NixOS/nixpkgs/blob/057f9aecfb71c4437d2b27d3323df7f93c010b7e/pkgs/top-level/all-packages.nix`
  Note: that 23.11 pin is an example snapshot only, and its exact file text was not retrieved
  during static audit; verify against the target project's own lock if exact merge or hook
  ordering matters.
- **Multi-output `.dev` resolution and setup hooks**: which output a bare package reference
  selects, and which hooks populate `PKG_CONFIG_PATH`, `CMAKE_PREFIX_PATH`, or compiler wrapper
  variables, depend on the individual package and nixpkgs revision.
- **Environment variable attributes**: flat attributes (`FOO = "bar";`) are documented in the
  nix.dev tutorial pinned to nixpkgs 24.05. Nested `env = { ... };` is a `mkDerivation`
  structured-attribute interface and is not established as portable `mkShell` guidance across
  revisions.
- **Compiler / `stdenv` overrides**: `mkShell.override { stdenv = ...; }` is the nixpkgs pattern
  used by `mkShellNoCC` (and shown in a 22.05-era Discourse thread for `clangStdenv`), but the
  available stdenv variants and override behavior must be checked on the target revision and OS.
- **Platform and Darwin SDKs**: package availability and macOS SDK / framework handling change
  across nixpkgs releases. Never claim a shell works on Darwin or Linux unless verified on that
  platform or restricted to evaluated metadata.
- **`buildFHSEnv`**: Linux-only and depends on host user-namespace support.

## Update tooling and tarball inputs

- **Nix locking vs dependency bots**: Nix can lock both `github:NixOS/nixpkgs/...` and
  `https://channels.nixos.org/...` tarball URLs in `flake.lock`. Whether an automated bot can
  update that URL is a separate tool question.
- **Renovate scope**: Renovate's Nix manager documentation (reviewed at version 44.181.0; beta /
  opt-in) documents `flake.nix` with the `git-refs` datasource and delegates lock file
  maintenance to Nix. Exact handling of `channels.nixos.org` tarball URLs and compression formats
  depends on the Renovate version and endpoint configuration (discussed in the Sep 2026 Discourse
  thread "PSA: Use nixos.org tarballs for your flake inputs!").
- **Binary cache availability**: neither a GitHub URL nor a channel tarball URL guarantees that
  every derivation in a shell is prebuilt by Hydra.

## Source attribution

- **Manuals & external docs**:
  - Nix 2.34.9 / 2.35 Reference Manual:
    [nix develop](https://nix.dev/manual/nix/2.35/command-ref/new-cli/nix3-develop.html),
    [nix flake check](https://nix.dev/manual/nix/2.35/command-ref/new-cli/nix3-flake-check.html),
    [nix flake](https://nix.dev/manual/nix/2.35/command-ref/new-cli/nix3-flake.html),
    [Experimental features](https://nix.dev/manual/nix/2.35/development/experimental-features)
  - nix.dev:
    [Flakes concepts](https://nix.dev/concepts/flakes),
    [Declarative shell environments](https://nix.dev/tutorials/first-steps/declarative-shell),
    [FAQ: non-Nix executables](https://nix.dev/guides/faq.html#how-to-run-non-nix-executables),
    "Nix language basics" tutorial
  - Nixpkgs Manual:
    [Setup hooks](https://nixos.org/manual/nixpkgs/stable/#sec-setup-hooks),
    [FHS environments](https://nixos.org/manual/nixpkgs/stable/#sec-fhs-environments)
  - Mutable nixpkgs master references (not cross-version proof):
    [mkshell/default.nix](https://github.com/NixOS/nixpkgs/blob/master/pkgs/build-support/mkshell/default.nix),
    [stdenv/generic/setup.sh](https://github.com/NixOS/nixpkgs/blob/master/pkgs/stdenv/generic/setup.sh)
  - Renovate: [Nix manager docs](https://docs.renovatebot.com/modules/manager/nix/)
- **Corpus articles & book material** (used for context and practical reports, not normative specs):
  - Julien Ayats, "The Nix development workflow" (May 28, 2023)
  - Austin, "How I've Been Using Nix Flakes (And What You Can Do With Them)", DEV Community (Feb 19, references nixos-24.11)
  - NixOS Discourse, "Looking for clarity on Nix developer shells and their design" (Oct 27-29, 2025)
  - NixOS Discourse, "PSA: Use nixos.org tarballs for your flake inputs!" (Sep 2025 - Sep 2026)
  - NixOS Discourse, "Nix Flakes best practices question" (Mar-Apr 2021)
  - NixOS Discourse, "Tips&Tricks for NixOS Desktop" (May 2023)
  - NixOS Discourse, "How to make mkShell to use clang's stdenv" (2020 / nixpkgs 22.05 era)
  - AdrienLemaire, GitHub issue #19 "Best practices for dev shells" (Jan 8, 2025)
  - Luc Perkins, "Best practices for Nix at work" (Mar 24, 2025, includes "Split things up") and "Building a highly optimized home environment with Nix" (Sep 15, 2022, includes Nome)
  - Gabriella Gonzalez, *NixOS in Production* (chapters on Setup, Flakes, BigPicture, CI/CD, IntegrationTesting, and the `cowsay` template)
