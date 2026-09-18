"""Generate or verify the committed M3 adversarial report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from adversarial_evaluation import run_suite


REPORT = Path(__file__).with_name("m3-evaluation-report.json")


def _render(value):
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = _render(run_suite())
    if args.check:
        if not REPORT.exists() or REPORT.read_text() != rendered:
            raise SystemExit("committed M3 evaluation report is stale")
        print("M3 evaluation report verified")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
