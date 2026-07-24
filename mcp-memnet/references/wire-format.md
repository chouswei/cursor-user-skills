# Wire format — token-efficient graph language

MemNet’s **wire format** is the LLM-facing output: one **`@TAG:` line per record**, fields separated by **`|`** — no JSON graph on the wire for model consumption. It is designed for **token efficiency** together with **atomisation** and **`query_warm`**.

MCP tools return JSON **envelopes** at the tool boundary; parse **`stdout`** for wire lines only.

## Design principles

| Principle | Why it saves tokens |
|-----------|---------------------|
| **Pipe rows, not JSON trees** | `@MOD: id\|path\|summary` beats nested objects; ~chars/3.2 tok for typical lines |
| **Atomisation** | Many small rows → warm pulls **only connected atoms** |
| **`query warm`, not cold context** | Active slice + `@LAW`; cold store warns `stale_in_store` |
| **Short fields** | ids, codes, keys, numbers — **no sentences** in fields |
| **`@EDG` not embedded lists** | Relations are separate one-line edges |
| **Recycle / settle** | Finished work drops out of warm reads |
| **Batch ingest** | One `add`/`update` with many `wire_lines` — fewer round trips |

Atomisation rules: [atomisation.md](atomisation.md).

## Wire line shape

```text
@TAG: field|field|field|…
```

- One record per line
- Escape `|` in values: `\|`
- Control tags on stderr: `@ERR`, `@WRN`, `@STAT`, `@SESSION`
- Data rows on stdout

Example (coding — compact):

```text
@SYM: SYM_send|send_command|fn|src/memnet/serve.py|96|send_command(argv,stdin?)|active|persistent
@EDG: E01|MOD_serve|defines|SYM_send|handler|persistent
```

Bad (token-heavy, breaks warm):

```text
@NOTE: N01|send_command lives in serve.py and handles TCP stdin for MCP add/update when the Pi runs 0.2.7 or later|persistent
```

## Warm read economics

Every **`query_warm`** prepends compact **`@LAW:`** rows (protocol discipline), then anchor + EDG-neighbours to **`depth`** / **`max_rows`**.

```text
Cost per turn ≈ LAW overhead + connected atoms (not whole graph)
```

- Increase **`depth`** only when the task needs more hops
- Cap with **`max_rows`** (default 50)
- Anchor narrowly (`SYM_*`, `TSK_*`) — not “everything about the project”

Prefer **`housekeep stats`** + settlement over re-injecting unchanged warm output (see `LLM-GUIDE`: `@STAT: modified`).

## What not to put on the wire

| Avoid | Do instead |
|-------|------------|
| Paragraphs, markdown, novel prose | Generate prose in the agent turn; store **codes** in graph |
| Whole file contents | `@MOD` path + `@SYM` signatures |
| Duplicate facts in chat + graph | Graph is source of truth; cite wire ids |
| JSON blobs inside fields | Split into rows + `@EDG` |
| `query context` for normal turns | **`query_warm`** with anchor |

## MCP mapping

| CLI / wire | MCP |
|------------|-----|
| `memnet add --stdin` | `add(wire_lines=[...])` |
| `memnet query warm --anchor X` | `query_warm(anchor="X", depth=2)` |
| stdout `@TAG:` lines | `envelope.stdout` — parse as text |

Tool args: [tool-parameters.md](tool-parameters.md).

## Handoff vs wire format

| Mechanism | Role |
|-----------|------|
| **MemNet wire** | Durable **graph store** + **pipeline step log** (`@CLM` type=`pipe`) when serve up |
| **Plain Markdown / prose** | In-prompt handoff when **serve down** or ephemeral same-turn scratch (do not use TOON/TRON) |

## Token estimate (rule of thumb)

For pipe-heavy `@TAG:` / `@EDG:` lines: **~chars ÷ 3.2** tokens (±15% by tokenizer). MemNet repo: `scripts/estimate_novel_io_tokens.py` for worked examples.

## Checklist

- [ ] Every field short and structured?
- [ ] Could this line be split for a smaller warm slice?
- [ ] Using `query_warm` with a tight anchor?
- [ ] Settling transient rows so warm stays lean?

Cross-ref: MemNet `README.md` (wire format) · `LLM-GUIDE.md` (EDG, recycle) · [mcp-policy.md](mcp-policy.md)
