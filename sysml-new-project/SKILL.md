---
name: sysml-new-project
description: >-
  Scaffold a new SysML v2 project under sysml-v2-models/projects/: folder layout, config.yaml,
  model files (connections, requirements, deploy, behaviour, root), READMEs, and repo index updates.
  Triggers: new project, create project, add project, scaffold project, new sysml project, start a project folder.
metadata:
  pattern: pipeline
  domain: sysml-v2
  version: "1.2"
  product: "package 0.19.2; PyPI wheel 0.19.0"
  pairs_with: [sysml-root-config, sysml-requirements-generator, sysml-modeling-session-checklist, sysml-memnet-cache, sysml-memnet-documentation, mcp-memnet, sysml-v2-lsp-mcp, project-planner]
token_guardrails: |
  - Ask for project slug, one-line purpose, and requirement ID prefix before bulk generation unless user gave them.
  - Use an existing project config.yaml as OMG Kernel template; do not invent library paths.
  - After scaffold: validate project load; update indexes; commit/push only when user asks.
  - When serve_status true at scaffold: create AGENT-CONTEXT stub + MemNet session skeleton (steps 11–12).
---

# SysML new project

**When:** Greenfield **`sysml-v2-models/projects/<slug>/`** — not fixing load order only (**sysml-import-order-helper**) or root/config drift only (**sysml-root-config**).

**Pairing:** In **weft.Projects**, hub **`.cursor/skills/sysml-v2-modeling`** + this skill for scaffold; elsewhere **sysml-modeling-workflow** + this skill. Use **one** specialist after (e.g. **sysml-requirements-generator**, **sysml-connections**) for content depth.

## Before you scaffold

Confirm with the user (or infer from the request):

| field | rule |
|-------|------|
| `slug` | kebab-case folder e.g. `delta-datacentre-heat-exchange-unit-test-bench` |
| `purpose` | One sentence for README and config comment |
| `req_id_prefix` | Project-specific e.g. `DDCHXU-R1` not generic `R1` unless agreed |
| `package_prefix` | Short PascalCase e.g. `DeltaDCHXU` for `DeltaDCHXUConnections` etc. |
| `libs_common` | Only if deploy uses NI catalog or shared ports `sbrio-9651-carrier-board`; else Kernel+ISQ/SI `temperature-iv-curve` |
| `hardware` | Optional `hardware/<slug>/` via repo `hardware-custom-pcba-workflow` when PCBA in scope (weft.Projects) |
For ambiguous scope or a roadmap, run **project-planner** first or state planning **skipped** per **sysml-modeling-session-checklist**.

## Pipeline

Copy this checklist and track progress:

```
- [ ] 1. Create project folder + models/ + outputs/
- [ ] 2. config.yaml (OMG chain + project model_files, root last)
- [ ] 3. connections-*.sysml (if deploy has links)
- [ ] 4. requirements-*.sysml (optional but typical)
- [ ] 5. deploy-*.sysml (parts + system composite)
- [ ] 6. behaviour-*.sysml (optional)
- [ ] 7. root-*.sysml (imports only)
- [ ] 8. Project README + outputs/README.md
- [ ] 9. Repo indexes (projects/README, root README, docs/DOCS_INDEX)
- [ ] 10. Validate / visualize smoke test
- [ ] 11. AGENT-CONTEXT.md (thin stub — when MemNet or multi-session design expected)
- [ ] 12. MemNet session_open + skeleton @TSK + @MOD rows (when serve_status true)
```

### 1. Folder layout

```
sysml-v2-models/projects/<slug>/
├── config.yaml
├── README.md
├── models/
│   ├── connections-<slug>.sysml   # if needed
│   ├── requirements-<slug>.sysml
│   ├── deploy-<slug>.sysml
│   ├── behaviour-<slug>.sysml     # optional
│   └── root-<slug>.sysml          # always last in config
└── outputs/
    └── README.md
```

**File names:** lowercase, hyphens; prefix matches slug: `deploy-<slug>.sysml`.

### 2. config.yaml

- Copy **`model_files`** OMG block from **temperature-iv-curve** or **delta-datacentre-heat-exchange-unit-test-bench** `config.yaml`.
- Set top comment to project purpose.
- List project files in dependency order; **`root-<slug>.sysml` last** ([load-order](~/.cursor/skills/sysml-root-config/references/load-order.md)).

Typical order: `connections` → `requirements` → `deploy` → `behaviour` → `root`.

### 3–7. Model files

| file | skill |
|------|-------|
| `connections-*` | `sysml-connections` / `sysml-software-port-generator` / `sysml-physical-port-generator` |
| `requirements-*` | `sysml-requirements-generator` |
| `deploy-*` | `sysml-hardware-part-generator` / `sysml-software-part-generator` / `sysml-nested-structure-modeling` |
| `behaviour-*` | `sysml-behaviour-generator` |
| `root-*` | `sysml-root-config` stub `assets/root-package-stub.sysml` |
**Root package** imports all project packages; no deploy logic in root.

**satisfy:** Add on system **`part def`** only after requirement defs exist and names are agreed.

### 8. READMEs

- **Project README:** purpose, model file table (file → package), validate commands, req ID table if any.
- **outputs/README.md:** model-first note, `visualize.py --project <slug>` example, pointer to **sysml-view-doc-sync**.

Do **not** put project docs under repo `docs/` when the workspace defines **sysml-docs-outputs** (e.g. weft.Projects `.cursor/rules/sysml-docs-outputs.mdc`).

### 9. Repo indexes

Add one row each to:

- `sysml-v2-models/projects/README.md`
- Repo root `README.md` (projects table + optional “Key docs” subsection)
- `docs/DOCS_INDEX.md` (sysml-v2-models project list sentence)

Match existing table style; link to `projects/<slug>/README.md`.

### 10. Verify

From `sysml-v2-models/` (venv + OMG submodule):

```bash
python scripts/visualize.py --project <slug> --diagram bdd --format svg
```

Or **sysml-v2-lsp-mcp** / **mcp-sysml-v2** **validate** on edited files (repo may use **sysml-v2-lsp-mcp** under `.cursor/skills/`).

**sysmledgraph:** After substantial scaffold, user may run `npm run sysmledgraph:analyze` at repo root.

### 11. AGENT-CONTEXT.md (required when MemNet-assisted or multi-session design)

Create `AGENT-CONTEXT.md` at project root per [sysml-memnet-snap.md](../sysml-memnet-documentation/references/sysml-memnet-snap.md#agent-contextmd-contract). Max 40 lines:

```markdown
# Agent context — <slug>
**MemNet session:** `<mn_…>` · **Anchor:** `TSK_model_<short>`
## Summary
<purpose one sentence + 5–10 line human overview as design grows>
## MemNet
Query `TSK_model_<short>` — do not duplicate topology/backlog here.
```

Derive `<short>` from slug (e.g. `vedan-foam-detection-lite-ver2` → `vfdl2`). Record session id after step 12.

### 12. MemNet skeleton (required when MemNet is up at scaffold)

1. `serve_status` -- if false, skip; complete step 11 with placeholder session.
2. `session_open` with coding/SysML kinds enabled (see [sysml-memnet-patterns.md](../sysml-memnet-documentation/references/sysml-memnet-patterns.md) for field notes).
3. `mutate` skeleton (openCypher-shaped; leftover `add` / `id:'NEW'` named leftover):

```cypher
CREATE (t:TSK {goal: $purpose, phase: 'model', status: 'in_progress', recycle: 'persistent'})
CREATE (m1:MOD {path: 'models/deploy-<slug>.sysml', role: 'deploy', status: 'active', recycle: 'persistent'})
CREATE (m2:MOD {path: 'models/root-<slug>.sysml', role: 'root', status: 'active', recycle: 'persistent'})
MATCH (t:TSK {goal: $purpose}), (m1:MOD {path: 'models/deploy-<slug>.sysml'})
CREATE (t)-[:OWNS {note: 'scope', recycle: 'persistent'}]->(m1)
```

Add MOD for each other `models/*.sysml` created. Store returned `session_id` in `AGENT-CONTEXT.md` and optionally `MEMNET_SESSION` in mcp.json.

## Optional follow-ups

| need | skill |
|------|-------|
| system design report `outputs/` | `system-design-report-generator` / `sysml-view-doc-sync` |
| custom PCBA `hardware/` | `hardware-custom-pcba-workflow` (weft.Projects repo skill) |
| shared part `libs/common/` | `sysml-common-lib-contribution` |
## Rename later

Use **`git mv`** for folder and `*-*.sysml` files; update `config.yaml`, README paths, and indexes in one commit.

## Reference

- File manifest and naming examples: [references/new-project-checklist.md](references/new-project-checklist.md)
- Load order detail: [sysml-root-config/references/load-order.md](~/.cursor/skills/sysml-root-config/references/load-order.md)
