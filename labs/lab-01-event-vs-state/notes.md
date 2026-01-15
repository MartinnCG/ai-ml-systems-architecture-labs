# Notes — Lab 01

## Common Confusions
- "Events are messages" — No. Messages are transport; events are facts.
- "State is faster so store only state" — Faster until it breaks, then you cannot recover.

## Practical Rule
If an operational bug cannot be explained by a sequence of events, the system is not debuggable.

## Extension Ideas (not implemented here)
- Add idempotency keys per event.
- Add event schema versioning.
- Add snapshot/checkpoint and verify rebuild equivalence.

## Real-World Considerations
- durable storage (WAL, DB append tables),
- ordering (monotonic sequence numbers),
- corruption handling,
- clock skew (avoid time-based logic in replay).
