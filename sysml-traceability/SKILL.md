---
name: sysml-traceability
description: >-
  Add or audit traceability in SysML v2: satisfy (requirement → design), allocate (software → hardware),
  doc cross-refs; optional deriveRefinement; align outputs/*.md tables with model. Treat deploy connections
  and documented site conventions as de facto operational truth vs nominal role naming—see references/de-facto-modeling.md.
  Triggers: traceability, satisfy, allocate, R1 maps to, verify requirement, gap analysis requirements vs design,
  de facto wiring, nominal vs actual ports, site convention.
metadata:
  pattern: pipeline
  pairs_with: [mcp-sysml-v2, mcp-sysmledgraph, sysml-requirements-generator, sysml-requirements-audit, sysml-connections]
token_guardrails: |
  - Use sysmledgraph impact before renaming requirement or part defs used in satisfy/allocate.
  - After edits: validate; update .md only as second step (model first).
  - Load references/traceability-patterns.md when auditing.
  - De facto vs nominal ports and deploy-as-built: [references/de-facto-modeling.md](references/de-facto-modeling.md).
  - After substantive .sysml changes: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) delta (`@EDG` satisfies/allocates); workflow step 6.
  - Before multi-file refactor: pin_map(TSK_model_*).
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML traceability

**When:** Establishing or checking **links** between requirements, structure (deploy), software allocation, and documentation.

## Pipeline

1. **Inventory** — List **`requirement def`** (requirements package) and **`satisfy`** / **`allocate`** in **deploy** (grep `satisfy`, `allocate`).

2. **Gap** — Requirements without any **`satisfy`** candidate → flag for user; design claims without requirement → optional **`doc`** note or new requirement.

3. **Add satisfy** — On **`part def`**, **`part`** usage, or element that implements: **`satisfy RequirementName;`** (import requirements package in deploy).

4. **Add allocate** — **`allocate softwarePart to hardwarePart;`** at deployment composite (see **sysml-allocate-generator** for focused scaffolding).

5. **Cross-file rename** — **sysmledgraph** or **SysML v2 MCP** impact before renaming linked elements.

6. **Docs** — Update **`outputs/*.md`** traceability tables / § references **from** model.

7. **De facto check** — Load [references/de-facto-modeling.md](references/de-facto-modeling.md). Confirm **deploy `connection`** port paths match **outputs** and **part `doc`** site conventions; flag **nominal** role names on COTS **part def** that contradict physical inventory or unstated conventions.

**Patterns:** [references/traceability-patterns.md](references/traceability-patterns.md)
