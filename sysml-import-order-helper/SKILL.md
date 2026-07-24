---
name: sysml-import-order-helper
description: >-
  Diagnose and fix SysML v2 project load order: config.yaml model_files sequence, private import closure,
  typical Kernel→ISQ/SI→common→connections→requirements→deploy→behaviour→root-last chain. Triggers: import error,
  unresolved type after reorder, circular load suspicion, model_files order, missing private import, config.yaml
  model_files, load order wrong, symbol not found wrong file order.
metadata:
  pattern: pipeline
  domain: sysml-v2
  pairs_with: [mcp-sysml-v2, sysml-root-config, mcp-sysmledgraph, sysml-refactorer]
token_guardrails: |
  - **Diagnose first:** read **config.yaml** `model_files` and compare to [references/import-order-diagnosis.md](references/import-order-diagnosis.md); do not reorder OMG Kernel paths casually.
  - **Minimal change:** move one file or add one import at a time when possible; re-validate after each logical step.
  - **Verify:** **SysML v2 MCP validate** on affected snippets or full merged `code`; run **exam_model.py** with **--project** for the affected project under **sysml-v2-models/projects/**.
  - For **new project** scaffold or wholesale **root-*.sysml** authoring, prefer **sysml-root-config** after order is understood.
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML import order helper

**When:** The model **fails to load**, shows **unresolved types**, or you suspect **`model_files`** or **`private import`** order is wrong — **not** when you are greenfield-scaffolding a project from scratch (use **sysml-root-config** first unless the only issue is order).

## Pipeline

1. **Read** — **`config.yaml`**: `model_dir`, full **`model_files`** list. Note which file fails (tool error, first diagnostic, or user pointer).

2. **Check chain** — Compare to [references/import-order-diagnosis.md](references/import-order-diagnosis.md) and [sysml-root-config/references/load-order.md](../sysml-root-config/references/load-order.md). Flag: **root not last**, **deploy before requirements** (when deploy references reqs), **connections** after parts that use connection defs, **FlowItems** / **hardware_ports** order in common.

3. **Import closure** — For the failing file, grep **`private import`** / **`import`**; confirm every referenced package is loaded **earlier** in **`model_files`** (or re-exported). **sysmledgraph** MCP **context** / **impact** optional for cross-file package names.

4. **Edit** — Reorder **`model_files`** or add **`private import`** in **`root-*.sysml`** / package file per project conventions; keep paths correct relative to **`model_dir`**.

5. **Verify** — **mcp-sysml-v2** **validate**; **exam_model.py** for the project.

6. **Escalate** — If structure is missing (no root package, empty project): hand off to **sysml-root-config**.

**Cross-file renames / splits:** Unresolved symbols may be **stale paths** or **missing imports** after a refactor — pair with **sysml-refactorer** when the root cause is coordinated renames, not **`model_files`** order alone.

**Repo:** [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) · [sysml-v2-models/libs/common/README.md](../../../sysml-v2-models/libs/common/README.md)

**Detail:** [references/import-order-diagnosis.md](references/import-order-diagnosis.md)
