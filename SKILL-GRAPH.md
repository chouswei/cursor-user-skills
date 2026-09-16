# Skill Graph (LLM-only hub)

**Audience:** model. Durable MemNet handoffs use the **GQL wire** (shaped `pin_map` + openCypher-shaped mutate). Wire SSOT: [memnet-format](memnet-format/SKILL.md). **Do not** treat this file as a flat graph database -- it routes you to the MemNet skill graph and defines stack architectures.

**MemNet skill graph:** Bind pack vs repo first (`skill-graph-workflow`). Query via `pin_map` / `find` on the bound SKG (`SKG_repo` if the open repo has a graph, else pack `SKG_global`). Pass `session=` from `AGENT-CONTEXT.md`. Optional exports: pack [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) and `<repo>/.cursor/skills/skill-graph-seed.wire`. MUST NOT merge repo SKL into the pack seed.

Pack graph-tooling cluster: `skill-graph-workflow` (bind) then one relative (`reasoning-strategy-selector`, `skill-creator`, `skill-reviewer`, `skillfish`).

---

## Architecture (three tiers)

Shaped present (as on a pin_map):

```cypher
(:MOD {id: 'SKILL-GRAPH.md'})-[:RUNTIME_GRAPH {id: 'E_sg_01', note: 'bound_skg', recycle: 'persistent'}]->(:SKG {id: 'SKG_global'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:REPO_GRAPH {id: 'E_sg_01b', note: 'open_repo_skg', recycle: 'persistent'}]->(:SKG {id: 'SKG_repo'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:SCHEMA_DOCS {id: 'E_sg_02', recycle: 'persistent'}]->(:MOD {id: 'reasoning-strategy-selector/references/skill-graph.md'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:CANONICAL_GRAPH {id: 'E_sg_03', note: 'optional_export_seed', recycle: 'persistent'}]->(:MOD {id: 'skill-graph-seed.wire'})
(:MOD {id: 'SKILL-GRAPH.md'})-[:AUDIT_VIEW {id: 'E_sg_04', note: 'generated', recycle: 'persistent'}]->(:MOD {id: 'reasoning-strategy-selector/references/core-strategy-principles.md'})
(:SKL {id: 'reasoning-strategy-selector'})-[:ROUTES_VIA {id: 'E_sg_05', note: 'memnet_pin_map', recycle: 'persistent'}]->(:SKG {id: 'SKG_global'})
```

| Tier | Artifact | Role |
|------|----------|------|
| 1 | `memnet serve` -> bound SKG (`SKG_repo` if present, else pack `SKG_global`) | **Runtime graph** -- `pin_map` / `find` with `session=` from `AGENT-CONTEXT.md`. Pack SKG does not list repo skills. |
| 1b | Repo `<repo>/.cursor/skills/skill-graph-seed.wire` | **Repo export** -- project SKL; MAY pointer-row pack skill ids as relatives |
| 2 | `SKILL-GRAPH.md` (this file) | **Pack routing hub** -- rules, domain stacks, offline fallback |
| 3 | Pack [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) | **Pack export** -- optional; never a gate when MemNet is up |

**D2:** Each graph has one seed export. Pack seed is pack SKL only. Repo seed is that repo. Markdown tables here are not the graph. MUST NOT merge repo SKL into the pack seed.

---

## Routing procedure (Skill Route)

```cypher
(:RUL {id: 'SG01', kind: 'MUST', code: 'bind SKG_repo if open-repo graph present else pack SKG_global; then pin_map or find (max 2 passes)', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG02', kind: 'MUST', code: 'open matched <skill-id>/SKILL.md only; do not glob every SKILL.md', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG03', kind: 'MUSTNOT', code: 'require skill-graph-seed.wire for routing when MemNet is up (seed is optional export)', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG04', kind: 'MUST', code: 'fallback when MemNet down: bound seed then SKILL-GRAPH.md; clone user pack if missing; do not stall', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG05', kind: 'MUST', code: 'ambiguous after 2 scans -> ask user or repo AGENTS; optional reasoning-strategy-selector only for explicit multi-match', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG06', kind: 'MUSTNOT', code: 'invent skill-ids; membership = bound SKG SKL (repo or pack)', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG07', kind: 'MUSTNOT', code: 'iterate related_skills.txt as checklist', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG08', kind: 'MUST', code: 'pass 1 repo graph if present; pass 2 pack graph if no repo match', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG09', kind: 'MUSTNOT', code: 'merge repo SKL into the pack seed or pack SKG', priority: 'high', recycle: 'persistent'})
```

Steps:

1. Extract keywords/intent from user phrase.
2. Bind graph: repo `SKG_repo` if `<repo>/.cursor/skills/skill-graph-seed.wire` exists, else pack `SKG_global`.
3. MemNet up: `find(kind="SKL", keyword="<term>", limit=5, session="<session>")` or `pin_map` on the bound SKG (max 2 passes).
4. MemNet down: parse the bound seed, then this hub file.
5. Open the matched SKL: repo id under `<repo>/.cursor/skills/<id>/SKILL.md`; pack id under `~/.cursor/skills/<id>/SKILL.md`. SysML domain follows SysML default stack.

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
(:SKL {id: 'sysml-modeling-workflow'})-[:DEFAULT_STACK {id: 'E_sys_02', note: 'cache', recycle: 'persistent'}]->(:SKL {id: 'sysml-memnet-cache'})
(:SKL {id: 'sysml-memnet-cache'})-[:DEFAULT_STACK {id: 'E_sys_02b', note: 'docs', recycle: 'persistent'}]->(:SKL {id: 'sysml-memnet-documentation'})
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

Load `memnet-use` when the job is **using** MemNet. Load `memnet-planner` when a plan must live in the session graph and be updated or repolished. Load `memnet-nested-sessions` when a nest is cut across sessions. Load `memnet-multitask` when Multitask Mode or Task sub-agents are in play (spawn a wave, checkpoint, repeat). Load `analytical-mechanics-propose` when proposing or reviewing an analytical-mechanics framing for any domain (STM thesis is the worked example, not the only target). Load `memnet-stm-harness` when wiring or triaging STM from thesis locks (W vs S, ShapeWalk harness, gauge/caps) -- fetch playbooks from [llm-stm-mechanics](https://github.com/chouswei/llm-stm-mechanics). Load `sysml-gql` when SysML modeling uses MemNet GQL working memory. Ops: MemNet `docs/operations/multi-agent-sessions.md`. Shape: `docs/SHAPE.md`. Version map: `docs/ROADMAP.md` (**package and PyPI 0.19.5**). System-repo pattern: MemNet `docs/application-notes/system/llm-system-dev-multitask.md`.

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

## ClickUp project-management stack (graph edges, not prose)

```cypher
(:TRG {id: 'trg-clickup-pm', phrase: 'ClickUp project management', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-hygiene', phrase: 'ClickUp status hygiene', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00b', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-kickoff', phrase: 'ClickUp kickoff', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00c', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-prd', phrase: 'ClickUp PRD', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00d', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-status-rollup', phrase: 'weekly status rollup', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00e', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-retro', phrase: 'ClickUp retrospective', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00f', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-plan-this', phrase: 'plan this in ClickUp', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00g', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-overdue', phrase: 'overdue ClickUp tasks', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00h', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-stakeholder', phrase: 'stakeholder update in ClickUp', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00i', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-standup', phrase: 'ClickUp standup', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00j', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-assign-due', phrase: 'assign and due-date work', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00k', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-feedback', phrase: 'ClickUp feedback loop', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00l', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:TRG {id: 'trg-clickup-feature-brief', phrase: 'feature brief in ClickUp', recycle: 'persistent'})-[:TRIGGERS {id: 'E_cu_00m', recycle: 'persistent'}]->(:SKL {id: 'clickup-project-management'})
(:SKL {id: 'clickup-project-management'})-[:COMPLEMENTS {id: 'E_cu_01', note: 'intake_plan', recycle: 'persistent'}]->(:SKL {id: 'project-planner'})
(:SKL {id: 'clickup-project-management'})-[:COMPLEMENTS {id: 'E_cu_02', note: 'kickoff_or_retro_notes', recycle: 'persistent'}]->(:SKL {id: 'meeting-notes-generator'})
```

Load `clickup-project-management` when running work in ClickUp (plan this in ClickUp, status hygiene, overdue tasks, kickoff, standup, stakeholder update, assign/due-date, feedback loop, PRD / feature brief, weekly status rollup, retrospective). Writes go through **user-clickup** MCP (`clickup_*`); this skill is PM practice, not an MCP wrapper. `mcp-clickup` is not in this pack. Load `project-planner` first when the user still needs a product-roadmap interview. Load `meeting-notes-generator` for kickoff or retro minutes, then create action-item tasks in ClickUp. Load `skill-creator` only when the user asked to author a new Agent Skill folder.

---

## Maintenance & Operations (Create, Update, Use)

```cypher
(:RUL {id: 'SG_M01', kind: 'MUST', code: 'create/update via MemNet ingest_skills or mutate on the bound SKG (pack vs repo)', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG_M02', kind: 'SHOULD', code: 'optional pack export: scan_skills_to_wire.py --write; repo export requires --repo-skills and --repo-seed', priority: 'med', recycle: 'persistent'})
(:RUL {id: 'SG_M03', kind: 'MUST', code: 'validate pack: python tools/validate_selector_pack.py --check-views', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG_M04', kind: 'MUSTNOT', code: 'scan_skills_to_wire --repo-skills --write without --repo-seed', priority: 'high', recycle: 'persistent'})
(:RUL {id: 'SG_M05', kind: 'MUSTNOT', code: 'merge repo SKL into the pack seed or pack SKG', priority: 'high', recycle: 'persistent'})
```

Mutate into a live session with openCypher-shaped **`mutate`** (GraphElement CREATE / MATCH SET).

---

## Why not duplicate the graph in this file?

| Option | Use? | Why |
|--------|------|-----|
| Flat 100-row table | No | Duplicates SKL+TRG+TRIGGERS; drifts from seed; ~3k tokens every load |
| MemNet runtime graph | Yes | Bounded `pin_map` / `find` queries; zero overhead in hub file |
| Hub + optional export seed | Yes | Single source; traversable; pin-map slice; edges queryable |
| SET in alwaysApply catalog | No | Burns tokens every turn; membership already in graph |

**End.** Bind via `skill-graph-workflow`. Run `pin_map` / `find` on the bound SKG (`SKG_repo` or pack `SKG_global`). Pack export: [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire). Repo export: `<repo>/.cursor/skills/skill-graph-seed.wire`.
