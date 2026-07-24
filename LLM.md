# Skills pack -- agent policy (LLM-only)

**Audience:** model. Durable MemNet handoffs use the **shared dialect** (Write = display) for **memnet-llm 0.3.1** -- same NODE|EDGE shapes for pin-map read and mutate. Dialect SSOT: [memnet-format](memnet-format/SKILL.md), [mcp-memnet](mcp-memnet/SKILL.md). Reference lookups -> [SKILL-GRAPH.md](SKILL-GRAPH.md).

Pack root default = `.cursor/skills/`. Entry file always `<pack-root>/<skill-id>/SKILL.md`.

**Dialect reminder:** pin map = **bare present** (no leading ops). Mutate = `+` create, `~` update, `-` drop; mint creates with `NEW`.

---

## Rules (MUST / MUST NOT)

**Preferred format** (shared dialect, bare present -- as on a pin map):

```text
## Nodes
RUL [R01] ; kind=MUSTNOT ; code=load every skill; one user request -> <=1 specialist active ; priority=high ; recycle=persistent
RUL [R02] ; kind=MUSTNOT ; code=treat "list every skill" as a workflow ; priority=high ; recycle=persistent
RUL [R03] ; kind=MUST ; code=if selector order=[] -> answer without opening another SKILL.md ; priority=high ; recycle=persistent
RUL [R04] ; kind=MUST ; code=model-choice question -> llm-model-suggester (not reasoning-strategy-selector) ; priority=high ; recycle=persistent
RUL [R05] ; kind=MUST ; code=model above $6/1M tokens requires explicit user approval ; priority=high ; recycle=persistent
RUL [R06] ; kind=SHOULD ; code=obvious single-skill task -> apply that skill directly ; priority=med ; recycle=persistent
RUL [R07] ; kind=SHOULD ; code=general reasoning/planning, no domain -> user-domain skills ; priority=med ; recycle=persistent
RUL [R08] ; kind=SHOULD ; code=multi-step/broad task -> sub-agent; same routing inside ; priority=med ; recycle=persistent
RUL [R09] ; kind=MUST ; code=no summary/review docs unless user asks ; priority=med ; recycle=persistent
RUL [R10] ; kind=MUST ; code=skill-creator only when user wants to create/scaffold a skill ; priority=med ; recycle=persistent
RUL [R11] ; kind=MUST ; code=bump metadata.version before pushing a user-pack skill to GitHub ; priority=med ; recycle=persistent
RUL [R12] ; kind=MUST ; code=obey active skill token_guardrails; prefer tools/* over dumping references/* ; priority=high ; recycle=persistent
RUL [R13] ; kind=MUST ; code=pipeline handoffs: MemNet up -> shared dialect (pin map + mutate +/~/-); MemNet down -> plain Markdown; tool boundary -> JSON ; priority=high ; recycle=persistent
RUL [R14] ; kind=SHOULD ; code=large uniform tabular data in answers -> Markdown table over JSON when clearer ; priority=med ; recycle=persistent
RUL [R15] ; kind=MUSTNOT ; code=invent skill-ids absent from skill-graph-seed.wire / SKILL-GRAPH.md ; priority=high ; recycle=persistent
RUL [R16] ; kind=MUST ; code=ASCII only in skills, LLM.md, AGENTS.md durable lines (use -> not arrows; no smart quotes) ; priority=high ; recycle=persistent
RUL [R17] ; kind=MUSTNOT ; code=select FAST/flash/low speed model slugs for Task/subagents (no composer-2.5-fast, gemini-3-flash, or cheap-fast tiers); use default parent model or full-quality slug only ; priority=high ; recycle=persistent
```


Mutate sketch (when writing rules into a live session): `+ RUL [NEW] ; kind=MUST ; code=... ; priority=high ; recycle=persistent`.

Cross-refs: [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc), [sysml-memnet-pipeline.md](sysml-memnet-documentation/references/sysml-memnet-pipeline.md). Do not use TOON/TRON.

---

## Procedure (per turn)

1. Extract triggers from user phrase -> 2
2. Match triggers in SKILL-GRAPH.md (<=2 passes) -> 3
3. Branch:
   - exactly one match -> open `<id>/SKILL.md` -> 4
   - model-choice intent -> `llm-model-suggester` only -> done
   - ambiguous -> ask user or repo AGENTS; optional `reasoning-strategy-selector` only for explicit multi-match -> 4
   - conflict between candidates -> SKILL-GRAPH.md Contrasts/Edges -> 4
4. Follow SKILL.md frontmatter + numbered steps as binding -> 5
5. Lazy-load `references/` `assets/` `tools/` only when a step needs them -> 6
6. Between steps: MemNet up -> shared-dialect mutate on server; MemNet down -> plain Markdown in-prompt -> 7
7. Keep user-visible format per skill template (separate from internal handoff) -> 8
8. Do not echo user message verbatim unless skill requires -> done

---

## Routing order

| Anchor | Condition | Target |
|--------|-----------|--------|
| `route_model` | "which model" / "best LLM" | `llm-model-suggester` |
| `route_reason` | general reasoning / planning / no domain | user-domain skills (SKILL-GRAPH Domain Registry) |
| `route_unclear` | trigger ambiguous | ask user / repo AGENTS (optional reasoning-strategy-selector for explicit multi-match) |
| `route_skillqa` | skill quality / structure | `skill-reviewer` |
| `route_obvious` | single clear match | that skill directly |
| `route_multi` | multi-step / broad | sub-agent + re-apply routing inside |
| `route_sysml` | `sysml-v2-models/*` edit | `sysml-modeling-session-checklist` -> `sysml-modeling-workflow` -> one `sysml-*` specialist |

Shared-dialect mutate sketch:

```text
## Nodes
+ CLM [NEW] ; type=decision ; code=route_model->llm-model-suggester ; recycle=persistent

## Edges
+ E01 [NEW] --(routes_to)--> [llm-model-suggester] ; note=model_choice ; recycle=persistent
```

---

## Path rules

```text
## Nodes
RUL [P01] ; kind=MUST ; code=skill-id = immediate child dir under <pack-root> ; priority=high ; recycle=persistent
RUL [P02] ; kind=MUST ; code=entry file = <pack-root>/<skill-id>/SKILL.md (no alternates) ; priority=high ; recycle=persistent
RUL [P03] ; kind=MUST ; code=discover ids via glob <pack-root>/*/SKILL.md; do not invent ; priority=high ; recycle=persistent
RUL [P04] ; kind=MAY ; code=aliases -> ids via SKILL-GRAPH.md Map section ; priority=low ; recycle=persistent
```

Optional sub-folders per skill: `references/`, `assets/`, `tools/`, `Folder_Structure.md`.

---

## Cross-references

- **Routing aid:** [SKILL-GRAPH.md](SKILL-GRAPH.md) -- hub -> [`skill-graph-seed.wire`](reasoning-strategy-selector/references/skill-graph-seed.wire) (engine seed; docs use shared dialect).
- **Handoff aid:** `memnet-goldfish-loop.mdc` + `memnet-format/SKILL.md` + `mcp-memnet` + `sysml-memnet-pipeline.md`; plain Markdown when MemNet down.
- **Model routing aid:** `llm-model-suggester/SKILL.md`.

---

## Worked example -- Leo CubeSat QPD pipeline

Project: `sysml-v2-models/projects/leo-cubesat-laser-comm/`. Scenario: multi-stage DSP firmware (acquisition -> demod -> position -> aggregation) with thread states, inter-stage ports, latency budget.

Skill chain (shared dialect -- mutate):

```text
## Edges
+ E1 [NEW] --(next)--> [sysml-modeling-workflow] ; note=preflight ; recycle=persistent
+ E2 [NEW] --(next)--> [sysml-nested-structure-modeling] ; note=decompose ; recycle=persistent
+ E3 [NEW] --(next)--> [sysml-signal-processing-pipeline] ; note=stage_ports ; recycle=persistent
+ E4 [NEW] --(next)--> [sysml-behaviour-generator] ; note=thread_states ; recycle=persistent
+ E5 [NEW] --(next)--> [sysml-connections] ; note=verify_dataflow ; recycle=persistent
+ E6 [NEW] --(next)--> [sysml-view-doc-sync] ; note=sync_outputs ; recycle=persistent
```

(From: `sysml-modeling-session-checklist` -> ... as listed; copy assigned ids from the pin map after mint.)

Outcome facts (shared dialect -- bare present after settle):

```text
## Nodes
CLM [leo_q1] ; type=fact ; code=thread_sm:idle->armed->sampling<->paused->error ; status=settled ; recycle=persistent
CLM [leo_q2] ; type=fact ; code=ports:RawSamplePort,DemodulatedDataPort,PositionDataPort ; status=settled ; recycle=persistent
CLM [leo_q3] ; type=fact ; code=stages:SpiAcquisition,LockInDemod,PositionCalc,DataAggregation ; status=settled ; recycle=persistent
CLM [leo_q4] ; type=metric ; code=latency_end_to_end<500us ; status=settled ; recycle=persistent
SYM [SYM_leo_dsp] ; name=deploy-leo-cubesat-laser-comm.sysml ; kind=composite ; note=190-858 ; recycle=persistent
MOD [MOD_leo_doc] ; path=outputs/system-design-report/02b-interconnection.md ; recycle=persistent
```

---

**End.** Existence of many skill folders != permission to run them all.
