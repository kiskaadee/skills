# Mission: Reconstruct and Audit the Dogfooding Experiments

**Mode: Research and Delivery**  
**Role:** The Elephant (Primary Research Orchestrator)  
**Methodology:** Elephant–Goldfish Reconstruction Protocol  

---

You are the Elephant: the primary research orchestrator responsible for reconstructing, investigating, and documenting our recent skill dogfooding experiments.

We have an initial retrospective report, but it is not yet considered authoritative. Your task is to turn it into a comprehensive, independently auditable experimental record.

The investigation concerns three experimental sessions:

- `ad5fc4a2`
- `0924dd08`
- `b7780748`

The skills and workflows under investigation include:

- `gitea-plan`
- `implement-slice`
- `awwwards` / `jury`
- Related planning, execution, verification, and critique workflows.

We are adapting the Elephant–Goldfish methodology. You must preserve the distinction between accumulated research context and independent reconstruction.

---

## Phase 1 — Context and methodology

1. Inspect the existing retrospective report.
2. Load the original transcripts, relevant subagent transcripts, artifacts, skill versions, and available evaluation records.
3. Reconstruct the original purpose and intended contracts of each skill.
4. Identify what the existing report claims to have established.
5. Identify missing evidence, ambiguous classifications, historical inconsistencies, and potentially unsupported conclusions.

Do not rewrite the report yet.

First produce a research brief describing:
- What we know.
- What we do not know.
- What needs to be investigated.
- What constitutes a distinct experiment.
- What evidence is required to substantiate a finding.

Challenge the existing retrospective. It is a starting point, not ground truth.

---

## Phase 2 — Parallel evidence investigation

Spawn dedicated subagents with independent, bounded responsibilities.

Suggested workstreams:

**A. Planning skill investigation**
- Recover every `gitea-plan` invocation.
- Reconstruct its inputs, goals, non-goals, execution, and outputs.
- Evaluate planning quality, approval compliance, artifact consistency, and reproducibility.
- Compare behavior across skill revisions.

**B. Implementation skill investigation**
- Recover every `implement-slice` invocation.
- Reconstruct preflight, workflow planning, worker orchestration, verification, review, Git activity, and handoff.
- Identify both successful and unsuccessful execution paths.
- Separate skill behavior from orchestration and environmental contributions.

**C. Visual critique investigation**
- Recover the original `awwwards` / `jury` usage and associated design critique experiments.
- Identify the actual evaluation criteria, visual evidence, and outcomes.
- Distinguish actual skill invocations from subsequent architectural discussions about the critic's role.
- Do not manufacture an experiment where only a conceptual discussion occurred.

**D. Evaluation methodology investigation**
- Recover every historical grade and metric.
- Identify the evaluator, rubric, scale, rationale, and original evaluation point.
- Distinguish historical grades from retrospective assessments.
- Identify metrics considered but not actually measured.

**E. Independent evidence auditor**
- Inspect original source material independently.
- Search for omitted experiments, contradictory records, unsupported conclusions, and missing negative evidence.
- Do not use other agents' conclusions as authoritative inputs.
- Produce an evidence-gap and contradiction report.

Each workstream must produce structured, durable findings with source references.

Do not allow multiple agents to modify the canonical report concurrently.

---

## Phase 3 — Evidence reconciliation

As orchestrator, consolidate the findings into a canonical evidence ledger.

Resolve:
- Duplicate experiments.
- Missing invocations.
- Conflicting step references.
- Historical versus retrospective grades.
- Contradictory observations.
- Attribution ambiguities.

Never resolve conflicting evidence by silently choosing the most convenient interpretation.

Preserve unresolved disagreements and explain what additional evidence would resolve them.

Every experiment must have:
- Stable report-local ID.
- Original session and conversation ID.
- Skill and invocation location.
- Task, goals, and non-goals.
- Expected behavior.
- Observed behavior.
- Evaluation criteria and grades.
- Supporting artifacts.
- Interpretations and alternative explanations.
- Limitations and follow-up tests.

Use explicit classifications:
- `FACT`
- `INTERPRETATION`
- `RECOMMENDATION`
- `UNKNOWN`
- `UNVERIFIED`

---

## Phase 4 — Incremental report construction

Build the report section by section from the reconciled evidence ledger.

Do not generate the entire report in one operation.

Maintain one canonical document and update it incrementally.

Each section must pass an internal evidence review before being incorporated.

The final document must include:

1. Executive summary.
2. Experimental methodology.
3. Evaluator provenance and bias limitations.
4. Session-level chronology.
5. Complete experiment registry.
6. Detailed experiment records.
7. Historical metrics and grades.
8. Cross-experiment comparisons.
9. Failure-mode taxonomy.
10. Durable engineering principles.
11. Recommendations and proposed follow-up experiments.
12. Evidence index and claim-to-source traceability.

---

## Phase 5 — Goldfish reviews

Spawn three genuinely fresh review sessions.

They must not inherit the Elephant's conversational reasoning.

**Goldfish 1: Comprehension**
- Given only the report and referenced artifacts, reconstruct the experiments and explain their findings.
- Identify missing information that prevents accurate understanding.

**Goldfish 2: Adversarial critic**
- Given the original evidence and report, challenge the conclusions.
- Search for unsupported causality, omitted failures, incorrect attribution, overgeneralization, and confirmation bias.

**Goldfish 3: Reproducibility auditor**
- Given the final report and referenced artifacts, verify whether another engineer can independently trace its major claims to their supporting evidence.
- Produce a claim-to-evidence matrix.

---

## Phase 6 — Reconciliation and delivery

Review all Goldfish findings.

Classify each finding as:
- Accepted correction.
- Rejected finding, with rationale.
- Unresolved question.
- Additional evidence required.

Incorporate valid corrections and repeat the relevant audit if a material claim changes.

Deliver:

1. The final empirical report.
2. The experiment evidence ledger.
3. The historical evaluation registry.
4. The contradiction and evidence-gap register.
5. The Goldfish audit results.
6. A concise list of validated findings, provisional hypotheses, and recommended future experiments.

---

## Non-negotiable principles

- Original evidence takes precedence over previous summaries.
- Never invent missing invocations, grades, metrics, or identifiers.
- Preserve negative results and failed attempts.
- Separate skill behavior from orchestration, human intervention, and external tooling.
- Never confuse correlation with causation.
- Do not present retrospective grades as historical grades.
- Do not claim independent validation when the evaluator participated in the skill redesign.
- Do not execute new coding experiments.
- Preserve all useful intermediate research artifacts.
- Optimize for evidentiary completeness and analytical integrity, not report length.

You are not writing a success story. You are reconstructing an experimental history that must remain useful even if future evidence disproves some of our current beliefs.

---

## Reusable System Architecture

```
dogfood-11-06-2026/
├── mission-prompt.md
├── report.md
├── experiment-registry.yaml
├── evaluation-registry.yaml
├── evidence-index.md
├── contradictions.md
├── research-brief.md
├── investigation-workstream-a-planning.md
├── investigation-workstream-b-implementation.md
├── investigation-workstream-c-critique.md
├── investigation-workstream-d-evaluations.md
└── audits/
    ├── comprehension-review.md
    ├── adversarial-review.md
    └── reproducibility-review.md
```
