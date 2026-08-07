---
name: sysml-traceability
description: >-
  Add or audit traceability in SysML v2: satisfy (requirement → design), allocate (software → hardware),
  refine/derive requirement trees, doc cross-refs; align outputs/*.md tables with model (including
  10-requirements-traceability). Treat deploy connections and site conventions as de facto operational
  truth -- see references/de-facto-modeling.md. Triggers: traceability, satisfy, allocate, refine
  requirements, derive requirements, R1 maps to, verify requirement, gap analysis requirements vs design,
  de facto wiring, nominal vs actual ports, site convention.
metadata:
  pattern: pipeline
  version: "1.1"
  pairs_with: [mcp-sysml-v2, mcp-sysmledgraph, sysml-requirements-generator, sysml-requirements-audit, sysml-connections, sysml-view-doc-sync]
token_guardrails: |
  - Use sysmledgraph impact before renaming requirement or part defs used in satisfy/allocate/refine/derive.
  - After edits: validate; update .md only as second step (model first).
  - Load references/traceability-patterns.md when auditing.
  - De facto vs nominal ports: [references/de-facto-modeling.md](references/de-facto-modeling.md).
  - Sync `outputs/**/10-requirements-traceability.md` (or pack section) with parent/child requirementIds and satisfy rows.
  - After substantive .sysml changes: sysml-memnet-cache delta (`@EDG` satisfies/allocates/refines); workflow step 6.
  - Before multi-file refactor: pin_map(TSK_model_*).
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML traceability

**When:** Establishing or checking **links** between requirements (including **refine** / **derive** trees), structure (deploy), software allocation, and documentation.

## Pipeline

1. **Inventory** — List **`requirement def`** / **`requirementId`**, **refine** / **derive** edges, and **`satisfy`** / **`allocate`** in deploy (grep those keywords).

2. **Hierarchy gap** — Parent themes without children where behaviour/setup needs them; orphans with no parent and no satisfy; broken refine/derive targets.

3. **Satisfy gap** — Requirements without any **`satisfy`** candidate → flag; design claims without requirement → optional **`doc`** or new / derived requirement (**sysml-requirements-generator**).

4. **Add satisfy** — On implementing element: **`satisfy RequirementName;`** (import requirements package).

5. **Add allocate** — **`allocate softwarePart to hardwarePart;`** (see **sysml-allocate-generator**).

6. **Cross-file rename** — **sysmledgraph** or **SysML v2 MCP** impact before renaming linked elements.

7. **Docs** — Update **`outputs/**/10-requirements-traceability.md`** (and related pack sections) **from** the model: parent → child requirementIds, satisfy, allocate. Model first; markdown second.

8. **De facto check** — [references/de-facto-modeling.md](references/de-facto-modeling.md): deploy **`connection`** paths match outputs and part **`doc`** conventions.

**Patterns:** [references/traceability-patterns.md](references/traceability-patterns.md)
