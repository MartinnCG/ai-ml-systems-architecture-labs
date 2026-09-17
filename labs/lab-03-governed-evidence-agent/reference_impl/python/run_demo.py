"""Run the deterministic Lab 03 M1 example."""

from __future__ import annotations

import json
from pathlib import Path

from governed_baseline import packet_from_mapping, result_to_mapping, run


def main() -> int:
    fixture = Path(__file__).with_name("fixtures") / "m9a_public.json"
    packet = packet_from_mapping(json.loads(fixture.read_text()))
    print(json.dumps(result_to_mapping(run(packet)), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
