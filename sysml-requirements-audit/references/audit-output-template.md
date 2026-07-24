# Requirements audit — output template

Use as the **user-visible** structure for a read-only audit (adjust sections if the project has no requirements file).

## Summary

- **Project / package:** …
- **Requirements file(s):** …
- **Deploy (and other) files scanned:** …
- **Counts:** requirement defs = *n*; requirement usages in deploy = *m*; **satisfy** statements = *k*.

## Requirement definitions

| Def name | requirementId / note | Doc snippet |
|----------|----------------------|-------------|
| … | … | … |

## Satisfy coverage

| Requirement usage (or def) | Satisfied by (element / part path) | File |
|-----------------------------|--------------------------------------|------|
| … | … | … |

## Gaps / findings

- **Orphaned defs** (no satisfy): …
- **Unknown / broken satisfy refs:** …
- **Duplicates / convention issues:** …

## Suggested next steps

- **sysml-traceability** — add or fix **satisfy** / **allocate**, align with design.
- **sysml-requirements-generator** — scaffold missing **requirement def** entries.
- **sysml-view-doc-sync** — refresh **outputs/*.md** tables **after** model changes (not part of this audit unless requested).
