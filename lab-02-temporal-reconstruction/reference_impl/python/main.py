"""
Lab 02 — Temporal Reconstruction & Deterministic Replay

This module defines the execution flow of the lab.

It demonstrates:
- live event processing,
- deterministic replay from genesis,
- bounded temporal replay,
- equivalence verification between live and replayed state.

No implementation logic is present here.
"""


from components import (
    Event,
    EventTimeline,
    OperationalState,
    Projector,
    ReplayEngine,
    StateComparator,
    empty_state,
)


def main() -> None:
    # -------------------------------------------------
    # System wiring (conceptual, not implemented)
    # -------------------------------------------------

    timeline = EventTimeline()
    projector = Projector()
    replay_engine = ReplayEngine(timeline=timeline, projector=projector)
    comparator = StateComparator()

    # -------------------------------------------------
    # Live processing path
    # -------------------------------------------------

    live_state: OperationalState = empty_state()

    # Conceptual list of events representing historical facts
    events: list[Event] = [
    Event(event_id=1, timestamp=1),
    Event(event_id=2, timestamp=2),
    Event(event_id=3, timestamp=3),
]


    for event in events:
        timeline.append(event)
        live_state = projector.apply(live_state, event)

    # -------------------------------------------------
    # Replay processing paths
    # -------------------------------------------------

    # Full replay from genesis
    replayed_full_state = replay_engine.replay_full()

    # Bounded replay (temporal cut)
    replayed_partial_state = replay_engine.replay_until(index=0)

    # -------------------------------------------------
    # Verification
    # -------------------------------------------------

    assert comparator.equivalent(
        live_state,
        replayed_full_state,
    ), "Live state and full replay state diverged"

    # Partial replay is expected to differ from full state
    assert not comparator.equivalent(
        replayed_partial_state,
        replayed_full_state,
    ), "Partial replay unexpectedly matched full state"

    print("Temporal reconstruction flow defined successfully.")


if __name__ == "__main__":
    main()
