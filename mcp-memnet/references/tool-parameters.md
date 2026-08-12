# MemNet MCP — tool parameters

MCP server key: typically **`memnet`** in Cursor MCP config. Tools return **JSON text** (parse as object) unless noted. Product: **`memnet-llm` 0.4.0**. User-pack engine: TCP **`10.0.0.10:18765`**.

## Invoke order (typical session)

1. **`serve_status`** — optional under default in-process; required when using TCP/`memnet serve`
2. **`session_open`** — `map_lines` (or `map_file`); store `session_id`
3. **`pin_map`** — every turn; anchor required (live **pin map**; `query_warm` is legacy alias)
4. **`add`** / **`update`** — shared-dialect mutate via `wire_lines`
5. **`session_current`** — optional; pass `session` or set `MEMNET_SESSION`
6. **`read_get`** / **`read_list`** — single-row or enumerate-by-tag
7. **`housekeep_stats`** — caps / row counts when the graph grows

Envelope and errors: [mcp-policy.md](mcp-policy.md). Atomisation: [atomisation.md](atomisation.md). Tool <-> grammar: [tool-grammar.md](tool-grammar.md).

## Tools

| Tool | Required args | Optional args | Notes |
|------|---------------|---------------|-------|
| `serve_status` | — | — | `{ running, host, port }` — transport probe |
| `session_open` | `map_lines` **or** `map_file` | `ttl`, `seed_lines`, `allow_new_relation` | Auto-seeds LAW01–LAW05 (shared dialect) |
| `session_save` | `file` | `session` | Snapshot to disk |
| `session_load` | `file` | `keep_id`, `ttl` | Resume; no prior session required |
| `session_current` | — | `session` | Needs `session` or `MEMNET_SESSION` |
| `pin_map` | `anchor` | `depth` (2), `max_rows` (50), `view`, `session` | **Primary read**; optional `view=shell\|interior` (also soft `flowchart\|parts\|statechart`) |
| `query_warm` | `anchor` | `depth` (2), `max_rows` (50), `view`, `session` | Deprecated alias for `pin_map` |
| `query_walk` | `anchor` | `depth`, `max_rows`, `session` | Hop lines for debug — not the agent pin-map loop |
| `add` | `wire_lines` | `allow_new_relation`, `agent`, `session` | Create; `+` / `NEW` inside lines |
| `update` | `wire_lines` | `allow_new_relation`, `agent`, `session` | Patch/drop; `~` / `-` inside lines |
| `read_get` | `id` | `session` | One row by id |
| `read_list` | — | `tag`, `active_only`, `where`, `session` | Enumerate without prior ids |
| `housekeep_stats` | — | `session` | Counts / caps |

## Response envelope (all tools except `serve_status`)

```json
{
  "exit_code": 0,
  "stdout": "…pin map…",
  "stderr": "…",
  "session_id": "mn_…",
  "errors": []
}
```

- Branch on **`exit_code`** and **`errors[]`**
- Parse **`stdout`** for the live pin map (shared dialect, bare present)
- **`wire_lines`** are joined with `\n` before send

## Environment

| Variable | Purpose |
|----------|---------|
| `MEMNET_MCP_TRANSPORT` | User pack: **`tcp`**. (Product default elsewhere: in-process.) |
| `MEMNET_SERVE_HOST` / `MEMNET_SERVE_PORT` | User pack: **`10.0.0.10`** / **`18765`**. (Library default: `127.0.0.1:18765`.) |
| `MEMNET_SESSION` | Default session id after open/load |

Set these under `mcpServers.memnet.env` in `~/.cursor/mcp.json`. Restart the `memnet` MCP server after changes.

## wire_lines

Shared dialect mutate (`+` / `~` / `-`):

```text
## Nodes
+ CLM [NEW] ; type=decision ; code=… ; recycle=persistent
~ [T42] ; status=in_progress ; recycle=persistent

## Edges
+ [N03] --(helps)--> [T42] ; recycle=persistent
~ E01 ; recycle=delete_on_settle
```

Batch many atoms in one `add`/`update` call.
