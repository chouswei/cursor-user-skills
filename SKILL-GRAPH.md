# Skill Graph (LLM-only hub)

**Audience:** model. Agent I/O is MemNet **GQL wire** (shaped `pin_map` + openCypher-shaped mutate). Wire SSOT: [memnet-format](memnet-format/SKILL.md). **Do not** treat this file as the graph -- it routes you to the graph.

**Engine seed:** Pack [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) is GQL `CREATE` rows for **user-pack SKL**. Each open repo has **its own** seed at `<repo>/.cursor/skills/skill-graph-seed.wire`. Same mutate shape. Cue then `pin_map`; `find` if ego unknown. Empty q is 0.11 outline. Product write is **`mutate`**. **1.0** unclaimed.

Pack graph-tooling cluster: `skill-graph-workflow` (bind) then one relative (`reasoning-strategy-selector`, `skill-creator`, `skill-reviewer`, `skillfish`).

---

## Architecture (three tiers)

Shaped present (as on a pin_map):

```cypher
(:MOD {id: 'SKILL-GRAPH.md'})-[:CANONICAL_GRAPH {id: 'E_sg_01', note: 'pack_seed_D2', recycle: 'persistent'}]->(:MOD {id: 'skill-graph-seed.wire'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:REPO_GRAPH {id: 'E_sg_01b', note: 'open_repo_seed', recycle: 'persistent'}]->(:MOD {id: 'repo/.cursor/skills/skill-graph-seed.wire'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:SCHEMA_DOCS {id: 'E_sg_02', recycle: 'persistent'}]->(:MOD {id: 'reasoning-strategy-selector/references/skill-graph.md'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:RUNTIME_GRAPH {id: 'E_sg_03', note: 'optional_sync', recycle: 'persistent'}]->(:SKG {id: 'SKG_global'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:MEMBERSHIP_INDEX {id: 'E_sg_04', note: 'SKL_rows', recycle: 'persistent'}]->(:MOD {id: 'skill-graph-seed.wire'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:AUDIT_VIEW {id: 'E_sg_05', note: 'generated', recycle: 'persistent'}]->(:MOD {id: 'reasoning-strategy-selector/references/core-strategy-principles.md'})
(:SKL {id: 'reasoning-strategy-selector'})-[:TRAVERSES {id: 'E_sg_06', note: 'route_graph', recycle: 'persistent'}]->(:MOD {id: 'skill-graph-seed.wire'})
```

| Tier | Artifact | Role |
|------|----------|------|
| 1 | Pack [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) | **Pack graph** -- user-pack skills, triggers, typed edges |
| 1b | Repo `<repo>/.cursor/skills/skill-graph-seed.wire` | **Repo graph** -- project SKL; MAY pointer-row pack skill ids as relatives |
| 2 | `memnet serve` -> bound SKG (`SKG_global` pack, `SKG_repo` repo) | **Runtime graph** -- `pin_map` from cue; do not treat pack SKG as listing repo skills |
| 3 | This file + slim catalog rule | **Pack routing hub** -- rules only; no duplicate node/edge payload |

**D2:** Each graph has one seed file. Pack seed is SSOT for **pack** SKL only. Repo seed is SSOT for **that repo**. Markdown tables here are not the graph -- regenerate pack audit via `python tools/bootstrap_skill_graph.py --regenerate-views`.

---

## Routing procedure

```cypher
(:RUL {id: 'SG01', kind: 'MUST', code: 'trigger routing via graph traversal (seed or MemNet pin_map), not flat table scan', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG02', kind: 'MUST', code: 'at most 2 trigger-match passes on TRG phrases connected to SKL via TRIGGERS', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG03', kind: 'MUST', code: 'open matched <skill-id>/SKILL.md only', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG04', kind: 'MUST', code: 'ambiguous after 2 scans -> ask user or repo AGENTS; optional reasoning-strategy-selector only for explicit multi-match', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG05', kind: 'MUSTNOT', code: 'invent skill-ids; membership = pack seed SKL or open-repo seed SKL', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG06', kind: 'MUSTNOT', code: 'iterate related_skills.txt as checklist', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG07', kind: 'MAY', code: 'MemNet down -> parse the bound seed.wire locally (D3 graph-only)', priority: 'med', recycle: 'persistent'})
(:RUL {id: 'SG08', kind: 'MUST', code: 'pass 1 repo seed if present; pass 2 pack seed if no repo match', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG09', kind: 'MUSTNOT', code: 'merge repo SKL into the pack seed', priority: 'high', recycle: 'persistent'})
```

Steps:

1. Extract keywords from user phrase
2. If `<repo>/.cursor/skills/skill-graph-seed.wire` exists, match **repo** TRG (pass 1)
3. If no match, parse pack seed or `pin_map` pack `SKG_global` and match **pack** TRG (pass 2)
4. Rank: `:LED_TO_SUCCESS` boost + `:COMPLEMENTS` / `:PRECEDES` / `:DEFAULT_STACK`
5. Open top SKL: repo id under `<repo>/.cursor/skills/<id>/SKILL.md`; pack id under `~/.cursor/skills/<id>/SKILL.md`. SysML hub stack if sysml domain and the match is a pack skill.

---

## Graph node shapes (summary)

Full schema: [`skill-graph.md`](reasoning-strategy-selector/references/skill-graph.md). Agent I/O uses GQL / shaped MemNet forms:

```cypher
(:SKG {id: 'SKG_global', version: '...', pack: 'user_pack', recycle: 'persistent'})
(:SKG {id: 'SKG_repo', version: '...', pack: 'repo', recycle: 'persistent'})
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
(:SKL {id: 'sysml-modeling-workflow'})-[:COMPLEMENTS {id: 'E_sys_03', note: 'sysmledge', recycle: 'persistent'}]->(:SKL {id: 'sysmledge-workflow'})
(:SKL {id: 'sysml-modeling-workflow'})-[:COMPLEMENTS {id: 'E_sys_04', note: 'oosem', recycle: 'persistent'}]->(:SKL {id: 'oosem-workflow'})
```

Then at most one specialist SKL from `TRIGGERS` match. **Repo graph first** for project SKL. Pack `AGENTS.md` / pack seed for pack methods. SysMLEdge day loop: `sysmledge-workflow`. OOSEM method cycle: `oosem-workflow`.

## Skill-graph tooling stack (pack relatives, not prose)

```cypher
(:SKG {id: 'SKG_global'})-[:DEFAULT_STACK {id: 'E_sgt_00', note: 'graph_cluster', recycle: 'persistent'}]->(:SKL {id: 'skill-graph-workflow'})
(:SKL {id: 'skill-graph-workflow'})-[:PRECEDES {id: 'E_sgt_01', note: 'route_pack', recycle: 'persistent'}]->(:SKL {id: 'reasoning-strategy-selector'})
(:SKL {id: 'skill-graph-workflow'})-[:COMPLEMENTS {id: 'E_sgt_02', note: 'scaffold', recycle: 'persistent'}]->(:SKL {id: 'skill-creator'})
(:SKL {id: 'skill-graph-workflow'})-[:COMPLEMENTS {id: 'E_sgt_03', note: 'audit', recycle: 'persistent'}]->(:SKL {id: 'skill-reviewer'})
(:SKL {id: 'skill-graph-workflow'})-[:COMPLEMENTS {id: 'E_sgt_04', note: 'registry', recycle: 'persistent'}]->(:SKL {id: 'skillfish'})
(:SKL {id: 'vibe-repo-init'})-[:PRECEDES {id: 'E_sgt_05', note: 'seed_repo_graph', recycle: 'persistent'}]->(:SKL {id: 'skill-graph-workflow'})
```

Load `skill-graph-workflow` to bind pack vs repo graph, then one relative. MUST NOT copy pack skill bodies into the repo to express a relative -- pointer SKL rows (`pack: 'user'`, path under `~/.cursor/skills/`).

## MemNet application stack (graph edges, not prose)

```cypher
(:SKL {id: 'memnet-use'})-[:DEFAULT_STACK {id: 'E_mn_00', note: 'hub', recycle: 'persistent'}]->(:SKL {id: 'mcp-memnet'})
(:SKL {id: 'memnet-use'})-[:COMPLEMENTS {id: 'E_mn_00b', note: 'nested', recycle: 'persistent'}]->(:SKL {id: 'memnet-nested-sessions'})
(:SKL {id: 'memnet-use'})-[:COMPLEMENTS {id: 'E_mn_00c', note: 'plan', recycle: 'persistent'}]->(:SKL {id: 'memnet-planner'})
(:SKL {id: 'memnet-planner'})-[:REQUIRES {id: 'E_mn_00d', note: 'tools', recycle: 'persistent'}]->(:SKL {id: 'mcp-memnet'})
(:SKL {id: 'memnet-planner'})-[:COMPLEMENTS {id: 'E_mn_00e', note: 'wire', recycle: 'persistent'}]->(:SKL {id: 'memnet-format'})
(:SKL {id: 'memnet-planner'})-[:COMPLEMENTS {id: 'E_mn_00f', note: 'execute_wave', recycle: 'persistent'}]->(:SKL {id: 'memnet-multitask'})
(:SKL {id: 'mcp-memnet'})-[:COMPLEMENTS {id: 'E_mn_01', note: 'wire', recycle: 'persistent'}]->(:SKL {id: 'memnet-format'})
(:SKL {id: 'memnet-multitask'})-[:COMPLEMENTS {id: 'E_mn_02', note: 'multitask', recycle: 'persistent'}]->(:SKL {id: 'mcp-memnet'})
(:SKL {id: 'memnet-multitask'})-[:COMPLEMENTS {id: 'E_mn_03', note: 'multitask', recycle: 'persistent'}]->(:SKL {id: 'memnet-format'})
(:SKL {id: 'sysml-gql'})-[:COMPLEMENTS {id: 'E_mn_04', note: 'sysml_bridge', recycle: 'persistent'}]->(:SKL {id: 'memnet-format'})
(:SKL {id: 'sysml-gql'})-[:COMPLEMENTS {id: 'E_mn_05', note: 'gql_core', recycle: 'persistent'}]->(:SKL {id: 'graph-query-language'})
(:SKL {id: 'sysml-gql'})-[:COMPLEMENTS {id: 'E_mn_06', note: 'snap_ssot', recycle: 'persistent'}]->(:SKL {id: 'sysml-memnet-documentation'})
(:SKL {id: 'analytical-mechanics-propose'})-[:COMPLEMENTS {id: 'E_am_01', note: 'stm_playbooks', recycle: 'persistent'}]->(:SKL {id: 'memnet-stm-harness'})
(:SKL {id: 'analytical-mechanics-propose'})-[:COMPLEMENTS {id: 'E_am_02', note: 'framing_before_surrogate', recycle: 'persistent'}]->(:SKL {id: 'physics-constrained-surrogate-routing'})
```

Load `memnet-use` when the job is **using** MemNet. Load `memnet-planner` when a plan must live in the session graph and be updated or repolished. Load `memnet-nested-sessions` when a nest is cut across sessions. Load `memnet-multitask` when Multitask Mode or Task sub-agents are in play (spawn a wave, checkpoint, repeat). Load `analytical-mechanics-propose` when proposing or reviewing an analytical-mechanics framing for any domain (STM thesis is the worked example, not the only target). Load `memnet-stm-harness` when wiring or triaging STM from thesis locks (W vs S, ShapeWalk harness, gauge/caps) -- fetch playbooks from [llm-stm-mechanics](https://github.com/chouswei/llm-stm-mechanics). Load `sysml-gql` when SysML modeling uses MemNet GQL working memory. Ops: MemNet `docs/operations/multi-agent-sessions.md`. Shape: `docs/SHAPE.md`. Version map: `docs/ROADMAP.md` (**package and PyPI 0.19.3**). System-repo pattern: MemNet `docs/application-notes/system/llm-system-dev-multitask.md`.

Build-the-engine hub **`memnet-reference`** lives in the MemNet checkout (`.cursor/skills/memnet-reference/`); this pack does not copy it.

---

## Physics constrained-surrogate stack (graph edges, not prose)

```cypher
(:SKL {id: 'physics-constrained-surrogate-routing'})-[:SPECIALIZES {id: 'E_phys_01', note: 'enforce', recycle: 'persistent'}]->(:SKL {id: 'physics-enforce-constrained-nn'})
(:SKL {id: 'physics-constrained-surrogate-routing'})-[:SPECIALIZES {id: 'E_phys_02', note: 'relu_milp', recycle: 'persistent'}]->(:SKL {id: 'physics-relu-milp-embed'})
(:SKL {id: 'physics-constrained-surrogate-routing'})-[:SPECIALIZES {id: 'E_phys_03', note: 'kan_minlp', recycle: 'persistent'}]->(:SKL {id: 'physics-kan-global-opt'})
(:SKL {id: 'physics-enforce-constrained-nn'})-[:COMPLEMENTS {id: 'E_phys_04', note: 'train_then_embed', recycle: 'persistent'}]->(:SKL {id: 'physics-relu-milp-embed'})
(:SKL {id: 'physics-enforce-constrained-nn'})-[:COMPLEMENTS {id: 'E_phys_05', note: 'train_then_kan', recycle: 'persistent'}]->(:SKL {id: 'physics-kan-global-opt'})
(:SKL {id: 'physics-relu-milp-embed'})-[:COMPLEMENTS {id: 'E_phys_06', note: 'relu_vs_kan', recycle: 'persistent'}]->(:SKL {id: 'physics-kan-global-opt'})
(:SKL {id: 'chemengkg-assist'})-[:COMPLEMENTS {id: 'E_phys_07', note: 'kg_then_surrogate', recycle: 'persistent'}]->(:SKL {id: 'physics-constrained-surrogate-routing'})
```

Load `physics-constrained-surrogate-routing` when choosing among ENFORCE / ReLU-ANN->MILP / KAN global opt for a physics-consistent surrogate. Load `chemengkg-assist` for generic ChemEngKG (kgtool) SPARQL assist -- never invent user/PDF-locked assay coefficients.

---

## Diagram / P&ID stack (graph edges, not prose)

```cypher
(:SKL {id: 'diagram-routing'})-[:SPECIALIZES {id: 'E_diag_01', note: 'dexpi_primary', recycle: 'persistent'}]->(:SKL {id: 'pydexpi-p-id'})
(:SKL {id: 'diagram-routing'})-[:SPECIALIZES {id: 'E_diag_02', note: 'sfiles', recycle: 'persistent'}]->(:SKL {id: 'sfiles2'})
(:SKL {id: 'diagram-routing'})-[:SPECIALIZES {id: 'E_diag_03', note: 'ggiles', recycle: 'persistent'}]->(:SKL {id: 'ggiles'})
(:SKL {id: 'diagram-routing'})-[:COMPLEMENTS {id: 'E_diag_04', note: 'anti_pattern_do_not_use_for_pid', recycle: 'persistent'}]->(:SKL {id: 'd2-pid'})
(:SKL {id: 'diagram-routing'})-[:PRECEDES {id: 'E_diag_05', note: 'pid_primary', recycle: 'persistent'}]->(:SKL {id: 'pydexpi-p-id'})
(:SKL {id: 'diagram-routing'})-[:COMPLEMENTS {id: 'E_diag_06', note: 'sysml_mermaid', recycle: 'persistent'}]->(:SKL {id: 'mermaid'})
(:SKL {id: 'pydexpi-p-id'})-[:COMPLEMENTS {id: 'E_diag_07', note: 'flowsheet_string', recycle: 'persistent'}]->(:SKL {id: 'sfiles2'})
(:SKL {id: 'pydexpi-p-id'})-[:COMPLEMENTS {id: 'E_diag_08', note: 'general_string', recycle: 'persistent'}]->(:SKL {id: 'ggiles'})
(:SKL {id: 'chemengkg-assist'})-[:COMPLEMENTS {id: 'E_diag_09', note: 'kg_then_pid', recycle: 'persistent'}]->(:SKL {id: 'pydexpi-p-id'})
```

Load `diagram-routing` when diagram format is unclear. Load `pydexpi-p-id` for real P&ID / DEXPI / Proteus (AGPL-3.0 -- flag before proprietary redistribute). Load `sfiles2` (MIT) for flowsheet strings and `ggiles` (MIT) for general graph<->string. **Do not** load `d2-pid` as a P&ID lane -- it is an anti-pattern stub (D2 is architecture posters only; never P&ID). `chemistry-routing` is not in this pack.

---

## Maintenance

```cypher
(:RUL {id: 'SG_M01', kind: 'MUST', code: 'pack graph edits in pack skill-graph-seed.wire only; repo graph edits in <repo>/.cursor/skills/skill-graph-seed.wire', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG_M02', kind: 'MUST', code: 'after pack seed change: bootstrap_skill_graph.py --regenerate-views', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG_M03', kind: 'SHOULD', code: 'bootstrap --sync to merge pack seed into MemNet (preserve LED_TO_SUCCESS)', priority: 'med', recycle: 'persistent'})
(:RUL {id: 'SG_M04', kind: 'MUST', code: 'validate pack: python tools/validate_selector_pack.py --check-views', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG_M05', kind: 'MUSTNOT', code: 'scan_skills_to_wire --repo-skills --write without --repo-seed', priority: 'high', recycle: 'persistent'})
```

Mutate into a live session with openCypher-shaped **`mutate`** (GraphElement CREATE / MATCH SET).

---

## Why not duplicate the graph in this file?

| Option | Use? | Why |
|--------|------|-----|
| Flat 100-row table | No | Duplicates SKL+TRG+TRIGGERS; drifts from seed; ~3k tokens every load |
| Hub + seed.wire | Yes | Single source; traversable; pin-map slice; edges queryable |
| SET in alwaysApply catalog | No | Burns tokens every turn; membership already SKL in seed |

**End.** Pack graph: [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) or `pin_map` `SKG_global`. Repo graph: `<repo>/.cursor/skills/skill-graph-seed.wire` or `pin_map` `SKG_repo`. Bind via `skill-graph-workflow`.
