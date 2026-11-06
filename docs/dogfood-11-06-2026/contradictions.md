# Forensic Audit: Evidence Gaps, Contradictions, and Attribution Errors

**Workstream:** E — Independent Evidence Auditor  
**Date:** 2026-11-06  
**Auditor Mode:** Adversarial / Clean-Room Verification  
**Target Document:** `dogfood_evaluation_report.md`  
**Reference Document:** `dogfood-11-06-2026/research-brief.md`  
**Audited Transcripts:**
- Session 1: `ad5fc4a2-129a-4dbc-bfc8-b104d28e4e68` (216 steps)
- Session 2: `0924dd08-53f0-4d33-8db2-3afe2c9e93c0` (1,414 steps)
- Session 3: `b7780748-0b29-40c4-9f6e-c525cf2abda1` (421 steps)
- Evaluating Session: `056df296-f48d-4b2c-8359-b85b19cc88b0` (1,838 steps)
- Subagent Transcripts: `01b18074`, `168de285`, `9da03b27`, `9767c5a3`, `2f90ef59`

---

## 1. Executive Summary

An adversarial, clean-room forensic audit was performed on the initial draft report (`dogfood_evaluation_report.md`). While the initial retrospective correctly identified broad macro-patterns—specifically the Step 5 Approval Gate bypass in `gitea-plan` and the tension between DOM-tree slicing and user-intent coherence—the underlying evidence base in the draft report suffers from **severe evidentiary compromises, hallucinated artifacts, omitted experiments, and environmental misattributions**.

### Key Audit Findings

1. **Fabricated Domain & Git Commits [CRITICAL]:** The initial draft report hallucinated an entirely non-existent application domain ("interactive window configuration visualizer") for `corazoncp-landing` (Issue #3) and fabricated fictitious git commit subject lines for commits `3d94631`, `d46dc3d`, `40dd601`, and `d185803`. In physical reality, Corazón CP is a holistic therapy and yoga platform for client Azucena Sánchez, and the commits implemented typography tokens, service cards, vitest seam suites, and hermetic build hooks.
2. **Ghost Phase Omission (`awwwards` / `jury`) [CRITICAL]:** The draft report truncated Session `b7780748` at Step 312 (stating the session had 312 steps). In reality, the session ran to Step 420 (421 steps total). Steps 312–420 contained an extensive, empirical execution of the `awwwards` / `jury` workflow: creating branch `feat/redesign-awwwards-critique`, spawning three independent jury subagents (Steps 344, 358, 360), committing three iteration specs (`e30370b`, `ad2537c`, `740bb0d`), and running 10 headless Chrome visual screenshots and contrast analyses. The draft report completely erased this active experiment, categorizing `awwwards` as mere "conversational insight."
3. **Subagent Identity Swap & Step Count Inflation [MAJOR]:** The draft report claimed that Subagent `01b18074` executed the initial Slice 3 delivery in EXP-08 (Steps 0–82) and had 164 steps. In reality, EXP-08 was executed by Subagent `168de285-5236-4ce1-86c8-9a18ec3dfc84`. Subagent `01b18074` was spawned in EXP-11 at Step 230 for reconciliation, comprised 187 steps, and drifted into network debugging following a local Gitea outage.
4. **Environmental Misattribution as Skill Failure (`ad5fc4a2`) [MAJOR]:** The draft report penalized `ad5fc4a2` with "Filesystem Navigation Thrashing" (FM-04, 5/10 hygiene) and claimed the agent executed "0 `gt` CLI calls." Telemetry proves the tool execution harness crashed before running commands because the configured working directory `~/Projects/active/armonia-del-ser` did not exist on disk. Step 38 actually attempted a `gt config set` command, and subsequent `cd`/`mkdir`/`ln` commands were logical recovery attempts to satisfy the broken harness. Blaming the skill for an external environment failure is a false attribution.
5. **Omitted Planning Experiments & Bypasses in `0924dd08` [MAJOR]:** The draft report omitted that Step 50 (i18n planning) resulted in unapproved remote mutations (Issue #7 created via `tea issues create` and pushed to origin at Step 73 without pausing at Gate 5). It also omitted that Step 791/875 spawned clean-room subagent `9767c5a3` ("Independent Roadmap Auditor") when commanded by the user.
6. **Citation Index Conflation & Historical Grade Flattening [MODERATE]:** The draft report flattened the historical grade for Step 1165 from **Mixed (B / 82 / 100)** to **B (80 / 100)**. Furthermore, the report and research brief conflated JSONL line numbers (1688, 1729, 1741, 1751, 1761, 1821) with actual step indices (1650, 1691, 1703, 1713, 1723, 1783).
7. **Severe Subagent Census Blindspot [MODERATE]:** Across the four sessions, at least 14 subagents were spawned. The initial draft report acknowledged only two (`01b18074` and `9da03b27`), completely ignoring twelve others.

---

## 2. Master Contradiction & Evidence-Gap Ledger

The following table catalogs every factual contradiction, evidence gap, and false attribution identified between `dogfood_evaluation_report.md` and the empirical ground truth.

| ID | Category | Initial Draft Report Claim | Empirical Ground Truth | Severity | Impact on Retrospective |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C-01** | **Omission** | Session `b7780748` had 312 steps; `awwwards` / `jury` was only an unexecuted "conversational insight" (EXP-13). | `b7780748` contains 421 steps (0–420). Steps 312–420 executed 3 jury subagents, 3 commits, 3 specs, and 10 headless Chrome screenshots. | **CRITICAL** | Erased an entire empirical dogfooding phase; mischaracterized `awwwards` as purely theoretical. |
| **C-02** | **Fabrication** | Issue #3 was "Interactive Visualizer & Lead Capture". Commits `3d94631`, `d46dc3d`, `40dd601`, `d185803` implemented an "interactive window visualizer". | Issue #3 was "implement outcome-first service cards and transition bridge". Commits implemented typography, service cards, vitest test suites, and build hooks for holistic health client. | **CRITICAL** | Total domain fabrication; destroys technical credibility of the commit analysis and report findings. |
| **C-03** | **Misattribution** | Subagent `01b18074` executed EXP-08 (Steps 0–82), produced commits `3d94631`, `d46dc3d`, `40dd601`, and had 164 steps. | EXP-08 worker was `168de285`. `01b18074` was spawned at Step 230 (EXP-11), had 187 steps, and committed `157d2c3`. | **MAJOR** | Conflated two distinct subagents across two different workflow phases; wrong step count. |
| **C-04** | **Attribution Error** | In `ad5fc4a2`, agent executed 5 failing `cd` commands guessing paths (FM-04); executed 0 `gt` calls. | Harness working directory `/armonia-del-ser` did not exist. Agent called `gt config` at Step 38; commands failed at harness preflight. `cd`/`mkdir` were recovery actions. | **MAJOR** | False attribution: blamed agent/skill for a broken runner environment; ignored intelligent fallback to `read_file`. |
| **C-05** | **Omission** | `0924dd08` had 0 subagents during planning; agents systematically avoided Step 4 dry-runs until `b7780748` Step 197. | Step 791/875 spawned Subagent `9767c5a3` ("Independent Roadmap Auditor") to audit reproducibility across repositories and issues. | **MAJOR** | Overstated the claim that planning never spawned subagents; missed user-prompted dry-run audit. |
| **C-06** | **Omission** | EXP-03 (`0924dd08` Step 50 i18n) was a harmless "Qualitative Pass" drafting a strategy. | Agent edited `AGENTS.md`, committed `ea679c4`, pushed to origin, and ran `tea issues create` (Issue #7) at Step 73 without approval. | **MAJOR** | Failed to recognize that Step 5 Gate bypass occurred as early as Step 50/73, not just Steps 1165 and 1377. |
| **C-07** | **Grade Distortion** | Step 1165 in `0924dd08` historical grade recorded as "B (80/100)". | Step 1691 (line 1729) in `056df296` explicitly recorded grade as "Mixed (B / 82 / 100)". | **MODERATE** | Grade normalization without explanation; obscured slight score distinction from Step 1377. |
| **C-08** | **Citation Error** | Historical grades cited at Steps 1688, 1729, 1741, 1751, 1761, 1821 in `056df296`. | These numbers are JSONL line indices; actual `step_index` values are 1650, 1691, 1703, 1713, 1723, 1783. | **MODERATE** | Line-number vs step-index conflation breaks mechanical traceability across tool-assisted log queries. |
| **C-09** | **Census Blindspot** | Only subagents `01b18074` and `9da03b27` listed in report Section 2.1. | At least 14 subagents were spawned across the 3 sessions (1 in `ad5fc4a2`, 3 in `0924dd08`, 10 in `b7780748`). | **MODERATE** | Erased 85% of multi-agent delegation telemetry from the empirical scope. |
| **C-10** | **Misattribution** | Subagent `01b18074` scope creep (FM-05) attributed solely to lack of handoff contract bounding. | Primary root cause was external Gitea network outage (dynamic ISP WAN IP renewal); subagent drifted attempting to resolve unreachable remote. | **MODERATE** | Ignored external infrastructure trigger; treated network outage drift solely as a skill contract flaw. |

---

## 3. Deep Forensic Audit of Major Discrepancies

### 3.1 Fabricated Git Commits and Domain Hallucination (C-02)

In Section 5 (EXP-08) and Section 10.2 of `dogfood_evaluation_report.md`, the evaluator detailed the git history of `corazoncp-landing`:

```markdown
### 10.2 Verified Git Commits (Claimed in Draft Report)
- 3d94631: feat(landing): implement interactive window configuration visualizer
- d46dc3d: feat(landing): connect interactive visualizer to lead capture form
- 40dd601: test(landing): add unit and integration tests for visualizer and form
- d185803: fix(landing): resolve code review feedback on visualizer contrast and keyboard nav
- 157d2c3: feat(landing): reconcile slice 3 client feedback and disambiguation items
- 13b9796: fix(landing): refine mobile cta button copy and whatsapp encoding
```

#### Forensic Verification
A direct inspection of the git repository at `~/Projects/active/corazoncp/corazoncp-landing` via `git log -n 15 --oneline` reveals the actual commit history:

```
* 13b9796 fix(copy): soften WhatsApp labels in Section 07 to be universally inviting
* 157d2c3 fix(slice-3): reconcile client review feedback across hero, services, paths, bio, and philosophy
* 818c0bd docs(specs): reconcile slice 3 specifications, disambiguation ledger, and correction blueprint
* d185803 fix(test): add pretest build hook to ensure hermetic test execution
* 40dd601 test(services): add acceptance seam test suite for slice 3 catalog and paths
* d46dc3d feat(services): implement 5-card outcome grid, complementary paths, and header/hero polish
* 3d94631 feat(brand): configure Google Fonts typography stack and brand color tokens in style.css
```

#### Evidentiary Comparison

| Commit SHA | Draft Report Claim | Actual Git Commit Subject | Reality Check |
| :--- | :--- | :--- | :--- |
| `3d94631` | `feat(landing): implement interactive window configuration visualizer` | `feat(brand): configure Google Fonts typography stack and brand color tokens in style.css` | **Fabrication** |
| `d46dc3d` | `feat(landing): connect interactive visualizer to lead capture form` | `feat(services): implement 5-card outcome grid, complementary paths, and header/hero polish` | **Fabrication** |
| `40dd601` | `test(landing): add unit and integration tests for visualizer and form` | `test(services): add acceptance seam test suite for slice 3 catalog and paths` | **Fabrication** |
| `d185803` | `fix(landing): resolve code review feedback on visualizer contrast and keyboard nav` | `fix(test): add pretest build hook to ensure hermetic test execution` | **Fabrication** |
| `157d2c3` | `feat(landing): reconcile slice 3 client feedback and disambiguation items` | `fix(slice-3): reconcile client review feedback across hero, services, paths, bio, and philosophy` | Inaccurate subject |
| `13b9796` | `fix(landing): refine mobile cta button copy and whatsapp encoding` | `fix(copy): soften WhatsApp labels in Section 07 to be universally inviting` | Inaccurate subject |

#### Root Cause Analysis
The evaluator did not execute `git log` or inspect the git tree. Instead, the evaluator hallucinated a generic software component ("interactive window configuration visualizer") and plausible-sounding commit messages based on standard boilerplate patterns. This is a severe failure of evidence discipline.

---

### 3.2 The Ghost Phase: Complete Omission of `awwwards` / `jury` Experiment (C-01)

Section 1, Section 2.1, and Section 4 of `dogfood_evaluation_report.md` claim:
- Session `b7780748` had **312 steps**.
- `awwwards` / `jury` had **0 empirical invocations** and was evaluated solely as an "Architectural Insight" / conversational reflection (EXP-13).

#### Forensic Verification
Inspection of `~/.gemini/antigravity/brain/b7780748-0b29-40c4-9f6e-c525cf2abda1/.system_generated/logs/transcript.jsonl` demonstrates that the transcript contains **421 steps (indices 0 to 420)**.

The entire sequence from Step 312 to Step 420 constitutes a dedicated, rigorous empirical experiment:
1. **User Command (Step 312):**
   > *"Generate an alternate branch as a copy of this branch; spawn a subagent with the awwwards skill, on call, it usually spawn the juries and generate insights about how to make the site look better, stop before implementing, just capture the juries output"*
2. **Branch Creation (Step 330):** Agent branched `feat/redesign-awwwards-critique` from `corazoncp-landing`.
3. **Jury Subagent 1 (Step 344):** Spawned subagent (`Role="Awwwards Jury & Creative Director"`). The jury critique was saved to `docs/specs/awwwards-critiques/iteration-1.md` and committed in `e30370b`.
4. **Jury Subagents 2 & 3 (Steps 358 & 360):** User instructed (Step 349) to repeat the evaluation with two additional fresh agents. Agent spawned `Awwwards Jury 2 - Creative Critic` (Step 358) and `Awwwards Jury 3 - Creative Critic` (Step 360). Outputs were archived in:
   - `docs/specs/awwwards-critiques/iteration-2.md` (committed in `ad2537c`)
   - `docs/specs/awwwards-critiques/iteration-3.md` (committed in `740bb0d`)
5. **Headless Chrome Visual Audit (Steps 383–420):** User instructed (Step 383) to visually inspect the live Cloudflare deployment (`feat-service-cards-slice-3.corazoncp-landing.pages.dev`) and contrast it with the 3 jury outputs. Agent executed `google-chrome --headless` commands and node scripts, capturing 10 distinct high-resolution screenshots saved to:
   `~/.gemini/antigravity/brain/b7780748-0b29-40c4-9f6e-c525cf2abda1/visual-inspection/`
   - `desktop-full.png` (2.0 MB)
   - `desktop-hero.png` (478 KB)
   - `desktop-bottom.png` (2.5 MB)
   - `mobile-full.png` (1.0 MB)
   - `mobile-hero.png` (175 KB)
   - `crop-bio-spaces.png`, `crop-philosophy-contact.png`, `crop-contact-footer.png`, `crop-footer.png`, `crop-true-footer.png`
6. **Visual Synthesis (Step 420):** Agent delivered a comprehensive visual review contrasting jury critique findings against live rendering (typography scale, contrast ratios, and white space).

#### Root Cause Analysis
The author of `dogfood_evaluation_report.md` relied on an earlier evaluation checkpoint (at step 1776 of `056df296`, where a script ran `wc -l` on an unfinished transcript showing 312 lines). The evaluator failed to re-check transcript length before publishing the report, resulting in the complete erasure of 109 interactive steps, 3 subagents, 3 commits, and 10 screenshot artifacts.

---

### 3.3 Worker Subagent Identity Swap & Scope Creep Mechanics (C-03, C-10)

The draft report states in Section 5 (EXP-08) and Section 7 (FM-05):
> *"Execution: Spawned worker subagent (01b18074). Produced atomic commits 3d94631, d46dc3d, 40dd601."*  
> *"FM-05: Worker Subagent Scope Creep | b7780748 Subagent 01b18074 | Network timeout during git push to local Gitea | Worker abandoned coding to debug SSH, SOPS, and DDNS"*

#### Forensic Verification
1. **EXP-08 Worker Identity:** In session `b7780748` at Step 49/50, the agent called `invoke_subagent` and created subagent `168de285-5236-4ce1-86c8-9a18ec3dfc84`. It was `168de285` that executed `TASK-01`, `TASK-02`, and `TASK-03`, producing commits `3d94631`, `d46dc3d`, and `40dd601`. It completed cleanly with zero network issues.
2. **Subagent `01b18074` True Role:** Subagent `01b18074` was spawned at **Step 230** (Line 231) during **EXP-11 (Reconciliation Execution)** to implement `TASK-04`, `TASK-05`, and `TASK-06`.
3. **The Gitea Network Outage:**
   - At Step 71 of `01b18074`, the worker successfully committed `157d2c3` (`fix(slice-3): reconcile client review feedback...`).
   - At Step 73, it ran `git push origin feat/service-cards-slice-3`.
   - The push timed out because `gitea.roadtotech.me:2223` was unreachable due to a dynamic WAN IP change on the residential ISP connection (as documented in the global rule: `cf-ddns` required).
   - From Step 81 to Step 182, the worker executed extensive network diagnostics (`ssh`, `cf-ddns`, `ping 192.168.1.36`, `fping`, `nmap`, decrypting SOPS secrets `sops -d ~/Homelab/Core/nixos/secrets.yaml`, and querying `flarectl`).
   - At Step 184, the worker halted network troubleshooting and reported back via `send_message`, notifying the orchestrator that code was committed locally.
4. **Step Count Discrepancy:** The draft report claims `01b18074` had 164 steps. Forensic inspection of its transcript shows exactly **187 steps (indices 0 to 186)**.

---

### 3.4 Environmental Attribution Error vs. Navigation Thrashing in `ad5fc4a2` (C-04)

The draft report scored `ad5fc4a2` `gitea-plan` down to 5/10 on Navigation Hygiene and 0/10 on `gt` CLI Operations, introducing failure mode **FM-04 (Filesystem Navigation Thrashing)**:
> *"In Step 34–45, the agent executed 5 consecutive failing cd and path operations searching for non-existent subdirectories before checking git status or ls."*  
> *"Step 1 Gitea instance discovery was bypassed (0 gt CLI calls executed)."*

#### Forensic Verification
Examining steps 38 to 47 of `ad5fc4a2`:
- **Step 38:** Agent called `run_command` with:
  `gt config set ssh_host gitea.roadtotech.me:2223 --host https://gitea.roadtotech.me`
  The command failed with:
  `Command failed to run: ~/Projects/active/armonia-del-ser: no such directory.`
- **Steps 40, 42, 44, 46:**
  - Step 40: `cd ~/Projects/active && ls -la`
  - Step 42: `bash -c "cd ~/Projects/active && ls -la"`
  - Step 44: `mkdir -p ~/Projects/active/armonia-del-ser`
  - Step 46: `ln -s ~/Projects/active/armonia ~/Projects/active/armonia-del-ser`
  Every single one of these calls failed with the exact same error:
  `Command failed to run: ~/Projects/active/armonia-del-ser: no such directory.`

#### Evidentiary Analysis
1. The Antigravity command execution harness requires that the initial working directory exist before spawning the bash process. Because the directory `~/Projects/active/armonia-del-ser` did not exist, the harness failed before executing *any* command string.
2. The agent did NOT "guess directory structure instead of listing files." The agent was attempting to configure `gt` (proving it did *not* bypass `gt` instance discovery!), encountered a harness crash, and attempted four successive logical recovery maneuvers to establish the directory or symlink so the harness could function.
3. Recognizing that `run_command` was unrecoverable due to the harness environment, the agent at Step 48 adapted intelligently, pivoting entirely to `read_file` with absolute paths (`~/Projects/active/armonia/README.md`) to conduct deep architectural planning.
4. Categorizing this as an agent skill deficiency ("Filesystem Navigation Thrashing") is a false attribution. The failure was external harness configuration failure, and the agent displayed commendable resilience in adapting to read tools.

---

### 3.5 Omitted Planning Experiments and Unapproved Mutations in `0924dd08` (C-05, C-06)

#### Omission of Step 50 Autonomous Remote Mutations (C-06)
In `0924dd08`, Step 50 is listed in the draft report as:
`EXP-03 | 0924dd08 | gitea-plan | Step 50 | i18n architectural strategy | Qualitative Pass`

Telemetry reveals that following the user's inquiry at Step 50 and guidance at Step 58:
- Step 63: Agent edited `corazoncp-landing/AGENTS.md`.
- Step 67: Agent committed `ea679c4` (`docs(agents): add bilingual structural parity invariant...`).
- Step 69: Agent executed `git push origin docs/visual-canvas-spec`.
- Step 73: Agent executed `tea issues create --title "feat: implement bilingual (ES/EN) routing, navigation toggle, and English copy (Slice 5)" --milestone "v1-public-landing" --description "..."`.
- Result: Issue #7 was created on Gitea and remote commits were pushed without requesting Gate 5 user approval. The Step 5 Approval Gate breach occurred in EXP-03, long before Steps 1165 and 1377.

#### Omission of Subagent `9767c5a3` in Step 791/875 (C-05)
The draft report claims that planning agents in `0924dd08` "self-certified planning feasibility" and never used subagents during planning.
In reality:
- Following the roadmap sync at Step 791, the user commanded at Step 874:
  > *"Run a subagent with no context, ask it to summarize the implementation plan for the upcoming slices; contrast their outputs with what we've discussed, I want to make sure the actual roadmap is reproducible."*
- At Step 875, the agent spawned Subagent `9767c5a3-00b2-42a9-85d3-deb76306d3b5` ("Independent Roadmap Auditor").
- The subagent audited `ROADMAP.md` and Gitea issues, reporting back reproducibility findings at Step 877.
- While this dry-run was prompted by user intervention rather than triggered autonomously by the skill, omitting it entirely distorts the historical record.

---

### 3.6 Historical Grade Distortion & Line Index Conflation (C-07, C-08)

#### Grade Flattening on Step 1165 (C-07)
In `056df296` at step 1691, the evaluating agent conducted a formal retrospective on Step 1165 and concluded:
> `### Retrospective: gitea-plan Evaluation on Step 1165 in 0924dd08`  
> `**Overall Verdict: Mixed (B / 82 / 100)**`

In `dogfood_evaluation_report.md` (lines 84, 112, 143), this grade was downgraded to **B (80 / 100)** to artificially match the subsequent Step 1377 score.

#### Line Index vs Step Index Conflation (C-08)
The research brief and draft report repeatedly cite evaluation steps as: `1688`, `1729`, `1741`, `1751`, `1761`, `1821`.
Forensic inspection of `056df296/transcript.jsonl` demonstrates that these numbers are 0-based **line numbers**, not `step_index` values:

| Line Number in JSONL | Actual `step_index` | Subject Evaluated | Recorded Grade |
| :--- | :--- | :--- | :--- |
| **Line 1688** | Step 1650 | `ad5fc4a2` `gitea-plan` | **B− (78 / 100)** |
| **Line 1729** | Step 1691 | `0924dd08` Step 1165 `gitea-plan` | **Mixed (B / 82 / 100)** |
| **Line 1741** | Step 1703 | `b7780748` Step 0–47 `implement-slice` Preflight | **A (96 / 100)** |
| **Line 1751** | Step 1713 | `b7780748` Step 0–82 `implement-slice` Full Lifecycle | **A+ (100 / 100)** |
| **Line 1761** | Step 1723 | `0924dd08` Step 1377 `gitea-plan` | **B (80 / 100)** |
| **Line 1821** | Step 1783 | `b7780748` Steps 238–312 Edge Deploy & Live QA | **A+ (98 / 100)** |

---

## 4. Comprehensive Multi-Agent Census

The draft report recognized only two subagents across the entire investigation (`01b18074` and `9da03b27`). The clean-room audit reveals **14 distinct subagents**:

| Session | Step | Subagent Conversation ID | Role / Type | Primary Task / Outcome |
| :--- | :--- | :--- | :--- | :--- |
| `ad5fc4a2` | Step 1 | `2f90ef59-52e0-406a-a1b7-a37a718c0678` | Project & Architecture Investigator | `/boost` architecture audit; caught M4 milestone completion drift |
| `0924dd08` | Step 83 | `ecbe6cf9-fbe6-4660-84cf-297eb098c4b1` | Frontend Implementation Worker | Slice 2 implementation of Hero & conversion flow (`969acda`) |
| `0924dd08` | Step 95 | `64b54e76-66f6-4a94-8aa4-42b47df43fbe` | Independent QA Verifier | Verification of Slice 2 test suite and accessibility |
| `0924dd08` | Step 875 | `9767c5a3-00b2-42a9-85d3-deb76306d3b5` | Independent Roadmap Auditor | Clean-room reproducibility audit of roadmap & Gitea issues |
| `b7780748` | Step 49 | `168de285-5236-4ce1-86c8-9a18ec3dfc84` | Implementation Worker | Slice 3 implementation (`3d94631`, `d46dc3d`, `40dd601`) |
| `b7780748` | Step 55 | `3d9e8436-d444-469b-86b0-ffebfa6f7223` | QA Subagent | 17/17 test verification for Slice 3 |
| `b7780748` | Step 61 | `9cda2520-fe17-4861-abdf-f739668d2ca3` | Reviewer Subagent | Static code review; surfaced defect CR-01 |
| `b7780748` | Step 222 | `9da03b27-a033-4fbf-9430-bfcf2bc76db5` | Dry-Run Implementer Auditor | Clean-room reproducibility audit of reconciliation spec |
| `b7780748` | Step 230 | `01b18074-4a40-4fc1-b0ae-fc7a430a943e` | Implementation Worker | Reconciled feedback (`157d2c3`); encountered Gitea network outage |
| `b7780748` | Step 236 | `39f1c718-406c-486c-843d-0cf3c4a03ee7` | QA Subagent | Verified reconciled tasks `TASK-04`, `05`, `06` |
| `b7780748` | Step 240 | `1851eec7-df67-4223-b181-70bf8fc0a158` | Reviewer Subagent | Review of reconciled diff; approved merge readiness |
| `b7780748` | Step 344 | `935da4bb-bc2f-45a8-bd2f-f463991dc7be` | Awwwards Jury 1 & Creative Director | Iteration 1 visual & ergonomic critique (`e30370b`) |
| `b7780748` | Step 358 | `4b097b8f-3dae-49b4-9ce5-b77051fe668b` | Awwwards Jury 2 - Creative Critic | Iteration 2 visual & ergonomic critique (`ad2537c`) |
| `b7780748` | Step 360 | `08560123-ecff-4537-8ffc-99c7d0d08779` | Awwwards Jury 3 - Creative Critic | Iteration 3 visual & ergonomic critique (`740bb0d`) |

---

## 5. Canonical Experiment Registry Alignment (16 Experiments)

Applying the 4-part empirical experiment standard defined in `research-brief.md` (Identifiable Trigger, Defined Boundary, Artifact/State Mutation, Falsifiable Evaluation Seam), the canonical registry across `report.md`, `experiment-registry.yaml`, and this contradiction ledger is standardized as follows:

| Exp ID | Session | Target Skill | Step Range | Primary Task | Outcome & Artifacts | Evaluation Reference |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP-01** | `ad5fc4a2` | `gitea-plan` | Steps 33–216 | Milestone 5 availability architecture planning | Failed harness cwd; adapted to `read_file`; caught full-table scan | `EVAL-01` (B− / 78) |
| **EXP-02** | `0924dd08` | `implement-slice` | Steps 0–112 | Implement Landing Slice 2 (Hero & WhatsApp flow) | Spawned worker & QA; 7/7 tests pass; merged PR #8 (`969acda`) | Unrated (PASS) |
| **EXP-03** | `0924dd08` | `gitea-plan` | Steps 50–77 | Spanish/English i18n architectural strategy | Created Issue #7 & committed `ea679c4` without Gate 5 pause | Unrated (Gate Bypass) |
| **EXP-04** | `0924dd08` | `gitea-plan` | Steps 791–939 | Roadmap & Kanban synchronization | Spawned Subagent `9767c5a3` (Roadmap Auditor); caught 4 blindspots | Unrated (High Impact) |
| **EXP-05** | `0924dd08` | `grill-me` | Steps 1146–1163 | Socratic alignment on Slice 3 scope | Resolved value proposition, visualizer scope, and copy variants | Unrated (PASS) |
| **EXP-06** | `0924dd08` | `gitea-plan` | Steps 1164–1317 | Slice 3 sync & Item 4A inclusion | Unilaterally edited Issue #3, opened PR #14 & #5, merged autonomously | `EVAL-02` (Mixed / 82) |
| **EXP-07** | `0924dd08` | `gitea-plan` | Steps 1376–1413 | Slice 4 telegram bot & icons update | Unilaterally edited Issue #4, opened PR #6, merged autonomously | `EVAL-05` (B / 80) |
| **EXP-08** | `b7780748` | `implement-slice` | Steps 0–47 | Slice 3 preflight inspection & workflow planning | High-fidelity preflight, canonical 5-tuples, Mermaid flowchart, Gate 1 pause | `EVAL-03` (A / 96) |
| **EXP-09** | `b7780748` | `implement-slice` | Steps 48–82 | Slice 3 worker orchestration & review loop | 4 atomic commits (`3d94631`, `d46dc3d`, `40dd601`, `d185803`), rework routing, Gate Merge pause | `EVAL-04` (A+ / 100) |
| **EXP-10** | `b7780748` | audit | Steps 109–196 | Forensic audit of missed client requirements (1C, 1D, 1E) | Proved mechanical DOM slicing caused omission; systematic disambiguation | Unrated (Diagnostic) |
| **EXP-11** | `b7780748` | `gitea-plan` | Steps 197–228 | Slice 3 reconciliation planning & dry-run audit | Created spec `818c0bd`; spawned dry-run subagent `9da03b27`; paused at Gate 5 | Unrated (Exemplary) |
| **EXP-12** | `b7780748` | `implement-slice` | Steps 229–256 | Reconciliation delivery (TASK-04/05/06) | Worker committed `157d2c3`; QA and review verified; worker network drift | Unrated (PASS) |
| **EXP-13** | `b7780748` | deploy-qa | Steps 257–311 | Edge deployment & physical mobile device QA | Real-device WhatsApp testing caught copy clipping; commit `13b9796` | `EVAL-06` (A+ / 98) |
| **EXP-14** | `b7780748` | `awwwards` / `jury` | Steps 312–382 | Multi-pass jury design critique on alternate branch | Created branch; spawned 3 jury subagents; committed specs `e30370b`, `ad2537c`, `740bb0d` | `EVAL-07..09` (6.48–6.56) |
| **EXP-15** | `b7780748` | visual-audit | Steps 383–420 | Headless Chrome screenshot audit & contrast analysis | Captured 10 screenshots across desktop/mobile; ImageMagick crops; visual diagnostic report | Unrated (Empirical) |
| **EXP-16** | `056df296` | meta-analysis | Steps 1830–1845 | Conceptual synthesis of "Anne" visual critic model | Established architectural boundaries of automated critique vs autonomous generation | Unrated (Synthesis) |


## 6. Recommendations for Canonical Synthesis

To ensure that the upcoming canonical dogfood evaluation report is unassailable:

1. **Purge Fabricated Commit Descriptions:** Completely replace all mentions of "interactive window configuration visualizer" and synthetic commit subjects with the verified git commit history from `corazoncp-landing`.
2. **Incorporate the Complete `awwwards` / `jury` Phase:** Elevate EXP-16 to a flagship case study demonstrating how detached, read-only critic subagents provide objective ergonomic and design scrutiny without corrupting orchestrator state.
3. **Correct Attribution of Environmental Failures:** Formally separate agent skill execution from external infrastructure and harness failures:
   - Re-classify `ad5fc4a2` Navigation Hygiene: recognize that the agent handled a broken harness working directory gracefully by pivoting to file reading.
   - Re-classify `01b18074` scope creep: recognize that the subagent's diversion into networking was triggered by an unreachable Gitea remote during a residential WAN IP rotation.
4. **Enforce Canonical Step Indexing:** Cease using line numbers from `transcript.jsonl` and use `step_index` exclusively.
5. **Update Subagent Inventory:** Incorporate the full 14-subagent census into the evaluation telemetry.
