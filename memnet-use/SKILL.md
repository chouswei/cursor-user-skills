---
name: memnet-use
description: >-
  How to use MemNet as mission working memory: goldfish loop, chat never
  SSOT, drop prior maps. Triggers: use memnet, how to use memnet, memnet
  goldfish, mission working memory, chat never SSOT, session graph.
metadata:
  pattern: pipeline
  version: "1.4"
  domain: memnet
  product: "memnet-llm==0.19.2"
---

# How to use MemNet

**Using** MemNet -- not building the engine. Doctrine: MemNet `docs/SHAPE.md`, `docs/grammar/gql-wire-profile.md`, `docs/LLM-GUIDE.md`, `docs/ROADMAP.md`. Open one specialist; do not paste those files here.

**Package and PyPI 0.19.2** (Hatch; tag `v0.19.2`; extras 0.10-0.19 unchanged). **Install:** `pip install memnet-llm` or `pip install memnet-llm==0.19.2`. **1.0** unclaimed. Chat is never SSOT. Novel-writer is out of scope. Open one specialist; this hub does not steal specialist triggers.

User-pack store: Cursor HTTP **`10.0.0.10:18766/mcp`** bridging TCP serve **`:18765`**. InvenTree MCP is not MemNet.

## Goldfish loop

1. **Open** -- `session_open` with a SCHEMA map (`map_file` / `map_lines`) covering every kind you will mutate. Missing map -> `no_map`. Missing kind -> `unknown_tag`. Bundled maps: MemNet checkout `parts/common/memnet/memnet/examples/schema.*.example.txt` (this pack does not vendor them).
2. **Transport** -- in-process MCP for a single agent. Multitask / Task workers: TCP or streamable-http; load [memnet-multitask](../memnet-multitask/SKILL.md). If the shared serve is down: files only; plain Markdown.
3. **Cue** -- `kind` / labels+properties / keyword. If ego unknown: `find` then `pin_map` from that pattern. Prefer one live `TSK_*`. leftover `anchor=` is leftover. Empty cue = session outline (0.11).
4. **`pin_map`** -- one session per generate; complete Shape of **this** cue. Drop the prior map next turn.
5. **Act** from that Shape plus the current request. Narrow-Read files at `SYM.line` / `SYM.path`.
6. **Sparse Commit** -- MCP/CLI **`mutate`**. leftover `add`/`update` / `id:'NEW'` are leftover-named.
7. **Settle** finished `TSK_*` (`status=settled`; `recycle=delete_on_settle` when done).

## Specialists (open on need)

| Need | Skill |
|------|--------|
| MCP tools, ingest, `snap_model`, export | [mcp-memnet](../mcp-memnet/SKILL.md) |
| GQL / shaped `pin_map` | [memnet-format](../memnet-format/SKILL.md) |
| Multitask / shared session | [memnet-multitask](../memnet-multitask/SKILL.md) |
| Code `MOD`/`SYM` | [memnet-codebase-snap](../memnet-codebase-snap/SKILL.md) |
| Nested sessions / look loop | [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md) |
| SysML relatives + nest cuts | pack `sysml-*` plus MemNet `docs/application-notes/system/llm-sysml-v2-modeling.md` |
| Build the MemNet engine | **not this pack** -- MemNet checkout `.cursor/skills/memnet-reference/` |

## MUST NOT

- Dump S or a fat `.sysml` into chat.
- Stack N nested `pin_map`s in one generate -- re-anchor with MCP `session=` / locator `session=`.
- Treat chat as ids / paths / mission state.
- `rag_query` / ANN of the session.
- Claim **1.0**.
- Load an in-repo `memnet-reference` copy unless **building** MemNet in that checkout.
