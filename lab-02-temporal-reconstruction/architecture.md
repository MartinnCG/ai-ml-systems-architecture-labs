# Architecture — Temporal Reconstruction & Deterministic Replay

## Architectural Goal

Enable a system to deterministically reconstruct its operational state at any point in time using only an immutable, ordered event timeline.

The architecture prioritizes:
- explainability over performance,
- determinism over convenience,
- debuggability over optimization.

---

## Core Components

### 1. Event Timeline

**Responsibility**  
Maintain the complete historical truth of the system.

**Properties**
- append-only
- totally ordered
- immutable once written

**Notes**
The timeline is not a log for observation.
It is the authoritative source of truth from which all states are derived.

---

### 2. Projector

**Responsibility**  
Derive operational state from the event timeline.

**Properties**
- pure (no side effects)
- deterministic
- idempotent

**Notes**
The projector must not:
- access external systems,
- generate new events,
- depend on wall-clock time.

Given the same ordered events, it must always produce the same state.

---

### 3. Replay Engine

**Responsibility**  
Reconstruct system state by reapplying events through the projector.

**Capabilities**
- full replay (from genesis)
- bounded replay (until a given event index)
- time-based replay (until a timestamp)

**Notes**
Replay is a first-class operation, not a recovery hack.
The system must be designed to replay at any time.

---

### 4. State Comparator

**Responsibility**  
Verify equivalence between live-derived state and replay-derived state.

**Purpose**
- detect divergence
- validate determinism
- surface hidden side effects

**Notes**
If live state and replayed state diverge, the system is not trustworthy.

---

## Processing Paths

### Live Processing Path

1. Event is appended to the event timeline.
2. Projector applies the event to the current operational state.
3. State is updated incrementally.

This path is optimized for normal operation.

---

### Replay Processing Path

1. Event timeline is read from the beginning or from a defined cut.
2. Projector reapplies each event in order.
3. State is rebuilt without external interaction.

This path is optimized for correctness and explainability.

---

## Hard Separation of Concerns

Live processing and replay processing share:
- the same event definitions,
- the same projector logic.

They must never share:
- side effects,
- external integrations,
- time-based behavior.

Mixing these paths introduces non-determinism and invalidates replay.

---

## Temporal Cuts

The architecture supports explicit temporal cuts:
- rebuild until event N,
- rebuild until timestamp T.

This enables:
- incident forensics,
- historical state inspection,
- pre-incident reconstruction.

Temporal cuts are treated as architectural primitives.

---

## Invariants

The architecture enforces the following invariants:

- The event timeline is the sole source of truth.
- Replay produces the same state as live processing.
- Replay does not emit new events.
- Replay does not trigger side effects.
- Event order defines system behavior.

Violating any of these breaks system explainability.

---

## Intentional Exclusions

This architecture intentionally excludes:
- snapshots or checkpoints,
- persistence mechanisms,
- concurrency handling,
- performance optimizations.

These concerns are deferred until determinism and explainability are guaranteed.
