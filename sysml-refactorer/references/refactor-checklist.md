# SysML refactor checklist

Use as a **lint list** during **sysml-refactorer** runs. Not every item applies to every refactor.

## Before editing

- [ ] Old symbol names and **all** spellings (qualified vs short) noted for grep.
- [ ] **sysmledgraph** indexed for the roots that contain the model (`sysml-v2-models/libs/common`, `sysml-v2-models/projects/...`).
- [ ] **Consumers:** every `config.yaml` that loads the changed package(s) identified.

## Edit layers (typical order)

1. **Kernel / OMG libs** — rarely changed; never reorder without **sysml-root-config** awareness.
2. **libs/common** — `parts/`, `connections/`, `composites/`; check **load order** in project `config.yaml` if new files or splits.
3. **SharedConnections** — `connection def` end port types affect **every** deploy using them.
4. **Project** — `connections-*.sysml`, `deploy-*.sysml`, `behaviour-*.sysml`, `requirements-*.sysml`.
5. **Scripts / YAML** — pin maps, `mappings/*.yaml`, `exam_model` assumptions (rare).

## De facto / physical port migrations

- [ ] **Part `doc`** states physical meaning and **site convention** (what deploy maps where).
- [ ] **No** mixed role + physical ports on the same COTS class without explicit **`doc`** rationale ([de-facto-modeling.md](../../sysml-traceability/references/de-facto-modeling.md)).
- [ ] **Connection def** ends use **`EthernetPort`** (or shared supertypes) when multiple concrete port types must connect.

## After editing

- [ ] **SysML v2 MCP validate** on changed sources (or merged snippet if single-document validate).
- [ ] **exam_model.py** run for **each** affected project name (e.g. `vedan-foam-detection`).
- [ ] **Grep** for stale strings (old port names, old `connection` end paths).
- [ ] **outputs/*.md** updated if the repo treats them as model-derived views.

## Optional

- [ ] **`ibd.py`** connection label map for PNG/Mermaid IBD readability.
- [ ] **sysmledgraph** **clean** + re-**indexDbGraph** only when the tool policy allows (see **mcp-sysmledgraph**).
