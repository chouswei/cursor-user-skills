# Requirements package — style (repo)

- **File:** `requirements-<projectfolder>.sysml`
- **Package:** `<Project>PascalCaseRequirements` (e.g. `SysmledgraphRequirements`)
- **Import:** `private import ScalarValues::String` when using `requirementId : String`
- **Each requirement:** `requirement def Name { attribute requirementId : String = "R#"; doc /* normative text; prefer SHALL for mandatory */ }`
- **Doc:** Use `doc /* ... */` per [common-library-naming-detailed.md](../../sysml-common-lib-contribution/references/common-library-naming-detailed.md) §8
- **Satisfy:** Declared on design elements in **deploy** (or behaviour) that implement the requirement; import requirements package there
- **Do not** duplicate requirement text only in Markdown without updating the model
