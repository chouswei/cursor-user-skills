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

| Host | How to run a ready wave |
|------|-------------------------|
| Multitask **off** | Parent runs ready steps **in `ord`** (even if `wave` ties). Graph still stores waves for a later parallel host. |
| Multitask **on** | Load memnet-multitask. Shared TCP or HTTP (`memnet-pi`); **MUST NOT** in-process. One worker per ready step in that `wave`. Pass session id, cue `kind=TSK` `goal=` of **that step**, `scope`, `llm_id`. `reserve` if scopes overlap. **End the turn** -- no poll. |

**Ready step:** `status='in_progress'`, `llm_id` empty (or absent), and every `PRECEDES` predecessor is `settled`.

**Claim before spawn:**

```cypher
MATCH (s:TSK {phase: 'step', goal: 'Confirm port mapping', ord: 1})
SET s.llm_id = 'worker-a'
```

MUST NOT spawn a step that already has a non-empty `llm_id`. That blocks double-spawn on a re-entrant coordinator turn.

Parent **owns** settle: next coordinator turn `pin_map` the plan, then `SET` step `status='settled'` from **graph facts**, not worker prose. Workers MUST NOT settle the plan root or sibling steps.

Prefer **one worker per step**. Do not spawn two workers on the same step or the same `scope` without RSV.

If the step is a nested `session=` interior: pass that `session=` in the worker prompt; worker goldfish only that S.

## Spawn prompt (parent -> worker)

Include: mission `session`, step `goal=`, locators, `scope`, `llm_id`, "mutate only this subgraph", "do not settle parent plan `:TSK`".

## Retrieval seeds

plan wave, parallel steps, PRECEDES step, multitask plan execution, reserve overlapping scope, llm_id claim spawn
