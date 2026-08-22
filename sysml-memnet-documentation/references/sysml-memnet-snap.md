# SysML MemNet snap -- canonical procedure (user pack)

**Wire:** agent mutate/read uses MemNet **GQL / shaped pin_map** ([memnet-format](../../memnet-format/SKILL.md)). Emit openCypher-shaped statements on the wire -- not pipe `@TAG` rows. Thin bridge: [sysml-gql](../../sysml-gql/SKILL.md).

Authoritative MemNet-first rules for SysML project roots. Pair with [sysml-memnet-patterns.md](sysml-memnet-patterns.md), [sysml-memnet-cookbook-bridge.md](sysml-memnet-cookbook-bridge.md), and [mcp-memnet](../../mcp-memnet/SKILL.md).

**Model root (pick one; do not mix):**

| Layout | Root | Snap dir |
|--------|------|----------|
| Multi-project pack | `sysml-v2-models/projects/<slug>/` | `.../projects/<slug>/.memnet/` |
| System repo (`modelbasedPrj-*`) | `sysml-models/` | `sysml-models/.memnet/` |

Copy the live root from repo `AGENTS.md`. **This MemNet repo:** `sysml-models/`.

## Three stores -- one authority each

| Store | Authority for | Agent rule |
|-------|---------------|------------|
| `<model-root>/models/*.sysml` | Structure, syntax, satisfy links | Edit here first. Validate the textual model. |
| MemNet (MCP) | Symbol index, locators, rationale, backlog | cue `pin_map` before edit; **`mutate`** after validate. leftover `add`/`update` named leftover. |
| `AGENT-CONTEXT.md` | Human stub only | Catalog session id + campaign cue. Never duplicate topology/backlog. |

**Snap** = Path-B `ingest_sysml` (into **this** session, 1->1) and/or catalog `snap_model`, then sparse **`mutate`**. Do **not** paste snap contents into chat. Do **not** smash ingest, Snap, and docs into one undifferentiated session when a nest applies -- [memnet-nested-sessions](../../memnet-nested-sessions/SKILL.md).

## Nested sessions (SysML delta)

Procedure SSOT: [memnet-nested-sessions](../../memnet-nested-sessions/SKILL.md). Multitask: [memnet-multitask](../../memnet-multitask/SKILL.md). Tools: [mcp-memnet](../../mcp-memnet/SKILL.md).

| Fact | Rule |
|------|------|
| Campaign cue | `:TSK` `goal=TSK_model_<short>` from repo `AGENTS.md`. Not a second session-id scheme. |
| Catalog | `snap_model` on the model root -- interiors carry locators `session=` + `qname=` |
| Path-B | `ingest_sysml` into the **current** interior (1->1). Not Snap. Not export. |
| This generate | One `pin_map`; MCP `session=` for **this** cut. Drop the prior map next turn. |
| Join | `import_slice` of a neighbourhood -- not a second Snap, not a paste of the nested tree |
| Already built | Reuse existing `session=` for that `qname=`. Do not Snap a twin. |
| Parent shell unclear | Serial: name the shell first. Parallel interiors only when children already have `session=` -- then one `TSK_*` per interior ([memnet-multitask](../../memnet-multitask/SKILL.md), TCP/HTTP). |
| `snap_model` hits session cap | MUST NOT ignore. `housekeep_stats`; settle stale `TSK_*`; cut further interiors. MUST NOT clip `max_rows` and call it Shape. If still capped: stop and report -- MUST NOT flatten leftover files into the current session. |

## Mandatory turn sequence (6 steps)

| Step | Action | MemNet |
|------|--------|--------|
| **0** | MemNet MCP in catalog? If no -> edit `.sysml` only; skip 1-2 and 6. Plain Markdown (no TOON/TRON). | -- |
| **1** | `serve_status` when TCP / unsure. If `running: false` -> edit `.sysml` only; skip 2 and 6. Skip this probe only under single-agent in-process. Multitask **MUST** TCP/HTTP -- MUST NOT in-process. | -- |
| **2** | Catalog: `pin_map(kind='TSK', locators=['goal=TSK_model_<short>'], depth=2, max_rows=50)`. If that pin carries `session=` for the cut under edit: **next generate** `pin_map(..., session=<interior>)` -- one map per generate. leftover `anchor=` / `id=` named leftover. | **READ** |
| **3** | Locate symbol (section Locate). Edit `models/*.sysml`. | -- |
| **4** | Validate (`mcp-sysml-v2` until pass, or the project's SysML CLI). | -- |
| **5** | Sync `outputs/` **iff** structure changed (`sysml-view-doc-sync`; interconnection figures: pack `sysml-interconnection-mermaid` before fenced Mermaid). | -- |
| **6** | MemNet delta (section Delta write) + **pipeline settle** (section Pipeline wire). Required when step 4 changed symbols/traceability. | **WRITE** |

### Pipeline wire (steps 1-6)

After each step when MemNet is up, **`mutate`** one `:CLM` with `type='pipe'` and `code='sN:payload'` under `TSK_turn_*`; settle turn when done. Full template: [sysml-memnet-pipeline.md](sysml-memnet-pipeline.md).

### Warm miss

- No `:TSK` for project anchor
- `:TSK` exists but zero `:PRT` / `:SYM` for non-greenfield project
- Wrong session / empty graph
- Snap/wire `path=` still cites a root that does not exist in the workspace (e.g. legacy `sysml-v2-models/...` under a `sysml-models/` system repo)

**On warm miss:** run section Initial snap once, then continue from step 3. If graph uses legacy `PARTD` / `PORTD` / `BEHD` / `TASK` kinds -> re-snap with unified labels. If the catalog already exists but this interior is empty: Path-B `ingest_sysml` into **that** `session=` only.

### Step 6 skip (only)

| Case | Skip? |
|------|-------|
| Comment/whitespace only | Yes |
| MemNet MCP missing / `serve_status` false | Yes (note stale) |
| User question only; no `.sysml` edit | Yes |
| Any new/renamed symbol, port, connection, req, satisfy, allocate, behaviour | **No** |

## Identity and locators

### Cue properties (not a store key)

House tokens such as `TSK_model_<short>` live in **`goal`** (or `name` / `qname` / `path` / `requirementId`). GraphElement is identity. leftover nickname `id` is leftover.

| Label | Cue on | Example |
|-------|--------|---------|
| `:TSK` | `goal` | `goal=TSK_model_vfdl2` |
| `:PRT` / `:POR` / `:CON` / `:BEH` / `:ITM` | `name` | `name=edgePc` |
| `:REQ` | `requirementId` | `requirementId=VFDL2-MQTT-RELAY` |
| `:MOD` | `path` | `path=models/deploy-vfdl2.sysml` |
| `:SYM` | `name` + `path` | `name=edgePc` |
| `:PKG` | `qname` | `qname=...FoamLiteVer2Deploy` |
| `:CONV` / `:DEC` / `:ISSUE` | `topic` / `code` | `DEC` by question; `ISSUE` by `code` |

### Ephemeral locator

- `:SYM` props: `path`, `line`, `kind`, `owner`
- **`line` is a hint.** Stable identity = **`name` + `path`**.

### `session_open` map

Use the **full canonical map** in [sysml-memnet-patterns.md](sysml-memnet-patterns.md) -- 19 kinds including `POR`, `BEH`, `ITM`, `CONV`, `DEC`, `ISSUE`.

### Example edges

```cypher
CREATE (:PRT {name: 'edgePc'})-[:declaredIn]->(:PKG {qname: 'FoamLiteVer2Deploy'})
CREATE (:SYM {name: 'edgePc'})-[:inFile {note: 'loc'}]->(:MOD {path: 'models/deploy-vfdl2.sysml'})
CREATE (:PRT {name: 'edgePc'})-[:hasPort]->(:POR {name: 'ethernet'})
CREATE (:POR {name: 'ethernet'})-[:typedBy]->(:POR {name: 'EthernetPort'})
CREATE (:PRT {name: 'edgePc'})-[:satisfies]->(:REQ {requirementId: 'VFDL2-MQTT-RELAY'})
```

## Locate before edit (step 3)

**Read policy:** [sysml-memnet-read-policy.md](sysml-memnet-read-policy.md) -- per-turn budget, anti-patterns, decision tree.

1. `pin_map` on `PRT_*` / `POR_*` / `REQ_*` / `CON_*` / `SYM_*` -> `path`, `name`, `line`, link ends
2. **Only if editing:** `Read(path, offset=line-12, limit=35)` -- not full file
3. Window miss -> `Grep` exact name scoped to `path` from `:MOD`
4. Still ambiguous -> Grep scoped to the `:MOD` path (not bulk Read)
5. Grep/LSP line != stored line -> `mutate` SET `SYM.line` (self-heal)

**MUST NOT** open `deploy*.sysml` without `SYM.line` or validate error when MemNet is up and warm hit.

## Line drift (after edit)

| When | Action |
|------|--------|
| Before edit | Stored line as hint; grep if window miss |
| After validate (step 6) | Re-grep every `SYM.name` under touched `MOD`(s) -> batch `mutate` SET lines |
| Multi-file edit | Refresh locators per touched file only |
| Large refactor in one file | Re-grep whole file -> batch `mutate` all `:SYM` for that `:MOD` |

## Delta write (step 6)

| `.sysml` change | MemNet write |
|-----------------|--------------|
| New/changed part | `:PRT` + `:SYM` + rels (`declaredIn`, `inFile`) |
| New/changed port | `:POR` + `:SYM` + `hasPort` + optional `typedBy` |
| New/changed connection | `:CON` + `:SYM` + rels |
| New/changed requirement | `:REQ` + `:SYM` |
| satisfy / allocate in root or deploy | rel only `satisfies` / `allocates` |
| Behaviour edit | `:BEH` + `:SYM` |
| Item / flow | `:ITM` + rel `flowOf` |
| User chose between options | `mutate` SET `DEC.chosen`; settle `:DEC` |
| New convention | `:CONV` + `constrained_by` |
| Open backlog | `:ISSUE` or `:CLM` assumption |
| Any touched file | Re-grep all `SYM.name` under that `:MOD` -> batch `mutate` SET line |

**Batch rule:** new `:PRT` / `:POR` / `:CON` **MUST** include `declaredIn` + `inFile` in the **same** `mutate`.

Do **not** store full `.sysml` text or paragraph prose on any graph row.

## Initial snap (warm miss only)

Greenfield / parent shell still invented: **serial**. Nested stack already named: catalog then interiors -- not one mutate dump of the whole tree.

1. `session_open` with full canonical map from [sysml-memnet-patterns.md](sysml-memnet-patterns.md) (catalog session).
2. Seed campaign `:TSK` `{goal: 'TSK_model_<short>'}` on the catalog if missing (`mutate`; no leftover NEW).
3. Prefer **`snap_model(root=<model-root>)`**. On session cap: Nested sessions table above -- do not flatten.
4. Else Path-B: **`ingest_sysml(path=...)`** into the interior for **this** generate (1 file or one qname cut). `Glob` `<model-root>/models/*.sysml` only to choose the next cut -- MUST NOT ingest the whole glob into one session when a nest applies.
5. Confirm: `pin_map` campaign cue on the catalog (outline if empty q). Next generate: `pin_map(session=<interior>)` for the cut under edit.
6. Write thin `AGENT-CONTEXT.md` if missing (catalog session id + campaign cue).

**Fallback** (no `snap_model` / `ingest_sysml` in catalog): grep-extract then `mutate` **into the current interior only** -- same per-file roles as before. One `mutate` batch 30-80 statements. MUST NOT use this fallback to merge interiors.

| File pattern | Grep / extract -> MemNet |
|--------------|-------------------------|
| `deploy*.sysml` | `part def`, `^\s*part\s+\w+`, `port def`, nested ports, top-level usages |
| `connections*.sysml` | `connection def`, `connect `, `link\w+` |
| `requirements*.sysml` | `requirement def`, `requirementId` |
| `behaviour*.sysml` | `state def`, `action def`, `perform action`, transitions |
| `root*.sysml` | imports -> `:PKG` kind=`root`; **`satisfy`** -> `:satisfies` |
| any file | `item def`, `flow of`, `allocate` |

Per file: one `:MOD` + N `:SYM` (with line) + semantic `:PRT` / `:POR` / `:CON` / `:REQ` / `:BEH` / `:ITM` + rels.

## Session `.snap` file

Graph persistence **MUST** use MemNet server-side save/load:

```text
memnet session save --file <project>.snap
memnet session load --file <project>.snap
```

Agents **MUST NOT** paste `.snap` contents into chat. After load: `pin_map` the campaign cue on the **catalog**; then `session=` for the interior.

Optional store path: `<model-root>/.memnet/<short>.snap` (not required in repo). For system repos this is typically `sysml-models/.memnet/`.

## AGENT-CONTEXT.md contract

Max 40 lines:

```markdown
# Agent context -- <slug>
**MemNet session:** `<mn_...>` (catalog) * **Anchor:** `TSK_model_<short>`
## Summary
<5-10 lines human overview>
## MemNet
Query `TSK_model_<short>` then `session=` for the cut -- do not duplicate topology/backlog here.
```

| Content | Store in |
|---------|----------|
| Session id (catalog), campaign cue, short summary | `AGENT-CONTEXT.md` |
| Topology, backlog, req trace | MemNet `:SEC` / `:CLM` / `:REQ` / `:ISSUE` |
| Symbol names, paths, line hints | MemNet `:SYM` / `:MOD` / `:POR` / `:BEH` |

## Incremental re-snap (after edits)

Same pattern as [memnet-codebase-snap](../../memnet-codebase-snap/SKILL.md): `mutate` affected `:SYM` rows; MATCH by `name`+`path`, do not mint leftover `id`.
