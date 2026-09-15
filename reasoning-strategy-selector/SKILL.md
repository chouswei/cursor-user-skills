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
  version: 3.8-method-pack
  related_skills: [academic-report-generator, adr-generator, architecture-reviewer, code-reviewer, commit-message-generator, control-theory-planner, decision-inverter, scientific-method-first-principles, empirical-paradox-synthesis, engineering-practices-learner, incentive-alignment-reviewer, launch-readiness-assessor, mcdm-decider, meeting-notes-generator, optimization-planner, pandas-expert, pr-reviewer, project-planner, risk-assessor, rfc-generator, security-reviewer, tech-report-generator, tech-report-reviewer, skill-creator, skillfish, skill-reviewer, sysml-new-project, sysml-refactorer]

pipeline_steps:
  1. Frame — objective, hidden_assumptions, polarities. Abort with `order: []` if a single domain skill already fits.
  2. Graph load — MemNet `pin_map` / `find` for `SKG_global` / matching `SKL` nodes (`session=` from AGENT-CONTEXT). Fallback to `SKILL-GRAPH.md` when MemNet is down.
  3. Rank — graph traversal: trigger hit -> typed neighbours (`PRECEDES`, `DEFAULT_STACK`, `COMPLEMENTS`, `SPECIALIZES`); score by edge weights + hop penalty. No 6D convolution over the skill table.
  4. Output — Markdown handoff (≤400 tokens): objective, hidden_assumptions, polarities, feature_scores{top skills}, order[], graph_path[], rationale[≤4], pass. `order` ⊆ graph SKL ids; never `reasoning-strategy-selector`.
  5. Revise — if ambiguous: `pin_map` the top SKL (`depth=1`) or widen trigger match; max once.
  6. Settle (parent agent, not selector) — on downstream `pass: true`, `mutate` `LED_TO_SUCCESS` per [phase4-learning-loop.md](references/phase4-learning-loop.md); `python tools/record_routing_success.py TSK_route_<slug> <skill-id> [...]`

system_instruction: |
  You route via skill graph traversal only; you do not solve the task.
  Prefer `order: []` + SKILL-GRAPH / repo AGENTS when domain intent is clear.

  1. Match intent to TRG phrases (MemNet pin_map / find, or SKILL-GRAPH hub).
  2. Traverse typed neighbours; rank per edge weights in skill-graph.md.
  3. Cold start (no trigger): cue `SKG_global` or domain hub via `DEFAULT_STACK`.
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

---

## 1. Skill Graph USE (Skill Route & Graph Traversal)

**Triggers:** `which skill`, `skill route`, `find skill`, `routing disambiguation`, `ambiguous multi-match after SKILL-GRAPH`.

### MUST / MUST NOT
- **MUST:** Query MemNet first using `find(kind="SKL", keyword="<term>", limit=5, session="<session>")` or `pin_map(kind="SKL", locators=["phrase=<term>"], depth=2, session="<session>")` (`session=` from `AGENT-CONTEXT.md`). Max 2 passes.
- **MUST:** Open only the single matched `<pack-root>/<skill-id>/SKILL.md`.
- **MUST:** If MemNet is down or ingest is missing, fallback immediately to `SKILL-GRAPH.md` hub lookup + open matched `SKILL.md` directly. If pack missing, clone `https://github.com/chouswei/cursor-user-skills.git` to `~/.cursor/skills` then continue. MUST NOT stall.
- **MUST NOT:** Glob every `SKILL.md`.
- **MUST NOT:** Require `skill-graph-seed.wire` for routing (seed is an optional export artifact only).
- **MUST NOT:** Iterate `related_skills.txt` as a checklist.
- **MUST NOT:** Invent skill ids.

### Checkable Procedure
1. **Extract keyword:** Extract key domain/action term from user request (e.g. `pcba`, `traceability`, `premortem`).
2. **MemNet query:** Call `find(kind="SKL", keyword="<term>", limit=5, session="<session>")` or `pin_map(kind="SKL", locators=["phrase=<term>"], depth=2, session="<session>")`.
3. **Fallback:** If MemNet is unavailable, match trigger in `SKILL-GRAPH.md`.
4. **Open single skill:** Open `<pack-root>/<skill-id>/SKILL.md` and follow instructions.

---

## 2. Skill Graph CREATE (Ingest & Graph Initialization)

**Triggers:** `create skill graph`, `ingest skills`, `init skill graph`, `ingest_skills`, `bootstrap skill graph`.

### MUST / MUST NOT
- **MUST:** Ingest skills into MemNet via `mcp-memnet` tool `ingest_skills(path="<pack_path>", session="<session>")` or GQL `mutate` rows in the active session.
- **MUST:** Ensure each skill has `SKL` and `TRG` nodes linked via `TRIGGERS` edges.
- **MUST NOT:** Require agents to manually parse or maintain `skill-graph-seed.wire` to use the graph.
- **MUST NOT:** Invent a second, parallel graph store.

### Checkable Procedure
1. **Ingest pack:** Call `ingest_skills(path="~/.cursor/skills", session="<session>")`.
2. **Verify nodes:** Call `find(kind="SKL", limit=5, session="<session>")` and confirm returned skills.
3. **Optional seed export:** Run `python tools/scan_skills_to_wire.py --write` to regenerate `references/skill-graph-seed.wire` as an offline artifact.

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
- `python tools/scan_skills_to_wire.py --write` — optional export of seed wire from SKILL.md scan
- `python tools/bootstrap_skill_graph.py --regenerate-views` — sync core-strategy-principles view from seed
- `python tools/record_routing_success.py TSK_route_<slug> <id> [...]` — format `LED_TO_SUCCESS` rows for MemNet

