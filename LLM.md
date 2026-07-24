# Skills pack — agent policy (LLM-only)

**Audience:** model. Wire rows are canonical; prose only for links / narrative. Reference lookups → [SKILL-GRAPH.md](SKILL-GRAPH.md).

Pack root default = `.cursor/skills/`. Entry file always `<pack-root>/<skill-id>/SKILL.md`.

---

## Rules (MUST / MUST NOT)

Format: `@RUL: id|kind|directive|priority`

```text
@RUL: R01|MUSTNOT|load every skill; one user request → ≤1 specialist active|high
@RUL: R02|MUSTNOT|treat "list every skill" as a workflow|high
@RUL: R03|MUST|if selector order=[] → answer without opening another SKILL.md|high
@RUL: R04|MUST|model-choice question → llm-model-suggester (not reasoning-strategy-selector)|high
@RUL: R05|MUST|model above $6/1M tokens requires explicit user approval|high
@RUL: R06|SHOULD|obvious single-skill task → apply that skill directly|med
@RUL: R07|SHOULD|general reasoning/planning, no domain → user-domain skills|med
@RUL: R08|SHOULD|multi-step/broad task → sub-agent; same routing inside|med
@RUL: R09|MUST|no summary/review docs unless user asks|med
@RUL: R10|MUST|skill-creator only when user wants to create/scaffold a skill|med
@RUL: R11|MUST|bump metadata.version before pushing a user-pack skill to GitHub|med
@RUL: R12|MUST|obey active skill token_guardrails; prefer tools/* over dumping references/*|high
@RUL: R13|MUST|pipeline handoffs: serve up → MemNet wire (@TSK + @CLM type=pipe); serve down → plain Markdown; tool boundary → JSON|high
@RUL: R14|SHOULD|large uniform tabular data in answers → Markdown table over JSON when clearer|med
@RUL: R15|MUSTNOT|invent skill-ids absent from skill-graph-seed.wire @SKL / SKILL-GRAPH.md|high
```

Cross-refs: [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc) · [sysml-memnet-pipeline.md](sysml-memnet-documentation/references/sysml-memnet-pipeline.md). Do not use TOON/TRON.

---

## Procedure (per turn)

Format: `@PRC: step|action|then`

```text
@PRC: p1|extract triggers from user phrase|p2
@PRC: p2|match triggers in SKILL-GRAPH.md (≤2 passes)|p3
@PRC: p3a|exactly one match → open <id>/SKILL.md|p4
@PRC: p3b|model-choice intent → llm-model-suggester only|done
@PRC: p3c|ambiguous → ask user or repo AGENTS; optional reasoning-strategy-selector only for explicit multi-match|p4
@PRC: p3d|conflict between candidates → SKILL-GRAPH.md Contrasts/Edges|p4
@PRC: p4|follow SKILL.md frontmatter + numbered steps as binding|p5
@PRC: p5|lazy-load references/ assets/ tools/ only when a step needs them|p6
@PRC: p6|between steps: serve_status → wire on server (up) or plain Markdown in-prompt (down)|p7
@PRC: p7|keep user-visible format per skill template (separate from internal handoff)|p8
@PRC: p8|do not echo user message verbatim unless skill requires|done
```

---

## Routing order

Format: `@ROU: anchor|condition|target`

```text
@ROU: route_model|"which model" / "best LLM"|llm-model-suggester
@ROU: route_reason|general reasoning / planning / no domain|user-domain skills (SKILL-GRAPH Domain Registry)
@ROU: route_unclear|trigger ambiguous|ask user / repo AGENTS (optional reasoning-strategy-selector for explicit multi-match)
@ROU: route_skillqa|skill quality / structure|skill-reviewer
@ROU: route_obvious|single clear match|that skill directly
@ROU: route_multi|multi-step / broad|sub-agent + re-apply routing inside
@ROU: route_sysml|sysml-v2-models/* edit|sysml-modeling-session-checklist → sysml-modeling-workflow → one sysml-* specialist
```

---

## Path rule

```text
@RUL: P01|MUST|skill-id = immediate child dir under <pack-root>|high
@RUL: P02|MUST|entry file = <pack-root>/<skill-id>/SKILL.md (no alternates)|high
@RUL: P03|MUST|discover ids via glob <pack-root>/*/SKILL.md; do not invent|high
@RUL: P04|MAY|aliases → ids via SKILL-GRAPH.md Map section|low
```

Optional sub-folders per skill: `references/`, `assets/`, `tools/`, `Folder_Structure.md`.

---

## Cross-references

- **Routing aid:** [SKILL-GRAPH.md](SKILL-GRAPH.md) — wire hub → [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) (canonical `@SKL`/`@TRG`/`@EDG` graph). Catalog rule injects ids via `@SET`.
- **Handoff aid:** `memnet-goldfish-loop.mdc` + `memnet-format/SKILL.md` (wire grammar) + `sysml-memnet-pipeline.md` (SysML); plain Markdown when serve down.
- **Model routing aid:** `llm-model-suggester/SKILL.md`.

---

## Worked example — Leo CubeSat QPD pipeline

Project: `sysml-v2-models/projects/leo-cubesat-laser-comm/`. Scenario: multi-stage DSP firmware (acquisition → demod → position → aggregation) with thread states, inter-stage ports, latency budget.

Skill chain (workflow edges):

```text
@EDG: E1|sysml-modeling-session-checklist|next|sysml-modeling-workflow|preflight|persistent
@EDG: E2|sysml-modeling-workflow|next|sysml-nested-structure-modeling|decompose|persistent
@EDG: E3|sysml-nested-structure-modeling|next|sysml-signal-processing-pipeline|stage_ports|persistent
@EDG: E4|sysml-signal-processing-pipeline|next|sysml-behaviour-generator|thread_states|persistent
@EDG: E5|sysml-behaviour-generator|next|sysml-connections|verify_dataflow|persistent
@EDG: E6|sysml-connections|next|sysml-view-doc-sync|sync_outputs|persistent
```

Trigger → skill:

```text
@TRG: model DSP pipeline|sysml-signal-processing-pipeline
@TRG: nested structure / decompose monolithic|sysml-nested-structure-modeling
@TRG: phase synchronization / lock-in|sysml-signal-processing-pipeline
@TRG: thread states / lifecycle|sysml-behaviour-generator
@TRG: latency budget|sysml-signal-processing-pipeline
```

Outcome facts:

```text
@CLM: leo_q1|leo-cubesat|fact|thread_sm:idle→armed→sampling↔paused→error|settled|persistent
@CLM: leo_q2|leo-cubesat|fact|ports:RawSamplePort,DemodulatedDataPort,PositionDataPort|settled|persistent
@CLM: leo_q3|leo-cubesat|fact|stages:SpiAcquisition,LockInDemod,PositionCalc,DataAggregation|settled|persistent
@CLM: leo_q4|leo-cubesat|metric|latency_end_to_end<500us|settled|persistent
@SYM: SYM_leo_dsp|deploy-leo-cubesat-laser-comm.sysml|190-858|composite|persistent
@MOD: MOD_leo_doc|outputs/system-design-report/02b-interconnection.md|persistent
```

---

**End.** Existence of many skill folders ≠ permission to run them all.
