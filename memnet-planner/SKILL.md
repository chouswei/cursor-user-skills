---
name: memnet-planner
description: >-
  Keep a working plan as MemNet session rows (campaign or plan task plus
  ordered step tasks with execution waves). Pin the live neighbourhood, then
  mutate to draft, update, or repolish. At plan time, mark which steps may
  run in parallel. Execute a ready wave via memnet-multitask when asked.
  Chat is a Shape of the graph, never the plan SSOT.
  Triggers: memnet plan, plan in memnet, update memnet plan, repolish plan,
  session plan, memnet planner, plan waves, parallel plan steps, execute plan
  wave. Skip: Markdown-only project-planner interview with no MemNet;
  building the MemNet engine.
metadata:
  pattern: pipeline
  version: "1.1"
  domain: memnet
  product: "memnet-llm==0.19.3"
  secondary: "hybrid: mcp-memnet + memnet-format; memnet-multitask on execute"
  pairs_with: [memnet-use, mcp-memnet, memnet-format, memnet-nested-sessions, memnet-multitask, project-planner]

pipeline_steps:
  1. Gate
     - MemNet tools in catalog. Else scratch Markdown only; say the plan is not durable.
  2. Session
     - Reuse current session. If none: session_open with the SCHEMA map in references/plan-graph.md.
  3. Cue then pin_map
     - Cue the plan task (kind TSK + phase=plan or goal=). Empty cue = outline. CueConflict if two unrelated in-progress plan roots.
  4. Draft or delta
     - New plan: mutate CREATE plan + step children with wave and PRECEDES (references/plan-graph.md + references/execution-waves.md). Existing: polish-protocol.md.
     - Same wave only if write scopes are disjoint (or one RSV writer). Else serial (wave = ord).
  5. Pin_map again
     - Drop the prior map. Present the Shape from stdout only (assets/chat-shape.md).
  6. Execute (only if the user asked to run)
     - Ready wave: predecessors settled. Multitask off -> parent serial. Multitask on -> memnet-multitask workers, then end the turn.
  7. Optional persist
     - session_save when the user wants a file snap.

system_instruction: |
  The plan SSOT is the MemNet session graph. Follow pipeline_steps in order.
  Product write is mutate (GQL). Do not teach leftover add/update or pin_map(anchor=).
  Record waves while planning. Spawn workers only on execute, and only a ready wave.
  Present a short Shape; do not paste the whole session.

token_guardrails: |
  - Do not paste sibling SKILL.md bodies; link ../mcp-memnet/SKILL.md and ../memnet-format/SKILL.md.
  - One pin_map per generate after a mutate; do not stack nested maps.
  - Cursor TodoWrite is this-turn UI only -- not the plan.
  - Do not spawn Task workers during draft unless the user asked to execute.
---

# MemNet planner

**Role:** Own the **plan graph** in the current MemNet session. Delegate tool names and wire shape to [mcp-memnet](../mcp-memnet/SKILL.md) and [memnet-format](../memnet-format/SKILL.md). Goldfish loop: [memnet-use](../memnet-use/SKILL.md). Nested catalog interiors: [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md). Human requirements interview without a graph: [project-planner](../project-planner/SKILL.md) first, then this skill to persist the result.

There is **no** `:PLAN` kind. A plan is one `:TSK` with `phase:'plan'` plus child `:TSK` steps (`phase:'step'`, `ord`, `wave`). Parallelism is a **wave** plus `PRECEDES`, not a second plan root.

## Execution contract

1. **Gate** -- if MemNet MCP is missing, stop durable writes.
2. **Session** -- same `session` id for the whole plan lifetime.
3. **Read** -- `pin_map` from a cue; `find` if ego unknown.
4. **Write** -- one `mutate` with many statements; then `pin_map`.
5. **Chat** -- fill [assets/chat-shape.md](assets/chat-shape.md) from the new map.
6. **Execute** -- only when asked; [references/execution-waves.md](references/execution-waves.md).

**Campaign attach:** if the repo already cues `goal=TSK_model_<short>`, the plan task `CHILDOF` that campaign. The campaign stays the mission cue; this skill cues the plan task for edit.

**Multitask:** while planning, still write `wave` / `scope` / `PRECEDES`. Running a wave uses [memnet-multitask](../memnet-multitask/SKILL.md) (shared TCP/HTTP; parent settles from the next `pin_map`).

## Delegated skills

| Skill | Path | When |
|-------|------|------|
| mcp-memnet | ../mcp-memnet/SKILL.md | session, pin_map, mutate, save |
| memnet-format | ../memnet-format/SKILL.md | GQL wire, labels |
| memnet-use | ../memnet-use/SKILL.md | goldfish; settle |
| memnet-nested-sessions | ../memnet-nested-sessions/SKILL.md | plan lives in another `session=` cut |
| memnet-multitask | ../memnet-multitask/SKILL.md | execute a ready wave (shared store, RSV, no poll) |

## Resources

- [references/plan-graph.md](references/plan-graph.md) -- kinds, status, SCHEMA, CREATE
- [references/execution-waves.md](references/execution-waves.md) -- plan-time waves; execute ready wave
- [references/polish-protocol.md](references/polish-protocol.md) -- update / repolish / settle
- [assets/chat-shape.md](assets/chat-shape.md) -- user-visible Shape

## MUST NOT

- Treat chat, README, or TodoWrite as the plan.
- Leftover `add` / `update` / `anchor=` / `id:'NEW'` as TARGET.
- Two in-progress plan roots in one session (CueConflict).
- Dump session S.
- Same `wave` for steps that share a write `scope` without RSV.
- Settle plan or sibling steps from worker chat.
