#!/usr/bin/env python3
"""Emit LED_TO_SUCCESS CREATE lines after successful routing (Phase 4).

Usage:
  python tools/record_routing_success.py TSK_route_abc sysml-refactorer code-reviewer
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_graph_lib import SEED_PATH, _cypher_escape, parse_wire_file  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Format LED_TO_SUCCESS CREATE lines for mutate")
    parser.add_argument("tsk_id", help="Routing task id, e.g. TSK_route_sysml_refactor")
    parser.add_argument("skill_ids", nargs="+", help="Skill ids that succeeded")
    parser.add_argument("--note", default="pass", help="Edge note field")
    args = parser.parse_args()

    if not re.match(r"^TSK_route_[a-z0-9_-]+$", args.tsk_id):
        print("ERROR: tsk_id must match TSK_route_<slug>", file=sys.stderr)
        sys.exit(2)

    g = parse_wire_file(SEED_PATH)
    bad = [s for s in args.skill_ids if s not in g.skills]
    if bad:
        print(f"ERROR: unknown SKL ids: {bad}", file=sys.stderr)
        sys.exit(1)

    note = _cypher_escape(args.note)
    tid = _cypher_escape(args.tsk_id)
    for i, sid in enumerate(args.skill_ids):
        eid = _cypher_escape(f"E_{args.tsk_id}_{sid}_{i}")
        sk = _cypher_escape(sid)
        print(
            f"CREATE (:TSK {{id: '{tid}'}})-[:LED_TO_SUCCESS "
            f"{{id: '{eid}', note: '{note}', recycle: 'persistent'}}]->(:SKL {{id: '{sk}'}})"
        )
    print("# Paste CREATE lines into mutate", file=sys.stderr)


if __name__ == "__main__":
    main()
