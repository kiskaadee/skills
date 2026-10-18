# Journal Authoring Specification

A Daily Journal is an evidence-grounded record of a day's engineering accomplishments, architectural decisions, and human-authored reasoning on key concepts.

---

## 1. Epistemic Role

* **Purpose**: Capture the terminal state of a day's work across projects, record human-authored mental models, and preserve active learning edges for future study.
* **Grounding**: Derived from primary evidence (commit ledger, git history) and user reflection, never from auto-summarized activity narration or promotional praise.
* **Scaffolding vs Review**: In learning mode, the journal begins as an agent-generated scaffold with facts and question blanks. The engineer completes the blanks, and curation adds diagnostic feedback and calibration.
* **Assessment Provenance**: The `assessed_commits` list in YAML frontmatter contains the full 40-character Git commit SHAs incorporated into the journal. This provides a deterministic boundary distinguishing processed history from unassessed ledger events.

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
status: draft | completed
revisit_after: YYYY-MM-DD # optional
---
```

---

## 3. Structural Sections

### 1. Document Title
`# Daily Journal: YYYY-MM-DD`

### 2. Facts (Agent) (`## Facts (Agent)`)
Grouped by project (`### <Project Name>`).
Plain, concise technical facts without promotional adjectives:
- **Commits**: `<short-sha>` description of change.
- **Artifacts**: links to ADRs, plans, debug records.
- **Evidence**: key files touched, test results.

### 3. Learning & Reasoning (User) (`## Learning & Reasoning (User)`)
Numbered prompts derived from substantive architectural changes, invariants, trade-offs, or bug diagnoses:
- `### 1. <Question prompt>`
- User's explanation in their own words.

### 4. Feedback & Calibration (Agent) (`## Feedback & Calibration (Agent)`)
Filled during review/curation after user answers:
- **Assistance**: `independent` | `hints` | `substantial` | `shown-solution`
- **Rubric Checklist**:
  - Invariant / Mechanism: [✓ | ✗ | ~] <note>
  - Edge cases / Failure modes: [✓ | ✗ | ~] <note>
  - Trade-offs / Constraints: [✓ | ✗ | ~] <note>
- **Diagnostic Feedback**: points labeled `correct`, `missing`, `wrong`, or `unsupported`.

### 5. Open / Gaps (`## Open / Gaps`)
Unresolved uncertainties, deferred questions, or edge cases identified during review.
