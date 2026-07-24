---
name: sysml-requirements-generator
description: >-
  Scaffold requirements-*.sysml: requirement def, requirementId attribute, doc (SHALL/SHOULD), package
  ProjectNameRequirements; wire satisfy on parts/actions in deploy or behaviour. Triggers: requirement def,
  R1 R2, SHALL, SysML requirements package, add requirement, trace to design.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first
  pairs_with: [mcp-sysml-v2, sysml-traceability, sysml-root-config]
token_guardrails: |
  - Ask for id scheme (R1, REQ-…) and parent package name before bulk generation.
  - After edits: validate; add satisfy in deploy only when user confirms mapping.
  - Load references/requirements-style-guide.md for patterns.
  - When requirements mention **cabling or ports**, prefer vocabulary that matches **deploy** and **physical** names, or explicitly say “as allocated in deploy”; see [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md).
  - After substantive .sysml changes: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) delta (`@REQ`/`@SYM`); workflow step 6.
  - Before multi-file refactor: query_warm(TSK_model_*).
---

# SysML requirements generator

**When:** New or extended **`requirements-<project>.sysml`** with **`requirement def`** and optional **`satisfy`** links from **`deploy-*.sysml`** (or behaviour).

## Pipeline

1. **Ask first** — Package name (e.g. `SysmledgraphRequirements`), **ID attribute** name (`requirementId`), list of **requirement short names** and **one-line SHALL intent** each.

2. **Conventions** — [references/requirements-style-guide.md](references/requirements-style-guide.md).

3. **Generate** — [assets/requirement-def-stub.sysml](assets/requirement-def-stub.sysml): `private import ScalarValues::String`; each **`requirement def`** with optional **`attribute requirementId : String = "R#"`** and **`doc /* ... */`**.

4. **Root / config** — Ensure **`root-<project>.sysml`** imports requirements package **before** deploy if satisfy resolves across packages (see **sysml-root-config**).

5. **Satisfy (optional)** — On **`part def`** or usages, add **`satisfy ReqName;`** only after user maps requirement → element; use exact requirement def name.

6. **Verify** — **SysML v2 MCP validate**.

**Example:** `sysml-v2-models/projects/sysmledgraph/models/requirements-sysmledgraph.sysml`
