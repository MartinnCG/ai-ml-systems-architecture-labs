from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


# =========================
# Events
# =========================

@dataclass(frozen=True)
class Event:
    event_id: int
    timestamp: int


# =========================
# Event Timeline
# =========================

class EventTimeline:
    def __init__(self) -> None:
        self._events: List[Event] = []

    def append(self, event: Event) -> None:
        if self._events:
            last = self._events[-1]
            if event.timestamp < last.timestamp:
                raise ValueError("Events must be appended in non-decreasing timestamp order")
        self._events.append(event)

    def read_all(self) -> List[Event]:
        return list(self._events)

    def read_until(
        self,
        *,
        index: Optional[int] = None,
        timestamp: Optional[int] = None,
    ) -> List[Event]:
        if (index is None and timestamp is None) or (index is not None and timestamp is not None):
            raise ValueError("Provide exactly one of index or timestamp")

        if index is not None:
            if index < 0:
                return []
            return list(self._events[: index + 1])

        # timestamp cut
        return [e for e in self._events if e.timestamp <= int(timestamp)]


# =========================
# Operational State
# =========================

class OperationalState:
    def __init__(self, applied_events: int = 0) -> None:
        self.applied_events = applied_events

    def copy(self) -> "OperationalState":
        return OperationalState(applied_events=self.applied_events)

    def __repr__(self) -> str:
        return f"OperationalState(applied_events={self.applied_events})"


def empty_state() -> OperationalState:
    return OperationalState(applied_events=0)


# =========================
# Projector
# =========================

class Projector:
    def apply(self, state: OperationalState, event: Event) -> OperationalState:
        new_state = state.copy()
        new_state.applied_events += 1
        return new_state


# =========================
# Replay Engine
# =========================

class ReplayEngine:
    def __init__(self, timeline: EventTimeline, projector: Projector) -> None:
        self._timeline = timeline
        self._projector = projector

    def replay_full(self) -> OperationalState:
        state = empty_state()
        for event in self._timeline.read_all():
            state = self._projector.apply(state, event)
        return state

    def replay_until(
        self,
        *,
        index: int | None = None,
        timestamp: int | None = None,
    ) -> OperationalState:
        state = empty_state()
        events = self._timeline.read_until(index=index, timestamp=timestamp)
        for event in events:
            state = self._projector.apply(state, event)
        return state


# =========================
# State Comparator
# =========================

class StateComparator:
    def equivalent(self, a: OperationalState, b: OperationalState) -> bool:
        return a.applied_events == b.applied_events
