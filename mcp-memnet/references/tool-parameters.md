# MemNet MCP — tool parameters (v1)

MCP server key: **`memnet`** in `~/.cursor/mcp.json`. Tools return **JSON text** (parse as object) unless noted.

## Invoke order (typical session)

1. **`serve_status`** — abort if `"running": false`
2. **`session_open`** — `map_lines` (required tag map); store `session_id`
3. **`query_warm`** — every turn; anchor required
4. **`add`** / **`update`** — atomised `@TAG:` rows via `wire_lines`
5. **`session_current`** — optional; pass `session` or set `MEMNET_SESSION`
6. **`read_get`** — single-row lookup by id
7. **`housekeep_stats`** — caps / row counts when graph grows

Full envelope and errors: [mcp-policy.md](mcp-policy.md). **Atomisation rules:** [atomisation.md](atomisation.md).

## Tools

| Tool | Required args | Optional args | Notes |
|------|---------------|---------------|-------|
| `serve_status` | — | — | Returns `{ running, host, port }` only |
| `session_open` | `map_lines` **or** `map_file` | `ttl` (minutes), **`seed_lines`** (list of `@TAG:` rows) | Auto-seeds **LAW01–LAW05** if missing; add **`seed_lines`** for `@CFG` + domain `@LAW` |
| `session_current` | — | `session` | Needs `session` arg or `MEMNET_SESSION` env |
| `query_warm` | `anchor` (string) | `depth` (default **2**), `max_rows` (default **50**), `session` | **Primary read** — always anchored |
| `add` | `wire_lines` (list[str]) | `allow_new_relation`, `agent`, `session` | Create only; fails if id exists |
| `update` | `wire_lines` (list[str]) | `allow_new_relation`, `agent`, `session` | Replace only; fails if id missing |
| `read_get` | `id` | `session` | One row by id |
| `housekeep_stats` | — | `session` | `@STAT:` lines in `stdout` |

## Response envelope (all tools except `serve_status`)

```json
{
  "exit_code": 0,
  "stdout": "@LAW: …\n@MOD: …",
  "stderr": "@WRN: …",
  "session_id": "mn_…",
  "errors": ["@ERR: …"]
}
```

- Branch on **`exit_code`** and **`errors[]`**
- Parse **`stdout`** for `@TAG:` wire lines (`@LAW` always prepended on warm)
- **`wire_lines`** are joined with `\n` before send (remote serve needs **≥ 0.2.7**)

## Environment (mcp.json `env`)

| Variable | Purpose |
|----------|---------|
| `MEMNET_SERVE_HOST` | Serve bind target (default `127.0.0.1`) |
| `MEMNET_SERVE_PORT` | TCP port (default `18765`) |
| `MEMNET_SESSION` | Default session id after `session_open` |

## wire_lines format

One record per line:

```text
@TAG: field|field|field|…
```

Pipe in values: escape as `\|`. Batch many atoms in one `add`/`update` call.
