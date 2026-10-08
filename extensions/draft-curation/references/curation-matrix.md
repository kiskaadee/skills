# Draft Curation Matrix & Invariants

Detailed specifications and epistemic classification table for ingesting inbox drafts into canonical lifecycle directories.

## 1. Core Invariants

1. **Epistemic Classification over Chronology**: Content is sorted by its epistemic nature, never simply by when it was created:
   - Roadmaps, milestones, phased execution: `01-plans/<project>/` (`type: plan`)
   - Exploratory debates, trade-offs, architecture options: `02-discussions/<project>/` (`type: discussion`)
   - Daily logs & reflections: `03-records/journal/` (`type: journal`)
   - Incidents, regressions, root-cause analyses: `03-records/debug/` (`type: debug`)
   - Architectural decisions: `03-records/decisions/` (`type: decision`)
   - General knowledge, concepts, languages: `04-learning/knowledge/` (`type: knowledge`)
   - Practical SOPs, runbooks, operation walkthroughs: `04-learning/guides/<project>/` (`type: guide`)
2. **The Validation Gate**: If the vault has an automated validator (e.g. `python scripts/validate-brain.py`), a curated document must pass before any commit is made.
3. **Zero Dangling Drafts**: Once a draft is curated and relocated to its destination, the original file in the staging directory must be deleted.
4. **Interactive Checkpoint**: The agent must present the proposed destination, frontmatter, and rationale to the user before relocating files, unless explicitly instructed to process autonomously.
5. **Atomic Curation Boundary**: Each curated document or cohesive bundle is relocated and validated as an independent unit. Git history is mutated only through `git-commit`.
6. **Unique Daily Journal & Reconciliation**: A daily journal (`03-records/journal/YYYY-MM-DD.md`) is a unique daily artifact. When a curated draft targets a date whose journal already exists, reconcile it with the existing record rather than creating a duplicate file (`-2.md`) or blindly overwriting. Reconciliation must preserve existing human edits, union the `assessed_commits` frontmatter list, and integrate genuinely new wins, artifacts, objectives, and reflections while avoiding duplicate entries.

## 2. Epistemic Classification Matrix

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
