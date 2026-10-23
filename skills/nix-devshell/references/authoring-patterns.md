# Authoring patterns

Used at step 5. Write in the project's existing style first; these are fallbacks and pitfall
checks. Labels: [compatibility.md](compatibility.md#evidence-labels).

> None of the snippets below has been evaluated, built, or entered. They are starting points.
> Confirm package names, systems, and APIs against the pinned nixpkgs before relying on them.

## Nix syntax pitfalls (`Established`, Nix language manual and nix.dev "Nix language basics")

- Every binding in `{ ... }` and `let ... in` ends with `;`. `{ a.b = 1; }` means
  `{ a = { b = 1; }; }`.
- Lists are whitespace-separated, no commas. Function application binds tighter than list
  construction, so `[ pkgs.python3.withPackages (ps: [ ps.requests ]) ]` is a two-element list
  (a function and a lambda) and fails during evaluation (commonly "cannot coerce a function to
  a string"). Parenthesize calls inside lists:
  ```nix
  packages = [ (pkgs.python3.withPackages (ps: [ ps.requests ps.pytest ])) ];
  ```
- `inherit (pkgs) git curl;` copies named attributes. `with pkgs; [ git curl ]` brings `pkgs`
  into scope, but explicit `let` and function bindings shadow `with`: if `system` is bound by
  `let`, `with pkgs; [ system ]` gives the `let` value, not `pkgs.system`. Avoid nested
  `with a; with b;`; prefer `pkgs.<name>` or `inherit` for short lists.
- Indented strings `'' ... ''` (used for `shellHook`): `${expr}` is Nix interpolation at
  evaluation time. Write `''${BASH_VAR}` to emit a literal `${BASH_VAR}` for Bash; plain
  `$VAR` without braces passes through. Write `'''` for a literal `''`.

## mkShell argument reference (`Contextual`; check the pinned API)

```nix
pkgs.mkShell {
  packages = [ pkgs.rustc pkgs.cargo pkgs.rust-analyzer ];  # tools
  nativeBuildInputs = [ pkgs.cmake pkgs.ninja ];            # build-platform tools, hooks
  buildInputs = [ pkgs.openssl pkgs.zlib ];                 # libraries linked against
  inputsFrom = [ ];                                         # reuse a package's inputs
  RUST_BACKTRACE = "1";                                     # flat env attribute
  shellHook = ''export REPO_ROOT="$PWD"'';                  # runtime setup only
}
```

Include only the arguments the requirements need. The roles are explained in
[design-decisions.md](design-decisions.md#6-where-each-dependency-goes).

## Pattern 1: minimal flake, one intended system

```nix
{
  description = "Project development shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { nixpkgs, ... }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages = [ pkgs.git ];
      };
    };
}
```

Replace the system with the project's actual one(s); add systems only when required and the
dependencies support them. The nixpkgs branch is a project decision (see
[design-decisions.md](design-decisions.md#3-nixpkgs-inputs-and-lock-policy)).

For several systems without an extra input (`Contextual`, standalone minimal flake pattern):

```nix
{
  description = "Multi-system development shell without extra inputs";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-darwin" ];   # only the systems the project needs
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShellNoCC {
          packages = [ pkgs.jq ];
        };
      });
    };
}
```

## Pattern 2: classic shell using the caller's package set

```nix
# shell.nix
{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShellNoCC {
  packages = [ pkgs.nodejs pkgs.pnpm pkgs.typescript-language-server ];
}
```

This follows the caller's `NIX_PATH` and is not a shared pin. For collaboration use the
project's existing pinning mechanism or a verified revision and hash. Never write a placeholder
hash and present it as runnable.

## Pattern 3: direnv

`.envrc` with `use flake` (flake) or `use nix` (shell.nix), per Ayats 2023 and Austin's
tutorial. Requires direnv (and usually nix-direnv) and the user's own `direnv allow`; do not run
`direnv allow` on the user's behalf.

## Platform-conditional packages

```nix
packages = [ pkgs.jq ] ++ pkgs.lib.optionals pkgs.stdenv.isLinux [ pkgs.inotify-tools ];
```

Check the package's `meta.platforms` in the pinned nixpkgs first
([compatibility.md](compatibility.md#checking-the-pinned-revision)).
