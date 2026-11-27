# Build-and-Break, Predict-Before-Run, and Code-Tracing Protocols

Used by `practice` when building stretch projects above your current skill level, debugging unknowns, or sharpening code-reading fluency.

## 1. Build-and-Break (Stretch Projects)

1. **Ugly Heartbeat (Vertical Flow First):**
   - Skip upfront architecture, config layers, and abstractions until data moves end-to-end.
   - Write the smallest working input -> output path (~30 ugly lines) in one sitting, touching raw primitives rather than hiding behind wrappers when learning is the goal.
   - Layer error handling, concurrency, and edge cases one at a time after the heartbeat runs.
2. **Read the Raw Spec ("Close the Tab"):**
   - When stuck on a protocol, runtime, or library, close secondary tutorials and inspect the primary specification, RFC, or upstream source directly.
   - State the exact contract or invariant from the primary source in your own words before writing code.
3. **Learner-Run 30-Line `scratch/` Isolation Labs:**
   - **Trigger:** Two unknowns interact, or you start guessing how a primitive behaves.
   - **Protocol:** Pause edits in the main project. Create an isolated ~30-line script in `scratch/` testing only the single unknown component.
   - **Break it on purpose:** Force boundary conditions (e.g., 1-byte buffers, empty input, timeouts, malformed payloads) until you predict every outcome accurately, then return to the main build.

## 2. Predict-Before-Run (Hypothesis Discipline)

Before running a test, command, or `scratch/` experiment, state your hypothesis explicitly:
- **Prediction:** "I expect `X` because of mechanism `Y`."
- **Falsifier:** "If `Z` happens instead, my assumption about `W` is wrong."
- After running, compare actual output against the prediction before changing a single line. Change one variable at a time.

## 3. Code-Tracing Drills (Read Before Running)

1. Select 25-50 lines of real code (from an active repo or standard library).
2. Given one normal input and one edge-case input, trace variables, branches, and return values on paper or in chat without executing the code.
3. State where the code could fail or misbehave, then run it to verify your trace and log any mismatch as a reasoning trap.
