---
name: draft-curation
description: >-
  Triage, classify, format, validate, and move raw notes and drafts from an inbox or staging
  directory into canonical knowledge lifecycle directories (plans, discussions, records,
  learning).
---

# Draft Curation & Knowledge Ingestion

This extension skill governs the systematic ingestion and curation of unprocessed drafts from an inbox/staging directory (e.g. `00-inbox/`) into canonical lifecycle directories.

> **Vault Contract**: This extension assumes a knowledge vault organized around epistemic lifecycle directories (`01-plans/`, `02-discussions/`, `03-records/`, `04-learning/`) with schema validation and semantic commit conventions.

---

## 1. Core Invariants

1. **Epistemic Classification over Chronology**: Content is sorted by its epistemic nature, never simply by when it was created:
   - Roadmaps, milestones, phased execution $\to$ `01-plans/<project>/` (`type: plan`)
   - Exploratory debates, trade-offs, architecture options $\to$ `02-discussions/<project>/` (`type: discussion`)
   - Daily logs & reflections $\to$ `03-records/journal/` (`type: journal`)
   - Incidents, regressions, root-cause analyses $\to$ `03-records/debug/` (`type: debug`)
   - Architectural decisions $\to$ `03-records/decisions/` (`type: decision`)
   - General knowledge, concepts, languages $\to$ `04-learning/knowledge/` (`type: knowledge`)
   - Practical SOPs, runbooks, operation walkthroughs $\to$ `04-learning/guides/<project>/` (`type: guide`)
2. **The Validation Gate**: If the vault has an automated validator (e.g. `python scripts/validate-brain.py`), a curated document MUST pass before any commit is made.
3. **Zero Dangling Drafts**: Once a draft is curated and relocated to its destination, the original file in the staging directory must be deleted.
4. **Interactive Checkpoint**: The agent must present the proposed destination, frontmatter, and rationale to the user before relocating files, unless explicitly instructed to process autonomously.
5. **Atomic Curation Boundary**: Each curated document or cohesive bundle is relocated and validated as an independent unit. Git history is mutated only through `git-commit`.
6. **Unique Daily Journal & Reconciliation**: A daily journal (`03-records/journal/YYYY-MM-DD.md`) is a unique daily artifact. When a curated draft targets a date whose journal already exists, reconcile it with the existing record rather than creating a duplicate file (`-2.md`) or blindly overwriting. Reconciliation must preserve existing human edits, union the `assessed_commits` frontmatter list, and integrate genuinely new wins, artifacts, objectives, and reflections while avoiding duplicate entries.

---

## 2. Operational Procedure

```mermaid
flowchart TD
    S1["1. Preflight Gate<br/>python scripts/validate-brain.py"] --> S2["2. Inventory & Inspection<br/>Scan 00-inbox/ for pending drafts"]
    S2 --> S3["3. Epistemic Classification<br/>Determine target directory & metadata"]
    S3 --> S4{"4. Interactive Checkpoint<br/>Present target path & frontmatter"}
    S4 -->|Approved| S5["5. Transform & Relocate<br/>Write/reconcile file, delete from inbox"]
    S5 --> S6["6. Validate Integrity<br/>python scripts/validate-brain.py"]
    S6 --> S7["7. Hand Off to git-commit<br/>Ready for user review & commit"]
```

### Step 1: Preflight Verification
Before touching any files, verify that the repository is currently in a healthy state:
```bash
python scripts/validate-brain.py
```
If the validator fails prior to curation, resolve existing repository issues or alert the user before proceeding.

### Step 2: Inventory & Inspection
Scan `00-inbox/` for files to curate, ignoring `.keep`, `README.md`, system ledgers (`commit-log.csv`), or active scratch notes specified by the user:
- Read the content of the staged draft.
- Identify the project context (e.g. `homelab`, `nekoweb`, `brain`, or global/general).
- Determine whether the draft contains a single concept or multiple mixed concerns that should be decomposed into separate files.

### Step 3: Epistemic Classification & Metadata Preparation
Select the target directory according to the repository's Directory Contracts:

| Content Nature | Target Directory | Frontmatter `type` | Naming Pattern |
| :--- | :--- | :--- | :--- |
| **Phased Roadmap / Blueprint** | `01-plans/<project>/` | `plan` | `<slug>.md` |
| **Exploratory Trade-off / Why** | `02-discussions/<project>/` | `discussion` | `<slug>.md` |
| **Daily Log / Journal** | `03-records/journal/` | `journal` | `YYYY-MM-DD.md` |
| **Incident Root Cause / Bug** | `03-records/debug/` | `debug` | `YYYY-MM-DD-<slug>.md` |
| **Architectural Decision (ADR)** | `03-records/decisions/` | `decision` | `<slug>.md` |
| **Theoretical / Disciplinary Concept** | `04-learning/knowledge/concepts/` | `knowledge` | `<slug>.md` |
| **Tool / Language Reference** | `04-learning/knowledge/technologies/` | `knowledge` | `<slug>.md` |
| **Engineering Best Practice** | `04-learning/knowledge/methods/` | `knowledge` | `<slug>.md` |
| **Operational SOP / How-to Runbook** | `04-learning/guides/<project>/` | `guide` | `<slug>.md` |

Prepare the compliant YAML frontmatter block matching the destination contract (see vault's `AGENTS.md` or templates).

### Step 4: Interactive Checkpoint
Present a 4-point curation checkpoint to the user:
1. **Source Draft**: Path in `00-inbox/`.
2. **Proposed Destination**: Target path in vault hierarchy.
3. **Proposed Frontmatter**: YAML block including `type`, `project`, `tags`, etc.
4. **Rationale**: Brief epistemic justification for why this target directory was selected.

*If the user confirms or if operating in approved autonomous mode, proceed to Step 5.*

### Step 5: Transformation, Relocation & Reconciliation
1. **Format Content**:
   - Prepend valid YAML frontmatter.
   - Ensure title is an H1 heading matching document purpose.
   - Convert any Obsidian `[[double-bracket]]` links to standard relative Markdown links (`[label](../path.md)`).
   - Ensure external code links use forge Git URLs (never machine-specific `file:///` URIs).
2. **Write or Reconcile Target File**:
   - *New document*: Write the transformed document directly to the destination path.
   - *Existing daily journal*: Perform journal-aware reconciliation. Preserve existing human-authored edits, append new project sections/wins, append new decisions/artifacts, union `assessed_commits` in YAML frontmatter, and record new learning edge outcomes without duplicating entries.
3. **Remove Staging File**: Delete the original file from `00-inbox/`.

### Step 6: Validation Pass
Run repository integrity tests:
```bash
python scripts/validate-brain.py
python scripts/test_validator.py
```
Ensure all checks pass cleanly: frontmatter validation, link resolution, code fences, Mermaid syntax, Ruff linting, and Pyright typing.

### Step 7: Hand Off to `git-commit`
With the staging draft removed and repository validation passing cleanly, hand off to `/git-commit` for inspection and explicit user approval. Propose the conventional or vault-specific semantic commit type:
- `plan(<project>): <description>`
- `discussion(<project>): <description>`
- `journal: record daily log for YYYY-MM-DD`
- `debug(<project>): <description>`
- `decision(<project>): <description>`
- `knowledge(<topic>): <description>`
- `guide(<project>): <description>`

Do not commit working-tree mutations directly; mutation of Git history belongs strictly to `git-commit`.
