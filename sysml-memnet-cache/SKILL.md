---
name: sysml-memnet-cache
description: >-
  OPS-ONLY MemNet tip/engine plumbing. Do NOT use as SysMLEdge product face or
  SysML day-1 query path. Product face is sysmledge
  (rev_status/ask/gql/pin_map/propose).
metadata:
  pattern: tool-wrapper
---
# OPS-ONLY - not SysMLEdge product teach

Soft-pass kill: teaching tip MemNet MCP as the SysML query face.
Product / Cursor day-1: **sysmledge-workflow** and **sysmledge-host-model-at-rev**.
Callable face: product `sysmledge` / `user-sysmledge`. tip != face.

(Original tip/engine content below for operators only.)

---
# SysML MemNet cache (modeling relatives)

**Role:** Tip MemNet is **not** a model SSOT. It caches relatives that are not already in the working model SSOT (SysMLEdge bound desk, or repo `models/*.sysml` when unbound/repo-based).

Specialist **`sysml-*`** skills (generators, reviewers, refactorers) **do not** keep their own parallel memory. They **read** from and **write** to this cache via **`mcp-memnet`** tools.

## Model root layouts

New house default is `sysml-models/` (legacy opt-in: `sysml-v2-models/projects/<slug>/`).

| Layout | Model root | Typical snap dir | Example anchor |
|--------|------------|------------------|----------------|
| House / system repo (`modelbasedPrj-*`) | `sysml-models/` (+ optional `parts/*/model/`) | `sysml-models/.memnet/` | e.g. NCU-LEO: `TSK_model_leo_cubesat` |
| Multi-project pack (legacy) | `sysml-v2-models/projects/<slug>/` | `.../projects/<slug>/.memnet/` | `TSK_model_<short>` |

**MUST** copy the live repo root from `AGENTS.md` / `AGENT-CONTEXT.md`. **MUST NOT** invent `sysml-v2-models/...` paths when the workspace only has `sysml-models/`. Stale `path=` fields in an old `.memnet` wire/snap are not SSOT -- re-snap or fix locators before trusting them.

## Three stores

| Store | Holds | Agent rule |
|-------|-------|------------|
| Project `models/*.sysml` | Repo SysML (author when unbound/repo-based; backup after Save when SysMLEdge-based) | Edit only when that kind is working SSOT; validate |
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
| Cue campaign `:TSK` with `kind=TSK`, `goal=TSK_model_<short>` from repo `AGENTS.md`, and `session=` for this campaign | Treat that house id as a competing session-id scheme; omit `session=` / use process-current / `session_list[0]` / `session_current`; treat CueConflict from `pin_map` without `kind=` (large `|Q|`, 118 observed) as a campaign hit; mutate after a foreign-package CueConflict (session-mismatch -- stop and retarget) |
| Catalog Snap = `snap_model`. Path-B = `ingest_sysml` into **this** `session` (1->1) | Smash ingest, Snap, and docs into one undifferentiated session when a nest applies |
| One `pin_map` this generate; MCP `session=` for **this** cut | Stack N nested maps in one prompt |
| Join with `import_slice` of a neighbourhood | Absorb a whole interior / paste the nested tree |
| `snap_model` cap -> `housekeep_stats`, settle stale `TSK_*`, cut further interiors | Silent ignore; clip `max_rows` and call it Shape; flatten leftovers into the current session; prune housekeep "orphans" in a mutate-maintained campaign catalog (they are unreachable from the cue; pruning deletes the mission record) |

**Transport:** key **`memnet`** / namespace **`user-memnet`** (`mcp.json` owns URL) -- [mcp-memnet](../mcp-memnet/SKILL.md). Tip MemNet = agent working memory, not the SysML graph. Multitask / Task workers: [memnet-multitask](../memnet-multitask/SKILL.md) -- **MUST NOT** in-process MCP. MUST NOT cite `:18766` / `:18765` / `10.0.0.10` or a SKILL.md URL as the live tip. MUST NOT treat old `memnet-pi` / `user-memnet-pi` as live. Single-agent in-process: skip `serve_status`; otherwise probe when unsure.

**MCP wire:** EDG `rel` names are **session-registered strings**. SysML closed list: [sysml-memnet-patterns.md](../sysml-memnet-documentation/references/sysml-memnet-patterns.md) (`declaredIn`, `hasPort`, `typedBy`, `inFile`, `satisfies`, `allocates`, ...). **Copy exact spellings from the live pin map**; seed unknowns with `allow_new_relation=true`. Engine-generic new edges prefer English verb / snake tokens (MemNet `docs/grammar/`); do not invent a second spelling for an existing link.

## Specialist defer rule

Any **`sysml-*`** skill that changes `.sysml` **MUST**:

1. **Before:** `pin_map` on the campaign cue (`kind=TSK`, `locators=["goal=TSK_model_<short>"]`, `session=<this campaign>`), then interior `session=` if the catalog pin carries one (or accept warm_miss -> initial snap). If MemNet MCP is missing: edit `.sysml` without cache.
2. **After validate:** emit MemNet delta per [relatives-cache-map.md](../sysml-memnet-documentation/references/relatives-cache-map.md) -- do **not** paste topology into chat.

Hub skills own the sequence: [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) step 6.

## Serve down / MCP missing

When MemNet MCP tools are absent from the session catalog, or `serve_status` is false:

- Edit `.sysml` only; note stale/absent graph in one line.
- Ephemeral handoff: plain Markdown tables or short prose (not TOON/TRON).
- **MUST NOT** call `pin_map` / `mutate` when tools are unavailable. leftover `add`/`update` named leftover.
- On return: run initial snap or catch-up delta before next substantive edit.

## Session persistence

| Action | When |
|--------|------|
| `session_open` + map; seed campaign `TSK` on the **catalog** | sysml-new-project / warm miss (see snap.md). Map MUST admit `CLM`, `SYM`, `USR`, `TSK` -- schema is fixed at open; a catalog that rejects CLM (`unknown_tag`) is unfit |
| `snap_model` / `ingest_sysml` | Catalog vs Path-B -- not both into one flat session when nested. `ingest_sysml` enforces per-call `ingest_budget`; raise or chunk large files -- a client timeout can still leave server-committed nodes |
| `session_save` -> `<model-root>/.memnet/<short>-<catalogId>-<YYYYMMDD>.snap` | After persistent CLM / USR / SYM / TSK mutate, or end of substantive turn (catalog id). MUST NOT overwrite `*warm*`. Does **not** extend TTL (engine 1..1440m) |
| `session_load` | Resume this campaign's id from `AGENT-CONTEXT.md` (or `MEMNET_SESSION` set for THAT campaign). MUST NOT `session_current` / `session_list[0]` |

Store **catalog** session id + campaign cue in `AGENT-CONTEXT.md`. Interior `session=` locators live on catalog pins.

On `session_not_found`: `session_list`, then `find(kind=TSK, locators=["goal=TSK_model_<short>"], session=<id>)` per live id. Adopt only a session that already holds this campaign cue (if several of this cue, richer of those). MUST NOT adopt a foreign catalog. If none, `session_open` for this repo only. Catalog recovery: re-ingest the live `.sysml` tree into **this** session; success = locator coverage (`qname` / `path`), not row count. MUST NOT import unlocatable rows as the recovery.

## NCU-LEO note (system repo)

Anchor `TSK_model_leo_cubesat`; model root `sysml-models/`. August hybrid ground-test scene lives in the model plus `docs/august-2026-prep-brief.md` -- do not treat that brief as MemNet topology.

## References

- [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md)
- [sysml-memnet-read-policy.md](../sysml-memnet-documentation/references/sysml-memnet-read-policy.md)
- [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md)
- [memnet-goldfish-loop.mdc](../rules/memnet-goldfish-loop.mdc)
