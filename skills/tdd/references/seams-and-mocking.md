# Public Seams and Boundary Mocking

Reference for `tdd`. Defines how to pick the test boundary, when to use real fixtures versus mocks, and how to shape interfaces so tests survive refactors.

Derived and adapted from Matt Pocock's `tdd` skill (`github.com/mattpocock/skills`), extended with cross-stack fixture and schema-integrity rules.

## 1. Choosing the Public Seam

A **seam** is the public interface where callers observe behavior without reaching into internal functions, private fields, or module wiring.

When proposing a new seam to the human owner, state two things in one line:
- **What it catches**: the behavioral contract verified through this boundary.
- **What it misses**: the outer integration layer left to `verify-slice` or higher-level tests.

| Stack | Typical Public Seam | Avoid Testing Directly |
| :--- | :--- | :--- |
| **Python API / Library** | HTTP route contract (`TestClient` / `AsyncClient`), CLI, or public service/client entrypoint | Private helper functions, ORM query-builder internals |
| **TypeScript UI / Client** | Rendered component DOM + user events + typed API client boundary | Internal component state variables, private render helpers |
| **Bash CLI / Script** | Script execution (`bats` `run ./script.sh` or subshell with exit code, stdout/stderr, files) | Internal shell helper functions sourced in isolation |
| **Rust CLI / Crate** | Public crate functions/traits or CLI command execution (`assert_cmd`) | Private module helpers, internal buffer representations |
| **Java Service / API** | Public service/controller interface (`MockMvc` / `TestRestTemplate` / domain facade) | Private methods, reflection-accessed fields |

## 2. Where to Mock (System Boundaries Only)

Mock or fake **external boundaries you do not control**:
- Third-party network services (payments, email, external webhooks, OAuth providers).
- Wall-clock time, timers, and randomness.
- External OS or hardware effects outside deterministic test control.

Prefer **real lightweight fixtures** over mocks whenever practical:
- Temporary or in-memory databases initialized through the real schema/migrations rather than mocked ORM sessions.
- Temporary directories (`tmp_path` in `pytest`, `tempfile::TempDir` in Rust) rather than mocked filesystem calls.
- Typed domain builders or service calls to seed state. Never maintain ad-hoc raw SQL seed strings that bypass migrations and silently drift from the real schema.

Never mock **collaborators you own**:
- Internal modules, domain services, formatters, or validators within the same codebase. If mocking an internal module feels necessary, the interface boundary is in the wrong place.

## 3. Shaping Interfaces for Clean Boundary Doubles

1. **Inject timing, clock, and external dependencies explicitly**: Pass clocks, sleep functions, HTTP/transport adapters, or external clients into functions/constructors with production defaults instead of globally monkeypatching stdlib runtime primitives in tests.
2. **Use operation-specific adapter methods**: Prefer typed boundary methods (`api.getSession(id)`, `api.checkInAttendee(id)`) over a single generic `fetch(url, options)` mock so each test stubs one explicit response without reimplementing URL routing inside test setup.

| Language | Ban Global Runtime Patching | Inject Timing / Clock Seam Instead |
| :--- | :--- | :--- |
| **Python** | `monkeypatch.setattr(asyncio, "sleep", ...)`, `patch("time.monotonic")` | `sleep_fn: Callable[[float], Awaitable[None]] = asyncio.sleep`, `clock_fn = time.monotonic` |
| **TypeScript** | `vi.spyOn(globalThis, "setTimeout")` / global `Date` patching when avoidable | Optional `{ now = Date.now, sleep = defaultSleep }` dependency param |
| **Bash** | Replacing system `sleep`/`date` globally in `PATH` when an arg/env seam fits | Injected env var/command hook (e.g. `SLEEP_CMD="${SLEEP_CMD:-sleep}"`) or CLI flag |
| **Rust** | Global static mutable clocks or `#[cfg(test)]` timer branches | Trait bound or closure param (`impl Fn() -> Instant` / `sleep: impl Fn(Duration)`) |
| **Java** | `MockedStatic<Instant>` / `System` time overrides | Inject `java.time.Clock` (`Clock.fixed(...)` in tests) or `Sleeper` functional interface |

## 4. Deterministic Async Synchronization and Guaranteed Teardown

1. **Never synchronize concurrent work with fixed sleeps or silent loops**: Fixed delays (`asyncio.sleep(0.02)`, `setTimeout(..., 50)`, `sleep 1`, `thread::sleep`, `Thread.sleep`) flake under CI load, and `for _ in range(N)` loops that break silently mask hung background tasks. Wait on explicit events/barriers or use a bounded condition helper that fails with a clear timeout error.
2. **Guarantee cleanup on assertion failure**: Every test spawning background tasks, subprocesses, sockets, or temp files must clean up even when an assertion fails.

| Language | Deterministic Synchronization | Guaranteed Teardown |
| :--- | :--- | :--- |
| **Python** | `asyncio.Event` / bounded `wait_for(predicate, timeout=1.0)` raising `AssertionError` | `pytest` `yield` fixture, `async with`, or `try...finally` |
| **TypeScript** | `vi.waitFor(...)` / `expect.poll(...)` / explicit deferred `Promise` | `afterEach` / `try...finally` |
| **Bash** | Bounded readiness polling loop exiting non-zero on timeout | `trap 'rm -rf "$tmpdir"; kill "$bg_pid" 2>/dev/null || true' EXIT` |
| **Rust** | Channels (`mpsc`), `Notify`, or bounded poll loop panicking on timeout | RAII `Drop` guards and `tempfile::TempDir` |
| **Java** | `CountDownLatch`, `CompletableFuture`, or `Awaitility.await()` | `@AfterEach` and `try-with-resources` (`AutoCloseable`) |
