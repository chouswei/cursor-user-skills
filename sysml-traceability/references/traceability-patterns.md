# Traceability patterns (repo)

| Link | Typical syntax | Where |
|------|----------------|--------|
| Requirement → design | `satisfy ReqName;` or `satisfy rParent.nestedChild;` inside `part def` / on usage | deploy package; imports requirements |
| Software → hardware | `allocate partUsage to partUsage;` | deployment composite in deploy |
| Parent → child requirement | **nested requirement usage** (default); `refine` / `derive` only when the project already uses those edges | requirements package |
| Doc cross-cite | Mention related requirementIds in `doc` | clarifying only; prose "refines" is not a SysML refine |

- **Imports:** Deploy needs `private import …Requirements::*` for `satisfy`.
- **Naming:** Exact **`requirement def`** name or nested usage path after `satisfy`.
- **Trees:** Prefer nested usages under one parent theme id over inventing refine/derive edges. Flat peers only when no parent fits.
- **Satisfy grain:** Parent-only satisfy may be deliberate (theme coverage; analysis-only `-FP`). Path satisfy (`rParent.nestedUsage`) when peers use path-level coverage and the user wants the same. Document the choice in the audit / trace table.
- **Outputs:** After model change, sync **`outputs/**/10-requirements-traceability.md`** (nested requirementIds + satisfy matrix). Wiki summarises; MUST NOT paste novels.
- **Rename gate:** Grep / Read live `.sysml`, then use Cursor **`user-sysml-v2` MCP** `getReferences` on the loaded file or code before deleting or renaming.
