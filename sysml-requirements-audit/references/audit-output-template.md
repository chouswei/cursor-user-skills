# Requirements audit -- output template

Use as the **user-visible** structure for a read-only audit (adjust sections if the project has no requirements file).

## Summary

- **Project / package:** …
- **Requirements file(s):** …
- **Deploy (and other) files scanned:** …
- **Hierarchy form:** nested usage | refine/derive | mixed (state which)
- **Counts:** requirement defs = *n*; nested usages = *u*; refine/derive edges = *r*; requirement usages in deploy = *m*; **satisfy** statements = *k*.

## Requirement definitions

| Def name | requirementId / note | Doc snippet |
|----------|----------------------|-------------|
| … | … | … |

## Hierarchy (nested usage and/or refine/derive)

| Parent path / requirementId | Relation | Child path / requirementId |
|-----------------------------|----------|----------------------------|
| … | nested usage / refine / derive | … |

- **Missing children** (parent theme needs nested obligations): …
- **Orphan / broken hierarchy links:** …
- **Prose "refines" without SysML refine edge:** … (nested usage may still be valid)

## Satisfy coverage

| Requirement usage path | Satisfied by (element / part path) | File |
|------------------------|--------------------------------------|------|
| … | … | … |

- **Parent-only satisfy** (children/grandchildren lack path satisfy): …
- **Asymmetry vs peers** (other subsystems with path-level satisfy): …
- **Analysis-only children** (e.g. `-FP`) with SHALL still present: …

## Gaps / findings

- **Orphaned defs** (no satisfy): …
- **Unknown / broken satisfy refs:** …
- **Duplicates / convention issues:** …
- **Flat peers** that should nest under one parent: …
- **Parent doc still long** vs generator short-parent gate: …
- **Parent duplicates child SHALL:** …
- **Domain smells** (`I_heat` vs emission; VacuumRs485Lane vs MKS; invented 24 V): …
- **Mutually exclusive / superseded satisfy:** conflicting requirements/actions on one subject; siblings left unsatisfied or pointing at superseded actions.

## Suggested next steps

- **sysml-traceability** -- add or fix **satisfy** / **allocate** / docs; decide parent-only vs `rParent.nestedUsage` path satisfy; sync **`10-requirements-traceability.md`**. MUST NOT invent refine edges by default.
- **sysml-requirements-generator** -- scaffold missing or **nested** **requirement def** / usage entries; shorten long parent docs.
- **sysml-view-doc-sync** -- refresh **outputs/*.md** / wiki **after** model changes (summarise; pointer to nested ids; not part of this audit unless requested).
