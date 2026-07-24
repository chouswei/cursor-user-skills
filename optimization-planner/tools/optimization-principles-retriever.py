"""
Tool Wrapper: return the most relevant bullets from references/core-optimization-principles.md.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Tuple


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_principle_bullets() -> List[str]:
    path = _skill_root() / "references" / "core-optimization-principles.md"
    text = path.read_text(encoding="utf-8")
    bullets: List[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            bullets.append(stripped[2:].strip())
    return bullets


_BULLETS: List[str] | None = None


def _bullets_cached() -> List[str]:
    global _BULLETS
    if _BULLETS is None:
        _BULLETS = _load_principle_bullets()
    return _BULLETS


def _tokenize(query: str) -> List[str]:
    return [t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{1,}", query.lower())]


def retrieve_principles(query: str, max_results: int = 7) -> List[str]:
    """Return up to max_results optimization principle lines ranked by keyword overlap."""
    keywords = _tokenize(query)
    bullets = _bullets_cached()
    if not keywords:
        return bullets[:max_results]

    scored: List[Tuple[int, str]] = []
    for b in bullets:
        bl = b.lower()
        score = sum(1 for k in keywords if k in bl)
        if score:
            scored.append((score, b))

    scored.sort(key=lambda x: (-x[0], x[1]))
    if not scored:
        return bullets[:max_results]
    return [p for _, p in scored[:max_results]]


tool_spec = {
    "name": "optimization-principles-retriever",
    "description": "Retrieves only relevant optimization and constraint principles by query keywords.",
    "parameters": {
        "query": {"type": "string"},
        "max_results": {"type": "integer", "default": 7},
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve optimization principles.")
    parser.add_argument("query", nargs="?", default="", help="Search query text")
    parser.add_argument(
        "-n",
        "--max-results",
        type=int,
        default=7,
        dest="max_results",
        help="Maximum bullets to return",
    )
    args = parser.parse_args()
    for line in retrieve_principles(args.query, args.max_results):
        print(line)


if __name__ == "__main__":
    main()
