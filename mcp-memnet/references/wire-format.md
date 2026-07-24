# Wire format — store and legacy pipe

**Agent-facing dialect (preferred):** **Tier A** Write = display — see MemNet `README.md` and `docs/grammar/`. Live **pin map** is bare present; mutate uses `+` / `~` / `-`.

This note covers the **legacy `@TAG:` pipe** still accepted on `add`/`update`, used in older snapshots, and referenced by domain tag maps. Prefer Tier A for new agent I/O. Do **not** use TOON/TRON.

MCP tools return JSON **envelopes**; parse **`stdout`** for pin-map / wire content.

## Design principles

| Principle | Why |
|-----------|-----|
| Atomisation | Many small rows → pin map pulls only connected atoms |
| Pin map (`query_warm`) | Active slice + LAW; not the whole graph |
| Short fields | ids, codes, keys, numbers — no sentences in fields |
| Explicit edges | Relations as separate rows / edges |
| Recycle / settle | Finished work drops out of warm reads |
| Batch mutate | One `add`/`update` with many lines — fewer round trips |

Atomisation: [atomisation.md](atomisation.md).

## Legacy pipe line shape

```text
@TAG: field|field|field|…
```

- One record per line
- Escape `|` in values: `\|`
- Control tags on stderr: `@ERR`, `@WRN`, `@STAT`, `@SESSION`

Example (coding — compact):

```text
@SYM: SYM_send|send_command|fn|src/memnet/serve.py|96|send_command(argv,stdin?)|active|persistent
@EDG: E01|MOD_serve|defines|SYM_send|handler|persistent
```

Bad (token-heavy):

```text
@NOTE: N01|send_command lives in serve.py and handles TCP stdin …|persistent
```

## Pin map economics

Every **`query_warm`** returns a bounded live pin map (LAW + anchor + neighbours to `depth` / `max_rows`).

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
| TOON / TRON handoffs | Tier A or plain Markdown |

## MCP mapping

| CLI | MCP |
|-----|-----|
| `memnet add --stdin` | `add(wire_lines=[...])` |
| `memnet query warm --anchor X` | `query_warm(anchor="X", depth=2)` |
| stdout pin map / wire | `envelope.stdout` |

Tool args: [tool-parameters.md](tool-parameters.md).

## Handoff

| Mechanism | Role |
|-----------|------|
| **Tier A / pin map** | Agent read + mutate (preferred) |
| **Legacy `@TAG` pipe** | Store / snapshots / older call sites |
| **Plain Markdown** | Ephemeral same-turn scratch when no session |

## Checklist

- [ ] Fields short and structured?
- [ ] Could this line be split for a smaller pin-map slice?
- [ ] Using `query_warm` with a tight anchor?
- [ ] Settling transient rows so the map stays lean?

Cross-ref: MemNet `README.md` · `docs/grammar/` · [mcp-policy.md](mcp-policy.md)
