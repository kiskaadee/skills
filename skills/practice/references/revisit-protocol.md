# Revisit & Delayed Retrieval Protocol

Protocol for spacing and successive relearning in `practice`. Implements recall-before-reveal and graduated spacing intervals without external databases or background schedulers.

---

## 1. Discovery

When `/practice` runs without arguments, or with `/practice review`, scan for existing practice records in:
- Notes inbox (e.g. `00-inbox/` or configured vault inbox)
- Learning guides (e.g. `04-learning/`)
- Project-local documentation (e.g. `docs/`)

Filter for markdown files where frontmatter has `type: practice` and `revisit_after` is on or before today's date (`YYYY-MM-DD`). If matches exist, surface up to 3 due topics and ask whether to review one or start a new topic.

---

## 2. Recall-Before-Reveal Sequence

1. **State the prompt**: Present the original topic or problem statement and any starting constraints. Never show the previous answer, code solution, or explanation.
2. **Elicit unaided retrieval**:
   - For concepts: "Explain the mechanism and core invariant in your own words."
   - For algorithms / LeetCode: "State the pattern, time/space complexity, and solve the problem without assistance."
   - For architecture: "Why was this choice made, and what trade-off did we accept?"
3. **Calibrate attempt**: Label feedback (`correct`, `missing`, `wrong`, `unsupported`) and record assistance level (`independent`, `hints`, etc.).
4. **Reveal and compare**: Open the previous practice record and compare. Highlight what held, what decayed, and what changed.
5. **Update record**: Record the new attempt, update calibration, and compute the next `revisit_after` date.

---

## 3. Spacing Interval Progression

Spacing expands as recall becomes more independent and durable:

| Stage | Trigger / Evidence | Next Revisit | Action |
|---|---|---|---|
| **Initial** | Solved with hints or shown-solution | `+2-3 days` | Scheduled for an unaided re-solve |
| **Stage 1** | Recalled with minor hint or prompt | `+7 days` | Reinforces decaying memory |
| **Stage 2** | Demonstrated independently without hints | `+21-30 days` | Long-term consolidation check |
| **Stage 3** | Succeeded independently on Stage 2 or solved transfer challenge | None | Remove `revisit_after`, set `status: retained` |
| **Regression** | Struggled, incorrect, or needed full solution | `+2-3 days` | Reset interval back to Initial |

---

## 4. LeetCode & Algorithm Practice Adaptation

1. **Independent attempt**: Read constraints, predict time and space complexity, and write initial approach before asking for guidance.
2. **Graduated hints**: If stuck, escalate through the hint ladder (syntax check -> directional hint -> invariant/pattern hint -> code example). Record assistance level.
3. **Post-acceptance invariant**: After submission is accepted, formulate:
   - Pattern name (e.g. Two Pointers, Monotonic Stack, Sliding Window).
   - Core invariant (what condition holds on each iteration/state transition).
   - Time and space complexity rationale.
4. **Revisit rule**: Any problem solved with `hints` or `shown-solution` gets `revisit_after: +2-3 days` for an unaided re-solve.
