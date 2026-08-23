"""
Validate reasoning-strategy-selector pack consistency.

1. related_skills.txt ↔ SKILL.md metadata
2. skill-graph-seed.wire edge-density contract (GQL CREATE rows)
3. Generated views drift check (optional --check-views)
4. Optional --order-json against full graph SKL ids

Run from this skill's root:
  python tools/validate_selector_pack.py
  python tools/validate_selector_pack.py --check-views
  python tools/validate_selector_pack.py --order-json '["code-reviewer"]'
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Allow import from tools/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_graph_lib import SEED_PATH, USER_PACK, parse_wire_file, validate_density  # noqa: E402
from bootstrap_skill_graph import (  # noqa: E402
    GENERATED_MARKER,
    regenerate_core_strategy_principles,
    regenerate_skill_graph_triggers,
)


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_txt_ids(txt_path: Path) -> list[str]:
    ids: list[str] = []
    for line in txt_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ids.append(line)
    return ids


def parse_related_skills_from_skill(skill_path: Path) -> list[str]:
    text = skill_path.read_text(encoding="utf-8")
    m = re.search(r"^  related_skills:\s*\[(.*?)\]\s*$", text, re.MULTILINE | re.DOTALL)
    if not m:
        print(f"ERROR: no '  related_skills: [...]' line in {skill_path}", file=sys.stderr)
        sys.exit(2)
    inner = m.group(1).replace("\n", " ")
    parts = [p.strip() for p in inner.split(",")]
    return [p for p in parts if p]


def check_views(g, root: Path) -> bool:
    ok = True
    core_path = root / "references" / "core-strategy-principles.md"
    if core_path.is_file():
        expected = regenerate_core_strategy_principles(g)
        actual = core_path.read_text(encoding="utf-8")
        if GENERATED_MARKER not in actual:
            print("WARN: core-strategy-principles.md missing GENERATED marker", file=sys.stderr)
        # Compare table rows only
        exp_rows = [l for l in expected.splitlines() if l.startswith("| ") and not l.startswith("| Skill")]
        act_rows = [l for l in actual.splitlines() if l.startswith("| ") and not l.startswith("| Skill")]
        if exp_rows != act_rows:
            print("ERROR: core-strategy-principles.md table drift from seed", file=sys.stderr)
            ok = False
        else:
            print("OK: core-strategy-principles.md table matches seed.")
    skill_graph = USER_PACK / "SKILL-GRAPH.md"
    if skill_graph.is_file():
        text = skill_graph.read_text(encoding="utf-8")
        if "CANONICAL_GRAPH" in text and "skill-graph-seed.wire" in text:
            print("OK: SKILL-GRAPH.md is GQL hub (graph in seed.wire).")
        elif GENERATED_MARKER in text:
            exp_triggers = regenerate_skill_graph_triggers(g)
            if exp_triggers not in text:
                print("ERROR: SKILL-GRAPH.md trigger table drift from seed", file=sys.stderr)
                ok = False
            else:
                print("OK: SKILL-GRAPH.md trigger rows match seed.")
        else:
            print("WARN: SKILL-GRAPH.md format unknown", file=sys.stderr)
    return ok


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate selector pack / graph / routing order.")
    parser.add_argument("--order-json", default="")
    parser.add_argument("--check-views", action="store_true")
    args = parser.parse_args()

    root = _skill_root()
    txt_path = root / "references" / "related_skills.txt"
    skill_path = root / "SKILL.md"

    txt_ids = load_txt_ids(txt_path)
    yaml_ids = parse_related_skills_from_skill(skill_path)

    if txt_ids != yaml_ids:
        print("ERROR: related_skills.txt and SKILL.md related_skills differ.", file=sys.stderr)
        sys.exit(1)
    print(f"OK: SKILL.md related_skills matches related_skills.txt ({len(txt_ids)} ids).")

    pack_root = skill_path.resolve().parent.parent
    missing = [sid for sid in txt_ids if not (pack_root / sid / "SKILL.md").is_file()]
    if missing:
        print(f"ERROR: missing peer SKILL.md: {missing}", file=sys.stderr)
        sys.exit(1)
    print(f"OK: related_skills peers exist ({len(txt_ids)}).")

    if not SEED_PATH.is_file():
        print(f"ERROR: seed missing at {SEED_PATH}", file=sys.stderr)
        sys.exit(1)
    g = parse_wire_file(SEED_PATH)
    density_errors = validate_density(g)
    if density_errors:
        print(f"ERROR: edge-density contract ({len(density_errors)}):", file=sys.stderr)
        for e in density_errors[:5]:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    print(f"OK: skill-graph seed ({len(g.skills)} SKL, density contract).")

    for sid in txt_ids:
        if sid not in g.skills:
            print(f"WARN: related_skills id {sid} not in seed graph", file=sys.stderr)

    if args.check_views and not check_views(g, root):
        sys.exit(1)

    if not args.order_json.strip():
        return

    allow = set(g.skills.keys())
    try:
        order = json.loads(args.order_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(order, list):
        print("ERROR: --order-json must be a JSON array", file=sys.stderr)
        sys.exit(2)

    bad = [x for x in order if not isinstance(x, str) or x not in allow]
    if bad:
        print(f"ERROR: order contains unknown ids: {bad}", file=sys.stderr)
        sys.exit(1)
    if "reasoning-strategy-selector" in order:
        print("ERROR: reasoning-strategy-selector must not appear in order.", file=sys.stderr)
        sys.exit(1)
    print(f"OK: order JSON valid against graph ({len(order)} ids).")


if __name__ == "__main__":
    main()
