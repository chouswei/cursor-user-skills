---
name: sysml-item-generator
description: >-
  Scaffold SysML v2 item definitions (item def) for flows: logical payloads, documents, commands, or
  physical flow (power/data) with optional ISQ/SI attributes. Place in FlowItems (libs/common) when
  shared across projects, or in project deploy/behaviour when local. Wire with in item / out item on
  ports or actions. Triggers: item def, flow item, conveyed item, Power3V3, DevelopmentPlan, logical data item.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first (gather inputs before generating)
  pairs_with: [mcp-sysml-v2, sysml-connections, sysml-behaviour-generator]
token_guardrails: |
  - Prefer extending FlowItems only for repo-wide reuse; ask before editing libs/common.
  - After edits: SysML v2 MCP validate; match load order (FlowItems before ports that reference items).
  - Load references/item-style-guide.md when generating; keep snippets small.
---

# SysML item generator

**When:** User needs **`item def`** types for **what flows** on connections, through ports (**`in item` / `out item`**), or in **actions** (**`in item` / `out item`** on action parameters).

## Pipeline

1. **Ask first** — If missing: **item name(s)** (PascalCase), **semantic** (power / logical document / signal / composite), **home** (common `FlowItems` vs **project package**), **attributes** (optional quantities with ISQ/SI), **nested sub-items** (e.g. PoE). One short question per gap.

2. **Placement** — Read [references/item-style-guide.md](references/item-style-guide.md):
   - **Shared physical/logical flow items** (e.g. new nominal rail, reusable payload type) → extend **`sysml-v2-models/libs/common/parts/flow_items.sysml`** only with user confirmation and library review.
   - **Project-specific** (e.g. `DevelopmentPlan`, domain messages) → **`deploy-*.sysml`** or **`behaviour-*.sysml`** in the project package.

3. **Generate** — Use [assets/item-def-stub.sysml](assets/item-def-stub.sysml). Each item: **`item def Name { doc /* ... */ }`**; optional **`attribute`** with **`ElectricPotentialDifferenceValue`** etc. when physical; **nested `item`** for composite items.

4. **Bind to ports** — On connection/port defs that convey the item, add **`in item` / `out item`** with the new type (see `QwiicMasterSourcePort` in `hardware_ports.sysml`). Ensure **imports** include the package that defines the item.

5. **Connection doc** — If using **`SharedConnections`**, align **`doc /* ... */`** on **`connection def`** with conveyed item (pattern in `connections.sysml` for PoE, power).

6. **Verify** — **SysML v2 MCP validate**. If **`flow_items.sysml`** changed, confirm **config.yaml** load order: **ISQ, SI** before **flow_items**, then **hardware_ports**.

## Pairing

- **sysml-connections** — when new items accompany new **connection def** or port typing.
- **sysml-behaviour-generator** — **`in item` / `out item`** on actions in behaviour packages.
- **sysml-software-port-generator** — logical software flow types before binding items to software ports (project convention).
- **sysml-part-reviewer** — when items are tied to **well-design** or **COTS** interfaces; changing shared **FlowItems** may need the doc gate (often **well-design**).

**Repo:** [flow_items.sysml](../../../sysml-v2-models/libs/common/parts/flow_items.sysml) · [sysml-common-lib-contribution](../sysml-common-lib-contribution/SKILL.md) · [libs/common README](../../../sysml-v2-models/libs/common/README.md)
