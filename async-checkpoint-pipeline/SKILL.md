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
  version: "1.0"
---

# Async checkpoint pipeline

Parent coordinates. Workers execute one atom. A **checkpoint** is the next parent turn after a wave; a worker MUST NOT declare the job done.

Skip this skill when the parent can finish a short in-scope answer with its own tools.

Pairing: [memnet-multitask](../memnet-multitask/SKILL.md) (shared MemNet session). [sysmledge-cursor-multitask](../sysmledge-cursor-multitask/SKILL.md) when both product `sysmledge` and tip `memnet` are visible. Model slugs: User Rules **Model by role**. Atom schema: [references/atom-and-wave.md](references/atom-and-wave.md). Role duties: [references/roles.md](references/roles.md).

## Route (parent)

| Signal | Next |
|--------|------|
| Unknown cause | Diagnose, then Bind |
| Complex new architecture | Architect (thin), accept, then Bind |
| Normal multi-step | Bind (plan + atom cards) |
| Short in-scope answer | Parent tools; no pipeline |

Grok parent **does Bind on parent**. Spawn a Bind worker only when the parent family is not Grok. MUST still emit Bind-ready atom cards before Implement. MUST NOT skip Bind because the parent is Grok.

Parent always: mint/settle `TSK_*` / `USR_*`, spawn, checkpoint. Parent MUST NOT Implement, Deploy, Visual, or Web when Bind tagged those roles.

## Two phases (MUST)

**Planner phase** -- at most one of Architect, Diagnose, or Bind-as-worker. Spawn it, then **end the turn**. Do not spawn Implement in the same message as a planner worker.

**Execute phase** -- only after Bind-ready atom cards exist (this turn if Bind was on parent; else the Bind checkpoint). Spawn **one** background Task **per** ready disjoint atom in the **same** message. Then **end the turn**.

Cursor Multitask "one coherent worker" MUST NOT collapse those atoms. One worker only when Bind emits one atom, the next atom is serial on prior proof, or the answer is a trivial parent call.

## Spawn recipe (Cursor Task)

For each ready atom:

| Field | Value |
|-------|--------|
| `description` | Role + atom id (distinct) |
| `subagent_type` | `generalPurpose` (house roles are not Cursor types) |
| `model` | Resolved slug from User Rules; MUST NOT omit / `inherit` |
| `run_in_background` | `true` |
| `prompt` | One atom card + return contract + session / `projectId@rev` |
| `environment` | `local` unless the user asked for cloud |

MUST NOT use `resume` to start a different atom. Resume the same atom only after a failed proof. MUST NOT use GPT Luna or `*-fast` for Architect, Bind, Diagnose, Deploy, Visual, or Web. MUST NOT default every atom to Implement. MUST name the slug used.

After the Task calls: no poll, no `AwaitShell`, no extra file edits. End the turn.

## Checkpoint (parent)

1. Campaign work: tip `user-memnet` `pin_map` with `session=` (ops only). SysMLEdge-based bound desk: product `user-sysmledge` `rev_status` / `ask` / `pin_map`. Tip is not the model SSOT.
2. Each finished worker: proof command produced sane output (`pass_if`). Fail -> same-atom resume or re-Bind that atom. Pass -> settle that atom.
3. Deploy proof: live host shows the change, PIDs/markers recorded, rollback stated. Local tests are not deploy proof.
4. Remaining waves: spawn the next ready set, end the turn. None left: stop.
5. Human desk Save is not an agent finish step.

## SysML

Architect I/O stays thin (pointers only). Bind fills purpose, packages, part/port/qname from the working model SSOT (SysMLEdge graph when bound; else `AGENTS.md` path, house default `sysml-models/`). Bound: `propose`; human Save; then sync files. Unbound or repo-based: Implement edits `.sysml` after Bind ready, then outputs and `parts/**`.
