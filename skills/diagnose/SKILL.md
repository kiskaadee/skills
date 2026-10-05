---
name: diagnose
description: >-
  Slash command `/diagnose`. Activates the disciplined engineering investigation lifecycle
  to troubleshoot bugs, regressions, or system anomalies using the scientific method,
  falsifiable hypotheses, and 6-part interactive checkpoints.
---

# Engineering Diagnosis (`/diagnose`)

This skill activates the **Engineering Investigation Workflow**, providing first-class slash command invocation for **`engineering-investigation`**.

When invoked via `/diagnose [optional symptom, error message, or anomaly]`:

1. **Activate Investigation Lifecycle**:
   Immediately transition the session into disciplined empirical reasoning following the scientific method:
   $$\text{Observe} \longrightarrow \text{Hypothesize} \longrightarrow \text{Inspect} \longrightarrow \text{Narrow Domain} \longrightarrow \text{RCA} \longrightarrow \text{Remediate} \longrightarrow \text{Validate} \longrightarrow \text{Verify}$$

2. **Core Operational Principles**:
   * **Separate Observation from Inference**: Clearly demarcate what the system reported (raw logs, error outputs, exit codes) from working inferences.
   * **Rationalized Diagnostics**: State what layer of the stack each inspection command tests and what result would confirm or eliminate a working hypothesis.
   * **Proportional Depth**: Scale the investigation to the complexity and impact of the issue; avoid ceremonial boilerplate for trivial typos.
   * **6-Part Checkpoint Protocol**: Pause at meaningful transitions (failure domain narrowed, hypothesis eliminated, local change applied, atomic commit boundary, or production deployment handoff) to present:
     1. *Current State*
     2. *Reasoning*
     3. *Changes*
     4. *Validation*
     5. *Next Action*
     6. *Recovery*
   * **Zero Secret Leakage**: Redact tokens, credentials, and private keys from diagnostic logs.

3. **Session Protocol**:
   * If an argument was provided (e.g. `/diagnose 502 Bad Gateway on /api/v1/auth`): Begin by inspecting relevant error logs and establishing the blast radius for that specific failure.
   * If invoked with no argument: Prompt the user: *"What unexpected symptom, error log, or regression are we investigating?"*

4. **Completion & Handoff**:
   The investigation terminates upon verified recovery in the target environment. If the investigation yielded architectural insights, non-obvious failure modes, or reusable operational heuristics, hand off to **`documentation-router`** to evaluate whether an ADR, Discussion, or Debug Record (`03-records/debug/`) is justified.

For the complete progression and checkpoint protocol, refer to [engineering-investigation](../engineering-investigation/SKILL.md).
