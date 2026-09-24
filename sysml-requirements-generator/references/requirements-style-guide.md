# Requirements package -- style (repo)

- **File:** `requirements-<projectfolder>.sysml` (house default path: `sysml-models/models/requirements.sysml` when the open repo `AGENTS.md` says so)
- **Package:** `<Project>PascalCaseRequirements` (e.g. `SysmledgraphRequirements`)
- **Import:** `private import ScalarValues::String` when using `requirementId : String`
- **Each requirement:** `requirement def Name { attribute requirementId : String = "R#"; doc /* normative text; prefer SHALL for mandatory */ }`
- **Hierarchy:** Prefer **nested requirement usages** under a parent usage (parent id family -> child requirementIds). Use SysML **refine** / **derive** only when the live project already uses those edges. MUST NOT invent refine/derive as the default. Doc prose that says "refines" is NOT a SysML refine edge.
- **Doc:** Use `doc /* ... */` per [common-library-naming-detailed.md](../../sysml-common-lib-contribution/references/common-library-naming-detailed.md) section 8. Cross-cite related requirementIds in doc for operator clarity; structural parentage stays in nested usages (or refine/derive when those edges exist).
- **Long doc (MUST):** Model `.sysml` `doc` is SSOT. Parent `doc` SHALL stay short (purpose; SHALL / SHALL NOT list; pointers to nested requirementIds). Long prose MUST live on nested children -- one topic each (e.g. I/V sense; isolation; PHY; PSU; first-principles); labelled sections belong on that child. MUST NOT treat seven labelled headings in one parent `doc` as done. MUST NOT invent peer-equipment or crate rail volts as SHALLs (catalog 24 V is not filament or lane power); unmodelled volts stay TBD. MUST NOT duplicate a child SHALL on the parent. Wiki / `outputs/` MUST summarise and cite nested requirementIds -- MUST NOT copy parent or child novels (see **sysml-view-doc-sync**).
- **Satisfy:** Default on the parent usage / theme part in **deploy** (or behaviour). Per-nested-usage satisfy only when the user maps each child. Nested usage alone does not create satisfy. Import requirements package there.
- **Domain (filament / RS-485):** `I_heat` is heating current -- MUST NOT call it emission. VacuumRs485Lane is digital PSU / control -- MUST NOT treat as MKS unless modelled.
- **Patterns (generic):** sticky MAC reservation; ordered commissioning steps; multi-edge join / per-site bands -- state as patterns, not hard-coded site addresses in shared skill stubs.
- **Do not** duplicate requirement text only in Markdown without updating the model; sync **`outputs/**/10-requirements-traceability.md`** after model change.
