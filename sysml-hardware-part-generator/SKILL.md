---
name: sysml-hardware-part-generator
description: >-
  Define SysML v2 hardware part structures (part def with ports, attributes) for development boards,
  HATs, modules, breakout boards, and custom PCBAs. Use when adding hardware blocks to common lib
  or project packages. Run sysml-physical-port-generator first for connector structures. If editing an
  existing part or maturity is unclear, run sysml-part-reviewer first (only under-design may change without docs).
  Triggers: hardware part, development board, HAT, breakout, PCBA, deploy hardware block, OTS module,
  physical ports only, COTS interface inventory.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first (gather inputs before generating)
token_guardrails: |
  - IMD PCBA, IPN, **network.sysml**, **poe_edge_computer.sysml**: [sysml-common-lib-contribution/references/workspace-imd-lib-conventions.md](../sysml-common-lib-contribution/references/workspace-imd-lib-conventions.md).
  - **Existing part or libs/common edit:** Prefer **sysml-part-reviewer** once to classify under-design / well-design / COTS before substantive edits.
  - MemNet cache: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) — pin_map before edit; `@PRT`/`@POR`/`@SYM` delta after validate.
---

# SysML Hardware Part Generator

0. **Maturity gate** — If the user edits an **existing** `part def` or a **libs/common** hardware part and has not classified maturity, follow **sysml-part-reviewer** first (only **under-design** allows changes without accompanying docs).
1. **Ask first** — If missing: part name, OTS vs custom/IMD, ports (names and HardwarePorts types), attributes (productCategory, partNumber, current draw, form factor) — ask user. One short question per gap. Map **OTS** → usually **COTS** for reviewer handoff; **custom/IMD** → often **well-design** once baselined.
2. Load `references/part-style-guide.md` for naming, OTS vs custom, and port patterns. For COTS with many identical jacks, load [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md) and choose **physical** vs **role** port naming consistently with sibling parts in the same library file.
3. Load `assets/part-def-template.sysml` for required structure.
4. Ensure port types exist in HardwarePorts (use sysml-physical-port-generator for connectors if needed).
5. Fill template; part def must appear; doc, productCategory, partNumber, and ports required.
6. Return **only** the completed SysML part definition (ready to insert into common lib or project) unless user asked for commentary.

## Pairing

- **sysml-part-reviewer** — classify before changing existing or shared parts.
- **sysml-physical-port-generator** — connector `port def` before part ports that use them.
- **sysml-item-generator** / **sysml-connections** — flow items and wiring after part shape exists.
- **sysml-view-doc-sync** — after **well-design** / **COTS** changes when the project keeps `outputs/*.md`.

## Inputs to gather

- **Part name** (e.g. PolarFireSoCDiscoveryKit, PatSpiI2cBreakoutHat, NucleoH753zi)
- **OTS or custom** — OTS: product name, Mfr part#; custom: descriptive name, partNumber = ClickUp ID
- **Ports** — name, HardwarePorts type (PowerIn5VPort, Gpio40PinPort, SpiPort, etc.)
- **Attributes** — productCategory, partNumber, currentDraw*, formFactor, estimatedCostUsd, etc.

## Post-generation

1. Insert into `sysml-v2-models/libs/common/parts/*.sysml` (common) or project models (project-specific) — **network gear → `network.sysml`**; see [workspace-imd-lib-conventions.md](../sysml-common-lib-contribution/references/workspace-imd-lib-conventions.md).
2. Add to config.yaml model_files if new package
3. Add connections in deploy model
4. Validate: SysML MCP validate
