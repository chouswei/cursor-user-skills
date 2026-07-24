# SysML MemNet snap — canonical procedure (user pack)

Authoritative MemNet-first rules for `sysml-v2-models/projects/<slug>/`. Pair with [sysml-memnet-patterns.md](sysml-memnet-patterns.md), [sysml-memnet-cookbook-bridge.md](sysml-memnet-cookbook-bridge.md), and [mcp-memnet](../../mcp-memnet/SKILL.md).

## Three stores — one authority each

| Store | Authority for | Agent rule |
|-------|---------------|------------|
| `models/*.sysml` | Structure, syntax, satisfy links | Edit here first. Validate with `mcp-sysml-v2`. |
| `memnet serve` | Symbol index, locators, rationale, backlog | `query_warm` before edit; `add`/`update` after validate. |
| `AGENT-CONTEXT.md` | Human stub only | Session id + anchor only. Never duplicate topology/backlog. |

**Snap** = batch `add` of atomised `@TAG:` rows. Do **not** paste snap contents into chat.

## Mandatory turn sequence (6 steps)

| Step | Action | MemNet |
|------|--------|--------|
| **1** | `serve_status`. If `running: false` → edit `.sysml` only; skip 2 and 6. | — |
| **2** | `query_warm(anchor=TSK_model_<short>, depth=2, max_rows=50)`. | **READ** |
| **3** | Locate symbol (§Locate). Edit `models/*.sysml`. | — |
| **4** | `mcp-sysml-v2 validate`. Fix until pass. | — |
| **5** | `sysml-view-doc-sync` **iff** outputs exist and structure changed. For **`system-design-report/`** packs → also MemNet report delta per [memnet-report-pipeline.md](../../system-design-report-generator/references/memnet-report-pipeline.md) when serve up. | — |
| **6** | MemNet delta (§Delta write) + **pipeline settle** (§Pipeline wire). Required when step 4 changed symbols/traceability. | **WRITE** |

### Pipeline wire (steps 1–6)

After each step when `serve_status` is true, `add`/`update` one `@CLM` type=`pipe` row (`sN:payload`) under `TSK_turn_*`; settle turn when done. Full template: [sysml-memnet-pipeline.md](sysml-memnet-pipeline.md). **Do not** keep pipeline step state only in chat when serve is up (use wire rows; plain Markdown only when serve is down).

### Warm miss

- No `@TSK` for project anchor
- `@TSK` exists but zero `@PRT`/`@SYM` for non-greenfield project
- Wrong session / empty graph

**On warm miss:** run §Initial snap once, then continue from step 3. If graph uses legacy `@PARTD`/`@PORTD`/`@BEHD`/`@TASK` → re-snap with unified tags.

### Step 6 skip (only)

| Case | Skip? |
|------|-------|
| Comment/whitespace only | Yes |
| `serve_status` false | Yes (note stale) |
| User question only; no `.sysml` edit | Yes |
| Any new/renamed symbol, port, connection, req, satisfy, allocate, behaviour | **No** |

## Identity and locators

### Stable keys

| Tag | Pattern |
|-----|---------|
| `@TSK` | `TSK_model_<short>` |
| `@PRT` | `PRT_<name>` |
| `@POR` | `POR_<name>` |
| `@CON` | `CON_<linkName>` |
| `@BEH` | `BEH_<name>` |
| `@ITM` | `ITM_<name>` |
| `@REQ` | `REQ_<requirementId>` |
| `@MOD` | `MOD_<file_slug>` |
| `@SYM` | `SYM_<name>` |
| `@CONV` | `CONV_<topic>` |
| `@DEC` | `DEC_<nn>` |
| `@ISSUE` | `ISS_<nn>` |

### Ephemeral locator

- `@SYM`: `path|line|kind|owner`
- **`line` is a hint.** Stable identity = **`name` + `path`**.

### `session_open` map

Use the **full canonical map** in [sysml-memnet-patterns.md](sysml-memnet-patterns.md) — 19 tags including `@POR`, `@BEH`, `@ITM`, `@CONV`, `@DEC`, `@ISSUE`.

### Example edges

```text
@EDG: E…|PRT_edgePc|declaredIn|PKG_FoamLiteVer2Deploy||persistent
@EDG: E…|SYM_edgePc|inFile|MOD_deploy_vfdl2|loc|persistent
@EDG: E…|PRT_edgePc|hasPort|POR_ethernet||persistent
@EDG: E…|POR_ethernet|typedBy|POR_EthernetPort||persistent
@EDG: E…|PRT_edgePc|satisfies|REQ_VFDL2-MQTT-RELAY||persistent
```

## Locate before edit (step 3)

**Read policy:** [sysml-memnet-read-policy.md](sysml-memnet-read-policy.md) — per-turn budget, anti-patterns, decision tree.

1. `query_warm` on `@PRT_*` / `@POR_*` / `@REQ_*` / `@CON_*` / `@SYM_*` → `path`, `name`, `line`, link ends
2. **Only if editing:** `Read(path, offset=line-12, limit=35)` — not full file
3. Window miss → `Grep` exact name scoped to `path` from `@MOD_*`
4. Still ambiguous → `mcp-sysml-v2` `getDefinition` or `getSymbols` (not bulk Read)
5. Grep/LSP line ≠ stored line → `update` `@SYM.line` (self-heal)

**MUST NOT** open `deploy-*.sysml` without `@SYM.line` or validate error when `serve_status` is true and warm hit.

## Line drift (after edit)

| When | Action |
|------|--------|
| Before edit | Stored line as hint; grep if window miss |
| After validate (step 6) | Re-grep every `@SYM.name` under touched `@MOD`(s) → batch `update` lines |
| Multi-file edit | Refresh locators per touched file only |
| Large refactor in one file | Re-grep whole file → batch `update` all `@SYM` for that `@MOD` |

## Delta write (step 6)

| `.sysml` change | MemNet write |
|-----------------|--------------|
| New/changed part | `@PRT` + `@SYM` + EDGs (`declaredIn`, `inFile`) |
| New/changed port | `@POR` + `@SYM` + `hasPort` + optional `typedBy` |
| New/changed connection | `@CON` + `@SYM` + EDGs |
| New/changed requirement | `@REQ` + `@SYM` |
| satisfy / allocate in root or deploy | `@EDG` `satisfies` / `allocates` only |
| Behaviour edit | `@BEH` + `@SYM` |
| Item / flow | `@ITM` + `@EDG` `flowOf` |
| User chose between options | `update` `@DEC.chosen`; settle `@DEC` |
| New convention | `@CONV` + `constrained_by` |
| Open backlog | `@ISSUE` or `@CLM` assumption |
| Any touched file | Re-grep all `@SYM.name` under that `@MOD` → batch `update` line |

**Batch rule:** new `@PRT`/`@POR`/`@CON` **MUST** include `declaredIn` + `inFile` in the **same** `add`/`update`.

Do **not** store full `.sysml` text or paragraph prose in any `@TAG` row.

## Initial snap (warm miss only)

1. `session_open` with full canonical map from [sysml-memnet-patterns.md](sysml-memnet-patterns.md)
2. `Glob` `sysml-v2-models/projects/<slug>/models/*.sysml`
3. Per file — grep by role:

| File pattern | Grep / extract → MemNet |
|--------------|-------------------------|
| `deploy-*.sysml` | `part def`, `^\s*part\s+\w+`, `port def`, nested ports, top-level usages |
| `connections-*.sysml` | `connection def`, `connect `, `link\w+` |
| `requirements-*.sysml` | `requirement def`, `requirementId` |
| `behaviour-*.sysml` | `state def`, `action def`, `perform action`, transitions |
| `root-*.sysml` | imports → `@PKG` kind=`root`; **`satisfy`** → `@EDG` satisfies |
| any file | `item def`, `flow of`, `allocate` |

4. Per file: one `@MOD` + N `@SYM` (with line) + semantic `@PRT`/`@POR`/`@CON`/`@REQ`/`@BEH`/`@ITM` + `@EDG`
5. One `add` batch 30–80 lines
6. `query_warm(anchor=TSK_model_<short>, depth=2)` to confirm
7. Write thin `AGENT-CONTEXT.md` if missing

## Session `.snap` file

Graph persistence **MUST** use MemNet server-side save/load:

```text
memnet session save --file <project>.snap
memnet session load --file <project>.snap
```

Agents **MUST NOT** paste `.snap` contents into chat. After load: `query_warm(TSK_model_*)` only.

Optional store path: `sysml-v2-models/projects/<slug>/.memnet/<slug>.snap` (not required in repo).

## AGENT-CONTEXT.md contract

Max 40 lines:

```markdown
# Agent context — <slug>
**MemNet session:** `<mn_…>` · **Anchor:** `TSK_model_<short>`
## Summary
<5–10 lines human overview>
## MemNet
Query `TSK_model_<short>` — do not duplicate topology/backlog here.
```

| Content | Store in |
|---------|----------|
| Session id, anchor, short summary | `AGENT-CONTEXT.md` |
| Topology, backlog, req trace | MemNet `@SEC`/`@CLM`/`@REQ`/`@ISSUE` |
| Symbol names, paths, line hints | MemNet `@SYM`/`@MOD`/`@POR`/`@BEH` |

## Incremental re-snap (after edits)

Same pattern as [memnet-codebase-snap](../../memnet-codebase-snap/SKILL.md): `update` affected `@SYM` rows; never duplicate ids.
