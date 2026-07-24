---
name: sysml-memnet-cache
description: >-
  MemNet MCP is the single cache for SysML modeling relatives — topology, locators, requirements,
  traceability, decisions, audit findings, diagram scope, report atoms. Specialist sysml-* skills
  read via pin_map and write deltas here; never duplicate in chat or AGENT-CONTEXT. Triggers:
  sysml cache, memnet cache, modeling relatives, warm read sysml, cache topology, defer memnet,
  specialist post-edit, avoid re-read deploy.
metadata:
  pattern: tool-wrapper
  domain: sysml-v2,memnet
  version: "1.0"
  pairs_with: [sysml-memnet-documentation, mcp-memnet, sysml-modeling-workflow, sysml-modeling-session-checklist, memnet-format]
token_guardrails: |
  - MemNet is the cache; .sysml is source of truth for structure; AGENT-CONTEXT is session+anchor only.
  - pin_map(TSK_model_<short>) before substantive edit; add/update delta after mcp-sysml-v2 validate.
  - Atomise only — one fact per @TAG row; never store full .sysml or paragraph prose.
  - Skip cache write: comment-only edit, serve down, question-only turn (see sysml-memnet-snap.md).
---

# SysML MemNet cache (modeling relatives)

**Role:** **`memnet serve`** is the **cache** for everything SysML modeling needs between turns that is **not** already authoritative in `models/*.sysml`.

Specialist **`sysml-*`** skills (generators, reviewers, refactorers) **do not** keep their own parallel memory. They **read** from and **write** to this cache via **`mcp-memnet`** tools.

## Three stores

| Store | Holds | Agent rule |
|-------|-------|------------|
| `models/*.sysml` | Structure, syntax, satisfy | Edit first; validate |
| **MemNet** | Relatives (below) | `query_warm` → act → delta |
| `AGENT-CONTEXT.md` | Session id + anchor + short summary | Never topology/backlog |

## What counts as a “relative”

Atomised rows the warm graph must carry so the next turn avoids re-reading deploy:

| Tag | Relative kind | Typical source skill |
|-----|---------------|---------------------|
| `@PRT` / `@POR` | Parts, ports | hardware/software part generators, nested-structure |
| `@CON` | Connection defs/usages | sysml-connections |
| `@BEH` | States, events | sysml-behaviour-generator |
| `@REQ` | Requirement defs | sysml-requirements-generator |
| `@ITM` | Flow items | sysml-item-generator |
| `@SYM` | File + line locators | **every** substantive edit |
| `@MOD` | Model file registry | sysml-new-project, root-config |
| `@EDG` | satisfies, allocates, hasPort, declaredIn | traceability, refactorer |
| `@DEC` / `@ISSUE` | Open choices, backlog | part-reviewer, requirements-audit |
| `@CONV` | Site conventions | common-lib-contribution |
| `@ART` / `@SEC` / `@CLM` | Report atoms | view-doc-sync, system-design-report |
| `@TSK` | Campaign + pipe steps | modeling-workflow |
| `@USR` | User constraints that must persist | any turn |

Full tag map: [sysml-memnet-patterns.md](../sysml-memnet-documentation/references/sysml-memnet-patterns.md).  
Per-skill write map: [relatives-cache-map.md](../sysml-memnet-documentation/references/relatives-cache-map.md).

## MCP tool loop (every modeling turn)

```text
1. serve_status
2. pin_map(anchor=TSK_model_<short>, depth=2, max_rows=50)   # READ cache
3. … specialist skill edits models/*.sysml …
4. mcp-sysml-v2 validate
5. sysml-view-doc-sync (iff outputs + structure changed)
6. add/update wire rows + refresh @SYM.line + pipe @CLM settle   # WRITE cache
7. session_save → projects/<slug>/.memnet/<short>.snap (multi-session projects)
```

Mechanics: [mcp-memnet](../mcp-memnet/SKILL.md). Procedure: [sysml-memnet-snap.md](../sysml-memnet-documentation/references/sysml-memnet-snap.md).

**MCP wire:** `@EDG` relation names are **`snake_case`** (`declared_in`, `in_file`, `has_port`, `typed_by`, `satisfies`) — the MemNet MCP rejects camelCase (`declaredIn`).

## Specialist defer rule

Any **`sysml-*`** skill that changes `.sysml` **MUST**:

1. **Before:** `query_warm` on project anchor (or accept warm_miss → initial snap).
2. **After validate:** emit MemNet delta per [relatives-cache-map.md](../sysml-memnet-documentation/references/relatives-cache-map.md) — do **not** paste topology into chat.

Hub skills own the sequence: [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) step 6.

## Serve down

When `serve_status` is false:

- Edit `.sysml` only; note stale graph in one line.
- Ephemeral handoff: plain Markdown tables or short prose (not TOON/TRON).
- On serve return: run initial snap or catch-up delta before next substantive edit.

## Session persistence

| Action | When |
|--------|------|
| `session_open` + seed `@TSK`/`@MOD` | sysml-new-project scaffold |
| `session_save` → `.memnet/<short>.snap` | End of substantive turn or session handoff |
| `session_load` | Resume when `MEMNET_SESSION` unset |

Store snap path in `AGENT-CONTEXT.md` header when used.

## References

- [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md)
- [sysml-memnet-read-policy.md](../sysml-memnet-documentation/references/sysml-memnet-read-policy.md)
- [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc)
