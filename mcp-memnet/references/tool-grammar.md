# MCP tools <-> MemNet grammar

**Audience:** model. Package SSOT: MemNet `parts/memnet-mcp/software/memnet_mcp/server.py` (13 tools). Formal dialect: `docs/grammar/` (`MemNet.g4`, golden fixtures).

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
| `session_open` | New session + tag map | Lifecycle + schema | `map_lines`: `SCHEMA KIND ; fields=id …`; `seed_lines` = optional shared-dialect seed (LAW01–05 auto) |
| `session_current` | Session id / TTL | Lifecycle | None |
| `session_save` | Write snapshot file | Snapshot | None (file holds graph) |
| `session_load` | Restore snapshot | Snapshot | None |
| `pin_map` | **Live pin map** | Primary **read** | `stdout`: bare present; optional tool arg `view` |
| `query_warm` | Deprecated alias for `pin_map` | Same as `pin_map` | Same (incl. `view`) |
| `query_walk` | Hop listing | Debug read | Walk lines — not the pin-map agent loop |
| `add` | Create rows | Mutate **create** | `wire_lines`: lines with `+` / `[NEW]` / `NEW` |
| `update` | Replace / drop rows | Mutate **patch/drop** | `wire_lines`: `~` / `-` on known ids |
| `read_get` | One row by id | Lookup | One rendered row |
| `read_list` | Enumerate by tag / where | Lookup | Many rows |
| `housekeep_stats` | Counts vs caps | Housekeeping | Stats text / envelope |

**Design (not yet shipped):** `reserve` / `extend` / `release` — session control plane; pin map shows `RSV [rid] ; llm_id=… ; anchor=… ; depth=… ; until=…` (shared dialect). See MemNet `docs/grammar/memnet-neighbourhood-reserve.md`.

## Grammar productions agents must recognise

| Situation | Tool | Shape (shared dialect) |
|-----------|------|------------------------|
| Read this turn | `pin_map` | Bare present: `KIND [Id] ; k=v` / `Eid [a] --(rel)--> [b]` — **no** leading `+`/`~`/`-` |
| Nodes of an EDGE | `read_get` or pin-map EDGE line | Parse `[a]` / `[b]` (shared dialect) or pipe columns `src`/`dist` — those values **are** the node ids; no extra tool |
| Create | `add` | `+ KIND [NEW] ; …` or `+ [from] --(rel)--> [to]` / `+ NEW [from] --(rel)--> [to]` |
| Patch | `update` | `~ [KnownId] ; …` (no kind on patch) |
| Re-id | `update` | `~ [OldId] ; id=NewId` (optional `; merge=true` if NewId exists; nodes only) |
| Patch edge (bare) | `update` | `~ Eid ; …` |
| Patch edge (full) | `update` | `~ [from] --(rel)--> [to] ; …` |
| Drop | `update` | `- KIND [KnownId]` or `- Eid` |
| Validate shapes | (offline) | `docs/grammar/tools/tier_a.py` + fixtures — not an MCP tool |

## Why names look "weird"

| MCP name | Shared-dialect vocabulary | Keep API? |
|----------|---------------------------|-----------|
| `pin_map` | live **pin map** | **Primary** read tool |
| `query_warm` | same as `pin_map` | Yes — deprecated alias |
| `add` / `update` | mutate ops `+` / `~` / `-` | Yes — ops live in `wire_lines` |
| `serve_status` | in-process needs no serve | Yes — optional under default transport |
| Missing novel tools | product dropped novel-writer | Expected |

## Config note (user pack)

This pack registers **`memnet`** in `~/.cursor/mcp.json` as a **stdio client** with `MEMNET_MCP_TRANSPORT=tcp` → **`10.0.0.10:18765`**. Do not also enable a second MemNet MCP in a project mcp.json (doubles the tool list). Engine version = remote serve, not the local stdio wrapper.

Cross-ref: [tool-parameters.md](tool-parameters.md) · [mcp-policy.md](mcp-policy.md) · MemNet `docs/grammar/memnet-grammar-design.md`
