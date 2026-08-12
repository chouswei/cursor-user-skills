---
name: reasoning-strategy-selector
description: >-
  Optional skill-graph router only: returns a short `order[]` of pack skill ids when the user
  explicitly asks which skill to use, or SKILL-GRAPH triggers are multi-match after two scans.
  Does not solve domain tasks. Do not use for SysML, PCBA, MCP, reports, or any clear single-skill fit —
  open that skill directly. Prefer ask-user or repo AGENTS.md over this router for project work.
  Triggers: which skill, ambiguous multi-match after SKILL-GRAPH, routing disambiguation only.
  Skip: obvious single-skill fit; domain work; trivial one-liners; default "think carefully" prompts.

metadata:
  pattern: pipeline
  secondary: router
  version: 3.4-method-pack
  related_skills: [academic-report-generator, adr-generator, architecture-reviewer, code-reviewer, commit-message-generator, control-theory-planner, decision-inverter, scientific-method-first-principles, empirical-paradox-synthesis, engineering-practices-learner, incentive-alignment-reviewer, launch-readiness-assessor, mcdm-decider, meeting-notes-generator, optimization-planner, pandas-expert, pr-reviewer, project-planner, risk-assessor, rfc-generator, security-reviewer, tech-report-generator, tech-report-reviewer, skill-creator, skillfish, skill-reviewer, sysml-new-project, sysml-refactorer]

pipeline_steps:
  1. Frame — objective, hidden_assumptions, polarities. Abort with `order: []` if a single domain skill already fits.
  2. Graph load — parse [`skill-graph-seed.wire`](references/skill-graph-seed.wire) locally, or `pin_map(SKL_<hit>|SKG_global)` when MemNet live. Match `@TRG` phrases; anchor per [skill-graph.md](references/skill-graph.md).
  3. Rank — graph traversal only: trigger hit → typed `@EDG` neighbours (`precedes`, `default_stack`, `complements`, `specializes`); score by edge weights + hop penalty. No 6D convolution over the skill table.
  4. Output — Markdown handoff (≤400 tokens): objective, hidden_assumptions, polarities, feature_scores{top skills}, order[], graph_path[], rationale[≤4], pass. `order` ⊆ graph `@SKL` ids; never `reasoning-strategy-selector`.
  5. Revise — if ambiguous: re-anchor `pin_map(SKL_<top>, depth=1)` or widen trigger match; max once.
  6. Settle (parent agent, not selector) — on downstream `pass: true`, emit `led_to_success` `@EDG` rows per [phase4-learning-loop.md](references/phase4-learning-loop.md); `python tools/record_routing_success.py TSK_route_<slug> <skill-id> [...]`

system_instruction: |
  You route via skill graph traversal only; you do not solve the task.
  Prefer `order: []` + SKILL-GRAPH / repo AGENTS when domain intent is clear.

  1. Match intent to `@TRG` rows (skill-graph-seed.wire or MemNet warm slice).
  2. Traverse typed `@EDG` neighbours; rank per edge weights in skill-graph.md.
  3. Cold start (no trigger): anchor `SKG_global` or domain hub via graph `default_stack` edges.
  4. Return top-3 with score ≥ 0.55, or `[]` → SKILL-GRAPH fast-path.

  **No convolution.** Do not score all skills against a 6D feature table.

  **MemNet optional:** `pin_map(anchor=SKL_<id>, depth=2, max_rows=30)`; if unavailable, parse seed wire locally.

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
  Graph rank from seed wire or pin_map only. Markdown handoff. Selector read-only for graph; parent agent writes led_to_success on settle (Phase 4). No convolution.
---

# Reasoning strategy selector (graph-first, optional)

**Optional router** — MemNet skill graph + wire seed. Canonical pack: **user-pack only** (D1).
Not a default fallback for unclear project work; use repo `AGENTS.md` / ask the user first.

**Source of truth:** [`references/skill-graph-seed.wire`](references/skill-graph-seed.wire) (D2). Generated views: `core-strategy-principles.md`, `SKILL-GRAPH.md` trigger table.

**Schema:** [skill-graph.md](references/skill-graph.md) · **Golden set:** [routing-golden-set.md](references/routing-golden-set.md)

**Tools:**
- `python tools/score_routing.py` — benchmark graph routing on golden set
- `python tools/bootstrap_skill_graph.py --regenerate-views` — sync generated views from seed
- `python tools/scan_skills_to_wire.py --write` — rebuild seed from SKILL.md scan
- `python tools/validate_selector_pack.py` — pack + graph density checks
- `python tools/strategy-retriever.py "<q>"` — graph trigger match helper (not convolution)

- `python tools/record_routing_success.py TSK_route_<slug> <id> [...]` — format `led_to_success` `@EDG` rows for MemNet

**Phase 4:** [phase4-learning-loop.md](references/phase4-learning-loop.md) — parent agent records empirical routing edges on settle.

**Main agent:** open `<pack-root>/<id>/SKILL.md` per `order[]`. SysML skills outside `related_skills` still routable via graph; for single obvious sysml-* match, `order: []` + SKILL-GRAPH fast-path remains valid.

## Limited iteration rule

1. Scan SKILL-GRAPH triggers (max 2 passes) for obvious match.
2. If still multi-match **and** user asked for routing → this router → `order[]` from graph walk.
3. Forbidden: exhaustive `related_skills.txt` iteration; using this skill as a thinking substitute.
