---
name: reasoning-strategy-selector
description: >-
  Skill-graph router and operator capabilities (Create, Update, Use): returns a short `order[]` of pack
  skill ids when the user explicitly asks which skill to use or triggers are multi-match; provides checkable
  procedures for MemNet skill-graph ingest, mutation, and live traversal.
  Triggers: which skill, ambiguous multi-match after SKILL-GRAPH, routing disambiguation, create skill graph,
  update skill graph, use skill graph, ingest skills, skill route.
  Skip: obvious single-skill fit; domain work; trivial one-liners; default "think carefully" prompts.

metadata:
  pattern: pipeline
  secondary: router
  version: 3.12-method-pack
  related_skills: [academic-report-generator, adr-generator, architecture-reviewer, code-reviewer, commit-message-generator, control-theory-planner, decision-inverter, scientific-method-first-principles, empirical-paradox-synthesis, engineering-practices-learner, incentive-alignment-reviewer, launch-readiness-assessor, mcdm-decider, meeting-notes-generator, optimization-planner, pandas-expert, pr-reviewer, project-planner, risk-assessor, rfc-generator, security-reviewer, tech-report-generator, tech-report-reviewer, skill-graph-workflow, skill-creator, skillfish, skill-reviewer, sysml-new-project, sysml-refactorer]

pipeline_steps:
  1. Frame — objective, hidden_assumptions, polarities. Abort with `order: []` if a single domain skill already fits.
  2. Graph load — bind pack vs repo (`skill-graph-workflow`): repo `SKG_repo` if present, else pack `SKG_global`. MemNet `pin_map` / `find` (`session=` from AGENT-CONTEXT). Fallback: bound seed, then `SKILL-GRAPH.md`.
  3. Rank — graph traversal: trigger hit -> typed neighbours (`PRECEDES`, `DEFAULT_STACK`, `COMPLEMENTS`, `SPECIALIZES`); score by edge weights + hop penalty. No 6D convolution over the skill table.
  4. Output — Markdown handoff (≤400 tokens): objective, hidden_assumptions, polarities, feature_scores{top skills}, order[], graph_path[], rationale[≤4], pass. `order` ⊆ graph SKL ids; never `reasoning-strategy-selector`.
  5. Revise — if ambiguous: `pin_map` the top SKL (`depth=1`) or widen trigger match; max once.
  6. Settle (parent agent, not selector) — on downstream `pass: true`, `mutate` `LED_TO_SUCCESS` per [phase4-learning-loop.md](references/phase4-learning-loop.md); `python tools/record_routing_success.py TSK_route_<slug> <skill-id> [...]`

system_instruction: |
  You route via skill graph traversal only; you do not solve the task.
  Prefer `order: []` + SKILL-GRAPH / repo AGENTS when domain intent is clear.

  1. Match intent to TRG phrases on the **bound** SKG (repo then pack) via MemNet pin_map / find, else bound seed / SKILL-GRAPH hub.
  2. Traverse typed neighbours; rank per edge weights in skill-graph.md.
  3. Cold start (no trigger): cue the bound SKG (`SKG_repo` or pack `SKG_global`) or domain hub via `DEFAULT_STACK`.
  4. Return top-3 with score ≥ 0.55, or `[]` → SKILL-GRAPH fast-path.

  **No convolution.** Do not score all skills against a 6D feature table.

  **MemNet primary:** `pin_map` / `find` from a cue; if unavailable, fallback to SKILL-GRAPH.md.

  **Output (Markdown bullets or short table):**
  ```
  objective: [1 line]
  hidden_assumptions: [≤2]
  polarities: [≤2]
  feature_scores: {skill: score}
  order: [id1, id2]
  graph_path: [ids traversed]
  rationale: [≤4 bullets]
  pass: [next instruction]
  ```

  ≤400 tokens. No user-message echo. Never invent skill ids.

token_guardrails: |
  Graph rank from MemNet pin_map/find or SKILL-GRAPH hub. Markdown handoff. Selector read-only for graph; parent agent writes led_to_success on settle (Phase 4). No convolution.
---

# Reasoning strategy selector & skill graph operations

**Role:** Graph-first router and operator capabilities for managing and querying the skill graph in MemNet.

**Bind:** [skill-graph-workflow](../skill-graph-workflow/SKILL.md). Live graph is MemNet on `SKG_repo` or pack `SKG_global`. Optional exports: pack [`references/skill-graph-seed.wire`](references/skill-graph-seed.wire); repo `<repo>/.cursor/skills/skill-graph-seed.wire`.

## 1. Skill Graph USE (Skill Route & Graph Traversal)

**Triggers:** `which skill`, `skill route`, `find skill`, `routing disambiguation`, `ambiguous multi-match after SKILL-GRAPH`, `skill graph`, `relative skills`.

### MUST / MUST NOT
- **MUST:** Bind pack vs repo first. Query MemNet on the bound SKG using `find(kind="SKL", keyword="<term>", limit=5, session="<session>")` or `pin_map(...)` (`session=` from `AGENT-CONTEXT.md`). Max 2 passes.
- **MUST:** Open only the single matched SKILL.md (repo id under `.cursor/skills/`; pack id under `~/.cursor/skills/`).
- **MUST:** If MemNet is down, fallback to the bound seed then `SKILL-GRAPH.md`. If pack missing, clone `https://github.com/chouswei/cursor-user-skills.git` to `~/.cursor/skills` then continue. MUST NOT stall.
- **MUST NOT:** Glob every `SKILL.md`.
- **MUST NOT:** Require `skill-graph-seed.wire` for routing when MemNet is up (seed is an optional export).
- **MUST NOT:** Merge repo SKL into the pack seed or pack SKG.
- **MUST NOT:** Iterate `related_skills.txt` as a checklist.
- **MUST NOT:** Invent skill ids.

### Checkable Procedure
1. **Bind graph:** Repo `SKG_repo` if `<repo>/.cursor/skills/` has a seed; else pack `SKG_global`.
2. **Extract keyword:** Extract key domain/action term from user request (e.g. `pcba`, `traceability`, `premortem`).
3. **MemNet query:** `find` / `pin_map` on the bound SKG.
4. **Fallback:** Bound seed, then `SKILL-GRAPH.md`.
5. **Open single skill:** Open the matched `SKILL.md` and follow instructions.

---

## 2. Skill Graph CREATE (Ingest & Graph Initialization)

**Triggers:** `create skill graph`, `ingest skills`, `init skill graph`, `ingest_skills`, `bootstrap skill graph`.

### MUST / MUST NOT
- **MUST:** Ingest into the **bound** SKG via `ingest_skills` or GQL `mutate`. Pack path `~/.cursor/skills`; repo path `<repo>/.cursor/skills`.
- **MUST:** Ensure each skill has `SKL` and `TRG` nodes linked via `TRIGGERS` edges.
- **MUST NOT:** Require agents to manually parse `skill-graph-seed.wire` to use the graph.
- **MUST NOT:** Ingest repo skills into pack `SKG_global` / pack seed.

### Checkable Procedure
1. **Ingest bound pack:** `ingest_skills(path="~/.cursor/skills", session="<session>")` for pack SKL, or `ingest_skills(path="<repo>/.cursor/skills", session="<session>")` for repo SKL.
2. **Verify nodes:** `find(kind="SKL", limit=5, session="<session>")`.
3. **Optional export:** Pack: `python tools/scan_skills_to_wire.py --write`. Repo: add `--repo-skills` and `--repo-seed`.

---

## 3. Skill Graph UPDATE (Refresh, Mutation & Learning)

**Triggers:** `update skill graph`, `refresh skills in memnet`, `reingest skills`, `record routing success`, `mutate skill edges`.

### MUST / MUST NOT
- **MUST:** Re-ingest modified skills with `ingest_skills(path="<skill_dir>", session="<session>")` or update typed relationships (`PRECEDES`, `COMPLEMENTS`, `DEFAULT_STACK`, `SPECIALIZES`) via GQL `mutate`.
- **MUST:** Record empirical success edges `(:TSK)-[:LED_TO_SUCCESS]->(:SKL)` via `mutate` or `python tools/record_routing_success.py`.
- **MUST:** Preserve existing `LED_TO_SUCCESS` history during updates.
- **MUST NOT:** Wipe or overwrite learning edges when refreshing nodes.

### Checkable Procedure
1. **Re-ingest folder:** Call `ingest_skills(path="~/.cursor/skills/<id>", session="<session>")`.
2. **Mutate edges:** Add typed edges via `mutate(wire_lines=["MATCH (a:SKL {id: '...'}), (b:SKL {id: '...'}) CREATE (a)-[:COMPLEMENTS {note: '...', recycle: 'persistent'}]->(b)"], session="<session>")`.
3. **Record success:** On task settle, record `(:TSK)-[:LED_TO_SUCCESS {recycle: 'persistent'}]->(:SKL)`.
4. **Verify:** Run `pin_map(kind="SKL", locators=["id=<id>"], depth=2, session="<session>")`.

---

## 4. Maintenance Tools

- `python tools/score_routing.py` — benchmark graph routing against golden set
- `python tools/validate_selector_pack.py` — pack consistency checks
- `python tools/scan_skills_to_wire.py --write` — optional **pack** export from pack SKILL.md scan
- `python tools/scan_skills_to_wire.py --repo-skills <repo>/.cursor/skills --repo-seed <repo>/.cursor/skills/skill-graph-seed.wire --write` — optional **repo** export (never without `--repo-seed`)
- `python tools/bootstrap_skill_graph.py --regenerate-views` — sync core-strategy-principles view from pack seed
- `python tools/record_routing_success.py TSK_route_<slug> <id> [...]` — format `LED_TO_SUCCESS` rows for MemNet

1. Scan bound SKG (repo then pack) for obvious match (max 2 passes).
2. If still multi-match **and** user asked for routing -> this router -> `order[]` from graph walk.
3. Forbidden: exhaustive `related_skills.txt` iteration; using this skill as a thinking substitute.
