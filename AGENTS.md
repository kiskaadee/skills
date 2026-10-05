# AGENTS.md: skills repo

Source of truth for my agent skills. Installed into agent tools by `install.sh`.

## Rules for working in this repo
- Direct commits to `main` are allowed (solo repo).
- Edit skills **here**, never in an installed location (`~/.gemini/config/skills/…`).
- Every `skills/*/SKILL.md` follows `skills/build-skill/references/skeleton.md` and stays ≤ 80 lines.
- Portable skills must not encode a user's filesystem topology (no home paths, no hardcoded vault directories).
- No absolute home paths (`/home/<user>`) and no secrets; this repo is public.
- Commit types: Conventional Commits; scope = skill name (e.g. `refactor(git-commit): …`).
