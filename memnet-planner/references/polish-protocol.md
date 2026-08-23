# Update and repolish

Always `pin_map` the plan task first. Apply a **delta**; do not recreate the whole tree unless the user asks to reset.

## Update (facts changed)

| Intent | Mutate |
|--------|--------|
| Reword a step | `MATCH` that step by `goal` + `ord`; `SET` `goal` |
| Reorder | `SET` `ord` on the affected steps (keep unique `ord`) |
| Change parallelism | `SET` `wave` / `scope`; add or `DELETE` `PRECEDES` (see [execution-waves.md](execution-waves.md)) |
| Add a step | `CREATE` step + `CHILDOF` to the plan |
| Drop a step | `SET` `status='settled'` (and `recycle='delete_on_settle'`) or `DELETE` the node if it never ran |
| New constraint | `CREATE` `:USR` + `constrained_by` from the plan |
| Supersede constraint | `SET` USR `status='superseded'` |

```cypher
MATCH (s:TSK {phase: 'step', ord: 2, goal: 'Cycle PoE then re-open pipeline'})
SET s.goal = 'Cycle PoE, wait 8s, then re-open pipeline'
```

## Repolish (same facts, clearer plan)

1. Pin the plan (`depth=2`, budgeted `max_rows`).
2. Name the polish in a `:CLM` `{type:'polish', code:'<short>'}` `about` the plan.
3. `SET` step `goal` strings only where wording improved; keep `ord` / `wave` unless order or parallelism actually changed.
4. Pin again. Chat Shape from the new map.

```cypher
MATCH (p:TSK {phase: 'plan', goal: 'Plan: recover PoE camera'})
CREATE (c:CLM {type: 'polish', code: 'shorter step verbs', status: 'in_progress', recycle: 'delete_on_settle'})
CREATE (c)-[:about {recycle: 'delete_on_settle'}]->(p)
```

## Settle

When the plan is finished or abandoned:

```cypher
MATCH (p:TSK {phase: 'plan', goal: 'Plan: recover PoE camera'})
SET p.status = 'settled', p.recycle = 'delete_on_settle'
```

Settle child steps the same way if they should drop from later maps. Do not settle a parent campaign `TSK_model_*` from this skill unless the user owns that campaign close-out.

Workers: parent owns settle ([memnet-multitask](../../memnet-multitask/SKILL.md)). Overlapping writers: `reserve` then matching `llm_id` on `mutate`. Execute a ready **wave** only when asked -- [execution-waves.md](execution-waves.md).

## Reset

Only if the user asks to replace the plan: settle or `DELETE` old steps, then CREATE a new tree. Keep the same plan `goal` if it is still the cue, or CREATE a new plan root and settle the old one.

## Retrieval seeds

repolish plan, update memnet plan, SET step goal, settle plan TSK, polish CLM, SET wave
