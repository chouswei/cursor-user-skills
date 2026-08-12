# MCP tools <-> MemNet GQL wire

**Audience:** model. Package SSOT: MemNet `parts/memnet-mcp/software/memnet_mcp/server.py` (13 tools). Wire shapes: [memnet-format](../../memnet-format/SKILL.md); general GQL: [graph-query-language](../../graph-query-language/SKILL.md).

MCP does **not** replace the grammar. Tools open a session and move **GQL / openCypher-shaped text** (or engine-rendered shaped subgraph) through a JSON envelope.

## Envelope vs wire

| Plane | Role |
|-------|------|
| MCP JSON `{exit_code, stdout, stderr, session_id, errors}` | Transport / CLI adapter result |
| `stdout` or `wire_lines` text | **GQL wire** (shaped pin_map or openCypher-shaped mutate) |
| MemNet grammar / engine | What those statements must look like |

`serve_status` is the only tool that returns a non-envelope JSON object (`{running, host, port}`).

## Full map (all tools)

| Tool | Purpose | Wire role | Dialect payload |
|------|---------|-----------|-----------------|
| `serve_status` | Probe TCP serve | Transport only | None |
| `session_open` | New session + tag map | Lifecycle + schema | `map_lines`: `SCHEMA Kind ; fields=id …`; `seed_lines` = optional openCypher-shaped seed (LAW01–05 auto) |
| `session_current` | Session id / TTL | Lifecycle | None |
| `session_save` | Write snapshot file | Snapshot | None (file holds graph) |
| `session_load` | Restore snapshot | Snapshot | None |
| `pin_map` | **Live shaped subgraph** | Primary **read** | `stdout`: neighbourhood; optional tool arg `view` |
| `query_warm` | Deprecated alias for `pin_map` | Same as `pin_map` | Same (incl. `view`) |
| `query_walk` | Hop listing | Debug read | Walk lines — not the pin-map agent loop |
| `add` | Create atoms | Mutate **create** | `wire_lines`: CREATE / NEW mint |
| `update` | Replace / drop | Mutate **patch/drop** | `wire_lines`: MATCH/SET/DELETE on known ids |
| `read_get` | One row by id | Lookup | One rendered row |
| `read_list` | Enumerate by label / where | Lookup | Many rows |
| `housekeep_stats` | Counts vs caps | Housekeeping | Stats text / envelope |

**Design (not yet shipped):** `reserve` / `extend` / `release` — session control plane; pin_map may show `:RSV` present forms. See MemNet `docs/grammar/memnet-neighbourhood-reserve.md`.

## Shapes agents must recognise

| Situation | Tool | Shape |
|-----------|------|-------|
| Read this turn | `pin_map` | Shaped subgraph present — **no** exploratory unbounded walk |
| Nodes of a relationship | `read_get` or pin_map rel | Parse endpoints — those values **are** the node ids; no extra tool |
| Create | `add` | `CREATE (n:Kind {id: 'NEW', …})` / `CREATE (a)-[:TYPE {id: 'NEW'}]->(b)` |
| Patch | `update` | `MATCH (n {id: $id}) SET n.…` |
| Re-id | `update` | `MATCH (n {id: $old}) SET n.id = $new` (optional merge; nodes only) |
| Patch / drop rel | `update` | MATCH by `{id}` or endpoints+type; SET or DELETE |
| Validate shapes | (offline) | MemNet `docs/grammar/` fixtures — not an MCP tool |

## Why names look "weird"

| MCP name | Wire vocabulary | Keep API? |
|----------|-----------------|-----------|
| `pin_map` | live **shaped subgraph** | **Primary** read tool |
| `query_warm` | same as `pin_map` | Yes — deprecated alias |
| `add` / `update` | CREATE / MATCH-SET-DELETE | Yes — ops live in `wire_lines` |
| `serve_status` | in-process needs no serve | Yes — optional under default transport |
| Missing novel tools | product dropped novel-writer | Expected |

## Config note (user pack)

This pack registers **`memnet`** in `~/.cursor/mcp.json` as a **stdio client** with `MEMNET_MCP_TRANSPORT=tcp` -> **`10.0.0.10:18765`**. Do not also enable a second MemNet MCP in a project mcp.json (doubles the tool list). Engine version = remote serve, not the local stdio wrapper.

Cross-ref: [tool-parameters.md](tool-parameters.md) · [mcp-policy.md](mcp-policy.md) · MemNet `docs/grammar/`
