# Common lib file scale (soft limits)

**Purpose:** Keep `sysml-v2-models/libs/common/**/*.sysml` chunks small enough for human review and for agents that must read a whole file. Numbers are **guidance**, not CI gates.

**Measure:** `python tools/count_common_sysml_lines.py` from repo root (path in [Folder_Structure.md](../Folder_Structure.md)) — prints lines and flags `>=REVIEW_TRIGGER` / `>=STRONG_SPLIT` when thresholds are crossed.

## Soft line-count trigger

- **~1200 lines** (logical lines, same as `str.splitlines()`): **review trigger** — consider staying as one package vs a **sibling file**.
- **~1800+ lines**: **strong split** — plan a split unless the content is one indivisible domain and tooling still performs well.

Adjust thresholds here if the team changes them; optionally mirror the numbers in `count_common_sysml_lines.py` (`soft`, `hard`).

## Last audit snapshot (repo)

*Regenerate after large edits:* run the script above.

| When | Largest file (lines) | Notes |
|------|----------------------|--------|
| 2025-03-25 | `parts/semiconductors.sysml` (~450) | All common `.sysml` **below** 1200 — **no split required** for size. |

## Split rule (one package per file)

- **Do:** Add **`new_snake_case.sysml`** with **one primary top-level package** (per [common-library-naming-detailed.md](../../sysml-common-lib-contribution/references/common-library-naming-detailed.md) §§1–2).
- **Do:** Carve by **cohesive subdomain** (e.g. power ICs vs interface ICs), not “first N lines / rest.”
- **Do not:** Split **one logical package** across two files to satisfy line count.
- **Do not:** Split only for LLM tokens if the domain boundary is unclear—prefer **MCP** (`symbols`, `definition`, `references`, `validate`) and **sysmledgraph** first.

## Exceptions (existing layout)

- **`composites/poe_edge_computer.sysml`** may contain **two** sibling top-level packages (`PoeEdgeComputer`, `EdgeAI`) when they stay **tightly coupled** and **combined size** remains modest. Do **not** duplicate this pattern for new files unless the same coupling applies; default remains **one package per file**.

## Anti-patterns

- New file that is only a **dump** of unrelated part defs with no shared naming theme.
- Changing **`model_files`** order in one project but not others that share common.
- Splitting without **grep** / graph pass for `import` of the old package in projects and common.

## After a split

1. **`config.yaml`** — Insert the new file in **`model_files`** in correct dependency order (see [libs/common/README.md](../../../../sysml-v2-models/libs/common/README.md)).
2. **Docs** — [libs/common/README.md](../../../../sysml-v2-models/libs/common/README.md), [parts/README.md](../../../../sysml-v2-models/libs/common/parts/README.md) if under `parts/`.
3. **Imports** — Fix any `private import` / qualified names in consumers (**grep** package name under `sysml-v2-models/`).
4. **Verify** — **SysML v2 MCP validate** on affected common files + at least one **full** project load.

**Checklist:** [assets/split-checklist.md](../assets/split-checklist.md).
