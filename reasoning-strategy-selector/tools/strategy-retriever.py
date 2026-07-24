"""
Graph trigger retriever — ranks skills from skill-graph-seed.wire @TRG rows.

Use instead of convolution or full corpus paste:
  python tools/strategy-retriever.py "cross-file refactor" -n 3
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_graph_lib import SEED_PATH, match_triggers, parse_wire_file, route_graph  # noqa: E402


def retrieve(query: str, max_results: int = 3) -> list[str]:
    g = parse_wire_file(SEED_PATH)
    if not g.skills:
        return []
    order, _, _ = route_graph(query, g, top_n=max_results)
    if order:
        return order
    hits = match_triggers(query, g)
    return [sid for sid, _ in hits[:max_results]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Graph trigger retriever for skill routing.")
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("-n", "--max-results", type=int, default=3)
    args = parser.parse_args()
    for sid in retrieve(args.query, args.max_results):
        print(sid)


if __name__ == "__main__":
    main()
