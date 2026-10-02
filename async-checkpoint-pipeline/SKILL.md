---
name: async-checkpoint-pipeline
description: >-
  Multi-wave parallel Task workers with house roles. Use when the job is
  multi-step, needs parallel disjoint edits, Architect/Bind/Diagnose/Implement/
  Deploy, Multitask Mode, spawn a wave then checkpoint, or Bind-ready atoms.
  Triggers: async checkpoint pipeline, multi-wave sub-agents, Bind ready,
  spawn wave end turn, role-tagged atoms, parallel Task workers.
metadata:
  pattern: pipeline
  domain: meta
  version: "1.1"
---

# Async checkpoint pipeline

Parent coordinates. Workers execute one atom. A **checkpoint** is the next parent turn after a wave; a worker MUST NOT declare the job done.

Pairing: [memnet-multitask](../memnet-multitask/SKILL.md) (shared MemNet session). [sysmledge-cursor-multitask](../sysmledge-cursor-multitask/SKILL.md) when both product `sysmledge` and tip `memnet` are visible. Model slugs: User Rules **Model by role**. Atom schema: [references/atom-and-wave.md](references/atom-and-wave.md). Role duties: [references/roles.md](references/roles.md).

## Named gates

| Term | Checkable meaning |
|------|-------------------|
| **Short** | One proof command, one write-path or one write-qname, empty `hosts`. Parent tools. No pipeline. |
| **Complex** | User asked for a root plan, OR the change adds a deploy part tree, OR a new port contract / allocate shape. |
| **Wave complete** | Every Task spawned for that ready set has returned `pass`, `fail`, or `blocked`. |
| **Family match** | Parent session family equals that role's User Rules family (Opus, Grok, Gemini, or Kimi). |

## Route (parent)

| Signal | Next |
|--------|------|
| Short | Parent tools; no pipeline |
| Unknown cause, not small | Diagnose, then Bind |
| Unknown cause, Grok parent, small | Bind on parent this turn |
| Complex | Architect worker (thin), accept, then Bind |
| Else | Bind (plan + atom cards) |

MUST NOT spawn Architect unless **Complex**. Grok parent **does Bind on parent**. Spawn a Bind worker only when the parent family is not Grok. MUST still emit Bind-ready atom cards before Implement. MUST NOT skip Bind because the parent is Grok.

Parent mints/settles `TSK_*` / `USR_*`. Parent MUST NOT Deploy (live host). Parent MUST NOT Implement, Visual, or Web unless **Family match** and the single-atom gate below.

## Two phases (MUST)

**Planner phase** -- at most one of Architect, Diagnose, or Bind-as-worker. Spawn it, then **end the turn**. Do not spawn Implement in the same message as a planner worker.

**Execute phase** -- only after Bind-ready atom cards exist (this turn if Bind was on parent; else the Bind checkpoint).

- If Bind emits **exactly one** atom, `hosts` is empty, role is not Deploy, and **Family match**: parent executes that atom this turn. MUST NOT spawn Task.
- Else spawn **one** background Task **per** ready disjoint atom in the **same** message (`n>=2`, or `n=1` without family match). Then **end the turn**.

Cursor Multitask "one coherent worker" MUST NOT collapse those atoms.

## Spawn recipe (Cursor Task)

For each spawned atom:

| Field | Value |
|-------|--------|
| `description` | Role + atom id (distinct) |
| `subagent_type` | `generalPurpose` (house roles are not Cursor types) |
| `model` | Resolved slug from User Rules; MUST NOT omit / `inherit` |
| `run_in_background` | `true` |
| `prompt` | One atom card + return contract + session / `projectId@rev` |
| `environment` | `local` unless the user asked for cloud |

MUST NOT use `resume` to start a different atom. Same-atom `resume` at most **twice**; then re-Bind that id. MUST NOT use GPT Luna or `*-fast` for Architect, Bind, Diagnose, Deploy, Visual, or Web. MUST NOT default every atom to Implement. MUST name the slug used.

After the Task calls: no poll, no `AwaitShell`, no extra file edits. End the turn.

## Checkpoint (parent)

1. If any Task in this ready set is still running: MUST NOT settle the wave and MUST NOT spawn the next wave. End the turn.
2. **Wave complete** only then: each returned atom -- proof command produced sane output (`pass_if`). Fail -> same-atom resume (cap above) or re-Bind that id. Pass -> settle that atom.
3. Campaign `pin_map` only if some atom in this wave listed `memnet_ids` or mutated MemNet. Bound desk `rev_status` / `ask` / product `pin_map` only if some atom in this wave wrote via `propose`. Tip is not the model SSOT.
4. Deploy proof: live host shows the change, PIDs/markers recorded, rollback stated. Local tests are not deploy proof.
5. Remaining waves: spawn the next ready set, end the turn. None left: stop.
6. Human desk Save is not an agent finish step.

## SysML

Architect I/O stays thin (pointers only). Bind fills purpose, packages, part/port/qname from the working model SSOT (SysMLEdge graph when bound; else `AGENTS.md` path, house default `sysml-models/`). Bound: `propose`; human Save; then sync files. Unbound or repo-based: Implement edits `.sysml` after Bind ready, then outputs and `parts/**`.
