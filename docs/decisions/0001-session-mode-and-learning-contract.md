---
type: decision
status: accepted
project: skills
date: 2026-10-13
tags: [learning-contract, session-mode, cognitive-load, git-commit, practice]
---

# Adopt Persistent Session Mode and Learning Contract Across Skills

## Context and Problem Statement
Autonomous AI agents in the engineering workflow routinely generated finished commit messages, comprehensive journal summaries, and polished technical explanations. While structured and grammatically fluent, this generated output created a fluency illusion: the AI performed the cognitive synthesis while the engineer acted merely as a reviewer, diminishing genuine recall, understanding, and long-term retention. 

How should the agent interaction model be restructured so that the engineer actively generates reasoning, practices retrieval, and builds engineering competence without eliminating high-throughput delivery when needed?

## Decision Drivers
* Preservation of cognitive effort for the learner (generation effect, retrieval practice, desirable difficulties).
* Clear boundary between empirical facts (diffs, test outputs, execution logs) and cognitive interpretation (commit rationale, conceptual synthesis).
* Deterministic session-wide state across skills without requiring agent reinvention on each turn.
* Avoidance of "AI slop": prevent AI from fabricating mastery or filling unanswered knowledge gaps.
* Low friction when time-sensitive delivery is required.

## Considered Options
* **Option 1: Ad-hoc prompts per skill execution**: Leave behavior to invocation-time user instructions (e.g. typing "don't write it for me" or relying on skill-specific defaults).
* **Option 2: Skill-local learning contracts**: Define contract files inside individual skills (e.g. `skills/practice/references/learning-contract.md`) and reference across skill boundaries.
* **Option 3: Profile-level session state and shared learning contract (Adopted)**: Define persistent `Session mode` (`learning` vs `delivery`) in `profile/AGENTS.md`, place `profile/learning-contract.md` adjacent to it, install both globally via `install.sh`, and require skills to adapt their behavior accordingly.

## Decision Outcome
Chosen option: **Option 3: Profile-level session state and shared learning contract**, because session mode must be globally authoritative, always present in context via `profile/AGENTS.md`, and enforceable across skills (`practice`, `git-commit`, `journal-builder`) without creating cross-skill dependency coupling.

### Summary of Architectural Commitments
1. **State Machine & Authority Boundary**:
   - Two session states: `learning` (user writes reasoning) and `delivery` (agent drafts).
   - Mode is set once per session and persists.
   - Only the user may transition states ("learn" / "deliver"); the agent may suggest but never switch states unilaterally.
   - Skill output must visibly display `mode: <state>`.
2. **The Write Rule & Diagnostic Feedback**:
   - In `learning` mode, the agent provides facts (diff slices, file changes, test outputs) and 0-5 evidence-grounded questions. The user writes the commit messages, explanations, and architectural rationale.
   - Agent feedback is strictly diagnostic (`correct`, `missing`, `wrong`, `unsupported`) against empirical evidence. Promotional judgment ("masterful", "expert") is forbidden.
   - Unanswered questions remain explicitly open; the agent must not fill gaps.
3. **Assistance Levels & Evidence Separation**:
   - Attempts track assistance (`independent`, `hints`, `substantial`, `shown-solution`).
   - Observed events (commits, passed tests) remain distinct from competence claims.
4. **Author-Driven Git Commits**:
   - `git-commit` inspects diffs and groups slices, but in `learning` mode prompts the user to draft the Conventional Commit message and only quizzes topological integration strategy when a non-trivial choice exists.

## Pros and Cons of the Options

### Option 1: Ad-hoc prompts per skill execution
* Good, because it requires zero architectural changes to existing files.
* Bad, because it suffers from prompt fatigue, inconsistent enforcement, and default drift back to AI generation.

### Option 2: Skill-local learning contracts
* Good, because it keeps files within the `skills/` directory tree.
* Bad, because other skills (`git-commit`, `document`) must import references across peer skill boundaries, creating fragile relative path dependencies and failing if a single skill is uninstalled.

### Option 3: Profile-level session state and shared learning contract (Adopted)
* Good, because `profile/AGENTS.md` is always loaded in agent context, ensuring uniform visibility and session state propagation.
* Good, because `profile/learning-contract.md` establishes a single source of truth for pedagogical invariants.
* Bad, because it introduces global configuration requirements in `install.sh` and requires manual user intervention to switch modes.

## Consequences
### Positive Consequences
* Prevents the fluency illusion by ensuring the user performs active recall and formulation.
* Eliminates AI slop in journals and commit histories by substituting AI-generated assessments with user-authored explanations and explicit gap tracking.
* Restores high-throughput drafting via a single-word mode switch ("deliver").

### Negative Consequences & Accepted Trade-offs
* Commits and learning interactions in `learning` mode take more time and cognitive effort.
* Session mode persistence in the agent prompt is subject to context-window attenuation during very long conversations, mitigated by the required `mode: <state>` banner in skill outputs.

## More Information
* **Governing Specification**: [learning-contract.md](../../profile/learning-contract.md)
* **Global Agent Profile**: [AGENTS.md](../../profile/AGENTS.md)
* **Installation Script**: [install.sh](../../install.sh)
