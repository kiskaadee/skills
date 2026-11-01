# Provenance

Used by `derive-skill` at steps 1 and 8. Defines how derived material records where it came from.

## Location

- Every skill that contains accepted derived material has `skills/<target>/references/provenance.md`.
- One `##` entry per source. A merge from a second source adds an entry; it never rewrites one.
- Rejected sources get no provenance file. Their record is the derivation brief.

## Revision evidence

Use the first one that exists. Never invent a value.

1. Commit SHA (full).
2. Release or tag.
3. Otherwise: retrieval date plus the URL, or for a local package the path and enough identifying
   detail to tell the inspected copy apart (e.g. file list with sizes, or a content hash).

## Entry format

```markdown
## <Source skill name>
- **Source:** <url or path>
- **Author:** <name or maintainers>
- **Revision:** <sha | release/tag | retrieved YYYY-MM-DD (+ identifying detail)>
- **License:** <SPDX id>; obligations: <e.g. retain copyright notice below | none>
- **Outcome:** new skill | merged into <skill>
- **Files affected:** <files in this repo containing derived material>
- **Incorporated:** <material taken and how it was adapted>
- **Rejected:** <notable omissions and why>

<upstream notice, verbatim, when the license requires it>
```

## Checks (step 8)

- Every file listed under **Files affected** actually contains the derived material.
- **Incorporated** matches the approved sort in the brief.
- Any notice the license requires is present verbatim.
