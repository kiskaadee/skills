---
name: build-skill
description: >-
  Slash command `/build-skill`. Activates the interactive skill-builder workflow to
  design, size, author, and iteratively refine agent skills.
disable-model-invocation: true
argument-hint: "What capability or workflow do you want to turn into a skill?"
---

# Skill Builder (`/build-skill`)

This skill activates the **Skill Builder Workflow**, providing first-class slash command invocation for **`skill-builder`**.

When invoked via `/build-skill [optional capability or workflow name]`:

1. **Activate Interactive Skill Architect**:
   Immediately transition the session into an interactive design and engineering review following the 6-stage lifecycle:
   $$\text{Need Discovery} \longrightarrow \text{Archetype Sizing} \longrightarrow \text{Operational Controls} \longrightarrow \text{Skill Design Specification} \longrightarrow \text{Review Gate} \longrightarrow \text{Authoring \& Dogfooding}$$

2. **Core Operational Principles**:
   * **The Human is the Architectural Authority**: The developer decides architectural intent, approves boundaries, and owns the final design. The assistant acts as an investigative coach and design reviewer.
   * **Proportional Structure (Anti-Overengineering)**: Size the skill proportionally to its diagnosed mode (Reference, Transformation, Procedural Workflow, or Interactive Elicitation). Never force a state machine where a simple reference or schema suffices.
   * **Mandatory Design Review Gate**: Synthesize all architectural choices into a formal **Skill Design Specification** and secure explicit human approval before generating any files.
   * **Smallest Mechanism Refinement**: When dogfooding reveals failures, modify the smallest relevant mechanism (a gate, a promoted rule, a negative boundary) rather than rewriting the skill.

3. **Session Protocol**:
   * If an argument was provided (e.g. `/build-skill release-notes`): Begin Stage 1 by exploring the specific friction and determining whether the capability is a Rule, Script, Guide, or Skill.
   * If invoked with no argument: Prompt the developer: *"What recurring engineering workflow, friction point, or failure mode would you like to turn into an agent skill?"*

For the complete 4-tier epistemic architecture, diagnostic questions, and refinement matrix, refer to [skill-builder](../skill-builder/SKILL.md).
