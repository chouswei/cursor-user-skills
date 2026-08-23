---
name: sysml-part-reviewer
description: >-
  Classify SysML part defs by design maturity: under-design, well-design, or COTS; enforce that only under-design
  parts may be edited without accompanying documentation. Apply Hakim Minimalist Engineering gates on parts,
  ports, allocate, behaviour, and items. Triggers: review part, part maturity, COTS vs custom,
  OTS vs IMD PCBA, can we edit without docs, part def gate, edit existing part, hardware part review,
  electronics part lifecycle, libs/common part change, nominal vs de facto ports, physical vs role interfaces,
  minimalist engineering, over-engineering, unused port, ceremony without allocate, fat interface, monolith part.
metadata:
  pattern: reviewer
  severity-levels: error, warning, info
  version: "1.1"
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

**Role:** Gate SysML **part def** changes by **design maturity**, **documentation**, and **Minimalist Engineering** (Hakim).

## Rules (binding)

1. Every part in scope has exactly one condition: **under-design**, **well-design**, or **COTS** (Commercial Off-The-Shelf).
2. **Only under-design parts** may be modified **without** additional documentation beyond the model (subject to project validate / outputs rules).
3. **well-design** and **COTS** parts require appropriate **documents or evidence** alongside (or before) model edits.

## Steps

0. **When to run first** -- Use before editing an **existing** `part def` or changing **libs/common** parts/ports when maturity is unknown. Greenfield **new** parts are often **under-design** until the user baselines them; still classify if the block is clearly COTS (e.g. dev kit with MPN).
1. Load [references/part-review-criteria.md](references/part-review-criteria.md) and [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md) when the part mixes **role-named** and **physical** ports or is COTS network/power gear.
2. Identify part(s): file path, `part def` name, domain (hardware / software / other).
3. Classify each part per the criteria table; use the **Mapping common inputs** table for OTS/custom/lib signals; if ambiguous, prefer stricter class (well-design or COTS) and state what is missing to confirm.
4. For the requested change: if condition is not **under-design**, list required documentation; do not approve "model-only" edits without that list being addressed.
5. Apply **Minimalist Engineering** gates (section below) to the same parts, ports, allocate, behaviour, and items.
6. Emit findings with severity **error** | **warning** | **info** when a maturity or Minimalist Engineering gate would be violated or evidence is weak.
7. Point to **Related skills** in the criteria doc for the next authoring step once the gate is satisfied.

## Minimalist Engineering

**Doctrine SSOT:** Ammar Hakim and Murtaza Hakim, [A Minimalist Approach to Software](https://ammar-hakim.org/minimalist-software.html) (updated 3 Nov 2022). Pointer only; do not paste or restyle the essay. Numbers below are the article's.

Apply to **parts, ports, allocate, behaviour, items**. Article 14-17 and 20-22 (C, scripting, builds) are out of scope unless they are the same finding as a dependency or layering issue.

**MUST flag** (`warning`; `error` if the requested edit *adds* unused structure):

1. **Counts; one thing well** -- each `part def` / `port def` / `item def` earns its place by doing one job. MUST NOT score fewer lines as the goal.
2. **Brutal MVP** -- drop "good to have" if it is not must-have for a stated requirement or allocate.
3. **Simplicity** -- over-engineering: unused layering, wrapper parts with no ports or allocate, ceremony without allocate.
4. **Clean ideas** -- rewrite a muddled def rather than pile aliases; keep only the axiomatic concepts the feature needs.
5. **Related data together; data and operators separate** -- `item` / attributes hold data; `action` / `state` / behaviour hold operators. MUST NOT invent a god part that mixes both.
6. **Mutate via functions** -- state change belongs in behaviour (actions / transitions), not ad-hoc attribute writes with no action.
7-9. **Do not force flexibility** from ordinary-language sameness. Separate systems; structured communication via **ports, items, connections** (Unix-pipe analogue).
10-12. **Nested parts OK**; inheritance / fat interfaces usually not. Some duplication, then refactor. Prefer multi-part functions (connections / allocate across peers) over shared incestuous state.
13. **Minimise dependencies** -- extra `import`, unused common types, magic package / framework piles; no exponential deps.
18. **Layers = indirection**, not a bandage over last year's contradiction.
19. **Popularity is not quality** -- MUST flag "framework" ceremony that does not serve allocate or behaviour.
23. **MVPs with structured exchange** -- `item` on ports; MUST flag a monolith `part def` that swallows many systems.

**MUST NOT** invent extra philosophy. Cite the article number on each finding.

## Output format

- **Summary** -- Count by condition; whether the requested edit is allowed without docs; Minimalist Engineering finding count.
- **Per part** -- Name; **Condition**; **Modification without docs:** yes|no; **Rationale** (one line); **Required docs** (if no).
- **Findings** -- Grouped by severity (errors first). Minimalist Engineering items: article #; SysML element; one-line why.

## Pairing

- After classification, **under-design** edits may use **sysml-hardware-part-generator**, **sysml-software-part-generator**, **sysml-item-generator**, or **sysml-connections** as appropriate.
- **well-design** / **COTS** changes should align with **sysml-view-doc-sync** or project `outputs/` when the repo uses derived docs.
