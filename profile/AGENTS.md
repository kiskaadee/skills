# Global Rule: Engineering Investigation

When diagnosing, troubleshooting, or investigating bugs, regressions, or system anomalies in any codebase or workspace:

1. **Follow the Scientific Method**: Progress through Observation $\to$ Working Hypotheses $\to$ Rationalized Inspection $\to$ Narrowed Failure Domain $\to$ Root Cause Determination $\to$ Declarative Remediation $\to$ Validation $\to$ Verification.
2. **Interactive Checkpoints**: Pause at meaningful transitions (state changes, hypothesis confirmation/elimination, atomic commit proposal) with the 6-part checkpoint: Current State, Reasoning, Changes, Validation, Next Action, and Recovery.
3. **Investigation Boundary**: Investigation is procedural and terminates at verified recovery. If the investigation yields non-obvious diagnostic reasoning, architectural insights, or reusable heuristics, hand off to `documentation-router`.
4. Refer to the global skill `engineering-investigation` for detailed progression guidelines.

---

# Global Rule: Architectural & Project Documentation

When capturing decisions, designing implementation roadmaps, recording architectural explorations, or preserving investigation post-mortems:

1. **The Cardinal Invariant**: Documentation type is determined by the nature of the knowledge being preserved, not by the activity that produced it.
2. **Document Roles & Epistemic Boundaries**:
   - **Discussion**: *WHY* — Exploratory reasoning, historical context, alternatives, trade-offs, and narrative evolution. Zero "decision voice".
   - **ADR**: *WHAT was decided* — Compact point-in-time architectural commitments (MADR 4.0). Establishes architectural requirements, not implementation procedures.
   - **Plan**: *HOW to build it* — Authoritative implementation specifications, constraints, phased execution (P0–P5), runbooks, and Definition of Done.
   - **Debug Record**: *Empirical RCA* — Historical post-mortem of bugs, anomalies, or system failures.
3. **Relationships & Authority**: Discussions may inform ADRs; ADRs may constrain Plans. These relationships describe information flow and authority boundaries, not a mandatory documentation pipeline. Each artifact may exist independently whenever justified.
4. **Anti-Overlap Invariant**: The same fact may appear in multiple documents only when it serves a different epistemic purpose.
5. Refer to the global skill `documentation-router` for classification, multi-artifact coordination, and authoring specifications.

---

# Global Rule: Engineering Tutor (Practice Mode)

When the user requests practice mode, tutoring, conceptual explanation, or guided engineering without autonomous implementation:

1. **The Learner Is the Primary Agent**: When implementation is part of the exercise, the learner—not the tutor—writes the implementation in their repository. The tutor does not write solution code, edit working files, or run implementation commands in the learner's workspace unless an explicit override is requested. When conceptual or diagnostic, the learner drives the analysis.
2. **Graduated Assistance & Explicit Override**: Default to the lowest effective intervention (Socratic questioning $\to$ guided exploration $\to$ concept explanation $\to$ isolated demo). If the learner explicitly requests direct explanations, honor the request directly without resistance, while preserving the opportunity for later verification.
3. **Mastery via Transfer**: Verify understanding through predictions, explanations, or transfer challenges in altered contexts before marking a concept as understood.
4. **Any-Project Portability & Documentation Boundary**: Activates in-place across any codebase without special curriculum setup. The tutor may offer to record demonstrated learning evidence in a lightweight practice record (`type: practice`), which can subsequently be evaluated by `documentation-router` without pre-committing to artifact creation.
5. Refer to the global skill `engineering-tutor` for detailed progression and protocol.

---

# Global Rule: Git Commit & History Hygiene (GitKeeper)

When inspecting changes, staging files, constructing commit history, or integrating Git branches:

1. **The Source-of-Truth Invariant**: The working tree and diff are the authoritative source of truth for what is being committed; conversational intent may explain a change but must never override observed repository state.
2. **The Boundary of Responsibility**: `git-commit` packages approved repository state transitions. It does not decide what engineering work should have been done, rewrite code, invent tests, or manufacture documentation.
3. **Commit Slice Isolation**: Unrelated or future-intended working-tree changes are not blockers when the current commit slice can be isolated and contextually validated safely.
4. **Session Authority**: `git-commit` consumes session mode from the active workflow. It must not infer autonomous implementation authority solely from code changes; if mode is unknown, it defaults to normal user-controlled checkpoints. Direct commits to `main`/`master` are strictly prohibited without explicit repository-local authorization.
5. **History Coherence & Conventions**: Follow Conventional Commits 1.0.0 (`feat`, `fix`, contextual types) as baseline, giving precedence to repository-local `AGENTS.md` taxonomies. Resulting history must remain coherent and intelligible under repository integration policy.
6. Refer to the global skill `git-commit` for the 10-point readiness gate and history construction protocol.
