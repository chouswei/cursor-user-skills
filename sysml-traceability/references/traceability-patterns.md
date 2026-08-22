# Traceability patterns (repo)

| Link | Typical syntax | Where |
|------|----------------|--------|
| Requirement → design | `satisfy ReqName;` inside `part def` / on usage | deploy package; imports requirements |
| Software → hardware | `allocate partUsage to partUsage;` | deployment composite in deploy |
| Parent → child requirement | `refine` / `derive` (project SysML v2 form) | requirements package |
| Doc cross-cite | Mention related requirementIds in `doc` | clarifying only; not a substitute for refine/derive |

- **Imports:** Deploy needs `private import …Requirements::*` for `satisfy`.
- **Naming:** Exact **`requirement def`** name after `satisfy`.
- **Trees:** Prefer one parent theme id with derived/refined children over parallel flat peers for the same concern (e.g. plant setup → sticky DHCP / ordered steps / power-cycle recovery).
- **Outputs:** After model change, sync **`outputs/**/10-requirements-traceability.md`** (parent/child + satisfy matrix).
- **Rename gate:** Grep / Read live `.sysml`, then use Cursor **`user-sysml-v2` MCP** `getReferences` on the loaded file or code before deleting or renaming.
