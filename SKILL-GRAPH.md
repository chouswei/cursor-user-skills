# Skill Graph (LLM-only hub)

**Audience:** model. Agent-facing examples use MemNet **GQL wire** (shaped pin_map + openCypher-shaped mutate). Wire SSOT: [memnet-format](memnet-format/SKILL.md). **Do not** treat this file as the graph -- it routes you to the graph.

**Engine seed only:** [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) is machine input for the selector/bootstrap tools (may still be compact store form). Skills and docs teach **GQL wire / shaped pin_map**; do not copy seed pipe syntax into agent I/O.

---

## Architecture (three tiers)

```text
## Edges
E_sg_01 [SKILL-GRAPH.md] --(canonical_graph)--> [skill-graph-seed.wire] ; note=single_source_D2 ; recycle=persistent
E_sg_02 [SKILL-GRAPH.md] --(schema_docs)--> [reasoning-strategy-selector/references/skill-graph.md] ; recycle=persistent
E_sg_03 [SKILL-GRAPH.md] --(runtime_graph)--> [memnet:SKG_global] ; note=optional_sync ; recycle=persistent
E_sg_04 [SKILL-GRAPH.md] --(membership_index)--> [skill-graph-seed.wire] ; note=SKL_rows ; recycle=persistent
E_sg_05 [SKILL-GRAPH.md] --(audit_view)--> [reasoning-strategy-selector/references/core-strategy-principles.md] ; note=generated ; recycle=persistent
E_sg_06 [reasoning-strategy-selector] --(traverses)--> [skill-graph-seed.wire] ; note=route_graph ; recycle=persistent
```

| Tier | Artifact | Role |
|------|----------|------|
| 1 | [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) | **Canonical graph** (engine seed) -- skills, triggers, typed edges |
| 2 | `memnet serve` -> `SKG_global` | **Runtime graph** -- pin map on `SKG_global` when MemNet is up; merge seed via `bootstrap --sync` |
| 3 | This file + slim catalog rule | **Routing hub** -- rules only; no duplicate node/edge payload |

**D2:** Seed file is single source. Markdown tables here were a generated view -- **removed**; regenerate audit table only via `python tools/bootstrap_skill_graph.py --regenerate-views`.

---

## Routing procedure

```text
## Nodes
RUL [SG01] ; kind=MUST ; code=trigger routing via graph traversal (seed or MemNet pin map), not flat table scan ; priority=high ; recycle=persistent
RUL [SG02] ; kind=MUST ; code=at most 2 trigger-match passes on TRG phrases connected to SKL via triggers edges ; priority=high ; recycle=persistent
RUL [SG03] ; kind=MUST ; code=open matched <skill-id>/SKILL.md only ; priority=high ; recycle=persistent
RUL [SG04] ; kind=MUST ; code=ambiguous after 2 scans -> ask user or repo AGENTS; optional reasoning-strategy-selector only for explicit multi-match ; priority=high ; recycle=persistent
RUL [SG05] ; kind=MUSTNOT ; code=invent skill-ids; membership = SKL rows in skill-graph-seed.wire ; priority=high ; recycle=persistent
RUL [SG06] ; kind=MUSTNOT ; code=iterate related_skills.txt as checklist ; priority=high ; recycle=persistent
RUL [SG07] ; kind=MAY ; code=MemNet down -> parse skill-graph-seed.wire locally (D3 graph-only) ; priority=med ; recycle=persistent
```

Steps:

1. Extract keywords from user phrase
2. MemNet up? pin map `pin_map(SKG_global, depth=2)` : parse seed.wire locally
3. Match TRG phrase -> follow `triggers` edges -> SKL
4. Rank: `led_to_success` boost + `complements` / `precedes` / `default_stack` edges
5. Open top SKL id `SKILL.md`; SysML hub stack if sysml domain

---

## Graph node shapes (summary)

Full schema: [`skill-graph.md`](reasoning-strategy-selector/references/skill-graph.md). Agent I/O uses GQL / shaped MemNet forms:

```text
## Nodes
SKG [SKG_global] ; version=... ; pack=user_pack ; recycle=persistent
SKL [skill-id] ; pack=... ; pattern=... ; dir=... ; domain=... ; recycle=persistent
TRG [trg-id] ; phrase=... ; recycle=persistent

## Edges
E01 [from] --(relation)--> [to] ; note=... ; recycle=persistent
```

Key relations: `triggers`, `precedes`, `default_stack`, `complements`, `specializes`, `requires`, `conflicts_with`, `led_to_success`.

Pattern codes: `G`=Generator, `R`=Reviewer, `P`=Pipeline, `T`=Tool-wrapper.

---

## SysML default stack (graph edges, not prose)

```text
## Edges
E_sys_01 [sysml-modeling-session-checklist] --(default_stack)--> [sysml-modeling-workflow] ; note=hub ; recycle=persistent
E_sys_02 [sysml-modeling-workflow] --(default_stack)--> [sysml-memnet-documentation] ; note=memnet ; recycle=persistent
```

Then at most one specialist SKL from `triggers` match. Repo `AGENTS.md` may add project overrides.

## MemNet application stack (graph edges, not prose)

```text
## Edges
E_mn_01 [mcp-memnet] --(complements)--> [memnet-format] ; note=wire ; recycle=persistent
E_mn_02 [memnet-multitask] --(complements)--> [mcp-memnet] ; note=multitask ; recycle=persistent
E_mn_03 [memnet-multitask] --(complements)--> [memnet-format] ; note=multitask ; recycle=persistent
E_mn_04 [sysml-gql] --(complements)--> [memnet-format] ; note=sysml_bridge ; recycle=persistent
E_mn_05 [sysml-gql] --(complements)--> [graph-query-language] ; note=gql_core ; recycle=persistent
E_mn_06 [sysml-gql] --(complements)--> [sysml-memnet-documentation] ; note=snap_ssot ; recycle=persistent
```

Load `memnet-multitask` when Multitask Mode or Task sub-agents are in play. Load `sysml-gql` when SysML modeling uses MemNet GQL working memory. Product **memnet-llm 0.9.0** (PyPI still 0.4.6). Ops: MemNet `docs/multi-agent-sessions.md`. Shape: `docs/SHAPE.md`. Version map: `docs/ROADMAP-0.5.md`. System-repo pattern: MemNet `docs/application-notes/llm-system-dev-multitask.md`.

---

## Maintenance

```text
## Nodes
RUL [SG_M01] ; kind=MUST ; code=graph edits in skill-graph-seed.wire only (or scan_skills_to_wire.py --write) ; priority=high ; recycle=persistent
RUL [SG_M02] ; kind=MUST ; code=after seed change: bootstrap_skill_graph.py --regenerate-views ; priority=high ; recycle=persistent
RUL [SG_M03] ; kind=SHOULD ; code=bootstrap --sync to merge into MemNet (preserve led_to_success) ; priority=med ; recycle=persistent
RUL [SG_M04] ; kind=MUST ; code=validate: python tools/validate_selector_pack.py --check-views ; priority=high ; recycle=persistent
```

---

## Why not duplicate the graph in this file?

| Option | Use? | Why |
|--------|------|-----|
| Flat 100-row table | No | Duplicates SKL+TRG+triggers; drifts from seed; ~3k tokens every load |
| Hub + seed.wire | Yes | Single source; traversable; pin-map slice; edges queryable |
| SET in alwaysApply catalog | No | Burns tokens every turn; membership already SKL in seed |

**End.** Open [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) or pin map `pin_map(SKG_global)` for the actual graph.
