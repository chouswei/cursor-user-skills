#!/usr/bin/env python3
"""Scan skills and write a skill-graph-seed.wire (pack or repo, never both).

Pack:
  python tools/scan_skills_to_wire.py --write

Repo (MUST pass --repo-seed; MUST NOT write repo SKL into the pack seed):
  python tools/scan_skills_to_wire.py --repo-skills <repo>/.cursor/skills \\
      --repo-seed <repo>/.cursor/skills/skill-graph-seed.wire --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skill_graph_lib import (
    SEED_PATH,
    build_seed_wire,
    discover_skills,
    graph_to_wire_lines,
    validate_density,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a skill-graph-seed.wire from SKILL.md scan (pack or repo, not merged)."
    )
    parser.add_argument(
        "--repo-skills",
        default="",
        help="Repo .cursor/skills path. Scan repo SKL only; do not merge into the pack seed.",
    )
    parser.add_argument(
        "--repo-seed",
        default="",
        help="Write path for a repo seed. Required with --repo-skills --write.",
    )
    parser.add_argument("--write", action="store_true", help="Write the bound seed file")
    args = parser.parse_args()

    repo_skills = args.repo_skills.strip()
    repo_seed = args.repo_seed.strip()

    if repo_skills and args.write and not repo_seed:
        print(
            "ERROR: --repo-skills --write requires --repo-seed. "
            "MUST NOT merge repo SKL into the pack seed.",
            file=sys.stderr,
        )
        sys.exit(2)
    if repo_seed and not repo_skills:
        print("ERROR: --repo-seed requires --repo-skills.", file=sys.stderr)
        sys.exit(2)

    if repo_skills:
        discovered = discover_skills(
            extra_repo_paths=[Path(repo_skills)],
            include_pack=False,
        )
        skg_id, pack, dest = "SKG_repo", "repo", Path(repo_seed) if repo_seed else None
    else:
        discovered = discover_skills(include_pack=True)
        skg_id, pack, dest = "SKG_global", "user_pack", SEED_PATH

    graph = build_seed_wire(discovered, skg_id=skg_id)
    errors = validate_density(graph)
    lines = graph_to_wire_lines(graph, skg_id=skg_id, pack=pack)

    print(
        f"Discovered {len(discovered)} skills, {len(graph.triggers)} triggers, "
        f"{len(graph.edges)} edges (skg={skg_id})."
    )
    if errors:
        print(f"WARN: {len(errors)} density issues (first 5):", file=sys.stderr)
        for e in errors[:5]:
            print(f"  {e}", file=sys.stderr)
    else:
        print("OK: edge-density contract satisfied.")

    if args.write:
        if dest is None:
            print("ERROR: no destination seed path.", file=sys.stderr)
            sys.exit(2)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {dest}")
    else:
        print("Dry-run (use --write to save).")


if __name__ == "__main__":
    main()
