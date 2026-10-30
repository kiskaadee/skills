# Code Smells and Design Diagnostics

Reference for `code-review`. Treats code smell catalogs as diagnostic heuristics rather than mechanical violation checklists.

Derived and adapted from Martin Fowler's refactoring catalog as curated in Matt Pocock's skills repository (github.com/mattpocock/skills).

## 1. Three-Tier Evaluation Framework

When a reviewer observes a suspicious pattern in the diff, they must classify it into one of three distinct categories:

1. **Confirmed Violation**: Observable evidence proves the pattern actively damages correctness, testability, or maintainability (e.g., duplicate business logic causing divergent bugfixes, or unreadable obfuscated variable names).
2. **Potential Design Smell**: A pattern that warrants architectural inquiry and discussion, but whose harm depends on future evolution (e.g., a function taking six parameters that might benefit from a dedicated parameter struct).
3. **Contextual Trade-Off**: An intentional compromise where the author consciously accepted a local cost for a tangible engineering benefit (e.g., inlining logic in a script to keep it self-contained, or using primitive strings in a one-off parser to avoid premature type layers).

Reviewers must never demand refactoring for a contextual trade-off without demonstrating concrete harm.

## 2. Fowler Smell Diagnostics

| Heuristic | What to Look For | When It Is a Problem | When It Is Acceptable |
| :--- | :--- | :--- | :--- |
| **Primitive Obsession** | Using basic strings, numbers, or dicts for domain concepts (e.g. raw string for currency or unvalidated email). | When parsing, validation, and operations on that concept are duplicated across multiple call sites. | At external system boundaries, simple internal scripts, or when the concept has zero invariant behavior. |
| **Feature Envy** | A method or function that accesses data from another module more than its own. | When business rules belonging to Module B are scattered across callers in Module A. | When implementing intentional adapters, serialization mappers, or presentation formatters. |
| **Speculative Generality** | Interfaces, generics, hook points, or abstract classes added for hypothetical future needs. | When the abstraction adds indirection today for requirements that do not yet exist. | When building published public libraries with strict semver compatibility commitments. |
| **Shotgun Surgery** | A single logical feature change forces scattered micro-edits across many different files. | When related behavior is fragmented across unrelated modules instead of cohesive units. | Cross-cutting infrastructure updates (e.g. updating a dependency signature or logging framework). |
| **Divergent Change** | A single file or module is edited frequently for completely different business reasons. | When unrelated concerns (e.g. UI rendering, database persistence, and auth) live in one file. | Cohesive coordinating modules (such as application entrypoints or top-level routers). |
| **Mysterious Name** | Variables, functions, or types whose names obscure what they do. | When reading the code requires mental translation or leaves ambiguity about side effects. | Conventional short loop indexes (`i`, `j`) or well-understood mathematical terms in algorithmic loops. |
| **Repeated Switches** | Identical `if`/`else` or `match`/`switch` chains repeated across several functions on the same type. | When adding a new type variant requires editing every switch statement manually. | Simple two-branch checks or isolated dispatchers in serialization code. |

## 3. Commit Cohesion and Granularity

Commit size is a **diagnostic signal**, not an absolute rule.

- **The Goal**: Commits should represent cohesive, localizable units of work that can be understood, reviewed, and reverted independently if needed.
- **Diagnostic Threshold**: A commit touching more than 350 lines is a signal to inspect whether multiple concerns were bundled together (for example, combining data model types, UI rendering, and a mutation modal into a single commit).
- **Legitimate Exceptions**: Generated schemas, lockfile updates, broad renaming refactors, or database seed migrations often legitimately exceed 350 lines while remaining completely cohesive.
- **The True Anti-pattern**: Splitting a single atomic change into non-functional fragments, or conversely, combining unrelated feature work and opportunistic refactorings into one commit.
