---
name: sysml-common-lib-contribution
description: >-
  Add or change shared types under sysml-v2-models/libs/common (FlowItems, hardware_ports, parts,
  connections, composites): when to use common vs project, naming rules, load order impact, validate
  consumers. Triggers: add to common lib, FlowItems, SharedConnections, reusable port, shared part def,
  consistent COTS port style (physical vs role).
metadata:
  pattern: pipeline
  pairs_with:
    [mcp-sysml-v2, mcp-sysmledgraph, sysml-item-generator, sysml-physical-port-generator, sysml-common-file-scale, sysml-part-reviewer]
token_guardrails: |
  - **Part / port / shared item maturity:** For substantive edits to **part def**, **port def**, or shared **item def**, consider **sysml-part-reviewer** (only **under-design** may change without accompanying docs).
  - Confirm user wants cross-project reuse before editing libs/common.
  - After common change: validate + consider grep projects importing the package.
  - Read [sysml-common-library-naming](../sysml-common-library-naming/SKILL.md) and libs/common/README.md.
  - IMD PCBA, **network.sysml**, **poe_edge_computer.sysml**: [references/workspace-imd-lib-conventions.md](references/workspace-imd-lib-conventions.md).
  - Very large common files: [sysml-common-file-scale/SKILL.md](../sysml-common-file-scale/SKILL.md).
  - **De facto modeling** for shared parts (especially `network.sysml`): [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md) — avoid mixing **physical** and **role** port patterns on the same product class without an explicit `doc` rationale.
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML common library contribution

**When:** A type should be **reused** across projects in **`sysml-v2-models/libs/common/`** instead of a single **`projects/<name>/`** package.

## Pipeline

0. **Optional gate** — If editing an existing shared **part**, **connector port**, or **FlowItems** entry and documentation impact is unclear, run **sysml-part-reviewer** once (libs/common changes are rarely **under-design** only).

1. **Decision** — **Common** if ≥2 projects or stable domain concept (rail, protocol port, generic link); else **project-local**.

2. **Target file** — [libs/common/README.md](../../../sysml-v2-models/libs/common/README.md) layout: `parts/flow_items.sysml`, `parts/hardware_ports.sysml`, `parts/network.sysml`, `connections/connections.sysml`, `composites/poe_edge_computer.sysml`, other `composites/*.sysml`. (Placement detail: [workspace-imd-lib-conventions.md](references/workspace-imd-lib-conventions.md).)

3. **Naming** — [sysml-common-library-naming](../sysml-common-library-naming/SKILL.md) / [detailed rules](../sysml-common-library-naming/references/common-library-naming-detailed.md): PascalCase defs, snake_case files, no shadowing OMG names.

4. **Load order** — **FlowItems** before **hardware_ports**; **parts** before **connections** where types are referenced; document new file in README if new top-level file.

5. **Blast radius** — **grep** `import.*FlowItems` / package name; **sysmledgraph** impact optional.

6. **Minimal change** — Smallest addition; avoid drive-by refactors.

6a. **Port naming consistency** — When adding or changing **COTS** blocks with many external interfaces, align with **de facto** guidance in [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md); note **site conventions** in `doc` if defaults are project-specific.

7. **Verify** — **SysML v2 MCP validate** with **`code`** = file contents (see [mcp-sysml-v2 tool-parameters](../mcp-sysml-v2/references/tool-parameters.md)) and at least one consuming **project** `exam_model.py` / `config.yaml` load.
