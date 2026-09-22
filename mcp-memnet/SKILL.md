---
name: mcp-memnet
description: >-
  OPS-ONLY tip. Product Multitask -> sysmledge-cursor-multitask + sysmledge MCP.
  Soft-pass: tip-as-face. MemNet MCP tip/engine tools only -- never SysMLEdge
  product face when sysmledge is installed.
metadata:
  pattern: tool-wrapper
  version: "5.0"
  domain: memnet
  product: memnet-llm
token_guardrails: |
  - Primary read is pin_map (shaped subgraph); parse envelope stdout -- not JSON keys as grammar.
  - Mutate with openCypher-shaped wire_lines; product Commit is mutate; copy locators from pin_map.
  - Wire shapes SSOT: memnet-format; general GQL: graph-query-language / gql-path-patterns.
---
# OPS-ONLY tip. Product Multitask -> skill sysmledge-cursor-multitask + sysmledge MCP. Soft-pass: tip-as-face.

# MemNet MCP (generic)

Product **`memnet-llm`** (CLI `memnet`). Engine + generic MCP only -- **novel-writer is out of scope**.

MemNet is working memory between LLM call pipelines and data search. Agents read a bounded **shaped subgraph** each turn via **`pin_map`** and write with **openCypher-shaped** mutate statements -- the **GQL wire**. Detail: [memnet-format](../memnet-format/SKILL.md).

## User-pack transport (this machine)

| Role | Where |
|------|--------|
| **Cursor MCP (live tip)** | Key **`memnet`**, namespace **`user-memnet`**; URL owned by `mcp.json` only + Bearer placeholder |
| Tip vs product face | Tip MemNet **MUST NOT** substitute for the SysMLEdge product face (panel `sysmledge` / namespace `user-sysmledge`) |
| Local stdio `command` | Optional `memnet-local` only -- **MUST NOT** treat as the primary tip path |

Cursor `~/.cursor/mcp.json` owns the tip URL for key **`memnet`** (Cursor may show namespace `user-memnet`). Skills/AGENTS name keys/namespaces only -- **MUST NOT** treat a SKILL.md URL as live. Bearer stays **placeholder only** -- **MUST NOT** write a real token into this skill or into tracked files. After editing mcp.json: **Cursor -> MCP / Tools -> restart `memnet`** (or reload the window). **MUST NOT** treat the old server id `memnet-pi` / namespace `user-memnet-pi` as live.

## Doctrine (must)

| Idea | Meaning |
|------|---------|
| Shaped subgraph | pin_map emits a bounded neighbourhood (nodes + relationships), not a dump |
| GQL wire | openCypher-shaped mutate in `wire_lines`; general GQL in sibling skills |
| Live pin map | Primary **read**; optional `view=shell|interior` for budget |
| Product Commit | MCP **`mutate`** (`wire_lines`); leftover `add`/`update` are registered façades |
| Locators vs identity | GraphElement identity; ingest pins use stable locators (`path`, `qname`, ...) |
| BIND vs relation | Port-port -> `BIND`; node-node -> typed rel labels |
| Transport (user pack) | Live tip: key **`memnet`** / namespace **`user-memnet`** (URL in `mcp.json`); tip != SysMLEdge product face |

Always pass explicit `session=` on every tool except `serve_status` (or set `MEMNET_SESSION`).

**Tool gloss:** Primary pin-map read is MCP `pin_map` / CLI `query pin-map`. Optional **`view=`** (`shell` | `interior`). Omit `view` for depth/`max_rows` only. `query_warm` is a leftover alias. Product mutate is MCP `mutate`. Formal shapes: [memnet-format](../memnet-format/SKILL.md) + MemNet `docs/grammar/`.

## How MCP tools fit the wire

MCP is a **thin CLI adapter**. Tools do **not** invent a second dialect: pin-map and mutate payloads live in the JSON envelope's **`stdout` / `wire_lines`** as GQL / openCypher-shaped text (or engine-rendered shaped subgraph).

| MCP tool | Role | What goes on the wire |
|----------|------|------------------------|
| `session_open` | Session lifecycle + schema map | `map_lines` = `SCHEMA Kind ; fields=id …` (registry). Optional `seed_lines` = openCypher-shaped seed (LAW auto-seeded). |
| `session_list` | Session listing | Live session ids + count |
| `session_close` | Session lifecycle | Close session |
| `session_current` | Session lifecycle | Metadata only |
| `session_save` / `session_load` | Snapshot persist / resume | File path; next pin_map is still a shaped subgraph |
| `pin_map` | **Live shaped-subgraph read** | `stdout` = neighbourhood (+ LAW). Optional arg `view`. |
| `find` | Seed search | Bounded MATCH by labels/props |
| `mutate` | **Product Commit** | `wire_lines` = openCypher-shaped CREATE / MERGE / SET / DELETE |
| `add` / `update` | Leftover façades (wrappers) | Wrap `mutate` envelope; do not teach as TARGET |
| `query_warm` | Leftover alias for `pin_map` | Same as `pin_map` (including `view`) |
| `query_walk` | Hop debug (not primary pin map) | Walk lines for topology debug |
| `read_list` | Enumerate | Multi-row listing to discover existing labels/props |
| `snap_model` | Snapshot model tree | Dedicated snap session; catalog + interiors |
| `housekeep_stats` | Caps / counts | Envelope stats |
| `serve_status` | Transport probe | `{running,host,port}` -- TCP-oriented |

**Agent loop <-> wire:** `pin_map` emits **shaped subgraph**; `mutate` accepts **openCypher-shaped** statements. Same property / label conventions.

**Not weird dialect -- transport envelope:** every tool except `serve_status` returns JSON `{exit_code, stdout, stderr, session_id, errors}`. Parse **`stdout`** for pin-map / row text. Do not treat the JSON keys as the MemNet grammar.

**Misfits (gloss, do not invent tools):**

| Looks odd | Why | Agent action |
|-----------|-----|--------------|
| Name `query_warm` | Legacy alias | Use **`pin_map`** |
| Names `add` / `update` | Leftover façades | Use **`mutate`** with Cypher ops inside `wire_lines` |
| `serve_status` | Sounds optional | User pack: transport probe; live tip is key **`memnet`** / namespace **`user-memnet`** |
| No novel-writer tools | Dropped from product | Do not expect them |

## Agent loop

```text
pin_map -> reason -> mutate -> pin_map
```

1. Pin map -- `pin_map(kind=..., locators=[...], depth<=2)` -- shaped subgraph; optional `view=shell` (tight) or `view=interior`.
2. Reason; use locators and copied properties from the map.
3. `mutate` with **openCypher-shaped** statements in `wire_lines`.
4. `session_save` when durability is needed.

**MCP missing:** if MemNet tools are not in the session catalog, skip this loop -- plain Markdown scratch only (no TOON/TRON). Do not invent tool calls. Wire shapes: [memnet-format](../memnet-format/SKILL.md).

## Graph about a node or relationship

| Want | Tool | Why |
|------|------|-----|
| Neighbourhood / ego slice (primary) | `pin_map` | Live **shaped subgraph** in `stdout` |
| Hop listing only | `query_walk` | Debug topology; not the reason loop |
| Find by label / prop / field | `find` / `read_list` | Discover seed first; then pin_map |

**Recipe (node):** resolve seed if needed (`find` / prior pin_map) -> `pin_map(kind=..., locators=[...], depth=2, max_rows=50, session=...)` -> parse envelope **`stdout`**. Raise `depth` only if the slice is too thin; keep `max_rows` bounded.

**Recipe (relationship -> its two endpoints):** endpoints are **on the relationship**.

1. Copy relationship line from pin_map `stdout`.
2. **Parse endpoints** (copy those values):
   - **GQL / shaped present:** `(a)-[:TYPE {props}]->(b)` or engine present form with from/to brackets -- first endpoint = source, second = destination.
3. Optional: `pin_map` on the endpoint node locator. Do not invent ids.

## When ids must match model / schematic

**Decision:** pin into SysML / codebase / schematic / skill -> **stable locator** (deterministic ground locator props such as `qname`, `path`, `refdes`). GraphElement identity in GQL wire; do not invent client NEW for ground locators.

| Need | Tool |
|------|------|
| Find by locator / field | `find(locators=["refdes=R1"])` or `read_list(tag=..., where=["refdes=R1"])` |
| Neighbourhood | `pin_map(kind="CMP", locators=["refdes=R1"], session=...)` |
| Materialise pin | `mutate` with explicit locators (e.g. `CREATE (:CMP {refdes: 'R1', path: 'boards/pdu/pdu.ato', recycle: 'persistent'})`) |
| Annotate about a pin | `mutate` with `:CLM` then relate to the matched pin |

```cypher
CREATE (c:CMP {refdes: 'R1', path: 'boards/pdu/pdu.ato', recycle: 'persistent'})
MATCH (c:CMP {refdes: 'R1'}) SET c.value = '10k', c.recycle = 'persistent'
CREATE (clm:CLM {type: 'decision', code: 'keep R1 10k', recycle: 'persistent'})
MATCH (clm:CLM {code: 'keep R1 10k'}), (c:CMP {refdes: 'R1'})
CREATE (clm)-[:documents]->(c)
```

**Forbidden:** client NEW for R1/U2/nets/SysML qnames/paths; inventing random ids; leftover NEW on patch. **Pitfall:** check existence before creating duplicate pins. Seed via `seed_lines` / `mutate` until ingest lands.

## Multi-agent reserve (design -- not yet shipped)

Neighbourhood **reserve** with holder **`llm_id`** + **TTL** prevents same-session write races. MCP sketch (next minor):

```text
reserve(session, kind, locators, depth=2, llm_id, ttl_s=120) -> rid, until
extend(session, rid, llm_id, ttl_s=120) -> until
release(session, rid, llm_id) -> ok
```

Pin map may show intersecting leases as shaped present:

```cypher
(:RSV {id: 'R7', llm_id: 'coder_a', anchor: 'ATO_R1', depth: 2, until: '2026-07-24T08:15:00Z', left_s: 87})
```

**Never** `@RSV:` pipe. SSOT: MemNet `docs/grammar/memnet-neighbourhood-reserve.md`. Mutate on reserved items requires matching `llm_id`.

## Essential tools (quick)

| Tool | When | Notes |
|------|------|-------|
| `serve_status` | Reachability / probe | Live tip: key **`memnet`** / namespace **`user-memnet`** |
| `session_open` | New session | `map_lines` (or `map_file`) + optional `seed_lines`; `allow_new_relation=true` for custom rel types |
| `session_list` / `session_close` | Session lifecycle | Enumerate / close live sessions |
| `session_save` / `session_load` | Persist / resume | Snapshot file path (`memnet-snapshot-v1` format) |
| `session_current` | Session metadata | |
| `pin_map` | **Primary read** = shaped subgraph | `kind` / `locators` / `cue`; `depth`/`max_rows`; optional `view` |
| `find` | Seed search | Bounded MATCH by labels/props |
| `mutate` | **Product Commit** | `wire_lines`: openCypher-shaped CREATE/SET/DELETE |
| `add` / `update` | Leftover façades | Wrap `mutate` envelope |
| `snap_model` | Model snapshot | Dedicated snap session; catalog + interiors |
| `read_list` | Enumerate | Multi-row listing |
| `housekeep_stats` | Caps / counts | Envelope stats |

Args detail: [references/tool-parameters.md](references/tool-parameters.md). Policy: [references/mcp-policy.md](references/mcp-policy.md). Full map: [references/tool-grammar.md](references/tool-grammar.md).

## GQL wire (shapes)

Line shapes, mutate ops, BIND vs relation, and examples: [memnet-format](../memnet-format/SKILL.md). General GQL: [graph-query-language](../graph-query-language/SKILL.md), [gql-path-patterns](../gql-path-patterns/SKILL.md). Formal SSOT: MemNet `docs/grammar/`.

## SysML v2 modeling (relatives cache)

**Policy skill:** [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md).

| Turn phase | Tool |
|------------|------|
| Preflight | MemNet MCP in catalog? Then optional `serve_status` (TCP only) |
| Read cache | pin_map -- `pin_map(kind="TSK", locators=["goal=TSK_model_<short>"], depth=2, max_rows=50, session=...)` |
| Bootstrap | `session_open` + `map_file` / `map_lines` + `seed_lines`; `allow_new_relation=true` for `owns` |
| Write delta | `mutate` (openCypher-shaped `wire_lines`) |
| Persist | `session_save` -> project `.memnet/` snap |
| Resume | `session_load` or `MEMNET_SESSION` |

Tag vocabulary: [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md).

**Do not** use chat or `AGENT-CONTEXT.md` for topology when a live session is available.

## MUST NOT

- Invent ids already present on the pin map -- copy them.
- Emit pipe `@TAG:...` or `memnet-snapshot-v1` rows as agent I/O -- that pipe format is persist / `session_save` dialect, not agent wire.
- Recommend TOON/TRON for handoffs -- prefer GQL wire or plain Markdown.
- Require leftover `anchor` or teach leftover `add`/`update` as TARGET.
- Restore or depend on novel-writer MCP extras.
- Insert live session ids, foreign product names, or snap dumps.
- Treat tip MemNet as the SysMLEdge product face -- tip != face.
- Cite `10.0.0.10`, `:18765`, `:18766`, or any SKILL.md host URL as the live tip; live tip is key **`memnet`** / namespace **`user-memnet`** (`mcp.json` owns the URL).
- Write a real Bearer token into this skill or tracked config -- placeholder only.

## Related

| Path | Role |
|------|------|
| [memnet-format](../memnet-format/SKILL.md) | MemNet GQL wire conventions |
| [graph-query-language](../graph-query-language/SKILL.md) | General GQL |
| [gql-path-patterns](../gql-path-patterns/SKILL.md) | Bounded paths |
| [references/atomisation.md](references/atomisation.md) | One fact per row |
| [references/tool-grammar.md](references/tool-grammar.md) | MCP tool <-> wire map |
| MemNet `README.md` / `docs/grammar/` | Product SSOT |
