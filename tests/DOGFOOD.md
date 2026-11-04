# Qualitative Dogfood Evaluation Protocol & Historical Results

This document records the qualitative dogfooding evaluation conducted during Milestone 23 ("Gitea Planning & Execution Refactor"), establishing empirical validation of the modernized skills workflow against real operational scenarios.

---

## 1. Clean-Room Reproducibility Audit Protocol

### Objective
Ensure that planning artifacts (specifications, roadmaps, and proposed Gitea issue markdown) contain zero conversational assumptions and can be deterministically parsed and executed by an independent subagent with zero context.

### Verification Case Study (Issue 10 -> Issue 11 Discovery)
- **Manifest**: Clean-room subagent spawned with only pinned commit SHA and raw draft markdown.
- **Observed Finding**: The auditor flagged that while `gitea-plan` and `implement-slice` were being migrated to `gt`, `gitea-pr` was left referencing deprecated `tea pr` commands. This material gap would have caused execution failure when opening and merging PRs.
- **Remediation**: Issue #11 was formally provisioned into Milestone #23, preventing an ecosystem contradiction before code was written.

---

## 2. Gitea Anti-Hallucination & API Lessons Learned

During live execution on `gitea.roadtotech.me`, five operational failure modes were surfaced, diagnosed, and codified into durable reference contracts:

| Operational Scenario | Failure Mode Encountered | Root Cause | Codified Solution |
| :--- | :--- | :--- | :--- |
| **Milestone Creation** | Hallucinated `/milestone/1` | Gitea auto-increments milestone IDs globally across the instance. Repository's first milestone was ID `23`. | Query IDs via `gt milestone list --json id,title,state,url`. Never guess numeric sequences. |
| **Sovereign SSH Remote** | `SSH remote does not match a configured instance` | `gt` does not recognize non-standard SSH port 2223 automatically. | `gt config set ssh_host gitea.roadtotech.me:2223 --host https://gitea.roadtotech.me`. |
| **Project Card Moves** | HTTP 404 / Unmarshal error | `gt api` requires the **global issue ID** (`gt issue list --json id,number`), not repository-local number, and typed integer `-F column_id=...`. | Documented API recipe: `gt api -X POST /repos/{owner}/{repo}/projects/{id}/issues/{global_id}/move -F column_id={col_id}`. |
| **PR Self-Review** | `you can't approve or request changes on your own pull request` | Gitea enforces the four-eyes principle; authors cannot self-approve. | Authors use `--comment` for informational feedback, or execute `gt pr merge <id> --squash --delete-branch` directly. |
| **Workflow State Tracking** | Branch state desynchronization | Working tree edits made on incorrect base or uncommitted PR branches. | Enforced Preflight Branch State Classifier (`CLEAN_BASE`, `ADOPTABLE_DIFF`, `CONFLICTING_STATE`, `WRONG_BASE`) in `implement-slice`. |

---

## 3. Tripartite Workflow Contract Validation

### 1. Planned Workflow (Step 3 Gate)
Pre-commits canonical 5-tuples (`node_id`, `claim`, `method`, `executor`, `pass_condition`) and dynamically projects Mermaid graphs exposing falsification routes.

### 2. Execution Record (Steps 4–5 Log)
Updated at each orchestrator turn. Transition states (`planned` -> `passed` / `failed` / `blocked` / `skipped`) require verified evidence (commit SHA or exit code). Missing evidence strictly prevents `passed`.

### 3. Deviation Report (Step 6 Handoff)
Explicitly logs skipped checks (e.g. unapproved `live-infra`), added checks, rework loops, and scope drift.
