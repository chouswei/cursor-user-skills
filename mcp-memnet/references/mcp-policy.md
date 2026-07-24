# MemNet MCP policy

## Architecture

```
Cursor (stdio) → memnet-mcp (PC) → TCP → memnet serve (local or LAN) → in-memory graph
```

- MCP is a thin adapter; it does **not** hold session state or auto-spawn `memnet serve`.
- Wire output (`@TAG:` lines) is passed through verbatim in tool JSON envelopes.
- The graph is a **knowledge graph** (nodes + `@EDG` edges). **Atomisation** + **compact wire format** — see [atomisation.md](atomisation.md), [wire-format.md](wire-format.md).

## mcp.json (user pack)

```json
"memnet": {
  "command": "memnet-mcp",
  "args": [],
  "env": {
    "MEMNET_SERVE_HOST": "<serve-host>",
    "MEMNET_SERVE_PORT": "18765",
    "MEMNET_SESSION": "mn_…"
  }
}
```

Use full path to `memnet-mcp.exe` on Windows if not on PATH. Set host to LAN IP when serve runs on another machine (e.g. Raspberry Pi). Restart Cursor after edits.

## v1 tools

See [tool-parameters.md](tool-parameters.md) for args, defaults, and invoke order.

| Tool | Purpose |
|------|---------|
| `serve_status` | Probe reachability |
| `session_open` | New session — prefer **`map_lines`** over **`map_file`** |
| `session_current` | Session metadata |
| `query_warm` | **Primary read** — anchor + depth + max_rows |
| `add` / `update` | Atomised rows via `wire_lines` |
| `read_get` | Single row by id |
| `housekeep_stats` | Counts vs caps |

## Response envelope

Every tool (except `serve_status`) returns JSON text:

```json
{
  "exit_code": 0,
  "stdout": "@LAW: …",
  "stderr": "@WRN: …",
  "session_id": "mn_…",
  "errors": []
}
```

Branch on **`errors[]`** and **`exit_code`**. Parse **`stdout`** for `@TAG:` rows.

## Domain references

| Topic | Doc |
|-------|-----|
| Wire format / token efficiency | [wire-format.md](wire-format.md) |
| Atomisation (required) | [atomisation.md](atomisation.md) |
| Article breakdown | [article-breakdown.md](article-breakdown.md) |
| Coding memory | [coding-memory.md](coding-memory.md) |
| User input | [user-input-memory.md](user-input-memory.md) |
| Goldfish loop | [memnet-goldfish-loop.mdc](../../../rules/memnet-goldfish-loop.mdc) |

## Errors

| Symptom | Action |
|---------|--------|
| `serve_required` | Fix `memnet serve` reachability on `MEMNET_SERVE_HOST` |
| `session_not_found` | `session_open` or set `MEMNET_SESSION` |
| `id_exists` on add | Use `update` instead |
| `not_found` on update | Use `add` or fix id from warm output |

## LAN notes

- No auth/TLS — trusted LAN only.
- Remote **`add`/`update`** require serve **≥ 0.2.7** (TCP `stdin` field for wire batches).
