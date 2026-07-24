# MCP tools <-> MemNet grammar

**Audience:** model. Package SSOT: MemNet `parts/memnet-mcp/software/memnet_mcp/server.py` (12 tools). Formal dialect: `docs/grammar/` (`MemNet.g4`, golden fixtures).

MCP does **not** replace the grammar. Tools open a session and move **shared-dialect text** through a JSON envelope. Legal line shapes are still NODE | EDGE (Write = display).

## Envelope vs dialect

| Layer | Role |
|-------|------|
| MCP JSON `{exit_code, stdout, stderr, session_id, errors}` | Transport / CLI adapter result |
| `stdout` or `wire_lines` text | **Shared dialect** (pin map or mutate) |
| `MemNet.g4` productions | What those lines must look like |

`serve_status` is the only tool that returns a non-envelope JSON object (`{running, host, port}`).

## Full map (all tools)

| Tool | Purpose | Grammar role | Dialect payload |
|------|---------|--------------|-----------------|
| `serve_status` | Probe TCP serve | Transport only | None |
| `session_open` | New session + tag map | Lifecycle + schema | `map_lines` = field schemas; `seed_lines` = optional shared-dialect seed (LAW01–05 auto) |
| `session_current` | Session id / TTL | Lifecycle | None |
| `session_save` | Write snapshot file | Snapshot | None (file holds graph) |
| `session_load` | Restore snapshot | Snapshot | None |
| `query_warm` | **Live pin map** (legacy name) | Primary **read** | `stdout`: bare present (`presentNode` / `presentEdge` / `lawPin`) |
| `query_walk` | Hop listing | Debug read | Walk lines — not the pin-map agent loop |
| `add` | Create rows | Mutate **create** | `wire_lines`: lines with `+` / `[NEW]` / `NEW` |
| `update` | Replace / drop rows | Mutate **patch/drop** | `wire_lines`: `~` / `-` on known ids |
| `read_get` | One row by id | Lookup | One rendered row |
| `read_list` | Enumerate by tag / where | Lookup | Many rows |
| `housekeep_stats` | Counts vs caps | Housekeeping | Stats text / envelope |

## Grammar productions agents must recognise

| Situation | Tool | Shape (shared dialect) |
|-----------|------|------------------------|
| Read this turn | `query_warm` | Bare present: `KIND [Id] ; k=v` / `Eid [a] --(rel)--> [b]` — **no** leading `+`/`~`/`-` |
| Create | `add` | `+ KIND [NEW] ; …` or `+ Eid [a] --(rel)--> [b]` |
| Patch | `update` | `~ KIND [KnownId] ; …` |
| Drop | `update` | `- KIND [KnownId]` or `- Eid` |
| Validate shapes | (offline) | `docs/grammar/tools/tier_a.py` + fixtures — not an MCP tool |

## Why names look “weird”

| MCP name | Shared-dialect vocabulary | Keep API? |
|----------|---------------------------|-----------|
| `query_warm` | live **pin map** | Yes — gloss in skills until rename wave |
| `add` / `update` | mutate ops `+` / `~` / `-` | Yes — ops live in `wire_lines` |
| `serve_status` | in-process needs no serve | Yes — optional under default transport |
| Missing `pin_map` tool | same as `query_warm` | Do not add a duplicate tool |
| Missing novel tools | product dropped novel-writer | Expected |

## Config note (one MemNet MCP)

Prefer **project** `.cursor/mcp.json` for MemNet repo work (in-process). Do not also register `memnet` in user `~/.cursor/mcp.json` — that doubles the MCP list.

Cross-ref: [tool-parameters.md](tool-parameters.md) · [mcp-policy.md](mcp-policy.md) · MemNet `docs/grammar/memnet-grammar-design.md`
