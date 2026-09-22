---
name: memnet-planner
description: >-
  OPS-ONLY MemNet tip/engine plumbing. Do NOT use as SysMLEdge product face or
  SysML day-1 query path. Product face is sysmledge
  (rev_status/ask/gql/pin_map/propose).
---
# OPS-ONLY - not SysMLEdge product teach

Soft-pass kill: teaching tip MemNet MCP as the SysML query face.
Product / Cursor day-1: **sysmledge-workflow** and **sysmledge-host-model-at-rev**.
Callable face: product `sysmledge` / `user-sysmledge`. tip != face.

(Original tip/engine content below for operators only.)

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
6. **Run a wave** -- only when asked, or Bind ready already holds; [references/execution-waves.md](references/execution-waves.md) (wave, checkpoint, repeat).

**Campaign attach:** if the repo already cues `goal=TSK_model_<short>`, the plan task `CHILDOF` that campaign. The campaign stays the mission cue; this skill cues the plan task for edit.

**Multitask:** while planning, still write `wave` / `scope` / `PRECEDES`. Running a wave uses [memnet-multitask](../memnet-multitask/SKILL.md) (shared TCP/HTTP; Task `model` from User Rules; runtime loop = spawn wave, end turn, checkpoint, repeat).

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
- Mint one bundled Implement step for a single Implement worker to run sequentially.
- Settle plan or sibling steps from worker chat.
- Re-spawn a step that already has `llm_id` set (claimed).
- Collapse several worker waves into one parent turn.
