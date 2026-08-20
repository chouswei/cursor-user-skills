---
name: mcp-memnet
description: >-
  MemNet MCP tools: cue then pin_map, GQL mutate, session, ingest, snap_model,
  export_pin_map. Triggers: memnet mcp, MCP pin_map, MCP mutate,
  session_open, session_close, session_list, find, ingest_sysml, snap_model,
  export_pin_map, reserve, RSV.
metadata:
  pattern: tool-wrapper
  version: "7.4"
  domain: memnet
  product: "memnet-llm==0.19.3"
token_guardrails: |
  - Product read is pin_map from a cue (kind / locators / keyword / session). leftover anchor= is leftover.
  - Product write is mutate (CREATE/MERGE/SET/DELETE). leftover add/update / id:'NEW' are leftover facades.
  - Parse envelope stdout. Wire SSOT: memnet-format + MemNet docs/grammar/gql-wire-profile.md.
---

# MemNet MCP (user pack)

**Use** MemNet via MCP. Doctrine SSOT: MemNet `docs/SHAPE.md`, `docs/LLM-GUIDE.md`, `docs/ROADMAP.md`. Wire: [memnet-format](../memnet-format/SKILL.md). Nested interiors: [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md). Hub: [memnet-use](../memnet-use/SKILL.md).

**Package and PyPI 0.19.3** (Hatch / `project.toml` / `memnet.__version__`; tag `v0.19.3`; extras **0.10-0.19** unchanged). **Install:** `pip install memnet-llm` or `pip install memnet-llm==0.19.3`. Extras `[mcp]`, `[agensgraph]`, `[neo4j]` are **drivers only**. **1.0** stays unclaimed (1.0 = claim of 0.5-0.8). CLI `memnet`. Novel-writer is out of scope. Arg **`session`** (not `session_id`). GraphGlot is parse-front only. Default `max_sessions` **1024**.

## User-pack transport (this machine)

| Role | Where |
|------|--------|
| **Cursor MCP** | HTTP `url` -> **`http://10.0.0.10:18766/mcp`** (streamable-http + Bearer) |
| **Pi graph store** | Prefer TCP `memnet serve` **`:18765`** with HTTP MCP `MEMNET_MCP_TRANSPORT=tcp` (same graph) |
| Local stdio `command` | Optional `memnet-local` only -- not the primary `memnet-pi` path |

Cursor `~/.cursor/mcp.json` -> primary server id **`memnet-pi`**. Shape matches Inventree-style `url` + `headers` (no local `command` / `env`). **InvenTree MCP is not MemNet** -- do not conflate.

```json
"memnet-pi": {
  "url": "http://10.0.0.10:18766/mcp",
  "headers": {
    "Authorization": "Bearer <token>"
  }
}
```

After editing mcp.json: **Cursor -> MCP / Tools -> restart `memnet-pi`**. Do **not** dual-run InProcess HTTP MCP against a separate TCP store without `MEMNET_MCP_TRANSPORT=tcp` on the Pi HTTP process.

## Doctrine (must)

| Idea | Meaning |
|------|---------|
| Product loop | `session_open(map)` then codebook **cue -> `pin_map`** + **`mutate`** (GQL Commit) |
| Empty q | **0.11 outline** (census of S), not a skip |
| GQL wire | openCypher-shaped statements in `wire_lines`; parse envelope `stdout` |
| leftover identity | leftover `--anchor` / `anchor=` / leftover id as identity -- not TARGET |
| leftover write | leftover-named `add`/`update`; leftover `id:'NEW'` / NEW mint -- not TARGET |
| Durable cabinet | Agens live claimed (0.7); **`liveNeo4jClaimed=true`** (0.14). Do not write hydrate-by-hid proven. Do not vendor a Neo4j/AgensGraph server. Agents MUST NOT talk Bolt. No `rag_query`. |
| HostSearch / Peak_L / export | **Shipped** extras 0.17 / 0.18 / 0.19 -- not Later |
| Transport | HTTP `:18766/mcp` -> Pi; bridge to TCP serve `:18765` when sharing one graph |

Always pass the same `session` id (or set `MEMNET_SESSION`). If ego unknown: **`find`** (`limit` required) then `pin_map` from labels+properties. Prefer **one live `TSK_*`**. When |Q|>1, CueConflict -- do not pick one root.

Formal shapes: [memnet-format](../memnet-format/SKILL.md) + MemNet `docs/grammar/`.

## Agent loop

```text
session_open(map) -> cue / find -> pin_map -> reason -> mutate -> pin_map
```

1. **Map** -- `session_open` needs `map_file` or `map_lines` else `no_map`. Missing kind -> `unknown_tag`. Bundled SCHEMA maps live in the MemNet checkout (`parts/common/memnet/memnet/examples/schema.*.example.txt`). This pack does not vendor those files.
2. **Cue** -- `kind` / locators (`qname=`, `path=`, ...) / `keyword` / nickname `cue`. Empty cue = outline. Prefer one live `TSK_*`.
3. **`pin_map`** -- one S per generate. MCP `session=` selects the stratum. Drop the prior map next turn. leftover `anchor=` / `anchors=` are leftover nicknames.
4. **`mutate`** -- sparse GraphElement `CREATE` / `MATCH`...`SET`/`DELETE`. No leftover `id:'NEW'` mint.
5. Persist if needed: `session_save` (file) or live cabinet (0.7 Agens / 0.14 Neo4j).

**MCP missing:** skip MemNet; plain Markdown only (no TOON/TRON).

## Product tools

| Tool | Role | Wire |
|------|------|------|
| `session_open` | Map required (`map_file` / `map_lines`) | SCHEMA registry; optional CREATE seed |
| `session_list` | Live ids plus `@STAT: sessions|n/max` (named strata; not ANN; default max **1024**) | text |
| `session_close` | Close that id (SessionLifecycle; does not dump S) | `@SESSION: ...|closed` |
| `session_save` / `session_load` / `session_current` | Snapshot / resume | file / metadata |
| `pin_map` | Primary read. Empty q = outline. `view=shell` is grain on a seed, not outline | shaped subgraph |
| `find` | Bounded seed (`limit` required). Not RAG | seed nodes |
| `mutate` | Product Commit | CREATE / MERGE / SET / DELETE |
| `snap_model` | One load tree -> catalog + interiors (`session=` + `qname=`) | locators |
| `ingest_sysml` / `ingest_codebase` / `ingest_pcba` / `ingest_skills` | Path-B locators into **this** session (1->1). Not Snap. Not export | locators; no leftover NEW |
| `export_pin_map` | Write out a cue `pin_map` as GQL. Not ingest. Not Absorb | shaped GQL |
| `import_slice` | Absorb a **slice** (not a whole S) | pattern match |
| `reserve` / `extend` / `release` | RSV; pass `llm_id` on mutate | `:RSV` present |
| `read_list` | Enumerate by kind / where | rows |
| `housekeep_stats` | Caps | stats |
| `session_acl_enable` / `session_acl_grant` / `session_acl_bind` | CapsPolicy **opt-in** (off by default). Not full `session_token` modes | ACL |
| `serve_status` | TCP probe | `{running,host,port}` |

**Not weird dialect -- transport envelope:** every tool except `serve_status` returns JSON `{exit_code, stdout, stderr, session_id, errors}`. Parse **`stdout`**. Do not treat JSON keys as the MemNet grammar.

## leftover (do not teach as product)

| Name | Status |
|------|--------|
| `add` / `update` | leftover facades; still registered. Prefer **`mutate`**. Path-B `session_open` seed may still call leftover `add` internally -- not TARGET |
| `query_warm` | leftover alias of `pin_map` |
| `query_walk` | leftover hop debug |
| `anchor=` / `--anchor` | leftover nickname |
| `read_get` | **unshipped**; `read_list` may still enumerate |
| `id:'NEW'` / NEW mint | leftover mint; not product Commit |

Args: [references/tool-parameters.md](references/tool-parameters.md). Policy: [references/mcp-policy.md](references/mcp-policy.md). Map: [references/tool-grammar.md](references/tool-grammar.md).

## Graph about a node or relationship

| Want | Tool |
|------|------|
| Neighbourhood / ego slice (primary) | `pin_map` from a cue |
| Enumerate by kind / field | `read_list` then cue `pin_map` |
| Hop listing only | leftover `query_walk` -- debug, not the reason loop |

**Recipe (node):** cue (`kind` / locators) -> `pin_map(..., depth=2, max_rows=50, session=...)` -> parse **`stdout`**. Raise `depth` only if the slice is too thin.

**Recipe (relationship -> its two nodes):** endpoints are **on the relationship**. Parse `(a)-[:TYPE]->(b)` from pin_map `stdout`. Do **not** use an edge as a leftover `--anchor`. leftover pipe `@EDG:` may still appear on import -- do not teach pipe as agent mutate format.

## When locators must match model / schematic

**Decision:** pin into SysML / `.ato` / codebase / skill -> **stable locators** (`path`, `qname`, ...). New MemNet-only fact -> GraphElement `CREATE` (no leftover NEW). Do not conflate ingest with goldfish mutate.

| Need | Tool |
|------|------|
| Find by schematic field | `read_list` with `where` (`refdes=`, `net=`, `qname=`, `path=`) |
| Neighbourhood | `pin_map` from that locator cue |
| First materialise pin | `ingest_*` or `mutate` with explicit locators |
| Annotate about a pin | `mutate` CREATE `:CLM` then rel to the copied pin |

```cypher
CREATE (c:CMP {refdes: 'R1', path: 'boards/pdu/pdu.ato', recycle: 'persistent'})
MATCH (c:CMP {refdes: 'R1', path: 'boards/pdu/pdu.ato'}) SET c.value = '10k'
CREATE (clm:CLM {type: 'decision', code: 'keep R1 10k', recycle: 'persistent'})
MATCH (c:CMP {refdes: 'R1'}), (clm:CLM {code: 'keep R1 10k'})
CREATE (clm)-[:mentions]->(c)
```

**Forbidden:** leftover client NEW for R1/U2/nets/SysML qnames/paths; inventing colliding store keys. Path-B ingest is **shipped**. Ingest is **not** pin-map export.

## Neighbourhood reserve (shipped)

```text
reserve(..., llm_id, depth=2, ttl_s=120, session=...) -> rid, until
extend(llm_id, rid, ttl_s=120, session=...) -> until
release(llm_id, rid, session=...) -> ok
```

RSV may still take a leftover nick `anchor` on the tool -- that parameter name is leftover. Mutate on reserved neighbourhoods requires matching `llm_id`. Full session ACL modes / `session_token` remain **design**; CapsPolicy ACL is opt-in. SSOT: MemNet `docs/grammar/memnet-neighbourhood-reserve.md`.

## SysML v2 modeling (relatives cache)

**Policy skill:** [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md).

| Turn phase | Tool |
|------------|------|
| Preflight | MemNet MCP in catalog? Then optional `serve_status` (TCP only) |
| Read cache | `pin_map(kind='TSK', locators=['goal=TSK_model_<short>'], depth=2, max_rows=50)` |
| Bootstrap | `session_open` + map + optional `ingest_sysml` / `snap_model` |
| Write delta | **`mutate`**; `llm_id` if RSV held |
| Persist | `session_save` -> project `.memnet/` snap |

Tag vocabulary: [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md).

## MUST NOT

- Invent ids already present on the pin map -- copy locators.
- Teach leftover `--anchor` / `id:'NEW'` / leftover `add`/`update` as TARGET.
- Emit pipe `@TAG:...` rows as agent I/O -- GQL / shaped wire only.
- Recommend TOON/TRON for handoffs.
- Restore novel-writer MCP extras.
- `rag_query` / ANN of S / dump S / stack N nested maps in one generate.
- Claim **1.0**. Claim hydrate-by-hid proven. Vendor a Neo4j/AgensGraph server.

## Related

| Path | Role |
|------|------|
| [memnet-use](../memnet-use/SKILL.md) | How to use MemNet (hub) |
| [memnet-format](../memnet-format/SKILL.md) | MemNet GQL wire conventions |
| [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md) | Catalog / look loop |
| [graph-query-language](../graph-query-language/SKILL.md) | General GQL |
| [references/atomisation.md](references/atomisation.md) | One fact per row |
| MemNet `docs/ROADMAP.md` | Version map SSOT |
