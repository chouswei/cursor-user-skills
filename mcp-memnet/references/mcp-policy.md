# MemNet MCP policy

```text
Cursor (stdio) -> memnet-mcp
                 ├─ in-process engine (default, single agent)
                 └─ TCP -> memnet serve (MEMNET_MCP_TRANSPORT=tcp)
```

- **Package and PyPI 0.19.5**. `session_open` needs a SCHEMA map. Cue then `pin_map`. Write **`mutate`**. leftover `add`/`update` / `query_warm` / `anchor=` named leftover (Path-B seed may still call leftover `add` internally).
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

Do **not** set serve host/port unless `MEMNET_MCP_TRANSPORT=tcp`. Live tip: key **`memnet`** / namespace **`user-memnet`**; URL owned by `mcp.json` only. InvenTree MCP is not MemNet.

## Tools (product)

`serve_status`, `session_open` / `list` / `close` / `save` / `load` / `current`, `pin_map`, `find`, `mutate`, `snap_model`, `ingest_*`, `export_pin_map`, `import_slice`, `reserve` / `extend` / `release`, `read_list`, `housekeep_stats`, CapsPolicy ACL opt-in.

leftover: `add`, `update`, `query_warm`, `query_walk`. No `read_get`.

Args: [tool-parameters.md](tool-parameters.md). Wire: [wire-format.md](wire-format.md).

## Errors

| Symptom | Action |
|---------|--------|
| Tools absent from catalog | Skip MemNet; plain Markdown |
| `serve_required` | Start `memnet serve` or stay in-process |
| `session_not_found` | `session_list`; `find(kind=TSK, locators=["goal=<this TSK_model_*>"], session=<id>)` per live id. Adopt only a session that already holds this campaign cue (if several of this cue, richer of those). MUST NOT take `session_list[0]` / `session_current` / a foreign catalog. `session_load` a snap only into a **new** id; MUST NOT load over a live catalog. `session_open` for this repo only when zero hits of this cue. |
| `unknown_tag` | Map at `session_open` is frozen. If the doctrine writes CLM/SYM/USR, those kinds MUST be in `map_lines` **before** first mutate. Do not keep using that session as campaign cache. |
| `no_map` | Pass `map_file` / `map_lines` |
| `limit_exceeded` | `session_list` for `sessions|n/max`; `session_close` unused strata of **this** campaign only |
| CueConflict | Do not pick one root. If the neighbourhood is a foreign package (session-mismatch), stop and retarget; MUST NOT mutate. SameThingAbsorb is a later Commit |

## MUST NOT

- Teach leftover NEW / leftover `--anchor` as TARGET.
- `rag_query`, Layer, pipe `@TAG`, TOON as agent I/O.
- Call tools that are not in the session catalog.
- Teach `hid` / `_memnet_hid` / `elementId` / nickname `id` on shaped `pin_map` / export / find emit.
- Treat old `memnet-pi` / `user-memnet-pi` as live. Live tip is key **`memnet`** / namespace **`user-memnet`** (`mcp.json` owns the URL).
