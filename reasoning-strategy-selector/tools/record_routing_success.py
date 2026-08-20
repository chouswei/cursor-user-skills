#!/usr/bin/env python3
"""Emit LED_TO_SUCCESS CREATE rows for MemNet after successful routing (Phase 4).

Usage:
  python tools/record_routing_success.py TSK_route_abc sysml-refactorer code-reviewer
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_graph_lib import SEED_PATH, _gql_esc, parse_wire_file  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Format LED_TO_SUCCESS edges for memnet.add")
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

    for i, sid in enumerate(args.skill_ids):
        eid = f"E_{args.tsk_id}_{sid}_{i}"
        print(
            "CREATE (:TSK {id: '"
            + _gql_esc(args.tsk_id)
            + "'})-[:LED_TO_SUCCESS {id: '"
            + _gql_esc(eid)
            + "', note: '"
            + _gql_esc(args.note)
            + "', recycle: 'persistent'}]->(:SKL {id: '"
            + _gql_esc(sid)
            + "'})"
        )
    print("# Paste into memnet.add with allow_new_relation=true", file=sys.stderr)


if __name__ == "__main__":
    main()
