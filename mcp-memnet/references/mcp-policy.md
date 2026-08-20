# MemNet MCP policy

```text
Cursor (stdio) -> memnet-mcp
                 ├─ in-process engine (default, single agent)
                 └─ TCP -> memnet serve (MEMNET_MCP_TRANSPORT=tcp)
```

- **Package and PyPI 0.19.3**. `session_open` needs a SCHEMA map. Cue then `pin_map`. Write **`mutate`**. leftover `add`/`update` / `query_warm` / `anchor=` named leftover (Path-B seed may still call leftover `add` internally).
- Multitask **MUST NOT** use in-process MCP for a shared session.
- Live Agens claimed (0.7); Neo4j live claimed (0.14); RSV + Path-B ingest + `snap_model` + `export_pin_map` shipped.
- Novel-writer MCP is dropped.

## mcp.json (this repo / local)

```json
"memnet": {
  "command": "memnet-mcp",
  "args": [],
  "env": { "MEMNET_WORKSPACE_ROOT": "<checkout>" }
}
```

Do **not** set serve host/port unless `MEMNET_MCP_TRANSPORT=tcp`. User-pack primary remote: HTTP **`memnet-pi`** `http://10.0.0.10:18766/mcp` bridging TCP serve **`:18765`**. InvenTree MCP is not MemNet.

## Tools (product)

`serve_status`, `session_open` / `list` / `close` / `save` / `load` / `current`, `pin_map`, `find`, `mutate`, `snap_model`, `ingest_*`, `export_pin_map`, `import_slice`, `reserve` / `extend` / `release`, `read_list`, `housekeep_stats`, CapsPolicy ACL opt-in.

leftover: `add`, `update`, `query_warm`, `query_walk`. No `read_get`.

Args: [tool-parameters.md](tool-parameters.md). Wire: [wire-format.md](wire-format.md).

## Errors

| Symptom | Action |
|---------|--------|
| Tools absent from catalog | Skip MemNet; plain Markdown |
| `serve_required` | Start `memnet serve` or stay in-process |
| `session_not_found` | `session_open` / `session_load` |
| `no_map` | Pass `map_file` / `map_lines` |
| `limit_exceeded` | `session_list` for `sessions|n/max`; `session_close` unused strata |
| CueConflict | Do not pick one root; SameThingAbsorb is a later Commit |

## MUST NOT

- Teach leftover NEW / leftover `--anchor` as TARGET.
- `rag_query`, Layer, pipe `@TAG`, TOON as agent I/O.
- Call tools that are not in the session catalog.
