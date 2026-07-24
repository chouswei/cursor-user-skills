"""
Rewrite metadata.related_skills in SKILL.md from references/related_skills.txt.

Run from this skill's root: python tools/sync_related_skills_from_txt.py
ADK and other loaders still read the embedded YAML list in SKILL.md.
"""
from __future__ import annotations

from pathlib import Path


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_ids(txt_path: Path) -> list[str]:
    ids: list[str] = []
    for line in txt_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ids.append(line)
    if not ids:
        raise SystemExit(f"No ids found in {txt_path}")
    return ids


def embed_in_skill(skill_text: str, ids: list[str]) -> str:
    flow = "  related_skills: [" + ", ".join(ids) + "]"
    lines = skill_text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("  related_skills:"):
            out.append(flow + "\n")
            i += 1
            while i < len(lines) and lines[i].startswith("    - "):
                i += 1
            continue
        out.append(line)
        i += 1
    return "".join(out)


def main() -> None:
    root = _skill_root()
    txt_path = root / "references" / "related_skills.txt"
    skill_path = root / "SKILL.md"
    ids = load_ids(txt_path)
    text = skill_path.read_text(encoding="utf-8")
    if "  related_skills:" not in text:
        raise SystemExit("SKILL.md: expected '  related_skills:' under metadata")
    new_text = embed_in_skill(text, ids)
    skill_path.write_text(new_text, encoding="utf-8")
    print(f"Updated {skill_path} with {len(ids)} ids from {txt_path}")
    print("Next: python tools/validate_selector_pack.py")


if __name__ == "__main__":
    main()
