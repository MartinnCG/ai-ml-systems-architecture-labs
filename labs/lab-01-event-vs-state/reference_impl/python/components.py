
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Union


# -------------------------
# Events (immutable facts)
# -------------------------

@dataclass(frozen=True)
class NodeRegistered:
 node_id: str


@dataclass(frozen=True)
class NodeHeartbeat:
 node_id: str
 ts: int  # timestamp must be supplied by the caller


@dataclass(frozen=True)
class NodeDecommissioned:
 node_id: str


Event = Union[
 NodeRegistered,
 NodeHeartbeat,
 NodeDecommissioned,
]


# -------------------------
# Derived State (disposable)
# -------------------------

@dataclass
class NodeView:
 node_id: str
 last_heartbeat_ts: Optional[int] = None
 is_decommissioned: bool = False


@dataclass
class OperationalState:
 nodes: Dict[str, NodeView]


def empty_state() -> OperationalState:
 return OperationalState(nodes={})


# -------------------------
# Event Log (append-only)
# -------------------------

class EventLog:
 def __init__(self) -> None:
     self._events: List[Event] = []

 def append(self, event: Event) -> None:
     # invariant: events are append-only
     self._events.append(event)

 def read_all(self) -> List[Event]:
     # return a copy to avoid accidental mutation
     return list(self._events)


# -------------------------
# Projector (deterministic)
# -------------------------

def apply_event(state: OperationalState, event: Event) -> OperationalState:
 # copy-on-write for clarity
 nodes = dict(state.nodes)

 if isinstance(event, NodeRegistered):
     if event.node_id not in nodes:
         nodes[event.node_id] = NodeView(node_id=event.node_id)

 elif isinstance(event, NodeHeartbeat):
     node = nodes.get(event.node_id)
     if node is None:
         node = NodeView(node_id=event.node_id)
         nodes[event.node_id] = node

     if not node.is_decommissioned:
         node.last_heartbeat_ts = event.ts

 elif isinstance(event, NodeDecommissioned):
     node = nodes.get(event.node_id)
     if node is None:
         node = NodeView(node_id=event.node_id)
         nodes[event.node_id] = node

     node.is_decommissioned = True

 else:
     raise TypeError(f"Unsupported event type: {type(event)}")

 return OperationalState(nodes=nodes)


def rebuild_state(events: List[Event]) -> OperationalState:
 state = empty_state()
 for event in events:
     state = apply_event(state, event)
 return state