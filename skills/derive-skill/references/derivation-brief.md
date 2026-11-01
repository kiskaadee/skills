# Derivation Brief

Used by `derive-skill` at step 6. The brief is the boundary between `derive-skill` and
`build-skill`: once approved, `build-skill` treats it as its spec and does not redo the source
investigation.

## Template

```markdown
# Derivation brief: <source skill name>

## Source
<provenance entry, format in provenance.md>

## License
- **License:** <SPDX id | none found>
- **Obligations:** <e.g. retain copyright and permission notice>
- **Assessment:** <appears compatible | unclear | not compatible | no permission>, and why.

## What it does
<2 to 4 lines: problem, mechanism, assumptions about harness, persona, tools>

## Scripts and executables
| File | Runs | Writes | Network | Executed during review? |
| :--- | :--- | :--- | :--- | :--- |

## Sort
| Material | Decision | Reason |
| :--- | :--- | :--- |
| <idea, step, file> | preserve / adapt / reject | <one line> |

## Outcome
- **Decision:** new skill `<name>` | merge into `<skill>` | reject
- **Target files:** <files to create or change; none if rejected>
- **Overlap checked:** <skills compared and where the edges fall>

## Open risks
- <unresolved questions, untested scripts, license doubts>
```

## Rules

- **Reject is a full outcome.** Fill in Source, License, What it does, Sort, and Outcome, then stop.
- **Merge briefs** name each existing file that changes and the source material it absorbs.
- **Keep it short.** One line per sort row. Long reasoning goes in Open risks.
