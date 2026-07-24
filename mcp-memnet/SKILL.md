---
name: mcp-memnet
description: >-
  MemNet MCP — generic in-memory NODE|EDGE graph: session management, live pin map,
  shared-dialect mutate via add/update. Triggers: memnet mcp, query_warm, pin map,
  session_open, shared dialect, Write=display, MutateGate, sysml memnet tools.
metadata:
  pattern: tool-wrapper
  version: "3.2"
  domain: memnet
  product: memnet-llm==0.3.1
---

# MemNet MCP (generic)

PyPI: **`memnet-llm` 0.3.1** (CLI `memnet`). Engine + generic MCP only — **novel-writer is out of scope**.

MemNet is working memory between LLM call pipelines and data search. Agents read a bounded **live pin map** each turn and write with the **same shapes** — the **shared dialect** (Write = display). Design docs may gloss this dialect as “Tier A”; prefer **shared dialect** in agent text.

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

**Tool gloss:** MCP/CLI pin-map read is still named `query_warm` / `query warm` until call sites rename. Formal shapes: MemNet `docs/grammar/` (`MemNet.g4`, golden fixtures) — do not invent a thinner dialect.

## How MCP tools fit the grammar

MCP is a **thin CLI adapter**. Grammar (`docs/grammar/`, `MemNet.g4`) defines **legal shared-dialect line shapes**. Tools do **not** invent a second dialect: pin-map and mutate payloads live in the JSON envelope’s **`stdout` / `wire_lines`** as shared-dialect text.

| MCP tool | Grammar role | What goes on the wire |
|----------|--------------|------------------------|
| `session_open` | Session lifecycle + schema map | `map_lines` = kind field schemas (not NODE/EDGE body). Optional `seed_lines` = shared-dialect rows (LAW auto-seeded). |
| `session_current` | Session lifecycle | Metadata only — no grammar body. |
| `session_save` / `session_load` | Snapshot persist / resume | File path; graph reloads; next pin map is still shared dialect. |
| `query_warm` | **Live pin map read** (legacy name) | `stdout` = bare present NODE/EDGE (+ LAW) — `presentNode` / `presentEdge` / `lawPin` in `MemNet.g4`. |
| `query_walk` | Hop debug (not primary pin map) | Walk lines for topology debug — prefer pin map for agent reason. |
| `add` | Mutate **create** | `wire_lines` = shared dialect with leading `+` and `[NEW]` / `NEW` as needed. |
| `update` | Mutate **patch / drop** | `wire_lines` = `~` / `-` on known ids (no invent). |
| `read_get` / `read_list` | Lookup / enumerate | Single-row or tag list; still shared-dialect (or engine render) — use to avoid inventing ids. |
| `housekeep_stats` | Caps / counts | Envelope stats — not NODE/EDGE body. |
| `serve_status` | Transport probe | `{running,host,port}` — TCP-oriented; optional under default in-process. |

**Agent loop ↔ grammar:** `query_warm` emits **bare present**; `add`/`update` accept **mutate ops** (`+`/`~`/`-`). Same field shapes = Write = display.

**Not weird dialect — transport envelope:** every tool except `serve_status` returns JSON `{exit_code, stdout, stderr, session_id, errors}`. Parse **`stdout`** for pin-map / row text. Do not treat the JSON keys as the MemNet grammar.

**Misfits (gloss, do not invent tools):**

| Looks odd | Why | Agent action |
|-----------|-----|--------------|
| Name `query_warm` | Pre–pin-map vocabulary | Treat as **live pin map** |
| Name `add` / `update` | CLI verbs, not `+`/`~` | Put ops **inside** `wire_lines`, not in the tool name |
| `serve_status` | Sounds required | Skip under in-process; use when `MEMNET_MCP_TRANSPORT=tcp` |
| No tool named `pin_map` / `mutate` | API kept stable | Skills use those words; MCP keeps CLI names |
| No novel-writer tools | Dropped from product | Do not expect them |

## Agent loop

```text
pin map → reason → mutate → pin map
```

1. Pin map — `query_warm(anchor=…, depth≤2)` — bare present.
2. Reason; copy assigned ids from the map.
3. `add` / `update` with **shared dialect** mutate lines.
4. `session_save` when durability is needed.

## Essential tools (quick)

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

Args detail: [references/tool-parameters.md](references/tool-parameters.md). Policy: [references/mcp-policy.md](references/mcp-policy.md). Full map: [references/tool-grammar.md](references/tool-grammar.md).

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
| [references/tool-grammar.md](references/tool-grammar.md) | MCP tool <-> grammar map |
| MemNet `README.md` / `docs/grammar/` | Product SSOT |
