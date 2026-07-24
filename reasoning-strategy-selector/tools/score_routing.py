#!/usr/bin/env python3
"""Score graph routing against routing-golden-set.md."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skill_graph_lib import SEED_PATH, SKILL_ROOT, parse_wire_file, route_graph

GOLDEN_PATH = SKILL_ROOT / "references" / "routing-golden-set.md"


def parse_golden(path: Path) -> list[dict]:
    cases = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|----") or line.startswith("| id"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        cid, intent, expected = cells[0], cells[1], cells[2]
        if cid.lower() == "id":
            continue
        alts_raw = cells[3] if len(cells) > 3 and cells[3] else expected
        alts = [a.strip() for a in alts_raw.replace("|", "/").split("/") if a.strip()]
        if not alts:
            alts = [expected]
        cases.append({"id": cid, "intent": intent, "acceptable": alts})
    return cases


def main() -> None:
    parser = argparse.ArgumentParser(description="Score graph routing golden set.")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if not GOLDEN_PATH.is_file() or not SEED_PATH.is_file():
        print("ERROR: golden set or seed missing", file=sys.stderr)
        sys.exit(2)

    cases = parse_golden(GOLDEN_PATH)
    g = parse_wire_file(SEED_PATH)
    top1 = top3 = 0
    for c in cases:
        order, _, _ = route_graph(c["intent"], g)
        hit1 = order and order[0] in c["acceptable"]
        hit3 = any(x in c["acceptable"] for x in order[:3])
        top1 += int(hit1)
        top3 += int(hit3)
        if args.verbose:
            mark = "OK" if hit1 else ("~3" if hit3 else "MISS")
            print(f"  [{mark}] {c['id']}: {order[:3]} (want {c['acceptable'][:2]})")

    n = len(cases) or 1
    print(f"graph: top1={top1}/{n} ({top1/n:.0%}) top3={top3}/{n} ({top3/n:.0%})")
    baseline = SKILL_ROOT / "references" / "routing-baseline.txt"
    baseline.write_text(f"graph: top1={top1}/{n} ({top1/n:.0%}) top3={top3}/{n} ({top3/n:.0%})\n", encoding="utf-8")


if __name__ == "__main__":
    main()
