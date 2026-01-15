# Lab 01 — Event vs State

## Purpose
This lab formalizes the most important distinction in event-driven systems:

- **Events** are immutable facts: what happened.
- **State** is a derived view: what we believe is true *now*, computed from events.

The lab provides a minimal, executable reference model to demonstrate:
- why events must be persisted as the source of truth,
- why state must be treated as disposable and reconstructible,
- how design mistakes in this boundary create non-debuggable systems.

## Scope
This lab focuses on:
- definitions that hold under operational constraints (crashes, restarts, partial failures),
- deterministic reconstruction of state from an event log,
- explicit invariants (what must always remain true).

Out of scope:
- distributed consensus,
- networking,
- storage engines,
- ML models.

## Core Definitions

### Event
An **event** is:
- an immutable record of a fact,
- append-only,
- time-ordered (by a chosen ordering mechanism),
- sufficient to reconstruct state.

An event is not “a message.” A message may be transient; an event is a persisted fact.

### State
**State** is:
- a derived projection,
- mutable,
- replaceable,
- safe to discard and recompute.

State exists to serve queries and operations efficiently. It must never be the only record of truth.

## Architectural Claim
A system is operationally trustworthy if:
1. Events are durable and append-only.
2. State can be deterministically rebuilt from events.
3. State changes are fully explainable by events.

If any of the above is false, you will eventually encounter "ghost" behavior that cannot be debugged.

## Invariants (Non-negotiable)
- **I1: Append-only log** — Events are never modified in place.
- **I2: Deterministic replay** — Given the same event sequence, replay produces the same state.
- **I3: No hidden state transitions** — Every state transition must be explainable by one or more events.
- **I4: Rebuildability** — The system can rebuild state after a crash using only the event log.

## Minimal Example Scenario
We model a simple “Node registration” lifecycle:

Events:
- `NodeRegistered(node_id)`
- `NodeHeartbeat(node_id, ts)`
- `NodeDecommissioned(node_id)`

Derived state:
- known nodes
- last heartbeat timestamp
- decommissioned flag

We intentionally keep this small to focus on the boundary, not on domain complexity.

## Failure Modes (What breaks systems)
- Persisting only state and treating it as truth (no audit trail, no replay).
- Mutating or deleting events to “fix” mistakes (breaks causality).
- Non-deterministic replay (time-based logic inside replay, random IDs).
- Side effects during replay (replay should be pure; side effects must be controlled).

## Outputs
This lab includes:
- a reference event log (in-memory for simplicity),
- a projector that derives state from events,
- a simple CLI run to show:
  - state update during live append,
  - full rebuild from scratch producing identical state.

See `architecture.md` and `reference_impl/python/README.md`.
