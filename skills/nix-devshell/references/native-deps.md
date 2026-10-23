# Native dependencies, compilers, and linking

Used at step 3 when anything is compiled or linked, and at step 7 for header, library, compiler,
or foreign-binary failures. Labels: [compatibility.md](compatibility.md#evidence-labels).

## Keep the mechanisms apart

Four different things can make a library usable. Diagnose which one the build actually relies
on before adding anything:

1. **Output selection**: nixpkgs packages can have several outputs (`out`, `lib`, `dev`, ...);
   contents vary per package. `Unresolved`: which output a bare package reference contributes
   (for example whether headers from `dev` arrive) is package- and revision-dependent. When a
   consumer needs an include or library path, inspect the actual outputs in the **pinned**
   nixpkgs (commands in [compatibility.md](compatibility.md#checking-the-pinned-revision)) and
   select one explicitly (`pkgs.zlib.dev`) if needed.
2. **Setup hooks**: shell code provided by individual packages. `Established` (nixpkgs manual,
   setup-hook overview; current setup.sh): hooks run for inputs and may add compiler flags,
   pkg-config paths, CMake metadata, or other variables, but only when that package ships an
   applicable hook. There is no universal list of variables a library will set.
3. **Compiler wrapper flags**: the nixpkgs compiler wrapper adds include and linker flags for
   inputs. `Unresolved`: which variables carry them, and their exact behavior, vary by platform
   and revision; read them from the shell (`nix develop --command env`) rather than assuming.
4. **Build-system discovery**: `pkg-config` (reads `.pc` files), CMake `find_package`, Meson,
   or hard-coded flags such as `-lz`.

Rule: add `pkg-config` only when the build queries `.pc` metadata (a `pkg-config` call in a
Makefile, `PKG_CHECK_MODULES`, Meson `dependency()`, a crate's `pkg-config` build dependency).
A Makefile that only passes `-lfoo` usually needs the library and a working compiler, not
pkg-config. `Recommended` basis: Ayats 2023 explains outputs and pkg-config use for C/C++.

## Placing native inputs

- Compiler needed: use `mkShell`, not `mkShellNoCC`.
- Libraries the program links against: `buildInputs`. Tools that run during the build
  (`pkg-config`, `cmake`, `ninja`, code generators): `nativeBuildInputs` or `packages`.
  The roles matter most when cross-compiling ([design-decisions.md](design-decisions.md#6-where-each-dependency-goes)).
- Language extensions compiled by a package manager (Python wheels, Node native modules, Rust
  `-sys` crates) need the compiler and the C library in the shell too, even when the project
  "is not C".

## Selecting a compiler

- `Established` pattern, revision-sensitive: nixpkgs defines `mkShellNoCC` as
  `mkShell.override { stdenv = stdenvNoCC; }`. The same shape selects a compiler, for example
  `(pkgs.mkShell.override { stdenv = pkgs.clangStdenv; }) { ... }`. Evidence: the nixpkgs
  definition and a nixpkgs-22.05-era Discourse thread ("How to make mkShell to use clang's
  stdenv"); neither is a contract for every later revision.
- `Unresolved`: putting `clang` in `packages` does not guarantee it becomes `CC`; the earlier
  claim that it always collides was not established.
- Before using an override: confirm in the pinned nixpkgs that `mkShell` accepts `override`
  with `stdenv` and that the chosen stdenv attribute exists for each target system
  ([compatibility.md](compatibility.md#checking-the-pinned-revision)). If you cannot confirm,
  mark it unverified in the report and get the user's decision.

## Hardening flags

If a build fails on a hardening-related flag, read the actual compiler invocation and error.
Disable only the specific flag that the evidence implicates (for example via `hardeningDisable`
after checking the pinned API), never all hardening by default.

## Foreign binaries on NixOS

`Established` (nix.dev FAQ, "How to run non-Nix executables"; nixpkgs manual on FHS
environments): generic dynamically linked Linux binaries often fail on NixOS because there is no
global library path or FHS layout. A dev shell does not change that. Diagnose first
(`file <binary>`, the reported interpreter, `ldd` output, the exact error):

| Evidence | Likely cause | Options, in order |
|---|---|---|
| "No such file or directory" for a binary that exists | Missing ELF interpreter (for example `/lib64/ld-linux-x86-64.so.2`) | Use the nixpkgs package; patch interpreter and rpath (`autoPatchelfHook`); compatibility layer |
| Interpreter present, `cannot open shared object file` | Missing shared libraries | Nixpkgs package; supply or patch the libraries; host-configured `nix-ld` |
| Program expects `/usr/...` paths, launches bundled or self-updating executables | FHS path assumptions | `buildFHSEnv` (Linux only; check user-namespace support on the host) |
| Wrong architecture, missing runtime data, GPU/driver issues, application bugs | Different problem | Neither FHS nor nix-ld fixes these by itself |

`nix-ld` is NixOS host configuration: recommend it, do not apply it. None of these is a macOS
remedy. Language-downloaded artifacts (prebuilt wheels, npm binaries) fall in the same table.
