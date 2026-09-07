---
name: memnet-format
description: >-
  MemNet GQL wire: GraphElement node/edge/property, shaped subgraph emit,
  BIND vs relation, openCypher-shaped Commit. Triggers: memnet format, GQL
  wire, GraphElement, shaped subgraph, BIND vs relation, openCypher mutate.
metadata:
  pattern: tool-wrapper
  version: "5.8"
  domain: data-formats,memnet
  product: "memnet-llm==0.19.5"
token_guardrails: |
  - Wire SSOT: MemNet docs/grammar/gql-wire-profile.md. This skill is MemNet-specific only.
  - Cue then pin_map(q); empty q = outline. leftover nickname cue / anchor= only as leftover. Do not dump S.
  - Identity is the graph element. MATCH locators (labels+observable properties). Never copy hid/id/elementId as law.
  - Product Commit is GraphElement CREATE / MATCH SET DELETE -- not leftover id:'NEW' / add / update.
---

# MemNet formats

Pair with [mcp-memnet](../mcp-memnet/SKILL.md). Formal SSOT: MemNet `docs/grammar/gql-wire-profile.md`. Version map: MemNet `docs/ROADMAP.md`. STM locks (pointer): [memnet-stm-harness](../memnet-stm-harness/SKILL.md).

**Package and PyPI 0.19.5** (honesty `c` on 0.19 -- not a usage-method `b`; tag `v0.19.5`; extras 0.10-0.19 unchanged). **Install:** `pip install memnet-llm` or `pip install memnet-llm==0.19.5`. **1.0** unclaimed. No 0.20. Recall/Commit `operatorCount` stays 2.

**GQL only.** Node / edge / property. Do not teach Layer, Tier A, pipe `@TAG`, or TOON/TRON. leftover `id:'NEW'` / leftover `anchor=` are leftover.

User-pack engine: Cursor HTTP **`10.0.0.10:18766/mcp`** bridging TCP serve **`:18765`**.

## Shaped pin_map

MCP `pin_map` / CLI `query pin-map` emits a bounded neighbourhood -- working set offer **W**, not a dump of inventory **S**. Parse envelope **`stdout`**.

| Control | Product use |
|---------|-------------|
| `kind` / `locators` / `keyword` / `cue` / `session` | Cue q then `pin_map(q)`. Empty q = 0.11 outline |
| `depth` / `max_rows` | Hard bound. Raise depth only if the slice is too thin. Over M: cut a nested session -- do not clip and call it Shape |
| `view` | Grain on a **seed** (`shell` / `interior`). Not the outline |
| leftover `anchor` / `anchors` | leftover nickname cue only -- not required, not identity |

If ego unknown: `find(limit=...)` then `pin_map` from labels+props. CueConflict when |Q|>1. `query_warm` is a leftover alias.

**Honesty `c` (shaped read):** `pin_map` / `export_pin_map` / `find` emit MUST NOT show `hid`, `_memnet_hid`, `elementId` (`SHAPE_DROP_KEYS`), or nickname property `id`. Cue / find / `match_nickname` MAY still look up a nickname the agent already holds. Mutate ack MAY echo nickname `id` the agent wrote. Rank excludes nickname `id` and `SHAPE_DROP_KEYS`. Do not put momentum / coverage / lambda / m on `pin_map`. Audit: MemNet `docs/operations/honesty-c-wire-audit.md`. Wire SSOT: MemNet `docs/grammar/gql-wire-profile.md` §5.2.

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

- [ ] Cue then `pin_map` (view / max_rows budgeted); `find` first if ego unknown
- [ ] MATCH / cue by locators from shaped emit (labels+observable properties)
- [ ] Values short and structured
- [ ] Relations are relationships (BIND for port-port)
- [ ] Recycle matches lifetime
- [ ] Atom reachable from a useful cue; drop the prior map next turn

## MUST NOT

- Unbounded `MATCH`...`RETURN` as goldfish read.
- leftover NEW on patch. Client NEW for artefact locators.
- Require leftover `anchor`. Treat nickname `id` / hid / elementId as identity.
- Duplicate the SysML construct table in this file.
- Claim **1.0**.
- Put momentum / coverage / lambda / m on `pin_map`.

## Further reading

- [references/memnet-wire-format.md](references/memnet-wire-format.md)
- [graph-query-language](../graph-query-language/SKILL.md)
- [gql-path-patterns](../gql-path-patterns/SKILL.md)
- [mcp-memnet](../mcp-memnet/SKILL.md)
- [memnet-stm-harness](../memnet-stm-harness/SKILL.md)
- [memnet-use](../memnet-use/SKILL.md)
- [sysml-gql](../sysml-gql/SKILL.md)
- MemNet `docs/grammar/` -- design SSOT
