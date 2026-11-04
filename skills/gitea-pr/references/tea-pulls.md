# [DEPRECATED] Tea CLI Pull Request Subroutines

> **Notice**: Upstream `tea` CLI is archived and officially deprecated in favor of `gt` (`gitea/cli`).
> For verified command patterns and JSON recipes, use **`skills/gitea-pr/references/gt-pulls.md`**.

This document is preserved for historical reference and legacy instance migrations only.

---

## Legacy Commands Reference (Archived)

### 1. Inspecting Pull Requests (Legacy)
```sh
tea pulls list
tea pulls <index>
```

### 2. Creating Pull Requests (Legacy)
```sh
tea pulls create --title "<title>" --base "<base>" --head "<head>" --description-file -
```

### 3. Review Comments (Legacy)
```sh
tea pulls review-comments <index>
tea pulls reply <index> <comment-id> "<reply-text>"
tea pulls resolve <comment-id>
```
