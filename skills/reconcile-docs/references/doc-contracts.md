# Documentation Contracts

Each reconciled fact belongs in exactly one primary repository document. Follow these boundaries and structures during Step 6 of `reconcile-docs`.

## 1. README.md

**Core Question**: What is this project, why does it matter, and how do I get started?

Keep this file intentionally shallow. It is a portal, not an architectural encyclopedia.

### Standard Sections
- **Project Identity & Title**: Name and one-sentence purpose.
- **Problem Statement**: What problem does this solve and why build it?
- **Key Capabilities**: Core user-facing features or operational strengths.
- **High-Level Overview**: A concise 10,000-foot summary (or brief diagram).
- **Quick Start / Usage**: Fast install or run commands.
- **Repository Navigation**: Pointers to deeper technical documents (`ARCHITECTURE.md`, `ROADMAP.md`, `docs/adr/`).

### Contract Invariants
- Never detail component internals, internal schemas, or low-level data flows here (belongs in `ARCHITECTURE.md`).
- Never list speculative feature ideas here (belongs in `ROADMAP.md`).

---

## 2. ARCHITECTURE.md

**Core Question**: How does the system currently work?

This represents the canonical present-state technical model.

### Standard Sections
- **System Overview**: High-level topology and architectural style.
- **Architectural Principles**: Non-negotiable system invariants (e.g. offline-first, immutable ledgers).
- **Components & Responsibilities**: Explicit inventory of subsystems and their boundaries.
- **Data Flow & Lifecycle**: How information traverses the system from entry to persistence.
- **Boundaries**: Runtime, process, network, persistence, and security boundaries.
- **Dependencies**: Key libraries, external services, or system prerequisites.
- **Architectural Constraints**: Hardware, platform, or performance limits.
- **Decision Log Index**: Links to active ADRs in `docs/adr/`.

### Contract Invariants
- Describes strictly what exists in the repository right now.
- Never write future plans or aspirational designs into this file.
- If a component does not exist in the codebase, it must not appear here.

---

## 3. ADRs (docs/adr/)

**Core Question**: Why was an important architectural decision made?

ADRs preserve rationale, trade-offs, and rejected alternatives. Use MADR format (or the repository's established convention).

### Standard Template (MADR)
```markdown
# ADR-XXXX: [Title]

- Status: [Accepted | Superseded by ADR-YYYY | Deprecated]
- Date: YYYY-MM-DD
- Deciders: [Names / Roles]

## Context and Problem Statement
What was the technical challenge, context, or constraint requiring a decision?

## Decision Outcome
Chosen option: "[Option]", because [justification based on constraints].

## Consequences
- Positive: [Positive outcomes and capabilities unlocked]
- Negative: [Trade-offs, maintenance burdens, or limitations accepted]

## Alternatives Considered
- [Alternative A]: [Why it was rejected]
- [Alternative B]: [Why it was rejected]

## Related Decisions
- Supersedes [ADR-ZZZZ] / Related to [ADR-WWWW]
```

### Contract Invariants
- Every ADR must stem from concrete historical discussions or deliberate human decisions.
- Do not invent decisions the author never made; surface them as questions or candidates instead.

---

## 4. ROADMAP.md

**Core Question**: Where is the project intentionally going?

Only items that represent intentional, validated future trajectory belong here.

### Standard Sections
- **Current Direction**: High-level strategic themes for active development.
- **Near Term**: High-confidence milestones and features scheduled next.
- **Medium Term**: Planned improvements dependent on near-term completions.
- **Future / Exploratory**: Unscheduled proposals and research spikes under consideration.
- **Completed**: Milestone log of completed phases with dates.

### Contract Invariants
- Never include implemented features as active roadmap items.
- Avoid dumping every scratchpad TODO into the roadmap; include only items with deliberate commitment or research interest.
