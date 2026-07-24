---
name: mcp-memnet
description: >-
  MemNet MCP — generic in-memory NODE|EDGE graph: session management, live pin map,
  shared-dialect mutate via add/update. Triggers: memnet mcp, query_warm, pin map,
  session_open, shared dialect, Write=display, MutateGate, sysml memnet tools.
metadata:
  pattern: tool-wrapper
  version: "3.0"
  domain: memnet
  product: memnet-llm==0.3.1
---

# MemNet MCP (generic)

PyPI: **`memnet-llm` 0.3.1** (CLI `memnet`). Engine + generic MCP only — **novel-writer is out of scope**.

MemNet is working memory between LLM call pipelines and data search. Agents read a bounded **live pin map** each turn and write with the **same shapes** — the **shared dialect** (Write = display).

## Doctrine (must)

| Idea | Meaning |
|------|---------|
| NODE \| EDGE | Conceptual kinds; tags realise node kinds |
| Shared dialect | Same shapes for live read and mutate (Write = display) |
| Live pin map | Bounded ego/anchor digest (not a session dump); **primary read** |
| Mutate ops | `+` create, `~` update, `-` drop; pin map is **bare present** (no leading ops) |
| `NEW` vs locators | LLM creates: mint with `NEW`; ingest pins use stable locators (`path=`, `qname=`, …) |
| Transport | **In-process first**; `MEMNET_MCP_TRANSPORT=tcp` + `memnet serve` as fallback |

Always pass the same `session` id (or set `MEMNET_SESSION`).

Gloss: the MCP/CLI pin-map tool may still be named `query_warm` / `query warm`.

## Agent loop

```text
pin map → reason → mutate → pin map
```

1. Pin map — `query_warm(anchor=…, depth≤2)` — bare present.
2. Reason; copy assigned ids from the map.
3. `add` / `update` with **shared dialect** mutate lines.
4. `session_save` when durability is needed.

## Essential tools

| Tool | When | Notes |
|------|------|-------|
| `serve_status` | Reachability / probe | TCP mode mainly; in-process is default |
| `session_open` | New session | `map_lines` (or `map_file`) + optional `seed_lines`; `allow_new_relation=true` for custom EDG relations |
| `session_save` / `session_load` | Persist / resume | Snapshot file path |
| `session_current` | Session metadata | |
| `query_warm` | **Primary read** = pin map | `anchor` required; `depth` default 2; `max_rows` default 50 |
| `query_walk` | Hop debug | |
| `add` / `update` | Mutate | `wire_lines`: shared dialect |
| `read_get` / `read_list` | Single id / enumerate | Prefer over inventing ids |
| `housekeep_stats` | Caps / counts | |

Args detail: [references/tool-parameters.md](references/tool-parameters.md). Policy: [references/mcp-policy.md](references/mcp-policy.md).

## Mutate sketch (shared dialect)

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
| Read cache | pin map — `query_warm(anchor=TSK_model_<short>, depth=2, max_rows=50)` |
| Bootstrap | `session_open` + `map_file` / `map_lines` + `seed_lines`; `allow_new_relation=true` for `owns` |
| Write delta | `add` / `update` (shared dialect) |
| Persist | `session_save` → project `.memnet/` snap |
| Resume | `session_load` or `MEMNET_SESSION` |

Tag vocabulary: [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md).

**Do not** use chat or `AGENT-CONTEXT.md` for topology when a live session is available.

## MUSTNOT

- Invent ids already present on the pin map — copy them.
- Emit pipe `@TAG:...` rows as agent I/O -- shared dialect only.
- Recommend TOON/TRON for handoffs — prefer shared dialect or plain Markdown.
- Restore or depend on novel-writer MCP extras.

## Related

| Path | Role |
|------|------|
| [memnet-format](../memnet-format/SKILL.md) | Shared dialect |
| [references/atomisation.md](references/atomisation.md) | One fact per row |
| MemNet `README.md` / `docs/grammar/` | Product SSOT |
