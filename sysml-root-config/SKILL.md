---
name: sysml-root-config
description: >-
  Scaffold or fix root-<project>.sysml (package Project<Name> with private imports) and config.yaml
  model_files load order: Kernel → ISQ/SI → common parts → connections → composites → requirements →
  deploy → behaviour → root last. Triggers: root package, config.yaml, model_files order, import missing,
  ProjectFoo package, new project sysml.
metadata:
  pattern: generator
  output-format: mixed
  pairs_with: [mcp-sysml-v2, sysml-requirements-generator, sysml-import-order-helper]
token_guardrails: |
  - Never reorder OMG kernel paths casually; follow an existing project config as template.
  - After changes: validate full project load; root file must be last in model_files.
  - Load references/load-order.md for standard chain.
  - New project doc/index updates: [references/new-project-index-updates.md](references/new-project-index-updates.md).
---

# SysML root & config

**When:** New **project**, broken **imports**, or **`config.yaml`** / **`root-*.sysml`** out of sync with [sysml-modeling-workflow](../../sysml-modeling-workflow/SKILL.md).

## Pipeline

1. **Template** — Copy **`model_files`** head from an existing project (e.g. `vedan-foam-detection/config.yaml`) for OMG Kernel + ISQ/SI + common `parts/` chain.

2. **Project packages** — List **`requirements-`**, **`connections-`** (if any), **`deploy-`**, **`behaviour-`** in dependency order: requirements before deploy if deploy references reqs; deploy before behaviour if behaviour imports deploy.

3. **Root file** — [assets/root-package-stub.sysml](assets/root-package-stub.sysml): **`package Project<Name> { private import … }`** only; rename main deploy package import to match your deploy file (stub shows `ProjectNameMain`).

4. **config.yaml** — **`model_dir: models`**; **`model_files`** ends with **`models/root-<project>.sysml`**.

5. **Verify** — **SysML v2 MCP validate** (or project load) with full file list.

6. **Register in docs** — For a **new** project folder: [references/new-project-index-updates.md](references/new-project-index-updates.md).

**Detail:** [references/load-order.md](references/load-order.md)
