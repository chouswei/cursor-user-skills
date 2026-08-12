---
name: mcp-memnet
description: >-
  MemNet MCP — generic in-memory NODE|EDGE graph: session management, live pin map,
  shared-dialect mutate via add/update. Triggers: memnet mcp, pin_map, query_warm,
  pin map, session_open, shared dialect, Write=display, MutateGate, sysml memnet tools.
metadata:
  pattern: tool-wrapper
  version: "4.1"
  domain: memnet
  product: memnet-llm==0.4.2
---

# MemNet MCP (generic)

Product **`memnet-llm` 0.4.2** (CLI `memnet`). Engine + generic MCP only — **novel-writer is out of scope**.

MemNet is working memory between LLM call pipelines and data search. Agents read a bounded **live pin map** each turn and write with the **same shapes** — the **shared dialect** (Write = display). Design docs may gloss this dialect as "Tier A"; prefer **shared dialect** in agent text.

## User-pack transport (this machine)

| Role | Where |
|------|--------|
| **Cursor MCP** | HTTP `url` → **`http://10.0.0.10:18766/mcp`** (0.4.2 streamable-http + Bearer) |
| **Pi graph store** | Prefer TCP `memnet serve` **`:18765`** with HTTP MCP set `MEMNET_MCP_TRANSPORT=tcp` (same graph) |
| Local stdio `command` | Optional `memnet-local` only — not the primary `memnet-pi` path |

Cursor `~/.cursor/mcp.json` → primary server id **`memnet-pi`** (Cursor may show it as `user-memnet-pi`). Shape matches Inventree-style `url` + `headers` (no local `command` / `env`):

```json
"memnet-pi": {
  "url": "http://10.0.0.10:18766/mcp",
  "headers": {
    "Authorization": "Bearer <token>"
  }
}
```

After editing mcp.json: **Cursor → MCP / Tools → restart `memnet-pi`** (or reload the window). Do **not** dual-run InProcess HTTP MCP against a separate TCP store without `MEMNET_MCP_TRANSPORT=tcp` on the Pi HTTP process.

## Doctrine (must)

| Idea | Meaning |
|------|---------|
| NODE \| EDGE | Conceptual kinds; tags realise node kinds |
| Shared dialect | Same shapes for live read and mutate (Write = display) |
| Live pin map | Bounded ego/anchor digest (not a session dump); **primary read** |
| Mutate ops | `+` create, `~` update, `-` drop; pin map is **bare present** (no leading ops) |
| `NEW` vs locators | LLM creates: mint with `NEW`; ingest pins use stable locators (`path=`, `qname=`, …) |
| Transport (user pack) | **HTTP `:18766/mcp` → Pi**; bridge HTTP MCP to TCP serve `:18765` when sharing one graph |
| Layer / `view=` (0.4) | Optional `pin_map(view=shell\|interior\|…)`; dual EDGE bind/relation — see MemNet `docs/grammar/memnet-multi-layer.md` |

Always pass the same `session` id (or set `MEMNET_SESSION`).

**Tool gloss:** Primary pin-map read is MCP `pin_map` / CLI `query pin-map`. Optional **`view=`** (`shell` \| `interior`; soft-accept `flowchart` \| `parts` \| `statechart`). Omit `view` for 0.3-style `depth`/`max_rows` only. `query_warm` / `query warm` are **deprecated aliases**. Formal shapes: MemNet `docs/grammar/` — do not invent a thinner dialect.

## How MCP tools fit the grammar

MCP is a **thin CLI adapter**. Grammar (`docs/grammar/`, `MemNet.g4`) defines **legal shared-dialect line shapes**. Tools do **not** invent a second dialect: pin-map and mutate payloads live in the JSON envelope's **`stdout` / `wire_lines`** as shared-dialect text.

| MCP tool | Grammar role | What goes on the wire |
|----------|--------------|------------------------|
| `session_open` | Session lifecycle + schema map | `map_lines` = `SCHEMA KIND ; fields=id …` rows (registry, not graph NODE/EDGE). Optional `seed_lines` = shared-dialect rows (LAW auto-seeded). |
| `session_current` | Session lifecycle | Metadata only — no grammar body. |
| `session_save` / `session_load` | Snapshot persist / resume | File path; graph reloads; next pin map is still shared dialect. |
| `pin_map` | **Live pin map read** | `stdout` = bare present NODE/EDGE (+ LAW). Optional arg `view`. |
| `query_warm` | Deprecated alias for `pin_map` | Same as `pin_map` (including `view`). |
| `query_walk` | Hop debug (not primary pin map) | Walk lines for topology debug — prefer pin map for agent reason. |
| `add` | Mutate **create** | `wire_lines` = shared dialect with leading `+` and `[NEW]` / `NEW` as needed. |
| `update` | Mutate **patch / drop** | `wire_lines` = `~` / `-` on known ids (no invent). |
| `read_get` / `read_list` | Lookup / enumerate | Single-row or tag list; still shared-dialect (or engine render) — use to avoid inventing ids. |
| `housekeep_stats` | Caps / counts | Envelope stats — not NODE/EDGE body. |
| `serve_status` | Transport probe | `{running,host,port}` — TCP-oriented; optional under default in-process. |

**Agent loop ↔ grammar:** `pin_map` emits **bare present**; `add`/`update` accept **mutate ops** (`+`/`~`/`-`). Same field shapes = Write = display.

**Not weird dialect — transport envelope:** every tool except `serve_status` returns JSON `{exit_code, stdout, stderr, session_id, errors}`. Parse **`stdout`** for pin-map / row text. Do not treat the JSON keys as the MemNet grammar.

**Misfits (gloss, do not invent tools):**

| Looks odd | Why | Agent action |
|-----------|-----|--------------|
| Name `query_warm` | Legacy alias | Use **`pin_map`**; alias kept for old call sites |
| Name `add` / `update` | CLI verbs, not `+`/`~` | Put ops **inside** `wire_lines`, not in the tool name |
| `serve_status` | Sounds optional | User pack: TCP store probe (`10.0.0.10:18765`); Cursor itself uses HTTP `:18766/mcp` |
| No tool named `mutate` | API kept stable | Mutate via `add` / `update` with ops in `wire_lines` |
| No novel-writer tools | Dropped from product | Do not expect them |

## Agent loop

```text
pin map → reason → mutate → pin map
```

1. Pin map — `pin_map(anchor=…, depth≤2)` — bare present; optional `view=shell` (tight) or `view=interior`.
2. Reason; copy assigned ids from the map.
3. `add` / `update` with **shared dialect** mutate lines.
4. `session_save` when durability is needed.

**MCP missing:** if MemNet tools are not in the session catalog, skip this loop — plain Markdown scratch only (no TOON/TRON). Do not invent tool calls. Dialect shapes: [memnet-format](../memnet-format/SKILL.md).

## Graph about a node or edge

| Want | Tool | Why |
|------|------|-----|
| Neighbourhood / ego slice (primary) | `pin_map` | Live **pin map**: LAW + NODE + EDGE in shared dialect (`stdout`) |
| Hop listing only | `query_walk` | Debug topology (`@WALK: …`); not the reason loop |
| One known id | `read_get` | Single row; not a full neighbourhood |
| Find ids by tag / field | `read_list` | Enumerate first; then pin map on a real id |

**Recipe (node):** resolve id if needed (`read_list` / prior pin map) → `pin_map(anchor=<node_id>, depth=2, max_rows=50, session=…)` → parse envelope **`stdout`** (bare present). Raise `depth` only if the slice is too thin; keep `max_rows` bounded.

**Recipe (edge → its two NODE ids):** there is **no** separate “get nodes of edge” tool. Endpoints are **on the EDGE row**.

1. Obtain the EDGE line: `read_get(id=<edge_id>)`, or copy the EDGE line already in a pin-map `stdout`.
2. **Parse endpoints** (copy those values — they *are* the node ids):
   - **Shared dialect** (pin map / mutate): `Eid [from] --(rel)--> [to]` — first `[…]` = source node, second `[…]` = destination node. Not trailing `from=` / `to=` / `src=` keys.
   - **Legacy pipe** (`read_get` / `read_list` still emit `@EDG:…`): `@EDG: <id>|<src>|<relation>|<dist>|…` — columns `src` and `dist` (store field names; grammar abstract model says `from`/`to`).
3. Optional: `read_get(id=<node>)` for each full NODE row; or `pin_map(anchor=<endpoint>, …)` for that node’s neighbourhood. Do **not** use the edge id as a pin-map anchor. Do not invent ids.

## When ids must match model / schematic

**Decision:** pin into SysML / `.ato` / codebase / skill → **stable locator** (deterministic ground id + locator fields). New MemNet-only fact → **`[NEW]`**. Do not conflate ingest with goldfish mutate.

| Need | Tool |
|------|------|
| Find by schematic field | `read_list(tag=…, where=["refdes=R1"])` (or `net=`, `qname=`, `path=`) |
| Confirm one ground id | `read_get(id=ATO_R1)` |
| Neighbourhood | `pin_map(anchor=ATO_R1, …)` |
| First materialise pin | `add` with **explicit** id + locators (not `NEW`) |
| Annotate about a pin | `add` with `+ CLM [NEW] …` then edge to the **copied** pin id |

```text
+ CMP [ATO_R1] ; refdes=R1 ; path=boards/pdu/pdu.ato ; recycle=persistent
~ [ATO_R1] ; value=10k ; recycle=persistent
+ CLM [NEW] ; type=decision ; code=keep R1 10k ; recycle=persistent
```

**Forbidden:** client `NEW` for R1/U2/nets/SysML qnames/paths; inventing `C_rand_99`; `NEW` on `~`. **Pitfall:** `add` fails if id exists — look up first. PinMapIngest_* may be stubs; seed via `seed_lines` / explicit-id `add` until ingest lands. Doctrine: MemNet `docs/grammar/` §4.2.1.

**Re-id (wrong ground id):** `update` with `~ [OldId] ; id=NewId` (patch omits kind — id is in brackets only). If `NewId` exists → `id_occupied` unless `; merge=true` (nodes only; fold mistaken mint into locator id; retarget edges; drop OldId). Self `id=OldId` is a no-op. Not the MCP tool rename `query_warm`→`pin_map`.

```text
~ [C_rand_99] ; id=ATO_R1 ; merge=true ; recycle=persistent
```

## Multi-agent reserve (design — not yet shipped)

Neighbourhood **reserve** with holder **`llm_id`** + **TTL** prevents same-session write races. MCP sketch (next minor):

```text
reserve(session, anchor, depth=2, llm_id, ttl_s=120) -> rid, until
extend(session, rid|anchor, llm_id, ttl_s=120) -> until
release(session, rid|anchor, llm_id) -> ok
```

Pin map may show intersecting leases as **bare present** (shared dialect only):

```text
## Reserves
RSV [R7] ; llm_id=coder_a ; anchor=ATO_R1 ; depth=2 ; until=2026-07-24T08:15:00Z ; left_s=87
```

**Never** `@RSV:` pipe. SSOT: MemNet `docs/grammar/memnet-neighbourhood-reserve.md`. Mutate on reserved ids requires matching `llm_id`.

## Essential tools (quick)

| Tool | When | Notes |
|------|------|-------|
| `serve_status` | Reachability / probe | TCP serve `:18765` when HTTP MCP bridges; Cursor entry is `:18766/mcp` |
| `session_open` | New session | `map_lines` (or `map_file`) + optional `seed_lines`; `allow_new_relation=true` for custom EDG relations |
| `session_save` / `session_load` | Persist / resume | Snapshot file path |
| `session_current` | Session metadata | |
| `pin_map` | **Primary read** = pin map | `anchor` required; `depth`/`max_rows`; optional `view` |
| `query_warm` | Legacy alias for `pin_map` | Same params |
| `query_walk` | Hop debug | |
| `add` / `update` | Mutate | `wire_lines`: shared dialect |
| `read_get` / `read_list` | Single id / enumerate | Prefer over inventing ids |
| `housekeep_stats` | Caps / counts | |

Args detail: [references/tool-parameters.md](references/tool-parameters.md). Policy: [references/mcp-policy.md](references/mcp-policy.md). Full map: [references/tool-grammar.md](references/tool-grammar.md).

## Shared dialect (wire shapes)

Line shapes, mutate ops, and examples: [memnet-format](../memnet-format/SKILL.md). Formal SSOT: MemNet `docs/grammar/` (`MemNet.g4`, golden fixtures).

## SysML v2 modeling (relatives cache)

**Policy skill:** [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md).

| Turn phase | Tool |
|------------|------|
| Preflight | MemNet MCP in catalog? Then optional `serve_status` (TCP only) |
| Read cache | pin map — `pin_map(anchor=TSK_model_<short>, depth=2, max_rows=50)` |
| Bootstrap | `session_open` + `map_file` / `map_lines` + `seed_lines`; `allow_new_relation=true` for `owns` |
| Write delta | `add` / `update` (shared dialect) |
| Persist | `session_save` → project `.memnet/` snap |
| Resume | `session_load` or `MEMNET_SESSION` |

Tag vocabulary: [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md).

**Do not** use chat or `AGENT-CONTEXT.md` for topology when a live session is available.

## MUSTNOT

- Invent ids already present on the pin map — copy them.
- Emit pipe `@TAG:...` rows as agent I/O -- shared dialect only. Includes `@RSV:` — use `RSV [rid] ; llm_id=…` present lines instead.
- Recommend TOON/TRON for handoffs — prefer shared dialect or plain Markdown.
- Restore or depend on novel-writer MCP extras.

## Related

| Path | Role |
|------|------|
| [memnet-format](../memnet-format/SKILL.md) | Shared dialect |
| [references/atomisation.md](references/atomisation.md) | One fact per row |
| [references/tool-grammar.md](references/tool-grammar.md) | MCP tool <-> grammar map |
| MemNet `README.md` / `docs/grammar/` | Product SSOT |
