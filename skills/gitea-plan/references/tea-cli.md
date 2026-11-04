# [DEPRECATED] Tea CLI Subroutines

> **Notice**: Upstream `tea` CLI is archived and officially deprecated in favor of `gt` (`gitea/cli`).
> For verified command patterns, JSON extraction discipline, and sovereign instance conventions, use the official skill:
> **`skills/gt-usage/`** and its reference manual **`skills/gt-usage/references/commands.md`**.

This document is preserved for historical reference and legacy instance migrations only.

---

## Legacy Commands Reference (Archived)

### 1. Issue Management (Legacy)
```sh
tea issues create --title "<title>" --description "<description>"
tea issues list
tea issues edit <index> --title "<new-title>"
tea issues close <index>
```

### 2. Milestone Management (Legacy)
```sh
tea milestones create --title "<milestone-title>" --description "<overview>"
tea milestones list
tea milestones close "<milestone-title>"
```
