---
name: memnet-multitask
description: >-
  Enforceable MemNet doctrine for Cursor Multitask Mode and Task sub-agents:
  one shared session SSOT, TCP or streamable-http transport, parent/worker
  MUST/MUSTNOT, MN-REQ-12 usage, system-dev two-store pattern for modelbasedPrj-*.
  Triggers: Multitask Mode, multitask, multi-agent, Task sub-agent, background
  worker, parent coordinator, delegate worker, shared session, memnet multitask,
  system-dev multitask, modelbasedPrj multitask, MN-REQ-12, parallel workers,
  TSK_* settle, TCP serve, streamable-http MCP.
metadata:
  pattern: pipeline
  version: "1.0"
  domain: memnet
  product: memnet-llm==0.4.2
---

# MemNet + Multitask Mode

User-pack skill for **applying** MemNet under Cursor **Multitask Mode** or **Task** sub-agents. Pair with [mcp-memnet](../mcp-memnet/SKILL.md) (tools) and [memnet-format](../memnet-format/SKILL.md) (wire shapes).

**Product ops SSOT (MemNet repo, developers):** `docs/multi-agent-sessions.md`.
**System-repo adoption (applications):** MemNet `docs/application-notes/llm-system-dev-multitask.md`.
**Docs index:** MemNet `docs/README.md`. Chat is **never** mission SSOT.

## When to load

| Signal | Action |
|--------|--------|
| Multitask Mode on | Follow this skill + MemNet `docs/multi-agent-sessions.md` |
| Spawning Task / background workers | Parent checklist below; pass session id in every worker prompt |
| `modelbasedPrj-*` system repo + Multitask | Also read MemNet `docs/application-notes/llm-system-dev-multitask.md` |
| Single-agent goldfish loop | [mcp-memnet](../mcp-memnet/SKILL.md) only -- default in-process MCP is fine |

## Transport (shared store)

| Transport | Multitask |
|-----------|-----------|
| **MCP in-process** (default) | **MUST NOT** -- isolated graph per process |
| **CLI + `memnet serve`** (TCP `:18765`) | **MUST** when workers share one session id |
| **MCP streamable-http** (`:18766/mcp`) | Same as TCP when all agents hit the same server |

Set `MEMNET_MCP_TRANSPORT=tcp` (or streamable-http). Probe with `serve_status` before delegating if uncertain. User-pack transport detail: [mcp-memnet](../mcp-memnet/SKILL.md).

## Parent coordinator

### MUST

- `session_open` / `session_load` **one** mission `session` id; pass it in every worker prompt.
- Mint and own **`TSK_*`** / **`USR_*`**: `status=active` -> `status=settled`; optional `led_to_success` edges.
- Self-contained worker prompts: session id, anchor ids, write scope (subgraph or relation types), return shape.
- **End the turn** after background spawn -- no poll, no await.
- Next coordinator turn: **`pin_map` first**; act from refreshed slice -- do not redo worker investigation from chat.
- Prefer **one worker** per coherent workstream; parallel only with **disjoint** anchors or **separate** session ids.

### MUST NOT

- Treat chat, tool transcripts, or sub-agent prose as durable mission state.
- Settle `TSK_*` / `USR_*` from worker chat -- only from shared-session pin-map facts.
- Use in-process MCP for a shared mission.
- Run parallel workers on the **same** anchor slice without serialisation (0.4.x last-write-wins).

## Worker agent

### MUST

- Use the parent's **session id**; **`pin_map` first** every turn.
- Copy assigned ids from pin map -- **MUST NOT** invent ids the parent already minted.
- Mutate only under the **assigned subgraph** (anchors + relations in the prompt).
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
| Verify package | `sysml-models/models/verify.sysml` -- **MN-VER-12-G00** + **S01...S09** |
| Worked scenario | `sysml-models/outputs/multitask-case-study.md` |

In downstream **`modelbasedPrj-*`** repos: adopt via doc pointer or thin local mirror -- **do not** import `MemNetRequirements` into the product load tree unless the project owns a merged model. Detail: MemNet `docs/application-notes/llm-system-dev-multitask.md` section 6.

## System-dev two-store pattern (`modelbasedPrj-*`)

| Store | SSOT for |
|-------|----------|
| **MemNet session** (TCP/HTTP) | Mission goldfish: `TSK_*`, `USR_*`, scoped `MOD_*` / `SYM_*`, `CLM_*` / `DEC_*` |
| **Product `sysml-models/`** (git) | Structural model: requirements, deploy, behaviour |
| **Source tree** | Code and artefacts on disk |

Recommended order when both SysML and code change: **SysML worker first** (disjoint `MOD_*` under `sysml-models/`), then **code worker** (`parts/`, tests). Full pattern: MemNet `docs/application-notes/llm-system-dev-multitask.md`.

Path-B external pins: seed via `session_open` `seed_lines` or `add` with deterministic locator ids -- **not** `PinMapIngest_*` (roadmap only).

## Deferred -- MUST NOT assume (0.4.x)

| Capability | Status |
|------------|--------|
| Session ACL (`private` / `shared` / `open`), roles, `session_token` | Design -- MemNet `docs/grammar/memnet-security-multi-agent.md` |
| Neighbourhood reserve (`RSV`, `llm_id` + TTL) | Design -- MemNet `docs/grammar/memnet-neighbourhood-reserve.md` |
| `PinMapIngest_*` engines (SysML, codebase, PCBA, skills) | Roadmap stubs -- MN-REQ-12.7 / MN-VER-12-S09 |
| Engine **WorkerWriteScope** enforcement | Doctrine only -- last-write-wins in 0.4.x |

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Chat as SSOT for ids / mission state | Parent and workers diverge |
| In-process MCP under Multitask | Each process gets its own graph |
| Parent polls or re-runs worker work | Token waste; violates turn boundary |
| Worker mints duplicate `TSK_*` | Parent owns task lifecycle |
| Teaching ACL / `RSV` / ingest as available | Not enforced in 0.4.x |

## Related (user pack)

| Skill | Role |
|-------|------|
| [mcp-memnet](../mcp-memnet/SKILL.md) | MCP tools, transport, session lifecycle |
| [memnet-format](../memnet-format/SKILL.md) | Shared dialect wire shapes |
| [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md) | SysML design memory (single-agent; pair when SysML + Multitask) |
