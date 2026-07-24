# Issue: Electronics footprint → SysML v2 part traceability

**Status:** Open (guidance + pilot done; no general mapper yet)  
**GitHub:** [instrumeasure/system-models-and-architecture#4](https://github.com/instrumeasure/system-models-and-architecture/issues/4)  
**Skill entry:** [../SKILL.md](../SKILL.md)

## Goal

Define a **traceability path from electronics footprint** (KiCad, JLCPCB package/LCSC, SamacSys, Mouser/DigiKey part) **to a SysML v2 part** in the common library (`sysml-models/libs/common/parts/*.sysml` or `sysml-v2-models/...` depending on repo).

## Why it matters

- **BOM and part trees** often reference both ECAD (netlists, footprints) and SysML part defs.
- **DigiKey / InvenTree / KiCad** workflows expose footprints, package names, and part numbers; teams need a clear map to the SysML part (and optionally `partNumber`, `productCategory`, `estimatedCostUsd`, InvenTree IPN).
- **Single source of truth:** SysML is structural; ECAD and distributors are references. A defined path avoids drift and answers “which SysML part is this footprint?”.

## Scope (to be refined)

- **Inputs:** Footprint name (KiCad ref), package (e.g. 0603, SOT-23), LCSC/MPN, distributor part number.
- **Outputs:** SysML part def and/or `partNumber`, `productCategory`, optional attributes.
- **Artifacts:** Mapping table, naming convention, or lightweight schema (mappings file or attributes on part def).
- **Tools:** DigiKey MCP, InvenTree MCP, KiCad MCP / pcba-libs, optional SamacSys/CSE when available.

### Resolution from SamacSys

SamacSys / Component Search Engine can be a resolution source when an MCP or download provides:

- Search by MPN/keyword → footprint/symbol availability
- KiCad symbol + footprint names/files

Web: [Component Search Engine](https://componentsearchengine.com/) (SamacSys).

To resolve **from** SamacSys to a SysML part, use one of:

1. **Attribute on part def** — e.g. MPN in `partNumber`, or a dedicated `ecadRef` / SamacSys id.
2. **Mapping table** — SamacSys/CSE key → SysML part def name (scale when many parts).
3. **Match via MPN** — If SysML already stores the manufacturer part number SamacSys returns, resolution is by MPN.

Minimal schema today: **`partNumber` + `footprintRef`**.

## Progress

- **Workflow documented** in common parts README (per workspace): section *Workflow: Adding an electronics part* — optional ECAD under `hardware/ecad-libs/<PartNumber>/` or shared `pcba-libs/footprints/`, generic part def first when applicable, attributes `productCategory`, `partNumber`, `footprintRef`, `estimatedCostUsd`.
- **Pilot:** AD8671ARZ op-amp. Generic `SingleOpAmp`; concrete `Ad8671arz :> SingleOpAmp`. ECAD historically at `hardware/ecad-libs/AD8671ARZ/` (KiCad SOIC127P600X175-8N). Part def holds `footprintRef` and docs link to ECAD path.
- **Schema in use:** `partNumber`, `footprintRef` (KiCad / pcba-libs id); resolution path ECAD README or MPN → SysML part → `footprintRef` / datasheet.

### Example (VEDAN / edge acquisition)

When workspace is `modelbasedPrj-ITRI-VEDAN-DecanterCentrifugeHealthDiagnosis`:

- Parts README: `sysml-models/libs/common/parts/README.md`
- Footprint placeholder catalog: `pcba-libs/footprints/README.md`
- Nested parts already carry `footprintRef` (e.g. W5500 `LQFP-48_7x7mm_P0.5mm`, HXB5007HLT, USB, WIZPoE mount)
- PCBA workflow: repo `.cursor/skills/hardware-custom-pcba-workflow/`

## Related skills

- [sysml-common-library-naming](../../sysml-common-library-naming/SKILL.md) — part naming, IPN
- [sysml-hardware-part-generator](../../sysml-hardware-part-generator/SKILL.md) — part scaffolding
- [mcp-digikey](../../mcp-digikey/SKILL.md) — MPN / category
- [mcp-inventree](../../mcp-inventree/SKILL.md) — stock / IPN
- Repo **`hardware-custom-pcba-workflow`** (under the system repo’s `.cursor/skills/`, not always in the user pack)

## Next steps

1. ~~Agree on minimal schema~~ — `footprintRef`, `partNumber`; ECAD README → SysML part reference.
2. ~~Document the path~~ — Parts README + this narrative.
3. Extend to more parts as needed; add mapping table or script only if scale demands it.
4. Keep skill and any repo `docs/TRACEABILITY_*.md` mirrors aligned; prefer this file as pack SSOT.
