# Plan graph (MemNet session)

Wire: [memnet-format](../../memnet-format/SKILL.md). Tools: [mcp-memnet](../../mcp-memnet/SKILL.md).

## Kinds

| Kind | Role | Typical props |
|------|------|----------------|
| `:TSK` `phase:'plan'` | Plan root | `goal`, `phase`, `status`, `recycle` |
| `:TSK` `phase:'step'` | Ordered step | `goal`, `phase`, `ord`, `wave`, `scope`, `status`, `recycle` |
| `:USR` | Constraint that must survive polish | `topic`, `content`, `status` (`active` / `superseded`) |
| `:CLM` | Assumption or polish note | `type` (`assumption` / `polish`), `code`, `status` |
| `:DEC` | Open choice | `code`, `status` (`open` / `closed`) |

Optional house nickname property `id` (e.g. `TSK_plan_foam_ui`) is **not** graph identity. Cue with `kind` + `goal=` or `phase=plan`.

## Status (tasks)

| Kind | Live | Finished |
|------|------|----------|
| Plan or step `:TSK` | `in_progress` | `settled` |
| `:USR` | `active` | `superseded` |

Do not use `done` or `active` on `:TSK`.

**Cardinality:** one in-progress plan root per session. Steps are children, not second roots. Prefer one live campaign `:TSK` (`goal=TSK_model_<short>`) plus this plan as `CHILDOF`.

**Recycle:** plan root `persistent` until the work is abandoned. Step rows default `delete_on_settle`. Constraints `persistent` while `active`.

## Rel types

| Rel | Direction | Meaning |
|-----|-----------|---------|
| `CHILDOF` | step -> plan, or plan -> campaign | Parent cue |
| `PRECEDES` | earlier step -> later step | Later not ready until earlier `settled` |
| `constrained_by` | plan -> USR | User constraint |
| `about` | CLM or DEC -> plan or step | Note / decision |

## SCHEMA (`session_open` `map_lines`)

```text
SCHEMA TSK ; fields=goal phase ord wave scope status recycle
SCHEMA USR ; fields=topic content status recycle
SCHEMA CLM ; fields=type code status recycle
SCHEMA DEC ; fields=code status recycle
```

Cover every kind you will mutate. Missing kind -> `unknown_tag`.

## Draft (CREATE)

```cypher
CREATE (p:TSK {goal: 'Plan: recover PoE camera', phase: 'plan', status: 'in_progress', recycle: 'persistent'})
CREATE (s1:TSK {goal: 'Confirm port mapping', phase: 'step', ord: 1, wave: 1, scope: 'items-host-config.sysml', status: 'in_progress', recycle: 'delete_on_settle'})
CREATE (s2:TSK {goal: 'Draft collector chip copy', phase: 'step', ord: 2, wave: 1, scope: 'watchdog-collector/static/app.js', status: 'in_progress', recycle: 'delete_on_settle'})
CREATE (s3:TSK {goal: 'Cycle PoE then re-open pipeline', phase: 'step', ord: 3, wave: 2, scope: 'poe_port_power.py', status: 'in_progress', recycle: 'delete_on_settle'})
CREATE (s1)-[:CHILDOF {note: 'step', recycle: 'persistent'}]->(p)
CREATE (s2)-[:CHILDOF {note: 'step', recycle: 'persistent'}]->(p)
CREATE (s3)-[:CHILDOF {note: 'step', recycle: 'persistent'}]->(p)
CREATE (s1)-[:PRECEDES {recycle: 'persistent'}]->(s3)
CREATE (s2)-[:PRECEDES {recycle: 'persistent'}]->(s3)
CREATE (u:USR {topic: 'safety', content: 'no unauthorised switch writes', status: 'active', recycle: 'persistent'})
CREATE (p)-[:constrained_by {recycle: 'persistent'}]->(u)
```

`s1` and `s2` share `wave: 1` (disjoint `scope`). `s3` is `wave: 2` after both. Waves: [execution-waves.md](execution-waves.md).

Attach to an existing campaign:

```cypher
MATCH (c:TSK {goal: 'TSK_model_vfdl2'}), (p:TSK {goal: 'Plan: recover PoE camera', phase: 'plan'})
CREATE (p)-[:CHILDOF {note: 'plan', recycle: 'persistent'}]->(c)
```

## Cue

| Want | Cue |
|------|-----|
| The plan | `kind='TSK'`, locators `phase=plan` and/or `goal=Plan: ...` |
| Outline of S | empty `pin_map` q |
| Ego unknown | `find` with `limit`, then `pin_map` |

When `|Q|>1` for plan roots: CueConflict -- do not pick one.

## Retrieval seeds

memnet plan, session plan, TSK phase plan, CHILDOF step, PRECEDES wave, mutate plan, pin_map plan, SCHEMA TSK
