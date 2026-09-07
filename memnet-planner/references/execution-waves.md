# Execution waves (plan-time multitask)

Doctrine: [memnet-multitask](../../memnet-multitask/SKILL.md). Nested interiors: [memnet-nested-sessions](../../memnet-nested-sessions/SKILL.md).

Record **how steps may run** while **drafting**, not only when spawning workers. Execution reads the same graph.

## Properties on step `:TSK`

| Prop | Meaning |
|------|---------|
| `ord` | Display / stable identity with `goal` |
| `wave` | Integer. Same `wave` => candidates for one parallel spawn |
| `scope` | Short write neighbourhood (`path=`, `qname=`, or `session=` cut). Empty => treat as overlapping |
| `llm_id` | Claim. Empty = not spawned. Parent sets worker id **before** spawn |

Default if unsure: `wave = ord` (fully serial). Do not invent parallelism.

## Rel: `PRECEDES`

`(earlier)-[:PRECEDES {recycle:'persistent'}]->(later)` -- later is not ready until earlier is `settled`.

MUST: every step in `wave N+1` that needs a result from `wave N` has `PRECEDES` from that earlier step. MUST NOT: `PRECEDES` between two steps in the **same** `wave` (that is serial; put them in different waves).

## Same-wave gate (planning)

Put two steps in the same `wave` only when **all** hold:

1. No `PRECEDES` between them.
2. Write `scope` is **disjoint** (different files / qnames / interiors), **or** the parent will `reserve` one neighbourhood and run **one** writer.
3. The plan shell is already named (plan root + children exist). If still inventing the plan: keep serial (`wave = ord`).

Otherwise bump `wave`.

## Execute (only when the user asks to run)

Task `model` for each step is User Rules **unsync checkpoint pipeline** (Model by role). Do not copy that table here.

| Host | How to run a ready wave |
|------|-------------------------|
| Multitask **on** | Load memnet-multitask. Shared TCP or HTTP (`memnet-pi`); **MUST NOT** in-process. One worker per ready step in that `wave`. Pass session id, cue `kind=TSK` `goal=` of **that step**, `scope`, `llm_id`, role `model`. `reserve` if scopes overlap. **End the turn** -- no poll. Next coordinator turn is a checkpoint. |
| Multitask **off** | Still spawn Task with the role slug (one ready step at a time in `ord` if the host cannot parallelise). Graph still stores `wave`. MUST NOT collapse Execute into the parent model. |

**Ready step:** `status='in_progress'`, `llm_id` empty (or absent), and every `PRECEDES` predecessor is `settled`.

**Claim before spawn:**

```cypher
MATCH (s:TSK {phase: 'step', goal: 'Confirm port mapping', ord: 1})
SET s.llm_id = 'worker-a'
```

MUST NOT spawn a step that already has a non-empty `llm_id`. That blocks double-spawn on a re-entrant coordinator turn.

Parent **owns** settle: next coordinator turn `pin_map` the plan, then `SET` step `status='settled'` from **graph facts**, not worker prose. Workers MUST NOT settle the plan root or sibling steps.

Prefer **one worker per step**. After Bind ready, Execute steps are atoms (one path, qname, or proof); spawn one Execute worker per ready atom in the same `wave` when scopes are disjoint. Do not spawn two workers on the same step or the same `scope` without RSV. Do not mint one bundled Execute step that a single Execute worker must run sequentially.

If the step is a nested `session=` interior: pass that `session=` in the worker prompt; worker goldfish only that S.

## Checkpoint loop

A checkpoint is a **coordinator turn** after a wave, not a worker self-declaration. Wave count sets checkpoint count. Named checkpoint kinds live in User Rules -- MUST NOT copy that table here. MUST NOT treat those kinds as "only four turns".

On each checkpoint turn:

1. `pin_map` the plan (cue / `find` if ego lost).
2. Settle finished steps from graph facts and proof commands -- not from worker chat.
3. If a ready wave remains: claim `llm_id`, spawn that wave (one Execute worker per execute atom after Bind ready), end the turn.
4. Else stop.

Execute after Bind ready usually yields **several** Execute-proof checkpoints (one per Execute wave). MUST NOT skip the checkpoint and poll. MUST NOT collapse several Execute waves into one parent turn.

## Spawn prompt (parent -> worker)

Include: mission `session`, step `goal=`, locators, `scope`, `llm_id`, role `model`, "mutate only this subgraph", "do not settle parent plan `:TSK`".

## Retrieval seeds

plan wave, parallel steps, PRECEDES step, multitask plan execution, reserve overlapping scope, llm_id claim spawn, checkpoint loop, execute atom
