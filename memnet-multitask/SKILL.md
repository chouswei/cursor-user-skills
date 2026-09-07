---
name: memnet-multitask
description: >-
  Enforceable MemNet doctrine for Cursor Multitask Mode and Task sub-agents:
  one shared session SSOT, TCP or streamable-http transport, parent/worker
  MUST/MUSTNOT, MN-REQ-12 usage, system-dev two-store pattern for modelbasedPrj-*.
  Triggers: Multitask Mode, multitask, multi-agent, Task sub-agent, background
  worker, parent coordinator, delegate worker, shared session, memnet multitask,
  system-dev multitask, modelbasedPrj multitask, MN-REQ-12, parallel workers,
  TSK_* settle, TCP serve, streamable-http MCP, GQL wire, shaped pin_map,
  checkpoint loop, execute atom, parallel Execute workers.
metadata:
  pattern: pipeline
  version: "3.1"
  domain: memnet
  product: "memnet-llm==0.19.3"
---

# MemNet + Multitask Mode

User-pack skill for **applying** MemNet under Cursor **Multitask Mode** or **Task** sub-agents. Pair with [mcp-memnet](../mcp-memnet/SKILL.md) (tools) and [memnet-format](../memnet-format/SKILL.md) (GQL wire / shaped pin_map).

**Product ops SSOT:** MemNet `docs/operations/multi-agent-sessions.md`.
**System-repo adoption:** MemNet `docs/application-notes/system/llm-system-dev-multitask.md`.
**Shape / version map:** MemNet `docs/SHAPE.md`, `docs/ROADMAP.md`.
**Package and PyPI 0.19.3** (extras 0.10-0.19 unchanged). **1.0** unclaimed (claim of 0.5-0.8). Chat is **never** mission SSOT.

## When to load

| Signal | Action |
|--------|--------|
| Multitask Mode on | Follow this skill + MemNet `docs/operations/multi-agent-sessions.md` |
| Spawning Task / background workers | Parent checklist below; pass session id in every worker prompt |
| Plan with parallel steps | [memnet-planner](../memnet-planner/SKILL.md) records `wave` / `PRECEDES` at plan time; this skill runs a **ready wave** |
| `modelbasedPrj-*` system repo + Multitask | Also read MemNet `docs/application-notes/system/llm-system-dev-multitask.md` |
| Single-agent goldfish loop | [memnet-use](../memnet-use/SKILL.md) -- default in-process MCP |

## Transport (shared store)

| Transport | Multitask |
|-----------|-----------|
| **MCP in-process** (default) | **MUST NOT** -- isolated graph per process |
| **CLI + `memnet serve`** (TCP `:18765`) | **MUST** when workers share one session id |
| **MCP streamable-http** (`:18766/mcp`) | Same as TCP when all agents hit the **same** HTTP process **bridged to that serve** |

Set `MEMNET_MCP_TRANSPORT=tcp` on the shared HTTP MCP (or use TCP CLI). Probe with `serve_status` before delegating if uncertain. User-pack: Cursor **`memnet-pi`** HTTP `http://10.0.0.10:18766/mcp`. InvenTree MCP is not MemNet. Detail: [mcp-memnet](../mcp-memnet/SKILL.md).

## Model and checkpoint

Task `model` SSOT is User Rules **unsync checkpoint pipeline** (Model by role). This skill owns shared session, transport, RSV, the **wave/checkpoint loop**, and parent/worker split -- not the role table and not the named checkpoint kinds.

## Runtime loop

The pipeline is a **loop**. Wave count sets checkpoint count.

1. Parent mints `TSK_*` / `USR_*`. Trivial single-tool work stays in the parent.
2. Spawn **one ready wave** only (disjoint `scope`, or one RSV writer). One worker per step. After Bind ready, Execute steps are **atoms** (one path, qname, or proof): spawn one Execute worker per atom in that wave. MUST NOT hand one Execute worker a bundled sequential job.
3. **End the turn** -- no poll, no await.
4. Next coordinator turn is a **checkpoint**: `pin_map` first; settle from graph facts and proof commands; spawn the next ready wave or stop.
5. Repeat 2-4 until no ready steps remain.

Named checkpoint kinds live in User Rules. MUST NOT copy that table here. MUST NOT treat those kinds as "only four turns" -- each wave produces its own checkpoint. Execute after Bind ready usually yields several Execute-proof checkpoints.

One role model per step (no committee on the same atom). Many Execute workers in one wave is not a committee.

## Parent coordinator

### MUST

- `session_open` / `session_load` **one** mission `session` id; pass it in every worker prompt.
- Mint and own **`TSK_*`** / **`USR_*`**: `status=active` -> `status=settled`; optional `led_to_success` edges. Prefer **one live `TSK`** (0.5 V5). leftover NEW mint is leftover.
- Self-contained worker prompts: session id, cue locators (`kind` / `goal=` / `path=` / `qname=`), write scope (subgraph or relation types), return shape, **`llm_id`**, Task `model` from User Rules. leftover nickname `id` is leftover.
- **`reserve`** overlapping neighbourhoods before parallel mutate (shipped RSV); pass matching `llm_id` on worker **`mutate`**.
- **End the turn** after background spawn -- no poll, no await.
- Next coordinator turn: **checkpoint** -- **`pin_map` first** (cue / `find` if ego lost); settle from the refreshed slice; then the next ready wave or stop -- do not redo worker investigation from chat.
- Prefer **one worker per execute atom**; Execute MUST run many atoms in one wave when scopes are disjoint. Parallel only when the **parent shell is already clear** and interiors are **disjoint** (or RSV) -- [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md).

### MUST NOT

- Treat chat, tool transcripts, or sub-agent prose as durable mission state.
- Settle `TSK_*` / `USR_*` from worker chat -- only from shared-session pin-map facts.
- Use in-process MCP for a shared mission.
- Run parallel writers on the **same** reserved slice with different `llm_id`s.
- Do the worker's role when that role applies (Plan/Detail/Execute stay on the spawned model).
- Copy the User Rules role table or checkpoint-kind list into this skill.
- Skip a checkpoint turn, or collapse several Execute waves into one parent turn.

## Worker agent

### MUST

- Use the parent's **session id**; **`pin_map` first** every turn (or `find` then pin_map).
- Cue locators from the pin map -- **MUST NOT** invent a store key. leftover nickname `id` is leftover.
- Mutate only under the **assigned subgraph**.
- Pass the assigned **`llm_id`** on mutate when RSV is held.
- Return a concise result; durable facts live in MemNet rows.

### MUST NOT

- Open a different session unless explicitly assigned.
- Use in-process MCP when the parent uses shared TCP/HTTP.
- Settle parent-owned `TSK_*` / `USR_*` unless delegated.

## MN-REQ-12 usage (MemNet product repo)

When working **in** the MemNet engine repository:

| Step | Path |
|------|------|
| Requirements group | `sysml-models/models/requirements.sysml` -- **MN-REQ-12** leaves 12.1-12.8 |
| Verify package | `sysml-models/models/verify.sysml` -- **MN-VER-12-G00** + **S01...S14** |
| Worked scenario | `sysml-models/outputs/multitask-case-study.md` |

In downstream **`modelbasedPrj-*`** repos: adopt via doc pointer or thin local mirror -- **do not** import `MemNetRequirements` into the product load tree unless the project owns a merged model.

## System-dev two-store pattern (`modelbasedPrj-*`)

| Store | SSOT for |
|-------|----------|
| **MemNet session** (TCP/HTTP) | Mission goldfish: `TSK_*`, `USR_*`, scoped `MOD_*` / `SYM_*`, `CLM_*` / `DEC_*` |
| **Product `sysml-models/`** (git) | Structural model: requirements, deploy, behaviour |
| **Source tree** | Code and artefacts on disk |

Path-B: **`ingest_*`** into the current session (locator ids; **no** leftover NEW). Catalog Snap: **`snap_model`**. Export: **`export_pin_map`**. Ingest is **not** export.

## Shipped vs still design (package 0.19.3)

| Capability | Status |
|------------|--------|
| Neighbourhood RSV | **Shipped** |
| Path-B ingest | **Shipped** |
| CapsPolicy ACL | **Shipped opt-in** (`session_acl_enable`) |
| Live AgensGraph | **Claimed 0.7** when URL set |
| Neo4j live | **Claimed 0.14** (`liveNeo4jClaimed=true`). Do not write hydrate-by-hid proven. Do not vendor a server. |
| HostSearch locators | Extra **0.17** (`RagHostHook`; no `rag_query`) |
| Peak_L | Extra **0.18** (last-resort; not default goldfish) |
| Pin-map export / catalog Snap | Extra **0.19** / **0.15** |
| Session ACL modes / `session_token` | **Design** -- MemNet `docs/extras/memnet-security-multi-agent.md` |
| N-server | **Research** #47 |
| Write without RSV | Last-write-wins |

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Chat as SSOT for ids / mission state | Parent and workers diverge |
| In-process MCP under Multitask | Each process gets its own graph |
| Parent polls or re-runs worker work | Token waste; violates turn boundary |
| Coordinator does the worker's role | Skips the unsync checkpoint pipeline |
| One bundled Execute worker for all Execute steps | User Rules: Execute is atomised parallel workers |
| One proof turn for all Execute waves | Wave count sets checkpoint count; each wave has its own checkpoint |
| Worker mints duplicate `TSK_*` | Parent owns task lifecycle |
| Teaching full ACL modes / `rag_query` as available | Full ACL modes still design; HostSearch is locators only (**0.17**) |
| Skipping RSV on overlapping parallel mutate | Last-write-wins |
| Teaching live Neo4j unclaimed / HostSearch as Later | leftover 0.9 law |

## Related (user pack)

| Skill | Role |
|-------|------|
| [mcp-memnet](../mcp-memnet/SKILL.md) | MCP tools, transport, session lifecycle |
| [memnet-format](../memnet-format/SKILL.md) | MemNet GQL wire / shaped pin_map |
| [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md) | Look loop / nested `session=` |
| [memnet-use](../memnet-use/SKILL.md) | How-to hub |
| [memnet-planner](../memnet-planner/SKILL.md) | Plan-time `wave` / `PRECEDES`; this skill executes a ready wave |
| [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md) | SysML relatives (pair when SysML + Multitask) |
