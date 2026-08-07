# Requirements audit — output template

Use as the **user-visible** structure for a read-only audit (adjust sections if the project has no requirements file).

## Summary

- **Project / package:** …
- **Requirements file(s):** …
- **Deploy (and other) files scanned:** …
- **Counts:** requirement defs = *n*; refine/derive edges = *r*; requirement usages in deploy = *m*; **satisfy** statements = *k*.

## Requirement definitions

| Def name | requirementId / note | Doc snippet |
|----------|----------------------|-------------|
| … | … | … |

## Refine / derive hierarchy

| Parent requirementId | Relation | Child requirementId |
|----------------------|----------|---------------------|
| … | refine / derive | … |

- **Missing children** (parent theme needs nested obligations): …
- **Orphan / broken hierarchy links:** …

## Satisfy coverage

| Requirement usage (or def) | Satisfied by (element / part path) | File |
|-----------------------------|--------------------------------------|------|
| … | … | … |

## Gaps / findings

- **Orphaned defs** (no satisfy): …
- **Unknown / broken satisfy refs:** …
- **Duplicates / convention issues:** …
- **Flat peers** that should derive/refine under one parent: …

## Suggested next steps

- **sysml-traceability** — add or fix **satisfy** / **allocate** / hierarchy docs; sync **`10-requirements-traceability.md`**.
- **sysml-requirements-generator** — scaffold missing or **derived/refined** **requirement def** entries.
- **sysml-view-doc-sync** — refresh **outputs/*.md** **after** model changes (not part of this audit unless requested).
