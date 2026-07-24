#!/usr/bin/env python3
"""Scan user-pack (+ optional repo) skills and write skill-graph-seed.wire."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skill_graph_lib import (
    SEED_PATH,
    SKILL_ROOT,
    build_seed_wire,
    discover_skills,
    graph_to_wire_lines,
    parse_wire_file,
    validate_density,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate skill-graph-seed.wire from SKILL.md scan.")
    parser.add_argument(
        "--repo-skills",
        default="",
        help="Optional repo .cursor/skills path for repo-local skills",
    )
    parser.add_argument("--write", action="store_true", help="Write seed file")
    args = parser.parse_args()

    extra = []
    if args.repo_skills.strip():
        extra.append(Path(args.repo_skills))

    discovered = discover_skills(extra_repo_paths=extra or None)
    graph = build_seed_wire(discovered)
    errors = validate_density(graph)
    lines = graph_to_wire_lines(graph)

    print(f"Discovered {len(discovered)} skills, {len(graph.triggers)} triggers, {len(graph.edges)} edges.")
    if errors:
        print(f"WARN: {len(errors)} density issues (first 5):", file=sys.stderr)
        for e in errors[:5]:
            print(f"  {e}", file=sys.stderr)
    else:
        print("OK: edge-density contract satisfied.")

    if args.write:
        SEED_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {SEED_PATH}")
    else:
        print("Dry-run (use --write to save).")


if __name__ == "__main__":
    main()
