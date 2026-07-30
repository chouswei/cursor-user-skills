---
name: traceability-footprint-to-sysml
description: >-
  Open-issue guidance: map electronics footprints (KiCad, JLCPCB/LCSC, SamacSys)
  to SysML v2 part defs via footprintRef and partNumber. Use when resolving an
  ECAD footprint to a SysML part, documenting footprintRef, or continuing the
  SamacSys/CSE pilot. Not a finished automation pipeline — read the reference
  narrative first. Triggers: footprint to SysML, footprintRef, ECAD traceability,
  SamacSys CSE, LCSC to part def.
metadata:
  pattern: pipeline
  domain: hardware-sysml
  version: "1.1"
  status: open-issue
  pairs_with:
    - sysml-hardware-part-generator
    - sysml-common-lib-contribution
    - mcp-digikey
    - mcp-inventree
system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.
---

# Traceability: footprint → SysML part

**Status:** Open issue (schema and pilot exist; no general automation yet).

**Full narrative (skill SSOT):** [references/traceability-footprint-to-sysml-issue.md](references/traceability-footprint-to-sysml-issue.md).

**GitHub:** [system-models-and-architecture#4](https://github.com/instrumeasure/system-models-and-architecture/issues/4).

## When to use

- User asks how a KiCad / JLCPCB / SamacSys footprint maps to a SysML part def.
- Adding or auditing `footprintRef` / `partNumber` on common-lib parts.
- PCBA work that must keep ECAD land-pattern ids aligned with SysML (e.g. edge acquisition + `pcba-libs/footprints`).

**Not for:** SysML requirement/allocate traceability ([sysml-traceability](../sysml-traceability/SKILL.md)); KiCad MCP board ops (repo `mcp-kicad`); DigiKey search alone ([mcp-digikey](../mcp-digikey/SKILL.md)).

## Working schema (in use)

On SysML part defs (generic or concrete):

| Attribute | Role |
|-----------|------|
| `partNumber` | MPN or IMD ClickUp task id |
| `footprintRef` | KiCad / pcba-libs land-pattern id (identity only; no pad geometry in SysML) |
| `productCategory` | DigiKey-style or InvenTree category string |
| `estimatedCostUsd` | Optional |

Resolution path: ECAD README or distributor MPN → SysML part name → `footprintRef` / datasheet in part `doc`.

## Workspace paths

This skill lives in the **user pack**. Do **not** rely on `../../../docs/...` relative links from here.

When the open workspace is a system repo:

| Need | Typical path |
|------|----------------|
| Parts workflow | `sysml-models/libs/common/parts/README.md` (or `sysml-v2-models/...` in older monorepos) |
| Footprint catalog | `pcba-libs/footprints/README.md` when present |
| Custom PCBA layout | Repo skill `hardware-custom-pcba-workflow` under `.cursor/skills/` |
| Naming | [sysml-common-lib-contribution](../sysml-common-lib-contribution/SKILL.md) |
| Part scaffolding | [sysml-hardware-part-generator](../sysml-hardware-part-generator/SKILL.md) |

If a copy of `docs/TRACEABILITY_FOOTPRINT_TO_SYSML_ISSUE.md` exists at the repo root, treat it as a mirror of the skill reference; prefer the skill `references/` file when they diverge.

## Pilot

**AD8671ARZ** — `Semiconductors::Ad8671arz :> SingleOpAmp`; `footprintRef` = `SOIC127P600X175-8N`; historical ECAD under `hardware/ecad-libs/AD8671ARZ/` in the architecture monorepo. Details in the reference narrative.
