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
| **Python API (FastAPI)** | HTTP route contract via `TestClient` / `AsyncClient` or domain service entrypoint | Private helper functions, ORM query-builder internals |
| **TypeScript UI** | Rendered component DOM + user events + typed API client boundary | Internal component state variables, private render helpers |
| **Rust CLI / Crate** | Public crate functions/traits or CLI command execution (`assert_cmd`) | Private module helpers, internal buffer representations |

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

1. **Inject external dependencies explicitly**: Pass clocks, HTTP adapters, or external clients into functions/constructors rather than instantiating globals or reading environment variables inside domain logic.
2. **Use operation-specific adapter methods**: Prefer typed boundary methods (`api.getSession(id)`, `api.checkInAttendee(id)`) over a single generic `fetch(url, options)` mock. Operation-specific methods let each test stub one explicit response without reimplementing URL routing conditionals inside test setup.
