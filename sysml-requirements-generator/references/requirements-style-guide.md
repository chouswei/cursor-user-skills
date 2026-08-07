# Requirements package -- style (repo)

- **File:** `requirements-<projectfolder>.sysml`
- **Package:** `<Project>PascalCaseRequirements` (e.g. `SysmledgraphRequirements`)
- **Import:** `private import ScalarValues::String` when using `requirementId : String`
- **Each requirement:** `requirement def Name { attribute requirementId : String = "R#"; doc /* normative text; prefer SHALL for mandatory */ }`
- **Hierarchy:** Prefer **refine** / **derive** so child defs specialise a parent theme (parent id family → child requirementIds). Do not grow a flat list when a parent already owns the theme (commissioning, power-cycle, LAN isolation, etc.).
- **Doc:** Use `doc /* ... */` per [common-library-naming-detailed.md](../../sysml-common-lib-contribution/references/common-library-naming-detailed.md) section 8. Cross-cite related requirementIds in doc for operator clarity; structural parentage stays in refine/derive.
- **Satisfy:** On design elements in **deploy** (or behaviour); import requirements package there.
- **Patterns (generic):** sticky MAC reservation; ordered commissioning steps; multi-edge join / per-site bands -- state as patterns, not hard-coded site addresses in shared skill stubs.
- **Do not** duplicate requirement text only in Markdown without updating the model; sync **`outputs/**/10-requirements-traceability.md`** after model change.
