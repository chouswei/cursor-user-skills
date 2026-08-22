---
name: sysml-common-file-scale
description: >-
  Soft line-count guardrails for sysml-v2-models/libs/common: measure with bundled script; when a *.sysml
  file grows large, split by cohesive subdomain into a new file (one primary package per file); update
  every project config.yaml and READMEs. Prefer Grep / Read on live `.sysml`, then SysML v2 MCP
  (getSymbols, getDefinition with name=, getReferences with name=, validate) on loaded code. Triggers: common lib too long, split
  package, line limit, monolithic sysml, refactor common, token budget, audit common file sizes.
metadata:
  pattern: pipeline
  output-format: mixed
  pairs_with: [mcp-sysml-v2, sysml-common-lib-contribution, sysml-hardware-part-generator]
token_guardrails: |
  - Split on domain cohesion, not line count alone; never tear one logical package across two files for size.
  - After adding a common file: update every project config.yaml that lists the common chain; grep imports.
  - For edits, prefer SysML MCP scoped tools over loading full multi-kLine files.
  - Use split-checklist asset before declaring a split done; refresh scale-policy audit table when thresholds change or after major growth.
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML common file scale

**When:** **`libs/common/**/*.sysml`** sizing review, **split planning**, **LLM context** discipline, or the user asks **how big is too big**.

## Pipeline

1. **Measure** — From repo root: `python .cursor/skills/sysml-common-file-scale/tools/count_common_sysml_lines.py` (or `python tools/...` from the skill folder). Compare output to [references/scale-policy.md](references/scale-policy.md). Update the **Last audit snapshot** table there after a formal review.

2. **Prefer tooling over split** — Use **Grep / Read** on live `.sysml`, then Cursor **`user-sysml-v2` MCP** (`getSymbols`, `getDefinition`, `getReferences`, `parse`, `validate`) on the file or code just loaded. Grep live imports and symbol usages for blast radius. Do not use abandoned `sysmledgraph` or treat an MCP workspace URI index as model SSOT. Splitting is for **maintainability**, not a substitute for MCP navigation.

3. **Decide split** — If at/above soft trigger **and** a **clear subdomain** (new package name, stable boundary, minimal cross-coupling): plan **one new file = one new package**. If no boundary, **defer**; track in `tasks/` if needed. **Part-heavy** moves: pair with **sysml-hardware-part-generator** for new defs’ shape.

4. **Execute** — Follow **sysml-common-lib-contribution**: naming rules, load order, minimal change. Move `part def` / `connection def` / composites as a coherent set; fix imports. **IMD / network / Poe edge** touches: [workspace-imd-lib-conventions.md](../sysml-common-lib-contribution/references/workspace-imd-lib-conventions.md).

5. **Register** — **`model_files`** in **all** projects using common; **libs/common/README.md**; **parts/README.md** when under `parts/`.

6. **Verify** — **Validate** edited common files + ≥1 consuming project **full** `config.yaml` load.

7. **Close** — Walk [assets/split-checklist.md](assets/split-checklist.md); refresh **Last audit** in `scale-policy.md` if you ran a sizing pass.

## Pairing

- **sysml-common-lib-contribution** — when/how to edit **`libs/common/`**.
- **sysml-hardware-part-generator** — scaffolding moved or new part defs after a **parts/** split.
- **mcp-sysml-v2** — validate and scoped navigation.
- **mcp-sysml-v2** — loaded-file dependency navigation, references, and validation after moves.

## References

- [references/scale-policy.md](references/scale-policy.md) — thresholds, audit table, anti-patterns, **poe_edge** exception.
- [assets/split-checklist.md](assets/split-checklist.md) — split PR / task checklist.
- [sysml-common-lib-contribution](../sysml-common-lib-contribution/references/common-library-naming-detailed.md) · [libs/common/README.md](../../../sysml-v2-models/libs/common/README.md)
