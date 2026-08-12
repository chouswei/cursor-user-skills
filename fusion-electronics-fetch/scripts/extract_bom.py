#!/usr/bin/env python3
"""Extract parts + nets from an Eagle/Fusion Electronics .sch (XML) into bom-extract.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PART_RE = re.compile(r"<part\s+([^/>]+)/>", re.I)
ATTR_RE = re.compile(r'(\w+)="([^"]*)"')
NET_RE = re.compile(r'<net\s+name="([^"]+)"')
SKIP_PREFIXES = ("GND", "FRAME", "SUPPLY")


def parse_sch(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    parts: list[dict] = []
    for m in PART_RE.finditer(text):
        d = dict(ATTR_RE.findall(m.group(1)))
        name = d.get("name", "")
        if any(name.startswith(p) for p in SKIP_PREFIXES):
            continue
        row = {
            k: d[k]
            for k in ("name", "value", "deviceset", "device", "package")
            if d.get(k)
        }
        if row:
            parts.append(row)
    nets = sorted(set(NET_RE.findall(text)))
    return {
        "source": path.name,
        "part_count": len(parts),
        "parts": parts,
        "nets": nets,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sch", type=Path, help="Path to .sch file")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output JSON (default: <sch-dir>/bom-extract.json)",
    )
    args = ap.parse_args()
    sch: Path = args.sch
    if not sch.is_file():
        print(f"error: not a file: {sch}", file=sys.stderr)
        return 1
    data = parse_sch(sch)
    out = args.output or (sch.parent / "bom-extract.json")
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"{sch.name}: parts={data['part_count']} nets={len(data['nets'])} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
