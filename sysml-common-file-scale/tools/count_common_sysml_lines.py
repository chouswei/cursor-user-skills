#!/usr/bin/env python3
"""Line counts for sysml-v2-models/libs/common/**/*.sysml (sorted descending).

Run from anywhere:
  python .cursor/skills/sysml-common-file-scale/tools/count_common_sysml_lines.py

Exit 0. Prints TSV: lines<TAB>relative_path from repo root. Flags when >= soft/hard (keep in sync
with references/scale-policy.md).
"""
from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    # tools/ -> sysml-common-file-scale/ -> skills/ -> .cursor/ -> repo
    return Path(__file__).resolve().parent.parent.parent.parent.parent


def main() -> None:
    root = _repo_root()
    common = root / "sysml-v2-models" / "libs" / "common"
    if not common.is_dir():
        raise SystemExit(f"Missing: {common}")

    rows: list[tuple[int, Path]] = []
    for p in sorted(common.rglob("*.sysml")):
        text = p.read_text(encoding="utf-8", errors="replace")
        n = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
        rows.append((n, p))

    rows.sort(key=lambda x: (-x[0], str(x[1])))
    soft, hard = 1200, 1800
    for n, p in rows:
        rel = p.relative_to(root).as_posix()
        flag = ""
        if n >= hard:
            flag = "\t>=STRONG_SPLIT"
        elif n >= soft:
            flag = "\t>=REVIEW_TRIGGER"
        print(f"{n}\t{rel}{flag}")


if __name__ == "__main__":
    main()
