# Skill Graph (LLM-only hub)

**Audience:** model. Agent I/O is MemNet **GQL wire** (shaped `pin_map` + openCypher-shaped mutate). Wire SSOT: [memnet-format](memnet-format/SKILL.md). **Do not** treat this file as the graph -- it routes you to the graph.

**Engine seed only:** [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) is machine input for selector/bootstrap tools (may still be compact store form). Skills and docs teach **GQL / shaped pin_map**; do **not** copy seed pipe / `KIND [id] ; k=v` syntax into agent I/O.

**Package and PyPI 0.19.3** (Hatch; tag `v0.19.3`; extras 0.10-0.19 unchanged). `session_open` needs a SCHEMA map. Cue then `pin_map`; `find` if ego unknown. Empty q is 0.11 outline. Product write is **`mutate`**. leftover `--anchor` / `id:'NEW'` / leftover `add` named leftover. **1.0** unclaimed.

---

## Architecture (three tiers)

Shaped present (as on a pin_map):

```cypher
(:MOD {id: 'SKILL-GRAPH.md'})-[:CANONICAL_GRAPH {id: 'E_sg_01', note: 'single_source_D2', recycle: 'persistent'}]->(:MOD {id: 'skill-graph-seed.wire'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:SCHEMA_DOCS {id: 'E_sg_02', recycle: 'persistent'}]->(:MOD {id: 'reasoning-strategy-selector/references/skill-graph.md'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:RUNTIME_GRAPH {id: 'E_sg_03', note: 'optional_sync', recycle: 'persistent'}]->(:SKG {id: 'SKG_global'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:MEMBERSHIP_INDEX {id: 'E_sg_04', note: 'SKL_rows', recycle: 'persistent'}]->(:MOD {id: 'skill-graph-seed.wire'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:AUDIT_VIEW {id: 'E_sg_05', note: 'generated', recycle: 'persistent'}]->(:MOD {id: 'reasoning-strategy-selector/references/core-strategy-principles.md'})
(:SKL {id: 'reasoning-strategy-selector'})-[:TRAVERSES {id: 'E_sg_06', note: 'route_graph', recycle: 'persistent'}]->(:MOD {id: 'skill-graph-seed.wire'})
```

| Tier | Artifact | Role |
|------|----------|------|
| 1 | [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) | **Canonical graph** (engine seed) -- skills, triggers, typed edges |
| 2 | `memnet serve` -> `SKG_global` | **Runtime graph** -- `pin_map` on cue `kind`/`goal` for `SKG_global` when MemNet is up; merge seed via `bootstrap --sync`. leftover `anchor=` named leftover. |
| 3 | This file + slim catalog rule | **Routing hub** -- rules only; no duplicate node/edge payload |

**D2:** Seed file is single source. Markdown tables here were a generated view -- **removed**; regenerate audit table only via `python tools/bootstrap_skill_graph.py --regenerate-views`.

---

## Routing procedure

```cypher
(:RUL {id: 'SG01', kind: 'MUST', code: 'trigger routing via graph traversal (seed or MemNet pin_map), not flat table scan', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG02', kind: 'MUST', code: 'at most 2 trigger-match passes on TRG phrases connected to SKL via TRIGGERS', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG03', kind: 'MUST', code: 'open matched <skill-id>/SKILL.md only', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG04', kind: 'MUST', code: 'ambiguous after 2 scans -> ask user or repo AGENTS; optional reasoning-strategy-selector only for explicit multi-match', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG05', kind: 'MUSTNOT', code: 'invent skill-ids; membership = SKL rows in skill-graph-seed.wire', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG06', kind: 'MUSTNOT', code: 'iterate related_skills.txt as checklist', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG07', kind: 'MAY', code: 'MemNet down -> parse skill-graph-seed.wire locally (D3 graph-only)', priority: 'med', recycle: 'persistent'})
```

Steps:

1. Extract keywords from user phrase
2. MemNet up? `pin_map` from cue (`kind` / locators; leftover `anchor='SKG_global'` is leftover nickname) or `find` then pin_map. Else parse seed.wire locally
3. Match TRG phrase -> follow `:TRIGGERS` -> SKL
4. Rank: `:LED_TO_SUCCESS` boost + `:COMPLEMENTS` / `:PRECEDES` / `:DEFAULT_STACK`
5. Open top SKL id `SKILL.md`; SysML hub stack if sysml domain

---

## Graph node shapes (summary)

Full schema: [`skill-graph.md`](reasoning-strategy-selector/references/skill-graph.md). Agent I/O uses GQL / shaped MemNet forms:

```cypher
(:SKG {id: 'SKG_global', version: '...', pack: 'user_pack', recycle: 'persistent'})
(:SKL {id: 'skill-id', pack: '...', pattern: '...', dir: '...', domain: '...', recycle: 'persistent'})
(:TRG {id: 'trg-id', phrase: '...', recycle: 'persistent'})
(:TRG {id: 'trg-id'})-[:TRIGGERS {id: 'E01', recycle: 'persistent'}]->(:SKL {id: 'skill-id'})
```

Key relationship types: `TRIGGERS`, `PRECEDES`, `DEFAULT_STACK`, `COMPLEMENTS`, `SPECIALIZES`, `REQUIRES`, `CONFLICTS_WITH`, `LED_TO_SUCCESS`.

Pattern codes: `G`=Generator, `R`=Reviewer, `P`=Pipeline, `T`=Tool-wrapper.

---

## SysML default stack (graph edges, not prose)

```cypher
(:SKL {id: 'sysml-modeling-session-checklist'})-[:DEFAULT_STACK {id: 'E_sys_01', note: 'hub', recycle: 'persistent'}]->(:SKL {id: 'sysml-modeling-workflow'})
(:SKL {id: 'sysml-modeling-workflow'})-[:DEFAULT_STACK {id: 'E_sys_02', note: 'memnet', recycle: 'persistent'}]->(:SKL {id: 'sysml-memnet-documentation'})
```

Then at most one specialist SKL from `TRIGGERS` match. Repo `AGENTS.md` may add project overrides.

## MemNet application stack (graph edges, not prose)

```cypher
(:SKL {id: 'memnet-use'})-[:DEFAULT_STACK {id: 'E_mn_00', note: 'hub', recycle: 'persistent'}]->(:SKL {id: 'mcp-memnet'})
(:SKL {id: 'memnet-use'})-[:COMPLEMENTS {id: 'E_mn_00b', note: 'nested', recycle: 'persistent'}]->(:SKL {id: 'memnet-nested-sessions'})
(:SKL {id: 'mcp-memnet'})-[:COMPLEMENTS {id: 'E_mn_01', note: 'wire', recycle: 'persistent'}]->(:SKL {id: 'memnet-format'})
(:SKL {id: 'memnet-multitask'})-[:COMPLEMENTS {id: 'E_mn_02', note: 'multitask', recycle: 'persistent'}]->(:SKL {id: 'mcp-memnet'})
(:SKL {id: 'memnet-multitask'})-[:COMPLEMENTS {id: 'E_mn_03', note: 'multitask', recycle: 'persistent'}]->(:SKL {id: 'memnet-format'})
(:SKL {id: 'sysml-gql'})-[:COMPLEMENTS {id: 'E_mn_04', note: 'sysml_bridge', recycle: 'persistent'}]->(:SKL {id: 'memnet-format'})
(:SKL {id: 'sysml-gql'})-[:COMPLEMENTS {id: 'E_mn_05', note: 'gql_core', recycle: 'persistent'}]->(:SKL {id: 'graph-query-language'})
(:SKL {id: 'sysml-gql'})-[:COMPLEMENTS {id: 'E_mn_06', note: 'snap_ssot', recycle: 'persistent'}]->(:SKL {id: 'sysml-memnet-documentation'})
```

Load `memnet-use` when the job is **using** MemNet. Load `memnet-nested-sessions` when a nest is cut across sessions. Load `memnet-multitask` when Multitask Mode or Task sub-agents are in play. Load `sysml-gql` when SysML modeling uses MemNet GQL working memory. Ops: MemNet `docs/operations/multi-agent-sessions.md`. Shape: `docs/SHAPE.md`. Version map: `docs/ROADMAP.md` (**package and PyPI 0.19.3**). System-repo pattern: MemNet `docs/application-notes/system/llm-system-dev-multitask.md`.

Build-the-engine hub **`memnet-reference`** lives in the MemNet checkout (`.cursor/skills/memnet-reference/`); this pack does not copy it.

---

## Maintenance

```cypher
(:RUL {id: 'SG_M01', kind: 'MUST', code: 'graph edits in skill-graph-seed.wire only (or scan_skills_to_wire.py --write)', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG_M02', kind: 'MUST', code: 'after seed change: bootstrap_skill_graph.py --regenerate-views', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG_M03', kind: 'SHOULD', code: 'bootstrap --sync to merge into MemNet (preserve LED_TO_SUCCESS)', priority: 'med', recycle: 'persistent'})
(:RUL {id: 'SG_M04', kind: 'MUST', code: 'validate: python tools/validate_selector_pack.py --check-views', priority: 'high', recycle: 'persistent'})
```

Mutate into a live session with openCypher-shaped **`mutate`** (GraphElement CREATE; leftover `id: 'NEW'` mint named leftover); do not emit `+ RUL [NEW] ; ...` pipe.

---

## Why not duplicate the graph in this file?

| Option | Use? | Why |
|--------|------|-----|
| Flat 100-row table | No | Duplicates SKL+TRG+TRIGGERS; drifts from seed; ~3k tokens every load |
| Hub + seed.wire | Yes | Single source; traversable; pin-map slice; edges queryable |
| SET in alwaysApply catalog | No | Burns tokens every turn; membership already SKL in seed |

**End.** Open [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) or cue `pin_map` for `SKG_global` (leftover `anchor=` named leftover) for the actual graph.
