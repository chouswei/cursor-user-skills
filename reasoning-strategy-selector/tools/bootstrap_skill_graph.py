#!/usr/bin/env python3
"""
Bootstrap skill graph: validate seed, regenerate views, optional MemNet sync.

  python tools/bootstrap_skill_graph.py --regenerate-views
  python tools/bootstrap_skill_graph.py --dry-run
  python tools/bootstrap_skill_graph.py --sync   # prints wire for manual memnet.add
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skill_graph_lib import (
    SEED_PATH,
    SKILL_ROOT,
    USER_PACK,
    graph_to_wire_lines,
    parse_wire_file,
    validate_density,
)

GENERATED_MARKER = "<!-- GENERATED: do not hand-edit; run bootstrap_skill_graph.py --regenerate-views -->"


def regenerate_core_strategy_principles(g) -> str:
    header = """# Core strategy principles (generated fallback + audit view)

""" + GENERATED_MARKER + """

**Source:** [`skill-graph-seed.wire`](skill-graph-seed.wire). Regenerate: `python tools/bootstrap_skill_graph.py --regenerate-views`.

**Purpose:** Human audit view of `@SKL` node metadata from the skill graph. **Not used for routing.**

| Skill | Direction | Domain | Complexity | Stakes | Evidence | Tension |
|-------|-----------|--------|------------|--------|----------|---------|
"""
    rows = []
    for sid in sorted(g.skills):
        n = g.skills[sid]
        rows.append(f"| {n.id} | {n.dir} | {n.domain} | {n.cx} | {n.stakes} | {n.ev} | {n.tension} |")
    footer = """
---

## Routing

Skill selection is **graph-only** (triggers + typed edges). See [`skill-graph.md`](skill-graph.md) and `route_graph()` in `tools/skill_graph_lib.py`.
"""
    return header + "\n".join(rows) + footer


def regenerate_skill_graph_triggers(g) -> str:
    """Return markdown table rows for SKILL-GRAPH.md trigger section."""
    pattern_label = {"G": "Generator", "R": "Reviewer", "P": "Pipeline", "T": "Tool-wrapper"}
    rows = []
    trg_by_skill: dict = {sid: [] for sid in g.skills}
    for e in g.edges:
        if e.relation == "triggers" and e.dst in trg_by_skill:
            trg = g.triggers.get(e.src)
            if trg:
                trg_by_skill[e.dst].append(trg.phrase)
    for sid in sorted(g.skills):
        phrases = ", ".join(trg_by_skill[sid][:3]) or sid.replace("-", " ")
        pat = pattern_label.get(g.skills[sid].pattern, g.skills[sid].pattern)
        rows.append(f"| `{sid}` | {phrases} | {pat} |")
    return "\n".join(rows)


def patch_skill_graph_md(trigger_rows: str) -> None:
    """SKILL-GRAPH.md is a static wire hub (D2); trigger table no longer patched here."""
    skill_graph_path = USER_PACK / "SKILL-GRAPH.md"
    if not skill_graph_path.is_file():
        print(f"WARN: {skill_graph_path} not found", file=sys.stderr)
        return
    if "canonical_graph|skill-graph-seed.wire" not in skill_graph_path.read_text(encoding="utf-8"):
        print(
            "WARN: SKILL-GRAPH.md is not wire-hub format; skip trigger table patch",
            file=sys.stderr,
        )
        return
    print(f"Skip trigger table patch (hub only): {skill_graph_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap skill graph seed and views.")
    parser.add_argument("--regenerate-views", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--sync", action="store_true", help="Emit wire lines for MemNet add")
    args = parser.parse_args()

    if not SEED_PATH.is_file():
        print(f"ERROR: seed missing at {SEED_PATH}. Run scan_skills_to_wire.py --write first.", file=sys.stderr)
        sys.exit(2)

    g = parse_wire_file(SEED_PATH)
    errors = validate_density(g)
    print(f"Seed: {len(g.skills)} skills, {len(g.triggers)} triggers, {len(g.edges)} edges.")
    if errors:
        print(f"ERROR: density contract failed ({len(errors)} issues):", file=sys.stderr)
        for e in errors[:10]:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    print("OK: edge-density contract.")

    if args.regenerate_views:
        core_path = SKILL_ROOT / "references" / "core-strategy-principles.md"
        core_path.write_text(regenerate_core_strategy_principles(g), encoding="utf-8")
        print(f"Regenerated {core_path}")
        patch_skill_graph_md(regenerate_skill_graph_triggers(g))

    if args.sync:
        for line in graph_to_wire_lines(g):
            if line.startswith("#"):
                continue
            print(line)
        print("# Paste above @ rows into memnet.add with allow_new_relation=true", file=sys.stderr)
        print("# MERGE only — do not delete existing led_to_success edges", file=sys.stderr)

    if args.dry_run:
        print("Dry-run complete.")


if __name__ == "__main__":
    main()
