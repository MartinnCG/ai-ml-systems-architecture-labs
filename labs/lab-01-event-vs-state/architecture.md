# Lab 01 — Architecture

## System Boundary
Single-process reference model.

Components:
- **EventLog**: append-only list of events (durable in real systems; in-memory here).
- **Projector**: pure function that applies events to derive state.
- **OperationalState**: current derived view.
- **Runner**: demo script that appends events and rebuilds state.

## Data Flow

1) Append event:
Event -> EventLog.append(event)

2) Live projection:
Event -> Projector.apply(state, event) -> new_state

3) Rebuild:
EventLog.read_all() -> fold(Projector.apply) -> rebuilt_state

## Determinism Constraints
To keep replay deterministic:
- no calls to `time.time()` inside projector logic,
- timestamps must be carried by events if needed,
- IDs must be generated outside replay and stored in events.

## Why This Matters
Operationally, systems crash.
If state is the source of truth, crashes destroy correctness.
If events are the source of truth, crashes are survivable: rebuild restores state.

This boundary is the foundation for:
- checkpointing,
- auditing,
- observability contracts,
- offline debugging,
- ML feature derivation from timelines.
