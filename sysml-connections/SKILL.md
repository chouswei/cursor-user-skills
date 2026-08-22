---
name: sysml-connections
description: >-
  Edit or review SysML v2 structural connections between parts (hardware deploy, software data flow).
  Workflow: locate deploy/behaviour, Grep / Read live `.sysml`, loaded-file SysML v2 MCP references, minimal .sysml edits, SysML v2 MCP
  validate, optional pinmap/scripts and outputs/*.md sync. Triggers: change connection, rewire blocks,
  add/remove link between parts, SpiLink UartLink deploy topology, PAT wiring, who connects to what,
  de facto wiring, retarget backbone port.
metadata:
  pattern: pipeline
  domain: sysml-v2
  pairs_with: [mcp-sysml-v2, sysml-part-reviewer, sysml-memnet-cache]
token_guardrails: |
  - Scope to one project or named deploy package; use **Grep / Read** on live `.sysml` before reading wider trees.
  - **Baselined deploy / COTS hardware:** If rewiring touches **well-design** or **COTS** parts, consider **sysml-part-reviewer** + **outputs** sync (doc gate).
  - After any .sysml edit: SysML v2 MCP validate; do not paste full model into chat.
  - MemNet cache: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) — pin_map before edit; `@CON`/`@SYM` delta after validate.
  - Load references/workflow.md only when steps need detail (connection defs, pinmap pattern).
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML connections

**When:** User asks to **add, remove, or retarget** connections between blocks (parts), or to **trace** who is wired to whom in structure or logical software flow.

## Pipeline

1. **Classify** — **Hardware / deployment:** `connection` usages in `deploy-*.sysml` (and sometimes project `connections-*.sysml`). Ends use `SharedConnections::*` (`SpiLink`, `UartLink`, `I2cLink`, `GpioExpansionLink`, …) or project `connection def`s. **Software:** logical `SoftwareDataFlow`, `StateCommandFlow`, etc. in the same deploy package or behaviour package. If unclear, ask one short question (hardware vs software vs both).

2. **Locate** — Grep `connection ` and part names in `sysml-v2-models/projects/<project>/models/`. Read only the **connection blocks** and **port paths** on both ends (`master`/`slave`, `host`/`device`, `a`/`b` per link type).

3. **Blast radius (cross-file)** — Before renames or wide rewires: use **Grep / Read** on live `.sysml`, then Cursor **`user-sysml-v2` MCP** (`getSymbols`, `getDefinition`, `getReferences`, `parse`, `validate`) on the file or code just loaded. Do not use abandoned `sysmledgraph` or treat an MCP workspace URI index as model SSOT.

4. **Edit** — **Minimal diff:** change only the relevant `connection` and, if needed, **port defs** on parts or HAT (`pat-breakout-hat.sysml`, `libs/common`). Match existing naming and link types; do not invent new `connection def` in the project unless the user asked for a new protocol. Prefer port paths that match **physical** names on COTS when the **part def** uses physical numbering (de facto traceability to labels and CLI).

5. **Verify** — **SysML v2 MCP: validate** on edited files / project. Fix diagnostics.

6. **Derived artifacts** — If the project maps deploy links to pin maps (e.g. `mappings/pat_pinmap_from_sysml.yaml`, `check_pinmap_from_sysml.py`), update YAML and run the script. Align `outputs/*.md` that describe wiring **from** the model ([sysml-modeling-workflow](../../sysml-modeling-workflow/SKILL.md): model first).

## Pairing

- **mcp-sysml-v2** — validate (mandatory after edits); getSymbols / getDefinition (`name`) / getReferences (`name`) for port paths ([tool-parameters](../mcp-sysml-v2/references/tool-parameters.md)).
- **mcp-sysml-v2** — loaded-file symbols, definitions, references, parsing, and validation.
- **sysml-part-reviewer** — when connection changes imply maturity/doc impact (not only **under-design**).
- **sysml-hardware-part-generator** / **sysml-software-part-generator** — only if new parts or ports are required.

**Repo:** [sysml-modeling-workflow](../../sysml-modeling-workflow/SKILL.md) · [AGENTS.md](../../../AGENTS.md)

**Detail:** [references/workflow.md](references/workflow.md)
