---
name: mcp-memnet
description: >-
  MemNet MCP — in-memory graph via shaped pin_map, session tools, and
  openCypher-shaped mutate (add/update). Triggers: memnet mcp, pin_map,
  query_warm, pin map, session_open, GQL wire, shaped subgraph, MutateGate,
  sysml memnet tools.
metadata:
  pattern: tool-wrapper
  version: "5.0"
  domain: memnet
  product: memnet-llm
token_guardrails: |
  - Primary read is pin_map (shaped subgraph); parse envelope stdout — not JSON keys as grammar.
  - Mutate with openCypher-shaped wire_lines; mint creates with NEW; copy ids from pin_map.
  - Wire shapes SSOT: memnet-format; general GQL: graph-query-language / gql-path-patterns.
---

# MemNet MCP (generic)

Product **`memnet-llm`** (CLI `memnet`). Engine + generic MCP only — **novel-writer is out of scope**.

MemNet is working memory between LLM call pipelines and data search. Agents read a bounded **shaped subgraph** each turn via **`pin_map`** and write with **openCypher-shaped** mutate statements — the **GQL wire**. Detail: [memnet-format](../memnet-format/SKILL.md).

## User-pack transport (this machine)

| Role | Where |
|------|--------|
| **Cursor MCP** | HTTP `url` -> **`http://10.0.0.10:18766/mcp`** (streamable-http + Bearer) |
| **Pi graph store** | Prefer TCP `memnet serve` **`:18765`** with HTTP MCP set `MEMNET_MCP_TRANSPORT=tcp` (same graph) |
| Local stdio `command` | Optional `memnet-local` only — not the primary `memnet-pi` path |

Cursor `~/.cursor/mcp.json` -> primary server id **`memnet-pi`** (Cursor may show it as `user-memnet-pi`). Shape matches Inventree-style `url` + `headers` (no local `command` / `env`):

```json
"memnet-pi": {
  "url": "http://10.0.0.10:18766/mcp",
  "headers": {
    "Authorization": "Bearer <token>"
  }
}
```

After editing mcp.json: **Cursor -> MCP / Tools -> restart `memnet-pi`** (or reload the window). Do **not** dual-run InProcess HTTP MCP against a separate TCP store without `MEMNET_MCP_TRANSPORT=tcp` on the Pi HTTP process.

## Doctrine (must)

| Idea | Meaning |
|------|---------|
| Shaped subgraph | pin_map emits a bounded neighbourhood (nodes + relationships), not a dump |
| GQL wire | openCypher-shaped mutate in `wire_lines`; general GQL in sibling skills |
| Live pin map | Primary **read**; optional `view=shell\|interior` for budget |
| NEW vs locators | LLM creates: mint with NEW; ingest pins use stable locators (`path`, `qname`, …) |
| BIND vs relation | Port-port -> `BIND`; node-node -> typed rel labels |
| Transport (user pack) | **HTTP `:18766/mcp` -> Pi**; bridge HTTP MCP to TCP serve `:18765` when sharing one graph |

Always pass the same `session` id (or set `MEMNET_SESSION`).

**Tool gloss:** Primary pin-map read is MCP `pin_map` / CLI `query pin-map`. Optional **`view=`** (`shell` | `interior`; soft-accept `flowchart` | `parts` | `statechart`). Omit `view` for depth/`max_rows` only. `query_warm` / `query warm` are **deprecated aliases**. Formal shapes: [memnet-format](../memnet-format/SKILL.md) + MemNet `docs/grammar/`.

## How MCP tools fit the wire

MCP is a **thin CLI adapter**. Tools do **not** invent a second dialect: pin-map and mutate payloads live in the JSON envelope's **`stdout` / `wire_lines`** as GQL / openCypher-shaped text (or engine-rendered shaped subgraph).

| MCP tool | Role | What goes on the wire |
|----------|------|------------------------|
| `session_open` | Session lifecycle + schema map | `map_lines` = `SCHEMA Kind ; fields=id …` (registry). Optional `seed_lines` = openCypher-shaped seed (LAW auto-seeded). |
| `session_current` | Session lifecycle | Metadata only |
| `session_save` / `session_load` | Snapshot persist / resume | File path; next pin_map is still a shaped subgraph |
| `pin_map` | **Live shaped-subgraph read** | `stdout` = neighbourhood (+ LAW). Optional arg `view`. |
| `query_warm` | Deprecated alias for `pin_map` | Same as `pin_map` (including `view`) |
| `query_walk` | Hop debug (not primary pin map) | Walk lines for topology debug |
| `add` | Mutate **create** | `wire_lines` = openCypher-shaped creates with NEW as needed |
| `update` | Mutate **patch / drop** | `wire_lines` = MATCH/SET/DELETE on known ids |
| `read_get` / `read_list` | Lookup / enumerate | Single-row or label list — use to avoid inventing ids |
| `housekeep_stats` | Caps / counts | Envelope stats |
| `serve_status` | Transport probe | `{running,host,port}` — TCP-oriented |

**Agent loop <-> wire:** `pin_map` emits **shaped subgraph**; `add`/`update` accept **openCypher-shaped** mutate. Same property / label conventions.

**Not weird dialect — transport envelope:** every tool except `serve_status` returns JSON `{exit_code, stdout, stderr, session_id, errors}`. Parse **`stdout`** for pin-map / row text. Do not treat the JSON keys as the MemNet grammar.

**Misfits (gloss, do not invent tools):**

| Looks odd | Why | Agent action |
|-----------|-----|--------------|
| Name `query_warm` | Legacy alias | Use **`pin_map`** |
| Name `add` / `update` | CLI verbs | Put Cypher ops **inside** `wire_lines` |
| `serve_status` | Sounds optional | User pack: TCP store probe (`10.0.0.10:18765`); Cursor itself uses HTTP `:18766/mcp` |
| No tool named `mutate` | API kept stable | Mutate via `add` / `update` with statements in `wire_lines` |
| No novel-writer tools | Dropped from product | Do not expect them |

## Agent loop

```text
pin_map -> reason -> mutate -> pin_map
```

1. Pin map — `pin_map(anchor=…, depth<=2)` — shaped subgraph; optional `view=shell` (tight) or `view=interior`.
2. Reason; copy assigned ids from the map.
3. `add` / `update` with **openCypher-shaped** statements.
4. `session_save` when durability is needed.

**MCP missing:** if MemNet tools are not in the session catalog, skip this loop — plain Markdown scratch only (no TOON/TRON). Do not invent tool calls. Wire shapes: [memnet-format](../memnet-format/SKILL.md).

## Graph about a node or relationship

| Want | Tool | Why |
|------|------|-----|
| Neighbourhood / ego slice (primary) | `pin_map` | Live **shaped subgraph** in `stdout` |
| Hop listing only | `query_walk` | Debug topology; not the reason loop |
| One known id | `read_get` | Single row; not a full neighbourhood |
| Find ids by label / field | `read_list` | Enumerate first; then pin_map on a real id |

**Recipe (node):** resolve id if needed (`read_list` / prior pin_map) -> `pin_map(anchor=<node_id>, depth=2, max_rows=50, session=…)` -> parse envelope **`stdout`**. Raise `depth` only if the slice is too thin; keep `max_rows` bounded.

**Recipe (relationship -> its two node ids):** there is **no** separate "get nodes of edge" tool. Endpoints are **on the relationship**.

1. Obtain the rel line: `read_get(id=<edge_id>)`, or copy it from pin_map `stdout`.
2. **Parse endpoints** (copy those values — they *are* the node ids):
   - **GQL / shaped present:** `(a)-[:TYPE {id: …}]->(b)` or engine present form with from/to brackets — first endpoint = source, second = destination.
   - **Legacy pipe** (`read_get` / `read_list` may still emit `@EDG:…`): columns `src` and `dist` — treat as from/to; do not teach pipe as agent mutate format.
3. Optional: `read_get(id=<node>)` for each full node; or `pin_map(anchor=<endpoint>, …)`. Do **not** use the edge id as a pin_map anchor. Do not invent ids.

## When ids must match model / schematic

**Decision:** pin into SysML / `.ato` / codebase / skill -> **stable locator** (deterministic ground id + locator props). New MemNet-only fact -> **NEW**. Do not conflate ingest with goldfish mutate.

| Need | Tool |
|------|------|
| Find by schematic field | `read_list(tag=…, where=["refdes=R1"])` (or `net=`, `qname=`, `path=`) |
| Confirm one ground id | `read_get(id=ATO_R1)` |
| Neighbourhood | `pin_map(anchor=ATO_R1, …)` |
| First materialise pin | `add` with **explicit** id + locators (not NEW) |
| Annotate about a pin | `add` with NEW `:CLM` then rel to the **copied** pin id |

```cypher
CREATE (c:CMP {id: 'ATO_R1', refdes: 'R1', path: 'boards/pdu/pdu.ato', recycle: 'persistent'})
MATCH (c {id: 'ATO_R1'}) SET c.value = '10k', c.recycle = 'persistent'
CREATE (clm:CLM {id: 'NEW', type: 'decision', code: 'keep R1 10k', recycle: 'persistent'})
```

**Forbidden:** client NEW for R1/U2/nets/SysML qnames/paths; inventing `C_rand_99`; NEW on patch. **Pitfall:** `add` fails if id exists — look up first. PinMapIngest_* may be stubs; seed via `seed_lines` / explicit-id `add` until ingest lands.

**Re-id (wrong ground id):** `update` with MATCH old id SET `id=NewId` (optional merge when NewId exists; nodes only; retarget rels; drop OldId). Self id=OldId is a no-op.

```cypher
MATCH (n {id: 'C_rand_99'}) SET n.id = 'ATO_R1', n.recycle = 'persistent' /* merge=true when engine supports fold */
```

## Multi-agent reserve (design — not yet shipped)

Neighbourhood **reserve** with holder **`llm_id`** + **TTL** prevents same-session write races. MCP sketch (next minor):

```text
reserve(session, anchor, depth=2, llm_id, ttl_s=120) -> rid, until
extend(session, rid|anchor, llm_id, ttl_s=120) -> until
release(session, rid|anchor, llm_id) -> ok
```

Pin map may show intersecting leases as shaped present:

```cypher
(:RSV {id: 'R7', llm_id: 'coder_a', anchor: 'ATO_R1', depth: 2, until: '2026-07-24T08:15:00Z', left_s: 87})
```

**Never** `@RSV:` pipe. SSOT: MemNet `docs/grammar/memnet-neighbourhood-reserve.md`. Mutate on reserved ids requires matching `llm_id`.

## Essential tools (quick)

| Tool | When | Notes |
|------|------|-------|
| `serve_status` | Reachability / probe | TCP serve `:18765` when HTTP MCP bridges; Cursor entry is `:18766/mcp` |
| `session_open` | New session | `map_lines` (or `map_file`) + optional `seed_lines`; `allow_new_relation=true` for custom rel types |
| `session_save` / `session_load` | Persist / resume | Snapshot file path |
| `session_current` | Session metadata | |
| `pin_map` | **Primary read** = shaped subgraph | `anchor` required; `depth`/`max_rows`; optional `view` |
| `query_warm` | Legacy alias for `pin_map` | Same params |
| `query_walk` | Hop debug | |
| `add` / `update` | Mutate | `wire_lines`: openCypher-shaped |
| `read_get` / `read_list` | Single id / enumerate | Prefer over inventing ids |
| `housekeep_stats` | Caps / counts | |

Args detail: [references/tool-parameters.md](references/tool-parameters.md). Policy: [references/mcp-policy.md](references/mcp-policy.md). Full map: [references/tool-grammar.md](references/tool-grammar.md).

## GQL wire (shapes)

Line shapes, mutate ops, BIND vs relation, and examples: [memnet-format](../memnet-format/SKILL.md). General GQL: [graph-query-language](../graph-query-language/SKILL.md), [gql-path-patterns](../gql-path-patterns/SKILL.md). Formal SSOT: MemNet `docs/grammar/`.

## SysML v2 modeling (relatives cache)

**Policy skill:** [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md).

| Turn phase | Tool |
|------------|------|
| Preflight | MemNet MCP in catalog? Then optional `serve_status` (TCP only) |
| Read cache | pin_map — `pin_map(anchor=TSK_model_<short>, depth=2, max_rows=50)` |
| Bootstrap | `session_open` + `map_file` / `map_lines` + `seed_lines`; `allow_new_relation=true` for `owns` |
| Write delta | `add` / `update` (openCypher-shaped) |
| Persist | `session_save` -> project `.memnet/` snap |
| Resume | `session_load` or `MEMNET_SESSION` |

Tag vocabulary: [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md).

**Do not** use chat or `AGENT-CONTEXT.md` for topology when a live session is available.

## MUSTNOT

- Invent ids already present on the pin map — copy them.
- Emit pipe `@TAG:...` rows as agent I/O — GQL / shaped wire only. Includes `@RSV:` — use `:RSV` present forms instead.
- Recommend TOON/TRON for handoffs — prefer GQL wire or plain Markdown.
- Restore or depend on novel-writer MCP extras.

## Related

| Path | Role |
|------|------|
| [memnet-format](../memnet-format/SKILL.md) | MemNet GQL wire conventions |
| [graph-query-language](../graph-query-language/SKILL.md) | General GQL |
| [gql-path-patterns](../gql-path-patterns/SKILL.md) | Bounded paths |
| [references/atomisation.md](references/atomisation.md) | One fact per row |
| [references/tool-grammar.md](references/tool-grammar.md) | MCP tool <-> wire map |
| MemNet `README.md` / `docs/grammar/` | Product SSOT |
