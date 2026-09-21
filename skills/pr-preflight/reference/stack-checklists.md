# Stack-specific review checklists

Load only the sections your diff touches. These are the defects that recur
per ecosystem — the universal dimensions in `SKILL.md` still apply on top.

## JavaScript / TypeScript

- `await` missing on a promise-returning call whose result is ignored — the
  error becomes an unhandled rejection, and the ordering guarantee you
  assumed is gone.
- Sequential `await` inside a `for` loop over independent work. `Promise.all`
  (or a bounded-concurrency helper) unless the calls genuinely depend on
  each other or you're deliberately rate-limiting.
- `Array.prototype.forEach` with an `async` callback — it does not await; the
  loop finishes before the work does.
- `useEffect` with a missing or over-broad dependency array; cleanup not
  returned for subscriptions, timers, or aborted fetches.
- `JSON.parse` on untrusted input without a try/catch or a schema validator.
- `==` where the operands can be `null`/`0`/`""`; `||` where `??` was meant
  (`0`, `""`, and `false` are valid values that `||` swallows).
- Type assertions (`as`) papering over a shape mismatch the compiler was
  right about. A validator at the boundary beats a cast.
- Dates: `new Date(string)` parsing is implementation-dependent for
  non-ISO input; timezone assumed rather than stated.

### Node / server

- Unbounded `fetch` with no timeout or abort signal — one slow upstream
  holds a connection until the platform kills it.
- Secrets read at module scope, so import order decides whether they exist.
- `process.env.X` used without a fallback or a startup assertion.

### React / frontend frameworks

- Server-only data (tokens, internal ids, full user records) passed into a
  client component's props, where it ships in the payload.
- A component marked client-side that has no interactivity — it costs bundle
  size and loses server rendering for nothing.
- `key` on a list set to the array index while the list reorders.
- State derived from props in `useState` and then never resynced.

## Python

- Mutable default argument (`def f(x=[])`) — shared across calls.
- Bare `except:` or `except Exception:` swallowing the error, including
  `KeyboardInterrupt` in the bare case.
- `async def` that calls a blocking library — it stalls the whole event loop.
- A file, socket, or lock opened without a context manager.
- Iterating a dict or list while mutating it.
- `# type: ignore` with no narrowing comment explaining what is actually
  guaranteed.
- f-strings building SQL. Parameterize.

## Go

- `err` assigned and not checked, or shadowed by an inner `:=`.
- A goroutine with no way to stop (no `context`, no done channel) — it
  outlives the request that started it.
- Loop-variable capture in a closure launched per iteration (pre-Go 1.22
  semantics, and still worth being explicit about).
- `defer` inside a loop, so cleanup only happens at function exit.
- A `sync.Mutex` copied by value along with its struct.
- A nil map written to; a nil interface compared against a typed nil.

## Rust

- `unwrap()` / `expect()` on a value that can genuinely be `None`/`Err` in
  production input, not just in tests.
- A `.clone()` added to silence the borrow checker where a reference or a
  restructure was the real answer.
- `unsafe` without a comment stating the invariant that makes it sound.
- Blocking I/O inside an async fn.
- Integer arithmetic that can overflow in release mode (where it wraps
  silently rather than panicking).

## SQL and migrations

- `UPDATE` or `DELETE` with a `WHERE` narrower in intent than in text.
- A migration that is not reversible, with no down path and no note saying
  so deliberately.
- Adding a `NOT NULL` column with no default to a populated table.
- An index created without `CONCURRENTLY` (Postgres) on a large hot table —
  it takes a write lock.
- A new query pattern with no supporting index; an index added that
  duplicates an existing prefix.
- Schema and application code changing in a way that requires them to deploy
  simultaneously. Make it work across one deploy boundary in each direction.

## CI, workflows, and infrastructure

- A workflow that checks out the **PR head** where it should check out the
  **merge result**. A head can pass while merged main breaks, because two
  independently-mergeable PRs can conflict semantically (one narrows an
  import, another adds callers of it). If the check exists to protect the
  base branch, it must test the merge.
- `pull_request_target` combined with checking out untrusted code — that
  pairing hands secrets to a fork's branch.
- A secret interpolated into a shell line where it lands in logs.
- An action pinned to a moving tag rather than a SHA.
- A required check whose job succeeds even when its real work failed (for
  example, a step chain after a `continue-on-error`) — it reports green over
  a broken gate.
- A new required check added without confirming the branch protection rules
  actually reference it, and vice versa.

## Shell scripts

- No `set -euo pipefail`, so a failing step silently continues.
- Unquoted variable expansions — word splitting and globbing on any path
  containing a space.
- `rm -rf "$VAR/"` where `$VAR` can be empty.
- Parsing `ls` output instead of globbing or using `find -print0`.

## Dependency changes

- A lockfile updated without the manifest, or a manifest without the
  lockfile. They ship together.
- A single member of a version-locked package family bumped alone (peer
  dependency conflicts).
- A new transitive dependency pulled in for something the standard library
  or an existing dependency already does.
- A major version bump described in the PR as a patch.
