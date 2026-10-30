# Defensive Invariants

Reference for `code-review`. Defines system properties that must hold true across backend APIs, frontend clients, CLI tools, and system infrastructure.

## 1. Core System Properties

Every change that handles external data, mutable state, or distributed operations must satisfy five defensive properties:

### A. Trust Boundaries
Untrusted data enters the system from HTTP parameters, headers, route variables, environment files, user input forms, external webhook bodies, or database text fields.
- **Verification Rule**: Trace every untrusted value from source to sink. Verify safe APIs, parameterization, or contextual encoding (e.g. escaping HTML for DOM text, quoting attribute values, validating URL protocols).
- **Anti-pattern**: Relying on HTML sanitization to protect URL targets (`href="javascript:..."`), or interpolating raw strings into SQL, HTML, or shell commands.

### B. Authority
Every piece of mutable state must have a single authoritative owner (usually a database, an authoritative server endpoint, or a dedicated state actor).
- **Verification Rule**: Components, views, and CLI tools must never invent duplicate truth or assume their local copy is permanently accurate after out-of-band mutations can occur.
- **Anti-pattern**: Mutating local UI counters or status badges via optimistic arithmetic without reconciling against authoritative responses.

### C. Consistency and Conflict Handling
Operations that touch shared or concurrent state must handle collisions and out-of-band updates predictably.
- **Verification Rule**: When a mutation encounters a conflict (such as HTTP 409, unique constraint violation, or file lock contention), the system must fetch authoritative state or signal conflict to the operator.
- **Anti-pattern**: Swallowing conflicts, or applying a naive local patch (like `counter + 1`) that desynchronizes whenever multiple records or operators mutate state simultaneously.

### D. Failure Semantics
When external calls, network sockets, or sub-processes fail, the system must behave deterministically.
- **Verification Rule**: Failure paths must release locks, clean up temporary files, surface understandable error messages, and avoid partial half-committed state. Retries must be idempotent.
- **Anti-pattern**: Empty `catch` or `except` blocks, unhandled promise rejections, silent fallback to empty arrays on network failures, or retrying non-idempotent mutations.

### E. Resource Boundaries
Input sizes, execution duration, concurrency, and memory consumption must have explicit boundaries.
- **Verification Rule**: Incoming payloads must have size limits; pagination must be enforced; timeouts must guard external calls; file streams and database connections must be closed deterministically.
- **Anti-pattern**: Unbounded `SELECT *` queries, unbounded regex evaluations vulnerable to catastrophic backtracking, or reading unbounded streams entirely into memory.

## 2. Multi-Stack Reference Examples

| Stack / Context | Property | Concrete Risk | Defect Pattern | Correct Invariant Pattern |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend / Web** | Trust Boundaries | XSS / DOM Injection | `el.innerHTML = '<span>' + user.name + '</span>'` | Use `textContent`, safe DOM builders, or context-aware `escapeHtml(user.name)`. |
| **Frontend / Web** | Consistency | Stale Counters on Conflict | Local counter increment on 409 duplicate check-in. | On 409 conflict, fetch authoritative session/record state from the server. |
| **Python / FastAPI** | Resource Boundaries | Memory exhaustion | Reading entire uploaded file via `await file.read()`. | Enforce payload size limits and stream chunks using configured buffer limits. |
| **Python / FastAPI** | Consistency | Race conditions | Non-atomic read-then-write on database balance or status. | Use database transactions with explicit row locks (`SELECT ... FOR UPDATE`) or atomic SQL increments. |
| **Rust / CLI** | Failure Semantics | Silent partial failure | Ignoring `Result` via `.unwrap_or_default()` on critical I/O. | Bubble up errors with contextual details via `anyhow` or domain error types; clean up staging files. |
| **NixOS / Homelab** | Authority | Secret leakage | Baking plaintext API keys into world-readable Nix store derivations. | Reference secret paths resolved at runtime via sops-nix or systemd credentials. |
