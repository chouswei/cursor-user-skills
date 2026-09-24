---
name: sysml-traceability
description: >-
  Add or audit traceability in SysML v2: satisfy (requirement → design), allocate (software → hardware),
  nested requirement usages (and refine/derive only when already used), doc cross-refs; align
  outputs/*.md tables with model (including 10-requirements-traceability). Treat deploy connections
  and site conventions as de-facto operational truth -- see references/de-facto-modeling.md. Triggers:
  traceability, satisfy, allocate, refine requirements, derive requirements, nested requirement usage,
  R1 maps to, verify requirement, gap analysis requirements vs design, de facto wiring, nominal vs
  actual ports, site convention, trace manifest, projection input, kind qname allocate.
metadata:
  pattern: pipeline
  version: "1.4"
  pairs_with: [mcp-sysml-v2, sysml-requirements-generator, sysml-requirements-audit, sysml-connections, sysml-view-doc-sync]
token_guardrails: |
  - Before renaming linked requirements or part defs, use **Grep / Read** on live `.sysml`, then Cursor **`user-sysml-v2` MCP** (`getSymbols`, `getDefinition`, `getReferences`, `parse`, `validate`) on the file or code just loaded. Do not use abandoned `sysmledgraph` or treat an MCP workspace URI index as model SSOT.
  - After edits: validate; update .md only as second step (model first).
  - Load references/traceability-patterns.md when auditing.
  - De facto vs nominal ports: [references/de-facto-modeling.md](references/de-facto-modeling.md).
  - Sync `outputs/**/10-requirements-traceability.md` (or pack section) with **nested** requirementIds and satisfy rows; wiki summarises (MUST NOT paste novels).
  - MUST NOT invent SysML refine/derive edges as the default hierarchy fix; nested usage is valid.
  - After substantive .sysml changes: sysml-memnet-cache delta (`@EDG` satisfies/allocates/refines); workflow step 6.
  - Before multi-file refactor: pin_map(TSK_model_*).
  - **Trace manifest:** Follow input contract in [references/trace-manifest.md](references/trace-manifest.md).
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML traceability

**When:** Establishing or checking **links** between requirements (including **nested usages** and optional **refine** / **derive** trees), structure (deploy), software allocation, and documentation.

## Pipeline

1. **Inventory** — List **`requirement def`** / **`requirementId`**, **nested requirement usages**, **refine** / **derive** edges (if any), and **`satisfy`** / **`allocate`** in deploy (grep those keywords). State hierarchy form: nested usage vs refine/derive.

2. **Hierarchy gap** — Parent themes without nested children where behaviour/setup needs them; orphans with no parent and no satisfy; broken refine/derive targets. MUST NOT invent refine edges as a default fix when nested usages already express the tree.

3. **Satisfy gap** — Requirements without any **`satisfy`** candidate -> flag; design claims without requirement -> optional **`doc`** or new / nested requirement (**sysml-requirements-generator**).
   - **Parent-only vs path satisfy:** When only the parent usage is satisfied (e.g. `rEi` / `rEi.tungstenWireDrive`) and nested grandchildren (`...-IV` / `-ISO` / `-PHY` / `-PSU` / `-FP`) have no path satisfy, MUST either (a) add **`satisfy rParent.nestedUsage`** on the implementing part when path-level coverage is wanted (peer pattern), or (b) document parent-only satisfy as **deliberate** (analysis-only children such as `-FP` often stay without path satisfy). Ask the user when asymmetry vs HVDC/RF/LIT peers matters.

4. **Add satisfy** — On implementing element: **`satisfy RequirementName;`** or path **`satisfy rParent.nestedChild;`** (import requirements package). Prefer matching the project's existing satisfy grain.

5. **Add allocate** — **`allocate softwarePart to hardwarePart;`** (see **sysml-allocate-generator**).

6. **Cross-file rename** — Grep / Read live `.sysml`, then use Cursor **`user-sysml-v2` MCP** on the loaded file or code (`getSymbols`, `getDefinition`, `getReferences`, `parse`, `validate`) before renaming linked elements.

7. **Docs** — Update **`outputs/**/10-requirements-traceability.md`** (and related pack / wiki sections) **from** the model: nested requirementIds, satisfy, allocate. Wiki / outputs MUST **summarise** and list nested ids; MUST NOT paste parent or child novels. Model first; markdown second. Prefer outputs path from open-repo **AGENTS.md** / **`sysml-models/outputs/`**.

8. **De facto check** — [references/de-facto-modeling.md](references/de-facto-modeling.md): deploy **`connection`** paths match outputs and part **`doc`** conventions.

9. **Trace manifest** — Produce a projection input table (kind, qname, target) per [references/trace-manifest.md](references/trace-manifest.md). This manifest is the contract for external board sync; it MUST NOT contain board-specific IDs.

**Patterns:** [references/traceability-patterns.md](references/traceability-patterns.md)
