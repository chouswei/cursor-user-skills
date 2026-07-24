# MemNet MCP — tool parameters

MCP server key: typically **`memnet`** in Cursor MCP config. Tools return **JSON text** (parse as object) unless noted. Product: **`memnet-llm` 0.3.1**.

## Invoke order (typical session)

1. **`serve_status`** — optional under default in-process; required when using TCP/`memnet serve`
2. **`session_open`** — `map_lines` (or `map_file`); store `session_id`
3. **`query_warm`** — every turn; anchor required (live **pin map**)
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
| `query_warm` | `anchor` | `depth` (2), `max_rows` (50), `session` | **Primary read** = live **pin map** (legacy tool name); `stdout` = bare present |
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
| `MEMNET_MCP_TRANSPORT` | Default **in-process**; set `tcp` for serve bridge |
| `MEMNET_SERVE_HOST` / `MEMNET_SERVE_PORT` | TCP bind target (default `127.0.0.1:18765`) |
| `MEMNET_SESSION` | Default session id after open/load |

## wire_lines

Shared dialect mutate (`+` / `~` / `-`):

```text
## Nodes
+ CLM [NEW] ; type=decision ; code=… ; recycle=persistent

## Edges
+ E01 [NEW] --(helps)--> [T42] ; recycle=persistent
```

Batch many atoms in one `add`/`update` call.
