---
name: memnet-use
description: >-
  How to use MemNet as mission working memory: cue then pin_map, sparse
  mutate, drop prior maps. Triggers: use memnet, how to use memnet, memnet
  goldfish, pin_map, session graph, memnet MCP, GQL wire, shaped pin map,
  memnet-format, mcp-memnet, memnet-multitask, nested session, look loop.
metadata:
  pattern: pipeline
  version: "1.2"
  domain: memnet
  product: "package 0.19.1; PyPI wheel 0.19.0"
---

# How to use MemNet

**Using** MemNet -- not building the engine. Doctrine: MemNet `docs/SHAPE.md`, `docs/grammar/gql-wire-profile.md`, `docs/LLM-GUIDE.md`, `docs/ROADMAP.md`. Open one specialist; do not paste those files here.

**Package 0.19.1** (Hatch; tag `v0.19.1`; extras 0.10-0.19 unchanged). **PyPI wheel** still **`memnet-llm==0.19.0`** until twine. **Install:** `pip install memnet-llm==0.19.0` **or** git / `v0.19.1`. Do **not** `pip install memnet-llm==0.19.1` (no wheel yet). **1.0** unclaimed. Chat is never SSOT. Novel-writer is out of scope.

User-pack store: Cursor HTTP **`10.0.0.10:18766/mcp`** bridging TCP serve **`:18765`**. InvenTree MCP is not MemNet.

## Goldfish loop

1. **Transport** -- in-process MCP for a single agent. Multitask / Task workers: TCP or streamable-http; load [memnet-multitask](../memnet-multitask/SKILL.md). If the shared serve is down: files only; plain Markdown.
2. **Cue** -- `kind` / labels+properties / keyword. If ego unknown: `find` then `pin_map` from that pattern. Prefer one live `TSK_*`. leftover `anchor=` is leftover. Empty cue = session outline (0.11).
3. **`pin_map`** -- one session per generate; complete Shape of **this** cue. Drop the prior map next turn.
4. **Act** from that Shape plus the current request. Narrow-Read files at `SYM.line` / `SYM.path`.
5. **Sparse Commit** -- MCP/CLI **`mutate`**. leftover `add`/`update` / `id:'NEW'` are leftover-named.
6. **Settle** finished `TSK_*` (`status=settled`; `recycle=delete_on_settle` when done).

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
- Stack N nested `pin_map`s in one generate -- re-anchor (`session=`).
- Treat chat as ids / paths / mission state.
- `rag_query` / ANN of the session.
- Claim **1.0**. Collapse package 0.19.1 and PyPI 0.19.0 into one install pin.
- Load an in-repo `memnet-reference` copy unless **building** MemNet in that checkout.
