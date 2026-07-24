# Traceability patterns (repo)

| Link | Typical syntax | Where |
|------|----------------|--------|
| Requirement → design | `satisfy ReqName;` inside `part def` / on usage | deploy package; imports requirements |
| Software → hardware | `allocate partUsage to partUsage;` | deployment composite in deploy |
| Refinement | `derive req` / refinement (project-specific; follow OMG examples if used) | requirements or deploy |

- **Imports:** Deploy file needs `private import …Requirements::*` for `satisfy`.
- **Naming:** Use exact **`requirement def`** name after `satisfy`.
- **sysmledgraph:** Query “who references ReqX” before deleting or renaming.
