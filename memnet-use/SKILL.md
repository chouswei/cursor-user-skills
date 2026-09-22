---
name: memnet-use
description: >-
  OPS-ONLY MemNet tip/engine plumbing. Do NOT use as SysMLEdge product face or
  SysML day-1 query path. Product face is sysmledge
  (rev_status/ask/gql/pin_map/propose).
metadata:
  pattern: pipeline
---
# OPS-ONLY - not SysMLEdge product teach

Soft-pass kill: teaching tip MemNet MCP as the SysML query face.
Product / Cursor day-1: **sysmledge-workflow** and **sysmledge-host-model-at-rev**.
Callable face: product `sysmledge` / `user-sysmledge`. tip != face.

(Original tip/engine content below for operators only.)

---
# How to use MemNet

**Using** MemNet -- not building the engine. Doctrine: MemNet `docs/SHAPE.md`, `docs/grammar/gql-wire-profile.md`, `docs/LLM-GUIDE.md`, `docs/ROADMAP.md`. Open one specialist; do not paste those files here.

**Package and PyPI 0.19.5** (honesty `c` on 0.19 -- not a usage-method `b`; Hatch; tag `v0.19.5`; extras 0.10-0.19 unchanged). **Install:** `pip install memnet-llm` or `pip install memnet-llm==0.19.5`. **1.0** unclaimed. No 0.20. Chat is never SSOT. Novel-writer is out of scope. Open one specialist; this hub does not steal specialist triggers.

User-pack store: Cursor **`memnet-pi`** HTTP `http://10.0.0.10:18766/mcp` bridging TCP serve `:18765`. InvenTree MCP is not MemNet. `serve_status` `"host":"127.0.0.1"` `"port":18765` is that serve process loopback, not the Windows workstation.

Engine session TTL is **1..1440 minutes** (`@ERR: bad_ttl`); a longer TTL is rejected. `session_save` does **not** extend it. Dated `session_save` snapshots are the only durable path. A catalog id recorded in a file goes stale roughly daily.

## Goldfish loop

1. **Open** -- `session_open` with a SCHEMA map (`map_file` / `map_lines`) covering every kind you will mutate. Schema is fixed at open. Missing map -> `no_map`. Missing kind -> `unknown_tag`. Campaign catalogs MUST admit at least `CLM`, `SYM`, `USR`, `TSK`. Bundled maps: MemNet checkout `parts/common/memnet/memnet/examples/schema.*.example.txt` (this pack does not vendor them).
2. **Transport** -- Cursor user-pack goldfish is `memnet-pi` streamable HTTP `http://10.0.0.10:18766/mcp` bridged to TCP `:18765`. In-process MCP is leftover for a non-shared single-agent loop only; MUST NOT teach in-process as the default when Multitask/Task/shared session applies (User Rules forbid in-process then). Multitask / Task workers: load [memnet-multitask](../memnet-multitask/SKILL.md) (wave, end turn, checkpoint, repeat). Task `model`: User Rules async (asynchronous) checkpoint pipeline. If the shared serve is down: files only; plain Markdown.
3. **Cue** -- `kind` plus labels+properties / keyword. Campaign pin: `kind=TSK` and locator `goal=<cue>`. If ego unknown: `find` then `pin_map` from that pattern. Prefer one live `TSK_*`. leftover `anchor=` is leftover. Empty cue = session outline (0.11). `pin_map` without `kind=` on a rich catalog can CueConflict with large `|Q|` (118 observed); that is not a campaign hit.
4. **`pin_map`** -- one session per generate; complete Shape of **this** cue. Drop the prior map next turn. Shaped emit MUST NOT show `hid` / `_memnet_hid` / `elementId` / nickname `id` (cue-by-nickname lookup still OK). Do not put momentum / coverage / lambda / m on `pin_map`. Audit: MemNet `docs/operations/honesty-c-wire-audit.md`.
5. **Act** from that Shape plus the current request. Narrow-Read files at `SYM.line` / `SYM.path`.
6. **Sparse Commit** -- MCP/CLI **`mutate`**. leftover `add`/`update` / `id:'NEW'` are leftover-named.
7. **Persist** -- after any `mutate` that created persistent CLM / USR / SYM / TSK facts, `session_save` to a new dated file (not a campaign warm file). Live cabinet is optional extra, not a substitute.
8. **Settle** finished `TSK_*` (`status=settled`; `recycle=delete_on_settle` when done).

On `session_not_found`: see **Campaign session** below. MUST NOT adopt the richest foreign catalog.

## Campaign session

A **campaign** is one git repo's live `TSK_model_*` graph.

- Each git repo / MemNet campaign (`TSK_model_*`) MUST have its own session id.
- Every `pin_map` / `find` / `mutate` / `ingest` MUST pass `session=` (or `MEMNET_SESSION` set for THAT campaign). MUST NOT rely on serve process-current. `session_list` / `session_current` envelopes MAY still show another campaign.
- MUST `session_open` or `session_load` for this campaign before the first pin. MUST NOT reuse another campaign's id from `session_list[0]` or `session_current`.
- Empty warm / `session_not_found`: `session_list`, then `find(kind=TSK, locators=["goal=<this TSK_model_*>"], session=<id>)` on live ids. Adopt only a session that already holds this campaign cue (if several of this cue, the richer of those). If none, `session_open` for this repo only.
- CueConflict or a neighbourhood whose package qname is not this campaign is a **session-mismatch**: stop and retarget; MUST NOT mutate.
- Parent and workers share one session id for the campaign; workers `pin_map` first WITH that id.

## Specialists (open on need)

| Need | Skill |
|------|--------|
| MCP tools, ingest, `snap_model`, export | [mcp-memnet](../mcp-memnet/SKILL.md) |
| STM harness / debug / W vs S | [memnet-stm-harness](../memnet-stm-harness/SKILL.md) |
| Analytical-mechanics framing (any domain) | [analytical-mechanics-propose](../analytical-mechanics-propose/SKILL.md) |
| GQL / shaped `pin_map` | [memnet-format](../memnet-format/SKILL.md) |
| Multitask / shared session | [memnet-multitask](../memnet-multitask/SKILL.md) |
| Code `MOD`/`SYM` | [memnet-codebase-snap](../memnet-codebase-snap/SKILL.md) |
| Nested sessions / look loop | [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md) |
| Plan in session (draft / update / repolish) | [memnet-planner](../memnet-planner/SKILL.md) |
| SysML relatives + nest cuts | pack `sysml-*` plus MemNet `docs/application-notes/system/llm-sysml-v2-modeling.md` |
| Build the MemNet engine | **not this pack** -- MemNet checkout `.cursor/skills/memnet-reference/` |

## MUST NOT

- Dump S or a fat `.sysml` into chat.
- Stack N nested `pin_map`s in one generate -- re-anchor with MCP `session=` / locator `session=`.
- Treat chat as ids / paths / mission state.
- `rag_query` / ANN of the session.
- Claim **1.0**.
- Teach `hid` / `_memnet_hid` / `elementId` / nickname `id` on shaped `pin_map` emit.
- Load an in-repo `memnet-reference` copy unless **building** MemNet in that checkout.
- Auto-adopt a session solely because it is the only `goal=<cue>` hit, `session_list[0]`, or `session_current`.
- Rely on serve process-current instead of passing `session=` for this campaign.
- Mutate after a foreign-package CueConflict (session-mismatch).
- Read CueConflict from `pin_map` without `kind=` as a campaign hit.
- Read `serve_status` host `127.0.0.1` as the Windows workstation.
- Prune housekeep "orphans" in a mutate-maintained campaign catalog -- they are legitimately unreachable from the cue; pruning deletes the mission record.
