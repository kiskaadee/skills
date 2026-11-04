# Gitea Instance Conventions & Remote Mapping

This reference documents generic host targeting, remote discovery, and non-standard SSH port conventions for `gt`.

## 1. Remote Discovery & Matching

`gt` discovers the active repository by inspecting `git remote -v`:
- It compares the remote origin URL against configured instance hostnames.
- If the git remote uses HTTPS (e.g. `https://gitea.example.com/owner/repo.git`), discovery matches automatically against authenticated host `https://gitea.example.com`.
- If the git remote uses a custom SSH port (e.g. `ssh://git@gitea.example.com:2223/owner/repo.git`), `gt` will fail remote matching unless `ssh_host` is configured.

## 2. Non-Standard SSH Port Mapping

For sovereign or private instances exposing Gitea SSH on a custom port, configure `ssh_host` in `gt` config:

```bash
# Map custom SSH host and port to the HTTPS instance URL
gt config set ssh_host <ssh-hostname>:<port> --host https://<instance-hostname>
```

Example pattern:
```bash
gt config set ssh_host gitea.example.com:2223 --host https://gitea.example.com
```

Once configured, `gt` automatically maps `ssh://git@gitea.example.com:2223/...` to `https://gitea.example.com`, eliminating the need to pass `-R owner/repo` on every command.

## 3. Explicit Repository & Host Targeting

When running commands outside a cloned repository working tree, or when resolving ambiguity across multiple configured remotes:
- Use `-R, --repo <owner>/<repo>` or full clone URL.
- Use `--host <url>` to target an explicit instance.
- Alternatively, set environment variables `GITEA_HOST` and `GITEA_CLI_REPO`.

## 4. User Profile Rules vs. Portable Skills

Instance-specific endpoints, dynamic DNS sync scripts (e.g. `cf-ddns`), internal IP addresses, and private domain names belong strictly in user profile rules (`profile/AGENTS.md` or gitignored configurations). Portable skills remain generic and portable across any Gitea 1.20+ instance.
