# Python Reference Implementation — Lab 02

## Purpose

This reference implementation exists to **prove**, not to optimize.

It demonstrates that:
- an operational state can be reconstructed at any point in time,
- replay produces the same result as live processing,
- time-aware reconstruction is deterministic,
- replay can be executed safely without side effects.

The implementation is intentionally minimal.



## What This Implementation Demonstrates

- append-only event timeline
- deterministic replay from genesis
- bounded replay (rebuild until a temporal cut)
- equivalence between live-derived state and replay-derived state
- explicit separation between live processing and replay processing


## What This Implementation Does Not Demonstrate

This implementation does **not** attempt to show:
- persistence layers or databases
- concurrency or distribution
- performance optimizations
- snapshotting or checkpointing
- real-world integrations

Those concerns are deliberately excluded.

---

## Execution Model

The implementation follows two explicit execution paths:

### Live Processing Path
- events are appended to the timeline,
- state is derived incrementally via the projector.

### Replay Processing Path
- the timeline is replayed from genesis or a temporal cut,
- state is rebuilt using the same projector,
- no side effects are triggered.

These paths share logic but must remain behaviorally isolated.

---

## Expected Outcome

When executed:
- live processing produces an operational state,
- replay reconstructs the same state,
- divergence indicates a violation of determinism.

Any divergence is considered a system failure.

---

## Design Constraints

- replay must be deterministic
- replay must be side-effect free
- time must be explicit in events
- state must be fully disposable

These constraints are non-negotiable.

---

## How to Run (When Implemented)

From this directory:

```bash
python main.py
