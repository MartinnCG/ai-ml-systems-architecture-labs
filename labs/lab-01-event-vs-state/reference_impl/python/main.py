from __future__ import annotations

from components import (
    EventLog,
    NodeRegistered,
    NodeHeartbeat,
    NodeDecommissioned,
    empty_state,
    apply_event,
    rebuild_state,
)


def serialize_state(state) -> dict:
    return {
        node_id: {
            "last_heartbeat_ts": view.last_heartbeat_ts,
            "is_decommissioned": view.is_decommissioned,
        }
        for node_id, view in sorted(state.nodes.items())
    }


def print_state(state) -> None:
    for node_id, data in serialize_state(state).items():
        print(f"- {node_id}: {data}")


def main() -> None:
    log = EventLog()
    state = empty_state()

    events = [
        NodeRegistered("node-001"),
        NodeHeartbeat("node-001", ts=1000),
        NodeHeartbeat("node-001", ts=1010),
        NodeRegistered("node-002"),
        NodeHeartbeat("node-002", ts=2000),
        NodeDecommissioned("node-001"),
        NodeHeartbeat("node-001", ts=9999),  # ignored after decommission
    ]

    # Live execution
    for event in events:
        log.append(event)
        state = apply_event(state, event)

    # Simulated crash + rebuild
    rebuilt_state = rebuild_state(log.read_all())

    print("LIVE STATE:")
    print_state(state)

    print("\nREBUILT STATE:")
    print_state(rebuilt_state)

    assert serialize_state(state) == serialize_state(rebuilt_state), \
        "Rebuilt state does not match live state"

    print("\nOK — deterministic replay confirmed.")


if __name__ == "__main__":
    main()
