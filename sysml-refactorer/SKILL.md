---
name: sysml-refactorer
description: >-
  Plan and execute cross-file SysML v2 refactors: rename parts/ports/connection defs, migrate role ports to de facto
  physical naming, update deploy + libs/common + SharedConnections consistently. Workflow: Grep / Read live `.sysml`,
  user-sysml-v2 MCP references, minimal diffs, SysML v2 MCP validate, exam_model.py project load, optional outputs sync. Triggers: refactor sysml,
  rename port across project, bulk port rename, de facto migration, restructure deploy, change connection def ends,
  blast radius sysml, find all references to part def.
metadata:
  pattern: pipeline
  domain: sysml-v2
  pairs_with:
    - mcp-sysml-v2
    - sysml-part-reviewer
    - sysml-connections
    - sysml-common-lib-contribution
    - sysml-import-order-helper
    - sysml-view-doc-sync
    - sysml-traceability
token_guardrails: |
  - **Scope:** One refactor intent per pass (e.g. one part family or one connection-def change); avoid drive-by cleanups.
  - **COTS / well-design:** Before changing baselined **part def** ports or shared **libs/common** types, consider **sysml-part-reviewer** (doc gate).
  - **Cross-file:** Use **Grep / Read** on live `.sysml` files, then Cursor **`user-sysml-v2` MCP** (`parse` / `validate` / `getSymbols` / `getDefinition` / `getReferences`) on the file or code just loaded. Do not use abandoned `sysmledgraph` or treat an MCP workspace URI index as model SSOT.
  - **Verify:** **SysML v2 MCP validate** on touched files or merged `code` where practical; run **exam_model.py** with **--project** for each affected project under **sysml-v2-models/projects/**.
  - Do not paste full multi-file models into chat; use file paths and targeted reads.
  - **Diagram labels:** `sysml-v2-models/core/ibd.py` edge labels are **presentation-only**; update only when the user cares about IBD/`--visualize` output (optional, not a substitute for validate).
  - After substantive .sysml changes: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) delta + line refresh; workflow step 6.
  - Before multi-file refactor: pin_map(TSK_model_*).
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML refactorer

**When:** A change must touch **multiple** `.sysml` files (or **common lib + one or more projects**) — renames, port model migrations (e.g. role → physical), **connection def** signature alignment, or deploy rewires driven by library changes.

**Not for:** Single-connection tweaks in one deploy only → **sysml-connections**; greenfield part authoring → **sysml-hardware-part-generator** / **sysml-software-part-generator**; requirements-only → **sysml-requirements-generator**.

## Pipeline

1. **Charter** — Name the refactor (old → new symbols, or “de facto migration for X”). List **in-scope** packages/files (e.g. `libs/common/parts/network.sysml`, `deploy-*.sysml`, `connections.sysml`).

2. **Gate (optional)** — If editing **COTS** or **well-design** **part def** / shared ports: **sysml-part-reviewer** once; list required docs if not **under-design**.

3. **Discovery** — **Grep** `import`, `::>`, and `part ` usages of old names. Use Cursor **`user-sysml-v2` MCP** `getSymbols`, `getDefinition`, and `getReferences` on the loaded file or code; use `parse` / `validate` for syntax and diagnostics. The live `.sysml` files remain SSOT.

4. **Plan** — Ordered edits: **library types first** (part/port/connection def), then **SharedConnections**, then **project** `connections-*` / `deploy-*`, then **requirements** `satisfy` text if affected. Note **config.yaml** `model_files` if new files split.

5. **Edit** — **Minimal diffs** per file; keep naming and comment style consistent with surrounding code.

6. **Verify** — **SysML v2 MCP:** **validate** (see [mcp-sysml-v2/references/tool-parameters.md](../mcp-sysml-v2/references/tool-parameters.md)). Run **exam_model.py** for every project that imports changed packages (or the user’s named project set). If errors look like **unresolved type** / **not defined** after splits or new files, check **`config.yaml`** **`model_files`** order and import closure → **sysml-import-order-helper** (escalate to **sysml-root-config** for a full greenfield scaffold).

7. **Derived docs (if repo uses them)** — Align `projects/*/outputs/*.md` or tables with new port paths → **sysml-view-doc-sync** / **sysml-traceability** as appropriate.

8. **Optional IBD** — If diagrams must read correctly: update **`ibd.py`** `_conn_edge_labels` only when the user wants **visualize** / **`--visualize`** parity; otherwise skip.

## Pairing

- **mcp-sysml-v2** — loaded-file parsing, validation, symbols, definitions, and references; do not use abandoned `sysmledgraph`.
- **sysml-common-lib-contribution** — when refactor centers on **`sysml-v2-models/libs/common/`**.
- **sysml-import-order-helper** — **`model_files`** / import order after new files, splits, or “mysterious” unresolved symbols post-rename.
- **sysml-connections** — after library stabilizes, for deploy-only rewires.
- **sysml-traceability** / **sysml-view-doc-sync** — satisfy text and outputs.

**Repo:** [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) · [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md) · [AGENTS.md](../../../AGENTS.md)

**Detail:** [references/refactor-checklist.md](references/refactor-checklist.md)
