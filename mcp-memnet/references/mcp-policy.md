# MemNet MCP policy

## Architecture

```text
Cursor (stdio) → memnet-mcp
                 ├─ in-process engine (default)
                 └─ TCP → memnet serve (MEMNET_MCP_TRANSPORT=tcp)
```

- MCP is a thin adapter. Default transport is **in-process** (no separate `memnet serve` required).
- Set `MEMNET_MCP_TRANSPORT=tcp` only when bridging to an external serve.
- Agent dialect is **Tier A** (Write = display). Legacy `@TAG:` pipe remains accepted on mutate and may appear in older snapshots.
- Primary read is the live **pin map** via `query_warm` (legacy name).

## mcp.json (user pack)

```json
"memnet": {
  "command": "memnet-mcp",
  "args": [],
  "env": {
    "MEMNET_SESSION": "mn_…"
  }
}
```

Optional TCP:

```json
"env": {
  "MEMNET_MCP_TRANSPORT": "tcp",
  "MEMNET_SERVE_HOST": "127.0.0.1",
  "MEMNET_SERVE_PORT": "18765",
  "MEMNET_SESSION": "mn_…"
}
```

Use full path to `memnet-mcp` on Windows if not on PATH. Restart Cursor after edits.

## Tools

See [tool-parameters.md](tool-parameters.md).

| Tool | Purpose |
|------|---------|
| `serve_status` | Probe (mainly TCP) |
| `session_open` / `save` / `load` / `current` | Session lifecycle |
| `query_warm` | Live pin map (legacy name) |
| `query_walk` | Hop debug |
| `add` / `update` | Mutate (Tier A preferred) |
| `read_get` / `read_list` | Lookup / enumerate |
| `housekeep_stats` | Counts vs caps |

## Response envelope

Every tool (except `serve_status`) returns JSON text:

```json
{
  "exit_code": 0,
  "stdout": "…",
  "stderr": "@WRN: …",
  "session_id": "mn_…",
  "errors": []
}
```

Branch on **`errors[]`** and **`exit_code`**. Parse **`stdout`** for pin-map / wire content.

## Domain references

| Topic | Doc |
|-------|-----|
| Agent dialect / Tier A | MemNet `README.md`, `docs/grammar/` |
| Pipe grammar (store/legacy) | [wire-format.md](wire-format.md), [memnet-format](../../memnet-format/SKILL.md) |
| Atomisation | [atomisation.md](atomisation.md) |
| Coding memory | [coding-memory.md](coding-memory.md) |
| User input | [user-input-memory.md](user-input-memory.md) |

## Errors

| Symptom | Action |
|---------|--------|
| `serve_required` | Under TCP: start `memnet serve` or switch to in-process |
| `session_not_found` | `session_open` / `session_load` or set `MEMNET_SESSION` |
| `id_exists` on add | Use `update` or mint with `NEW` |
| `not_found` on update | Use `add` or fix id from pin map |

## MUSTNOT

- Depend on novel-writer MCP extras (dropped from MemNet product).
- Recommend TOON/TRON for agent handoffs — use Tier A or plain Markdown.
