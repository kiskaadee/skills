# Journal Authoring Specification

A Daily Journal is a durable, evidence-grounded record of a day's engineering accomplishments, architectural decisions, and the learning edges identified through retrospective reflection.

---

## 1. Epistemic Role

* **Purpose**: Capture the terminal state of a day's work across projects, record verified mental models, and preserve active learning edges for future study.
* **Grounding**: Derived from primary evidence (commit ledger, git history) and interactive reflection, never from passive memory or auto-summarized activity narration.
* **Mutability**: Journals are date-scoped historical records. Once curated, existing human-authored content must be preserved; subsequent journal runs may extend the same day's record with genuinely new work, learning, and reflections.
* **Assessment Provenance**: The `assessed_commits` list in YAML frontmatter contains the full 40-character Git commit SHAs incorporated into the journal's assessment loop. This provides a deterministic, machine-readable boundary distinguishing processed history from unassessed ledger events.

---

## 2. Frontmatter Contract

```yaml
---
type: journal
project: brain # or primary project scope
date: YYYY-MM-DD
tags:
  - project-name
  - technology-or-topic
assessed_commits:
  - 42927b9858c1b091bb6e78d3abcf6f9500bd7547
  - fee7429a1064193c066b8c20bd6927977599a67f
---
```

---

## 3. Structural Sections

### 1. Document Title
`# Daily Journal: YYYY-MM-DD`

### 2. Wins (`## Wins`)
Subdivided by project or scope (`### <Project Name>`).
Bullet points detailing concrete accomplishments, architectural boundaries established, and working implementations. Use plain, precise technical language.

### 3. Decisions, Incidents & Artifacts (`## Decisions, Incidents & Artifacts`)
Links to formal artifacts produced or updated during the day:
- Architectural Decision Records (`03-records/decisions/` or repo `docs/`)
- Implementation Plans & Roadmaps (`01-plans/`)
- Debug Records & Post-mortems (`03-records/debug/`)
- Key commit SHAs or pull requests.

### 4. Mistakes, Gaps & Learning Edges (`## Mistakes, Gaps & Learning Edges`)
Organized by project/domain. Records the epistemic state of assessed learning objectives:
- **Achieved**: The concept or invariant the user successfully demonstrated and explained.
- **Unresolved**: Knowledge gaps where the user struggled or answered `Skip: I don't get it`. Includes the concrete code/evidence needed for follow-up.
- **Deferred**: Objectives skipped due to external constraints (e.g. `Skip: I'm exhausted`).

### 5. Technical & Personal Reflections (`## Technical & Personal Reflections`)
Synthesized takeaways on system behavior, engineering discipline, trade-offs, and shifts in mental models.

### 6. Next Objectives (`## Next Objectives`)
Optional forward-looking priorities for upcoming sessions.
