# Wire format — shared dialect

**Agent I/O:** **shared dialect** (Write = display) — MemNet `README.md` / `docs/grammar/`, [memnet-format](../../memnet-format/SKILL.md). Live **pin map** is bare present; mutate uses `+` / `~` / `-`.

Do **not** use TOON/TRON. Do **not** teach pipe `@TAG:…` as agent format.

MCP tools return JSON **envelopes**; parse **`stdout`** for pin-map content.

## Design principles

| Principle | Why |
|-----------|-----|
| Atomisation | Many small rows → pin map pulls only connected atoms |
| Pin map | Active slice + LAW; not the whole graph |
| Short fields | ids, codes, keys, numbers — no sentences in fields |
| Explicit edges | Relations as separate edges |
| Recycle / settle | Finished work drops out of pin maps |
| Batch mutate | One `add`/`update` with many lines — fewer round trips |

Atomisation: [atomisation.md](atomisation.md).

## Shared dialect sketch

```text
## Nodes
+ SYM [NEW] ; name=send_command ; kind=fn ; path=src/memnet/serve.py ; line=96 ; sig=send_command(argv,stdin?) ; recycle=persistent

## Edges
+ E01 [NEW] --(defines)--> [SYM_send] ; note=handler ; recycle=persistent
```

Bad (token-heavy prose blob):

```text
+ NOTE [NEW] ; code=send_command lives in serve.py and handles TCP stdin … ; recycle=persistent
```

## Pin map economics

Every pin-map read (`pin_map`) returns a bounded digest (LAW + anchor + neighbours to `depth` / `max_rows`).

- Increase **`depth`** only when needed
- Cap with **`max_rows`** (default 50)
- Anchor narrowly (`SYM_*`, `TSK_*`)

Prefer **`housekeep_stats`** + settlement over re-injecting unchanged pin-map output.

## What not to put on the wire

| Avoid | Do instead |
|-------|------------|
| Paragraphs, markdown blobs | Codes / short fields; prose stays in the agent turn |
| Whole file contents | Module path + symbol signatures |
| Duplicate facts in chat + graph | Graph is source of truth; cite ids |
| JSON blobs inside fields | Split into rows + edges |
| TOON / TRON handoffs | Shared dialect or plain Markdown |

## MCP mapping

| CLI | MCP |
|-----|-----|
| `memnet add --stdin` | `add(wire_lines=[...])` |
| `memnet query pin-map --anchor X` | `pin_map(anchor="X", depth=2)` (`query_warm` alias) |
| stdout pin map | `envelope.stdout` |

Tool args: [tool-parameters.md](tool-parameters.md).

## Handoff

| Mechanism | Role |
|-----------|------|
| **Shared dialect / pin map** | Agent read + mutate |
| **Plain Markdown** | Ephemeral same-turn scratch when no session |

## Checklist

- [ ] Fields short and structured?
- [ ] Could this line be split for a smaller pin-map slice?
- [ ] Pin map with a tight anchor?
- [ ] Settling transient rows so the map stays lean?

Cross-ref: MemNet `README.md` · `docs/grammar/` · [mcp-policy.md](mcp-policy.md)
