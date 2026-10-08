# Human Checkpoint Report Format

During Step 5 of `reconcile-docs`, the agent pauses before modifying or creating any files. Present this structured Reconciliation Report for explicit user review and approval.

## Report Structure

```markdown
# Documentation Reconciliation Report

## 1. Present State Summary
- Core components identified in codebase: [list verified components]
- Key boundaries and dependencies: [list verified boundaries]
- Existing docs audit: [e.g. README is obsolete, ARCHITECTURE missing]

## 2. Historical Discoveries
- Recovered decisions: [list decisions with date and context]
- Pivots and migrations: [list architectural changes confirmed by history]
- Identified constraints / incidents: [list discovered items]

## 3. Future Intent
- Active roadmap candidates: [list validated near/medium term items]
- Filtered out proposals: [list abandoned or superseded notes excluded from roadmap]

## 4. Conflict Log
| Conflict | Source Claim | Code Evidence | Proposed Resolution |
| :--- | :--- | :--- | :--- |
| Historical Contradiction | [e.g. Brain notes claim PostgreSQL] | [Code uses SQLite WAL] | [Supersede note, draft migration ADR] |
| Premature Promotion | [e.g. Plan states gRPC API ready] | [Only REST API exists] | [Move to ROADMAP near-term] |
| Zombie Documentation | [e.g. README mentions Worker daemon] | [Worker removed in commit abc1234] | [Remove from README/ARCHITECTURE] |

## 5. Proposed File Actions
| Target File | Action | Summary of Changes |
| :--- | :--- | :--- |
| `README.md` | Update | Align quick start, prune dead features, link architecture |
| `ARCHITECTURE.md` | Create | Document verified present component topology and boundaries |
| `docs/adr/0001-*.md` | Create | Record rationale for core architectural choices |
| `ROADMAP.md` | Update | Align future milestones with active plans |

## 6. Open Decisions for You
1. [Specific conflict or ADR candidate requiring user confirmation]
2. [Ambiguous rationale requiring engineer input]
```

## Checkpoint Rules

1. **Hard Pause**: Never start Step 6 (drafting/modifying files) until the user explicitly confirms the proposed actions.
2. **Surface Gaps Honestly**: If an architectural component has no discovered rationale, highlight it in "Open Decisions for You" rather than inventing a backstory.
3. **Editable Options**: Offer concrete options if there is ambiguity regarding whether an abandoned proposal should be documented in an ADR or omitted entirely.
