---
name: sysml-memnet-cache
description: >-
  MemNet MCP is the single cache for SysML modeling relatives -- topology, locators, requirements,
  traceability, decisions, audit findings, diagram scope, report atoms. Specialist sysml-* skills
  read via pin_map and write deltas here; never duplicate in chat or AGENT-CONTEXT. Triggers:
  sysml cache, memnet cache, modeling relatives, warm read sysml, cache topology, defer memnet,
  specialist post-edit, avoid re-read deploy.
metadata:
  pattern: tool-wrapper
  domain: sysml-v2,memnet
  version: "2.1"
  product: "memnet-llm==0.19.3"
  pairs_with: [sysml-memnet-documentation, mcp-memnet, sysml-modeling-workflow, sysml-modeling-session-checklist, memnet-format, sysml-gql, memnet-nested-sessions, memnet-multitask]
token_guardrails: |
  - MemNet is the cache; .sysml is source of truth for structure; AGENT-CONTEXT is catalog session + campaign cue only.
  - Nested organisation SSOT: memnet-nested-sessions. Campaign cue TSK_model_<short> is not a second session-id scheme.
  - pin_map this cut (session=) before edit; mutate delta after mcp-sysml-v2 validate. leftover add/update named leftover.
  - Atomise only -- one fact per GQL/shaped graph row; never store full .sysml or paragraph prose.
  - Skip cache write: comment-only edit, serve down / MCP missing, question-only turn (see sysml-memnet-snap.md).
  - Multitask: memnet-multitask + memnet-pi TCP/HTTP. MUST NOT in-process MCP.
---

# SysML MemNet cache (modeling relatives)

**Role:** MemNet is the **cache** for everything SysML modeling needs between turns that is **not** already authoritative in project `models/*.sysml`.

Specialist **`sysml-*`** skills (generators, reviewers, refactorers) **do not** keep their own parallel memory. They **read** from and **write** to this cache via **`mcp-memnet`** tools.

## Model root layouts

| Layout | Model root | Typical snap dir | Example anchor |
|--------|------------|------------------|----------------|
| Multi-project pack | `sysml-v2-models/projects/<slug>/` | `.../projects/<slug>/.memnet/` | `TSK_model_<short>` |
| System repo (`modelbasedPrj-*`) | `sysml-models/` (+ optional `parts/*/model/`) | `sysml-models/.memnet/` | e.g. NCU-LEO: `TSK_model_leo_cubesat` |

**MUST** copy the live repo root from `AGENTS.md` / `AGENT-CONTEXT.md`. **MUST NOT** invent `sysml-v2-models/...` paths when the workspace only has `sysml-models/`. Stale `path=` fields in an old `.memnet` wire/snap are not SSOT -- re-snap or fix locators before trusting them.

## Three stores

| Store | Holds | Agent rule |
|-------|-------|------------|
| Project `models/*.sysml` | Structure, syntax, satisfy | Edit first; validate |
| **MemNet** | Relatives (below) | cue `pin_map` then **`mutate`** |
| `AGENT-CONTEXT.md` | Catalog session id + campaign cue + short summary | Never topology/backlog |

## What counts as a "relative"

Atomised rows the warm graph must carry so the next turn avoids re-reading deploy:

| Kind | Relative kind | Typical source skill |
|-----|---------------|---------------------|
| `PRT` / `POR` | Parts, ports | hardware/software part generators, nested-structure |
| `CON` | Connection defs/usages | sysml-connections |
| `BEH` | States, events | sysml-behaviour-generator |
| `REQ` | Requirement defs | sysml-requirements-generator |
| `ITM` | Flow items | sysml-item-generator |
| `SYM` | File + line locators | **every** substantive edit |
| `MOD` | Model file registry | sysml-new-project, root-config |
| Typed rels | satisfies, allocates, hasPort, declaredIn | traceability, refactorer |
| `DEC` / `ISSUE` | Open choices, backlog | part-reviewer, requirements-audit |
| `CONV` | Site conventions | common-lib-contribution |
| `ART` / `SEC` / `CLM` | Report atoms | view-doc-sync, system-design-report |
| `TSK` | Campaign + pipe steps | modeling-workflow |
| `USR` | User constraints that must persist | any turn |

Full kind map: [sysml-memnet-patterns.md](../sysml-memnet-documentation/references/sysml-memnet-patterns.md).
Per-skill write map: [relatives-cache-map.md](../sysml-memnet-documentation/references/relatives-cache-map.md).
Thin bridge: [sysml-gql](../sysml-gql/SKILL.md).

## MCP loop (every modeling turn)

Six-step sequence SSOT: [sysml-memnet-snap.md](../sysml-memnet-documentation/references/sysml-memnet-snap.md). Tools: [mcp-memnet](../mcp-memnet/SKILL.md). Wire: [memnet-format](../memnet-format/SKILL.md).

**SysML nested delta** (procedure SSOT: [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md)):

| MUST | MUST NOT |
|------|----------|
| Cue campaign `:TSK` `goal=TSK_model_<short>` from repo `AGENTS.md` | Treat that house id as a competing session-id scheme |
| Catalog Snap = `snap_model`. Path-B = `ingest_sysml` into **this** `session` (1->1) | Smash ingest, Snap, and docs into one undifferentiated session when a nest applies |
| One `pin_map` this generate; MCP `session=` for **this** cut | Stack N nested maps in one prompt |
| Join with `import_slice` of a neighbourhood | Absorb a whole interior / paste the nested tree |
| `snap_model` cap -> `housekeep_stats`, settle stale `TSK_*`, cut further interiors | Silent ignore; clip `max_rows` and call it Shape; flatten leftovers into the current session |

**Transport:** Cursor **`memnet-pi`** HTTP `:18766` bridging TCP `:18765` ([mcp-memnet](../mcp-memnet/SKILL.md)). Multitask / Task workers: [memnet-multitask](../memnet-multitask/SKILL.md) -- **MUST NOT** in-process MCP. Single-agent in-process: skip `serve_status`; otherwise probe TCP when unsure.

**MCP wire:** EDG `rel` names are **session-registered strings**. SysML closed list: [sysml-memnet-patterns.md](../sysml-memnet-documentation/references/sysml-memnet-patterns.md) (`declaredIn`, `hasPort`, `typedBy`, `inFile`, `satisfies`, `allocates`, ...). **Copy exact spellings from the live pin map**; seed unknowns with `allow_new_relation=true`. Engine-generic new edges prefer English verb / snake tokens (MemNet `docs/grammar/`); do not invent a second spelling for an existing link.

## Specialist defer rule

Any **`sysml-*`** skill that changes `.sysml` **MUST**:

1. **Before:** `pin_map` on the campaign cue, then `session=` for the interior under edit if the catalog pin carries one (or accept warm_miss -> initial snap). If MemNet MCP is missing: edit `.sysml` without cache.
2. **After validate:** emit MemNet delta per [relatives-cache-map.md](../sysml-memnet-documentation/references/relatives-cache-map.md) -- do **not** paste topology into chat.

Hub skills own the sequence: [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) step 6.

## Serve down / MCP missing

When MemNet MCP tools are absent from the session catalog, or `serve_status` is false (TCP mode):

- Edit `.sysml` only; note stale/absent graph in one line.
- Ephemeral handoff: plain Markdown tables or short prose (not TOON/TRON).
- **MUST NOT** call `pin_map` / `mutate` when tools are unavailable. leftover `add`/`update` named leftover.
- On return: run initial snap or catch-up delta before next substantive edit.

## Session persistence

| Action | When |
|--------|------|
| `session_open` + map; seed campaign `TSK` on the **catalog** | sysml-new-project / warm miss (see snap.md) |
| `snap_model` / `ingest_sysml` | Catalog vs Path-B -- not both into one flat session when nested |
| `session_save` -> `<model-root>/.memnet/<short>.snap` | End of substantive turn or handoff (catalog id) |
| `session_load` | Resume when `MEMNET_SESSION` unset |

Store **catalog** session id + campaign cue in `AGENT-CONTEXT.md`. Interior `session=` locators live on catalog pins.

## NCU-LEO note (system repo)

Anchor `TSK_model_leo_cubesat`; model root `sysml-models/`. August hybrid ground-test scene lives in the model plus `docs/august-2026-prep-brief.md` -- do not treat that brief as MemNet topology.

## References

- [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md)
- [sysml-memnet-read-policy.md](../sysml-memnet-documentation/references/sysml-memnet-read-policy.md)
- [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md)
- [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc)
