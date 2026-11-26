# CI Workflow & Planning Contract Migration

Detailed procedure for Step 5 of `gitea-to-github`. All edits run inside an ephemeral `/tmp/` clone of the newly pushed GitHub repository before Gitea pull-mirror attachment.

## 1. Resume Guard

Before modifying files in `/tmp/`, inspect the GitHub default branch:
- If all planned `.github/workflows/` files and `AGENTS.md` (`project_number: <int>` when applicable) are already present, skip Step 5 without creating duplicate commits.

## 2. `.gitea/workflows/` to `.github/workflows/` Translation

1. **Move Workflows:** Move `.gitea/workflows/*.yml` and `.gitea/workflows/*.yaml` to `.github/workflows/` (removing `.gitea/workflows/` once migrated).
2. **Context & Secret Translation:**
   - Replace `${{ gitea.* }}` expressions with `${{ github.* }}`.
   - Replace `secrets.GITEA_TOKEN` / `GITEA_TOKEN` with `secrets.GITHUB_TOKEN` / `GITHUB_TOKEN`.
   - Extract all non-`GITEA_TOKEN` `${{ secrets.<NAME> }}` references and warn the user during dry-run and Step 5 so those secrets can be provisioned on GitHub.
3. **Runner Label Mapping & Security Boundary:**
   - Default `runs-on:` to GitHub-hosted `ubuntu-latest` for both `public` and `private` repositories.
   - Allow `self-hosted` only when the user explicitly opts in during dry-run review AND the target GitHub visibility is `private`. **Block `self-hosted` opt-in on `public` repositories** to prevent PR supply-chain RCE against homelab runners.
4. **Badges & External Action URLs:**
   - Automatically rewrite standard Gitea workflow status badge URLs in `README.md` to GitHub Actions badge URLs (`https://github.com/<owner>/<repo>/actions/workflows/<file>/badge.svg`) when the corresponding workflow is migrated.
   - Flag non-standard Gitea-hosted action URLs (`https://<gitea-host>/...`) or custom badge URLs for explicit user review/replacement.

## 3. Legacy `AGENTS.md` Planning Contract Rewrite

1. **Detect Legacy Contracts:** Inspect repo `AGENTS.md` for legacy `gitea-plan` fields (Gitea `project_id`, `{Backlog..Completed -> column_id}` maps, hex colors, or `gitea-plan` sync rules).
2. **Rewrite to State-Free Schema:** Propose rewriting legacy planning sections to the state-free `project_number: <int>` contract defined in `../../projects/references/planning-contract.md` (when a Projects v2 board was created/linked in Step 4, or remove stale Gitea board IDs for `Small`-tier boardless repos).
3. **Commit & Push:** Commit translated `.github/workflows/`, updated `README.md` badges, and rewritten `AGENTS.md` in the `/tmp/` clone and push to GitHub before Step 7 creates the Gitea pull mirror.
