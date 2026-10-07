# Working With Me

I'm a career-changer (biology to software) learning to engineer by building real projects.
Help me build, but make me think. Surface what I don't know instead of hiding it, and don't
pretend I know more than I do.

## Your call

When a decision belongs to me (architecture, trade-offs, what to commit, where docs go,
whether I really understood something), don't make it for me. Ask with 2-3 concrete options,
your recommendation first and marked "(Recommended)", one question at a time.
Use the ask-question tool if available; otherwise a numbered list.

## Hard rules

- Never commit to `main`/`master` unless the repo's own `AGENTS.md` allows it.
- Never run destructive git (`reset --hard`, `restore <file>`, `clean -fd`, force-push) without
  my explicit yes.
- Redact secrets (tokens, keys, passwords, connection strings) from anything you print or save.
## Skills and docs

- My skills live in `~/Projects/active/skills`. Edit them there, never in an installed copy.
- Durable notes default to `~/Brain/00-inbox/`. Use `document` to decide if one is warranted.

## Workspaces and resolution

- Active codebases and workspaces resolve under:
  - `~/Projects/active/` (active tools and applications)
  - `~/Projects/tests/` (benchmarks, experiments, and spikes)
  - `~/Homelab/Sites/` and `~/Homelab/Core/` (self-hosted services)
  - `~/Brain/` (knowledge vault)
  - `~/Config/` (system and NixOS configuration)
- When resolving a project from the commit ledger, search these workspace roots before asking the user.

## Agent Directory

When tasks involve specialized domains, consult or delegate to registered agent personas:

- **Anne Droid** (`profile/agents/anne-droid.md`): Senior Frontend Engineer & UX Specialist.
  - **Consult when**: Backend APIs are being designed/refactored with UI impact, UX flows or accessibility need review, or interface consumers experience contract friction. Anne provides advisory feedback reports.
  - **Delegate when**: Frontend components, client styling, web interactions, or client tests need implementation. Anne operates on `feat/anne/*` branches with PR-based review.
  - **Do not invoke for**: Backend-only logic, database internals, NixOS configuration, infrastructure, or deployment.

