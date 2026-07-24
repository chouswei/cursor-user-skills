---
name: sysml-part-reviewer
description: >-
  Classify SysML part defs by design maturity: under-design, well-design, or COTS; enforce that only under-design
  parts may be edited without accompanying documentation. Triggers: review part, part maturity, COTS vs custom,
  OTS vs IMD PCBA, can we edit without docs, part def gate, edit existing part, hardware part review,
  electronics part lifecycle, libs/common part change, nominal vs de facto ports, physical vs role interfaces.
metadata:
  pattern: reviewer
  severity-levels: error, warning, info
  pairs_with:
    - sysml-hardware-part-generator
    - sysml-software-part-generator
    - sysml-physical-port-generator
    - sysml-item-generator
    - sysml-connections
    - sysml-view-doc-sync
    - sysml-common-lib-contribution
---

# SysML part reviewer

**Role:** Gate SysML **part def** changes by **design maturity** and **documentation**.

## Rules (binding)

1. Every part in scope has exactly one condition: **under-design**, **well-design**, or **COTS** (Commercial Off-The-Shelf).
2. **Only under-design parts** may be modified **without** additional documentation beyond the model (subject to project validate / outputs rules).
3. **well-design** and **COTS** parts require appropriate **documents or evidence** alongside (or before) model edits.

## Steps

0. **When to run first** — Use before editing an **existing** `part def` or changing **libs/common** parts/ports when maturity is unknown. Greenfield **new** parts are often **under-design** until the user baselines them; still classify if the block is clearly COTS (e.g. dev kit with MPN).
1. Load [references/part-review-criteria.md](references/part-review-criteria.md) and [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md) when the part mixes **role-named** and **physical** ports or is COTS network/power gear.
2. Identify part(s): file path, `part def` name, domain (hardware / software / other).
3. Classify each part per the criteria table; use the **Mapping common inputs** table for OTS/custom/lib signals; if ambiguous, prefer stricter class (well-design or COTS) and state what is missing to confirm.
4. For the requested change: if condition is not **under-design**, list required documentation; do not approve “model-only” edits without that list being addressed.
5. Emit findings with severity **error** | **warning** | **info** when the gate would be violated or evidence is weak.
6. Point to **Related skills** in the criteria doc for the next authoring step once the gate is satisfied.

## Output format

- **Summary** — Count by condition; whether the requested edit is allowed without docs.
- **Per part** — Name; **Condition**; **Modification without docs:** yes|no; **Rationale** (one line); **Required docs** (if no).
- **Findings** — Grouped by severity (errors first).

## Pairing

- After classification, **under-design** edits may use **sysml-hardware-part-generator**, **sysml-software-part-generator**, **sysml-item-generator**, or **sysml-connections** as appropriate.
- **well-design** / **COTS** changes should align with **sysml-view-doc-sync** or project `outputs/` when the repo uses derived docs.
