# Common lib split — checklist

Use when adding a **sibling** `.sysml` under `libs/common/` (see [scale-policy.md](../references/scale-policy.md)).

- [ ] **Name** — New `snake_case.sysml` + **one** new top-level **PascalCase** package (or documented exception).
- [ ] **Boundary** — Subdomain is **cohesive** (not “first N lines”).
- [ ] **Load order** — New file inserted in **`model_files`** after its dependencies, before consumers ([libs/common/README.md](../../../../sysml-v2-models/libs/common/README.md)).
- [ ] **Every project** — All `sysml-v2-models/projects/*/config.yaml` that load common: updated.
- [ ] **Imports** — `private import` / qualified types fixed in common + projects.
- [ ] **Docs** — `libs/common/README.md`; `parts/README.md` if under `parts/`.
- [ ] **IMD / network / Poe edge** — If touched, [workspace-imd-lib-conventions.md](../../sysml-common-lib-contribution/references/workspace-imd-lib-conventions.md).
- [ ] **Validate** — SysML v2 MCP **validate** on changed files + **full** project load (≥1 project).
