---
name: sysml-physical-port-generator
description: >-
  Define SysML v2 physical port structures (connector { protocol { pin# } }) for hardware connectors
  (GPIO headers, mikroBUS, JST, etc.). Use when adding or modeling multi-pin connectors, breakout boards,
  development-kit headers, or custom PCBA interfaces in sysml-v2-models/libs/common/parts/hardware_ports.sysml.
  Changing published connector defs in libs/common often implies well-design or COTS—use sysml-part-reviewer
  when maturity or doc impact is unclear.
metadata:
  pattern: generator
  output-format: sysml
token_guardrails: |
  - **libs/common `hardware_ports.sysml`:** Pinouts from standards/datasheets behave like **COTS**/baselined specs; substantive edits need rationale or **sysml-part-reviewer** + docs.
  - **Physical connector defs** are **de facto** pin truth for PCBs and cables; keep aligned with pin maps and deploy. See [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md).
  - MemNet cache: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) — `@POR`/`@SYM` delta after validate.
---

# SysML Physical Port Generator

1. Load `references/port-style-guide.md` for naming, port types, and compatibility rules.
2. Load `assets/port-def-template.sysml` for required structure.
3. If missing: connector name, pinout source (datasheet/schematic/standard), protocol groups with pin assignments — ask user. Look up pinout from standard (e.g. BCM2835 40-pin, mikroBUS v2.0) if not provided.
4. Fill template; every protocol and the connector must appear. Use `redefines` for I2C/UART when connecting via I2cLink/UartLink.
5. Return **only** the completed SysML port definitions (ready to insert into `hardware_ports.sysml`) unless user asked for commentary.

## Inputs to gather

- **Connector name** (e.g. Gpio40Pin, MikroBus, AcquisitionMcuHat)
- **Pinout** — pin number → signal (from datasheet, schematic, or standard)
- **Protocol groups** — which pins belong to power, I2C, SPI, UART, GPIO, etc.

## Post-generation

1. Insert defs into `sysml-v2-models/libs/common/parts/hardware_ports.sysml`
2. Use in part defs (e.g. `development_boards.sysml`)
3. Add `I2cLink`/`UartLink` in `connections.sysml` if needed
4. Validate: SysML MCP validate

## Pairing

- **sysml-part-reviewer** — when changing existing connector defs or impact on shared lib is unclear.
- **sysml-hardware-part-generator** — parts that reference these port defs.
- **sysml-common-lib-contribution** — checklist for any `libs/common` edit.
