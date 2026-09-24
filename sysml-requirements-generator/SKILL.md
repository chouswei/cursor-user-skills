---
name: sysml-requirements-generator
description: >-
  Scaffold or extend requirements-*.sysml: requirement def, requirementId, doc (SHALL/SHOULD),
  package ProjectNameRequirements; prefer nested requirement usages under a parent usage (or
  refine/derive only when the project already uses those edges); wire satisfy on parts/actions.
  Long requirement/part doc MUST nest children (one topic each); parent doc stays short (purpose +
  SHALL list + pointers) -- not one labelled novel. Triggers: requirement def, R1 R2, SHALL, SysML
  requirements package, add requirement, refine requirements, derive requirements, nested requirement
  usage, trace to design, long doc, doc decomposition, SysML documentation split, structured doc block.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first
  version: "1.5"
  pairs_with: [mcp-sysml-v2, sysml-traceability, sysml-root-config, sysml-requirements-audit, sysml-view-doc-sync]
token_guardrails: |
  - Ask for id scheme and parent package name before bulk generation.
  - Prefer nested requirement usages under an existing parent usage (same id prefix family). Use SysML refine/derive edges only when the live project already uses them; MUST NOT invent refine/derive as the default hierarchy.
  - Prose that says "refines" in a doc block is NOT a SysML refine edge. Nested usage is the hierarchy unless refine/derive edges exist.
  - Model SSOT for normative prose is `.sysml` `doc /* ... */`. MUST NOT park the primary long text only in wiki or `outputs/`.
  - Long `doc` MUST nest children (one topic each). Parent `doc` SHALL stay short: purpose, SHALL / SHALL NOT list, pointers to nested requirementIds. MUST NOT treat seven labelled headings in one parent `doc` as done.
  - MUST NOT invent peer-equipment or crate rail voltages as SHALLs (e.g. turbopump catalog 24 V is not lane or filament power). Unmodelled volts stay TBD.
  - Satisfy lives on the parent usage (or the part that owns the theme) unless each nested child has its own `satisfy`. Nested usage alone does not create per-child satisfy.
  - After edits: validate; add satisfy in deploy only when user confirms mapping.
  - Load references/requirements-style-guide.md for patterns.
  - When requirements mention cabling or ports, match deploy / physical names (or say "as allocated in deploy"); see sysml-traceability/references/de-facto-modeling.md.
  - Do not hard-code site IPs or hostnames in skill prose or stubs -- use generic patterns (sticky MAC reservation, ordered commissioning, multi-edge octet bands).
  - After substantive .sysml changes: sysml-memnet-cache delta (`@REQ`/`@SYM`); workflow step 6; sync outputs requirements-traceability section via sysml-traceability / sysml-view-doc-sync.
  - Before multi-file refactor: pin_map(TSK_model_*).
---

# SysML requirements generator

**When:** New or extended **`requirements-<project>.sysml`** with **`requirement def`**, nested **requirement usages** (and optional **refine** / **derive** only when already in use), and optional **`satisfy`** from deploy or behaviour.

## Pipeline

1. **Ask first** -- Package name, **ID attribute** (`requirementId`), whether work is **new root**, **nested usage** under an existing parent, or **refine** / **derive** (only if the project already uses those edges); short names + one-line SHALL each.

2. **Hierarchy first** -- Prefer a **parent usage -> nested child usages** tree (same id prefix family). Flat new peers only when no parent fits. Child ids inherit the parent family (e.g. `EILIT-R-EI-002` -> `EILIT-R-EI-002-IV`). MUST NOT invent SysML **`refine`** / **`derive`** edges as the default; nested usage is the hierarchy. Doc prose that says "refines" MUST NOT be treated as a SysML refine.

3. **Conventions** -- [references/requirements-style-guide.md](references/requirements-style-guide.md).

4. **Generate** -- [assets/requirement-def-stub.sysml](assets/requirement-def-stub.sysml): `private import ScalarValues::String`; each **`requirement def`** with **`requirementId`** and **`doc /* ... */`**. Cross-reference sibling ids in **doc** only when they clarify scope; hierarchy links belong in nested usages (or in refine/derive when those edges already exist).

5. **Long doc decomposition (MUST)** -- When a requirement or part needs more than a short SHALL:
   - Keep SSOT in the model `doc` blocks (parent + nested children).
   - **Parent `doc` SHALL stay short:** purpose; SHALL / SHALL NOT list; pointers to nested requirementIds. No plant novel, no first-principles essay, no multi-page TBD catalogue on the parent.
   - **Long prose MUST live on nested children** -- one topic each (e.g. `...-IV`, `...-ISO`, `...-PHY`, `...-PSU`, `...-FP` for first-principles / analysis). Labelled sections belong on the child that owns that topic.
   - MUST NOT treat seven labelled headings in one parent `doc` as done. A sectioned parent novel is still a novel -- split it.
   - MUST NOT duplicate a child SHALL on the parent once the child owns that topic.
   - MUST NOT invent unmodelled rail or setpoint volts from peer equipment or crate catalogs (catalog **24 V** is not a filament or lane-power SHALL). Leave those TBD until deploy models them.
   - Domain checks when modelling filament / RS-485 drivers: heating current is **`I_heat`** (MUST NOT call it emission); VacuumRs485Lane is a digital PSU / control rail (MUST NOT treat as MKS instrument bus unless the model says so).
   - Hand off wiki / `outputs/` summary to **sysml-view-doc-sync** (summarise + point at nested requirementIds; MUST NOT duplicate parent or child novels).

6. **Root / config** -- Ensure **`root-<project>.sysml`** imports requirements **before** deploy if satisfy resolves across packages (**sysml-root-config**).

7. **Satisfy (optional)** -- On implementing elements: **`satisfy ReqName;`** only after user maps requirement -> element. Default: satisfy the **parent usage** (theme). Add per-nested-usage satisfy (`rParent.nestedChild`) only when the user wants path-level coverage like peer subsystems; nested usage alone does not imply per-child satisfy.

8. **Verify + docs** -- **SysML v2 MCP validate**. Hand off **sysml-traceability** / **sysml-view-doc-sync** so **`outputs/**/10-requirements-traceability.md`** (or project equivalent) shows nested requirementIds and satisfy coverage.

**Example (checkable ids):** EI tungsten-wire drive -- parent short; nested children `EILIT-R-EI-002-IV` / `-ISO` / `-PHY` / `-PSU` / `-FP`; `-FP` is analysis-only (no path satisfy by default); heating `I_heat` (not emission); 1.5 kV digital isolator; Pico 2 on shared crate RS-485 (VacuumRs485Lane; SHALL NOT invent MKS). MUST NOT invent crate **24 V** SHALLs.
