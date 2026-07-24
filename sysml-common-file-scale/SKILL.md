---
name: sysml-common-file-scale
description: >-
  Soft line-count guardrails for sysml-v2-models/libs/common: measure with bundled script; when a *.sysml
  file grows large, split by cohesive subdomain into a new file (one primary package per file); update
  every project config.yaml and READMEs. Prefer SysML v2 MCP (getSymbols, getDefinition with name=, getReferences with name=, validate)
  and sysmledgraph over reading whole files for LLM token efficiency. Triggers: common lib too long, split
  package, line limit, monolithic sysml, refactor common, token budget, audit common file sizes.
metadata:
  pattern: pipeline
  output-format: mixed
  pairs_with: [mcp-sysml-v2, mcp-sysmledgraph, sysml-common-lib-contribution, sysml-hardware-part-generator]
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

2. **Prefer tooling over split** — For **localized** work: **SysML v2 MCP** **getSymbols**, **getDefinition** (`name`), **getReferences** (`name`), **validate** (`code` or per [mcp-sysml-v2 tool-parameters](../mcp-sysml-v2/references/tool-parameters.md)); use **read_file** with **line range** if you must open text. For **blast radius**: **sysmledgraph** (`indexDbGraph` then `impact` / `query`) or **grep** `private import PackageName` under `sysml-v2-models/`. Splitting is for **maintainability**, not a substitute for MCP navigation.

3. **Decide split** — If at/above soft trigger **and** a **clear subdomain** (new package name, stable boundary, minimal cross-coupling): plan **one new file = one new package**. If no boundary, **defer**; track in `tasks/` if needed. **Part-heavy** moves: pair with **sysml-hardware-part-generator** for new defs’ shape.

4. **Execute** — Follow **sysml-common-lib-contribution**: naming rules, load order, minimal change. Move `part def` / `connection def` / composites as a coherent set; fix imports. **IMD / network / Poe edge** touches: [workspace-imd-lib-conventions.md](../sysml-common-lib-contribution/references/workspace-imd-lib-conventions.md).

5. **Register** — **`model_files`** in **all** projects using common; **libs/common/README.md**; **parts/README.md** when under `parts/`.

6. **Verify** — **Validate** edited common files + ≥1 consuming project **full** `config.yaml` load.

7. **Close** — Walk [assets/split-checklist.md](assets/split-checklist.md); refresh **Last audit** in `scale-policy.md` if you ran a sizing pass.

## Pairing

- **sysml-common-lib-contribution** — when/how to edit **`libs/common/`**.
- **sysml-hardware-part-generator** — scaffolding moved or new part defs after a **parts/** split.
- **mcp-sysml-v2** — validate and scoped navigation.
- **mcp-sysmledgraph** — dependency / impact after moves.

## References

- [references/scale-policy.md](references/scale-policy.md) — thresholds, audit table, anti-patterns, **poe_edge** exception.
- [assets/split-checklist.md](assets/split-checklist.md) — split PR / task checklist.
- [sysml-common-library-naming](../sysml-common-library-naming/references/common-library-naming-detailed.md) · [libs/common/README.md](../../../sysml-v2-models/libs/common/README.md)
