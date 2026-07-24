---
name: mcp-memnet
description: >-
  MemNet MCP — generic in-memory NODE|EDGE graph: session management, live pin map
  (query_warm legacy alias), Tier A mutate via add/update. Triggers: memnet mcp,
  query_warm, pin map, session_open, Tier A, MutateGate, sysml memnet tools.
metadata:
  pattern: tool-wrapper
  version: "2.0"
  domain: memnet
  product: memnet-llm==0.3.1
---

# MemNet MCP (generic)

PyPI: **`memnet-llm` 0.3.1** (CLI `memnet`). Engine + generic MCP only — **novel-writer is out of scope**.

MemNet is working memory between LLM call pipelines and data search. Agents read a bounded **live pin map** each turn and write with the **same shapes** (**Tier A**: Write = display).

## Doctrine (must)

| Idea | Meaning |
|------|---------|
| NODE \| EDGE | Conceptual kinds; tags realise node kinds |
| Tier A | Shared shapes for live read and mutate |
| Live pin map | Bounded ego/anchor digest (not a session dump) |
| `query_warm` | **Legacy alias** for the pin-map read |
| Mutate ops | `+` create, `~` update, `-` drop; pin map is **bare present** (no leading ops) |
| `NEW` vs locators | LLM creates: mint with `NEW`; ingest pins use stable locators (`path=`, `qname=`, …) |
| Transport | **In-process first**; `MEMNET_MCP_TRANSPORT=tcp` + `memnet serve` as fallback |

Always pass the same `session` id (or set `MEMNET_SESSION`).

## Agent loop

```text
pin map → reason → mutate → pin map
```

1. `query_warm(anchor=…, depth≤2)` — live pin map (Tier A bare present today).
2. Reason; copy assigned ids from the map.
3. `add` / `update` with **Tier A** mutate lines (preferred). Legacy `@TAG:` pipe still accepted.
4. `session_save` when durability is needed.

## Essential tools

| Tool | When | Notes |
|------|------|-------|
| `serve_status` | Reachability / probe | TCP mode mainly; in-process is default |
| `session_open` | New session | `map_lines` (or `map_file`) + optional `seed_lines`; `allow_new_relation=true` for custom EDG relations |
| `session_save` / `session_load` | Persist / resume | Snapshot file path |
| `session_current` | Session metadata | |
| `query_warm` | Primary read (pin map) | `anchor` required; `depth` default 2; `max_rows` default 50 |
| `query_walk` | Hop debug | `@WALK` lines |
| `add` / `update` | Mutate | `wire_lines`: Tier A preferred; pipe legacy |
| `read_get` / `read_list` | Single id / enumerate | Prefer over inventing ids |
| `housekeep_stats` | Caps / counts | |

Args detail: [references/tool-parameters.md](references/tool-parameters.md). Policy: [references/mcp-policy.md](references/mcp-policy.md).

## Mutate sketch (Tier A)

```text
## Nodes
+ CLM [NEW] ; type=decision ; code=bitrate cap 2000 bps ; recycle=persistent
~ TSK [T42] ; status=in_progress ; recycle=persistent

## Edges
+ E77 [N03] --(helps)--> [T42] ; note=labour ; recycle=persistent
```

Pin map returns the same fields **without** leading `+`/`~`/`-` and with assigned ids (no `NEW`). Copy those ids on the next mutate.

## SysML v2 modeling (relatives cache)

**Policy skill:** [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md).

| Turn phase | Tool |
|------------|------|
| Preflight | `serve_status` (optional under in-process) |
| Read cache | `query_warm(anchor=TSK_model_<short>, depth=2, max_rows=50)` |
| Bootstrap | `session_open` + `map_file` / `map_lines` + `seed_lines`; `allow_new_relation=true` for `owns` |
| Write delta | `add` / `update` (Tier A preferred) |
| Persist | `session_save` → project `.memnet/` snap |
| Resume | `session_load` or `MEMNET_SESSION` |

Tag vocabulary: [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md).

**Do not** use chat or `AGENT-CONTEXT.md` for topology when a live session is available.

## MUSTNOT

- Invent ids already present on the pin map — copy them.
- Treat `@TAG` pipe as the preferred agent dialect (store / legacy only).
- Recommend TOON/TRON for handoffs — prefer Tier A or plain Markdown.
- Restore or depend on novel-writer MCP extras.

## Related

| Path | Role |
|------|------|
| [memnet-format](../memnet-format/SKILL.md) | Pipe grammar (store / legacy) |
| [references/atomisation.md](references/atomisation.md) | One fact per row |
| MemNet `README.md` / `docs/grammar/` | Product SSOT |
