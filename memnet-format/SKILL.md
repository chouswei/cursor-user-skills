---
name: memnet-format
description: >-
  MemNet GQL wire: GraphElement node/edge/property, shaped subgraph emit,
  BIND vs relation, openCypher-shaped Commit. Triggers: memnet format, GQL
  wire, GraphElement, shaped subgraph, BIND vs relation, openCypher mutate.
metadata:
  pattern: tool-wrapper
  version: "5.4"
  domain: data-formats,memnet
  product: "package 0.19.2; PyPI wheel 0.19.0"
token_guardrails: |
  - Wire SSOT: MemNet docs/grammar/gql-wire-profile.md. This skill is MemNet-specific only.
  - pin_map from a cue; leftover anchor= is leftover. Do not dump S.
  - Product Commit is GraphElement CREATE / MATCH SET DELETE -- not leftover id:'NEW'.
---

# MemNet formats

Pair with [mcp-memnet](../mcp-memnet/SKILL.md). Formal SSOT: MemNet `docs/grammar/gql-wire-profile.md`. Version map: MemNet `docs/ROADMAP.md`.

**Package 0.19.2** (tag `v0.19.2`; extras 0.10-0.19 unchanged). **PyPI wheel** still **`memnet-llm==0.19.0`** until twine. **Install:** `pip install memnet-llm==0.19.0` **or** git / `v0.19.2`. Do **not** `pip install memnet-llm==0.19.1` or `==0.19.2` as the current wheel. **1.0** unclaimed.

**GQL only.** Node / edge / property. Do not teach Layer, Tier A, pipe `@TAG`, or TOON/TRON. leftover `id:'NEW'` / leftover `anchor=` are leftover.

User-pack engine: Cursor HTTP **`10.0.0.10:18766/mcp`** bridging TCP serve **`:18765`**.

## Shaped pin_map

MCP `pin_map` / CLI `query pin-map` emits a bounded neighbourhood. Parse envelope **`stdout`**.

| Control | Product use |
|---------|-------------|
| `kind` / `locators` / `keyword` / `cue` / `session` | Cue q. Empty q = 0.11 outline |
| `depth` / `max_rows` | Hard bound. Raise depth only if the slice is too thin. Over M: cut a nested session -- do not clip and call it Shape |
| `view` | Grain on a **seed** (`shell` / `interior`). Not the outline |
| leftover `anchor` / `anchors` | leftover nicknames |

If ego unknown: `find(limit=...)` then `pin_map` from labels+props. CueConflict when |Q|>1. `query_warm` is a leftover alias.

Loop: `session_open(map)` -> cue -> `pin_map` -> reason -> `mutate` -> `pin_map`. Drop the prior map next turn.

## Mutate

Product tool: MCP/CLI **`mutate`**. leftover `add`/`update` wrap the same envelope -- do not teach them as TARGET.

```cypher
CREATE (t:TSK {goal:'Clear warehouse', status:'in_progress'})
MATCH (n:NPC {role:'helper'}), (t:TSK {goal:'Clear warehouse'})
CREATE (n)-[:helps {note:'labour'}]->(t)
MATCH (t:TSK {goal:'Clear warehouse'}) SET t.status = 'settled', t.recycle = 'delete_on_settle'
```

| Intent | Shape |
|--------|-------|
| Create | `CREATE (:Kind {props})` -- GraphElement identity; no required `id` |
| Patch / settle | `MATCH` by labels+props; `SET` / `DELETE` |
| Rel | typed label on ends; port-port **`BIND`** (`fromPort` / `toPort` as needed) |
| Schema | `SCHEMA Kind ; fields=...` on `session_open` only |

Properties: short atoms. Membership = edges, not id-lists. Ingest pins: locators (`path`, `qname`), never leftover NEW.

Field notes: [references/memnet-wire-format.md](references/memnet-wire-format.md). Atomise: [../mcp-memnet/references/atomisation.md](../mcp-memnet/references/atomisation.md).

## When to use which label

| Need | Label |
|------|-------|
| Fact / claim | `:CLM` (+ relationships) |
| Directed relation | typed relationship |
| Flat membership | many rels -- not id lists in props |
| Work unit | `:TSK` |
| User constraint | `:USR` |
| File / symbol | `:MOD` / `:SYM` |
| Rule / policy | `:RUL` |
| SysML model atoms | [sysml-memnet-patterns.md](../sysml-memnet-documentation/references/sysml-memnet-patterns.md) -- do not invent kinds here |

House nicknames (optional property `id`, not identity): `TSK_model_<short>`, `USR_*`, `PRT_` / `POR_` / `REQ_` / `SYM_` / `MOD_`. leftover mint `id:'NEW'` is leftover.

## Handoff tiers

| Priority | When | Format |
|----------|------|--------|
| 1 | Durable / multi-step with MemNet up | GQL / openCypher-shaped mutate |
| 2 | No session / same-turn scratch | Plain Markdown |
| 3 | Tool / MCP / CLI boundary | JSON envelope |
| 4 | Human deliverable | Prose Markdown |

## Pre-write checklist

- [ ] pin_map from a cue (view / max_rows budgeted); `find` first if ego unknown
- [ ] Values short and structured
- [ ] Relations are relationships (BIND for port-port)
- [ ] Recycle matches lifetime
- [ ] Atom reachable from a useful cue

## MUST NOT

- Unbounded `MATCH`...`RETURN` as goldfish read.
- leftover NEW on patch. Client NEW for artefact locators.
- Duplicate the SysML construct table in this file.
- Claim **1.0**. Teach `pip install memnet-llm==0.19.1` or `==0.19.2` as the current wheel.

## Further reading

- [references/memnet-wire-format.md](references/memnet-wire-format.md)
- [graph-query-language](../graph-query-language/SKILL.md)
- [gql-path-patterns](../gql-path-patterns/SKILL.md)
- [mcp-memnet](../mcp-memnet/SKILL.md)
- [memnet-use](../memnet-use/SKILL.md)
- [sysml-gql](../sysml-gql/SKILL.md)
- MemNet `docs/grammar/` -- design SSOT
