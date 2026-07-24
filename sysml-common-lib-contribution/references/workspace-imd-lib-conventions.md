# Workspace conventions: IMD PCBAs, parts, composites

Canonical detail for this repo. Linked from **sysml-common-lib-contribution**, **sysml-hardware-part-generator**, **mcp-inventree** policy.

## IPN rule

- InvenTree IPN = **MfrPart#@MfrAbbr** (MfrAbbr from manufacturer list).
- **Self-made PCBAs (InstruMeasure Dynamics, IMD):** partNumber = ClickUp task ID. In InvenTree the part IPN is **partNumber@IMD** (e.g. `86ewdvt0r@IMD`). Keep the **part name the same** in ClickUp and InvenTree.
- In SysML part `doc`: state "Self-made PCBA, InstruMeasure Dynamics (IMD). partNumber = X (= ClickUp task ID). InvenTree ID: partNumber@IMD (X@IMD). Name aligned with ClickUp and InvenTree."
- Netlist in `hardware/boards-86e/<partNumber>/<partNumber>.scr`; reference it in the doc.

**Refs:** [semiconductors.sysml](../../../../sysml-v2-models/libs/common/parts/semiconductors.sysml) · [BOARDS_86e_REFERENCE.md](../../../../hardware/boards-86e/BOARDS_86e_REFERENCE.md) · [hardware-custom-pcba-workflow](../../hardware-custom-pcba-workflow/SKILL.md)

## New network / switch parts

Add to `sysml-v2-models/libs/common/parts/network.sysml`. Use existing port types from HardwarePorts (`FromCoreRouterPort`, `ToPoeEdgeAIPort`, `UplinkPort`, `NetworkPort`, etc.). Include `attribute productCategory : String` and `doc /* ... */` with brief description and refs. PoE-capable switches: add `poeBudgetTotal`, `poePlusPortCount`, `poePlusPlusPortCount` where applicable.

## New edge composites

Add to `sysml-v2-models/libs/common/composites/poe_edge_computer.sysml` in the right package (`PoeEdgeComputer` or `EdgeAI`). Reuse SharedConnections (`PowerExpansionToRpi5`, `GpioStackPiToExpansion`, `GpioStackExpansionToBreakout`, `PcieLinkRpi5ToM2Hat`, etc.). List parts (`rpi5`, `powerBoard`, `pcieEthM2Hat`, `signalBreakoutHat`, etc.) and connections with `end port ... ::> part.port`. Update the file header comment to mention the new composite.
