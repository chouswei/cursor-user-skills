---
name: sysml-memnet-documentation
description: >-
  MemNet MCP for SysML v2 design memory and model snap: atomised graph (parts, ports, connections, behaviour,
  locators, rationale), mandatory pin_map before edit, delta write after validate. Also outputs/*.md and
  system design reports. Triggers: memnet sysml, sysml memnet, model snap, goldfish sysml, memnet outputs,
  design memory sysml, TSK_model, AGENT-CONTEXT memnet, sysml knowledge graph, read sysml, memnet vs sysml, avoid re-read deploy.
metadata:
  pattern: pipeline
  secondary: tool-wrapper
  domain: sysml,memnet
  version: "1.6"
  pairs_with: [sysml-memnet-cache, sysml-modeling-workflow, mcp-memnet, memnet-codebase-snap, sysml-view-doc-sync, mcp-sysml-v2, mcp-sysmledgraph, memnet-format]
token_guardrails: |
  - Follow the 6-step turn sequence in references/sysml-memnet-snap.md; pin_map before substantive edits.
  - MUST follow references/sysml-memnet-read-policy.md: topology from warm; ≤2 narrow Read windows per turn; no full deploy re-read.
  - MUST follow references/sysml-memnet-pipeline.md: pipeline step atoms via shared dialect mutate when MemNet is up; plain Markdown when down (not TOON/TRON).
  - Use unified tags @PRT/@POR/@BEH with kind field; MUST NOT write @PARTD/@PORTD/@BEHD/@TASK.
  - Atomise first: one fact per row; short pipe fields; never store full .sysml or paragraph prose.
  - Copy stable ids from warm output; refresh @SYM.line after every validated edit.
  - satisfy/allocate → @EDG only (satisfies, allocates); @SYM only for line locators.
  - AGENT-CONTEXT.md: agents read session+anchor only; topology/backlog live in MemNet.
  - Confirm serve_status before session work. Skip MemNet write only per snap reference (comment-only, serve down).
---

# SysML MemNet (design memory + model snap)

**Layout:** `SKILL.md` + references (load order below).

**Entry point for “use MemNet as cache”:** [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) — specialist `sysml-*` skills defer read/write there.

**Durable graph memory** for SysML v2 projects: symbol index with file/line locators, ports, connections, behaviour, design rationale, and documentation atoms. Complements `mcp-sysmledgraph` (structural impact) and `mcp-sysml-v2` (validate/parse).

MemNet stores **structure + atomic facts** (not full prose). **Do not re-read `deploy-*.sysml` for topology** when warm has `@PRT`/`@CON` — see [sysml-memnet-read-policy.md](references/sysml-memnet-read-policy.md). See [mcp-memnet](mcp-memnet/SKILL.md) for wire format and tools.

## Read policy (mandatory)

**Discovery:** `pin_map` → `@PRT` / `@CON` / `@SYM` / `@REQ`. (`query_warm` is legacy alias.)  
**Edit:** `Read(path, offset=line-12, limit=35)` at `@SYM.line` only.  
**Forbidden per turn:** full deploy read; re-grep names already in warm; multi-file read without warm miss.

Full rules: [sysml-memnet-read-policy.md](references/sysml-memnet-read-policy.md).

## Reference load order

1. [references/sysml-memnet-snap.md](references/sysml-memnet-snap.md) — **mandatory** 6-step sequence, grep, delta, `.snap`
2. [references/sysml-memnet-read-policy.md](references/sysml-memnet-read-policy.md) — **when to read `.sysml`** vs warm (anti-patterns, read budget)
3. [references/sysml-memnet-pipeline.md](references/sysml-memnet-pipeline.md) -- **pipeline handoffs** (shared dialect step atoms)
4. [references/sysml-memnet-patterns.md](references/sysml-memnet-patterns.md) — canonical 19-tag map, construct table, EDG list
5. [references/relatives-cache-map.md](references/relatives-cache-map.md) — **which specialist skill writes which tags**
6. [references/sysml-memnet-cookbook-bridge.md](references/sysml-memnet-cookbook-bridge.md) — upstream cookbook pointer, unified-tag policy
7. Upstream cookbook — `C:/Projects/MemNet/application-notes/llm-sysml-v2-modeling.md` (worked turns)

Pair with [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) and [memnet-codebase-snap](../memnet-codebase-snap/SKILL.md).

## Prerequisites

1. `pip install memnet-llm[mcp]`
2. `memnet` entry in `~/.cursor/mcp.json`. Set `MEMNET_SERVE_HOST`, `MEMNET_SERVE_PORT`, optional `MEMNET_SESSION`.
3. `memnet serve` running — confirm with `serve_status`.

## When to use

- Opening or resuming work on `sysml-v2-models/projects/<slug>/`
- Recording design decisions, assumptions, backlog not fully expressed in `.sysml`
- Maintaining `outputs/*.md` / system-design-report atoms (`@ART`/`@SEC`/`@CLM`)
- Multi-turn refactors, requirement audits, report updates

**Skip MemNet** only when: one-shot question with no edit; comment-only `.sysml` change; or `serve_status` false.

## Atomisation (docs + model)

Model elements: `@PRT`/`@POR`/`@CON`/`@BEH`/`@ITM`/`@REQ` + `@SYM` (path, line) + `@MOD` per file. Conventions: `@CONV`. Open forks: `@DEC`. Backlog: `@ISSUE`. Docs: `@ART`/`@SEC`/`@CLM`. Campaign: `@TSK_model_<short>`.

## Pairing

- **sysml-modeling-workflow** — encodes the 6-step sequence
- **system-design-report-generator** — full pack generate/maintain: warm before prose, `@ART`/`@SEC`/`@CLM` after sync ([memnet-report-pipeline.md](../system-design-report-generator/references/memnet-report-pipeline.md))
- **sysml-view-doc-sync** — sync outputs, then atomise key claims as `@CLM`
- **sysml-refactorer**, **sysml-traceability**, **sysml-requirements-audit** — persist findings after work
- **memnet-format** — engine shared dialect; thin SysML x MemNet kind/id pointer only
- **mcp-sysmledgraph** — impact/rename; record intent in MemNet
- **mcp-memnet** — base MCP mechanics

## Quick anchors

| Anchor | Use when |
|--------|----------|
| `TSK_model_<short>` | Start/resume project session |
| `TSK_diagram_<figureId>` | Mermaid placement graph ([mermaid-placement-by-degree.md](../mermaid/references/mermaid-placement-by-degree.md)) |
| `SYM_<name>` | Jump to edit location (path + line) |
| `PRT_<name>` / `POR_<name>` | Part or port + linked claims/reqs |
| `BEH_<name>` | Behaviour under edit |
| `REQ_<requirementId>` | Requirement audit / satisfy |
| `DEC_<nn>` | Pending design choice |
| `CONV_<topic>` | Site convention |
| `ART_<project>-design` | Outputs / report pack |

## References

- [sysml-memnet-snap.md](references/sysml-memnet-snap.md)
- [sysml-memnet-read-policy.md](references/sysml-memnet-read-policy.md)
- [sysml-memnet-pipeline.md](references/sysml-memnet-pipeline.md)
- [sysml-memnet-patterns.md](references/sysml-memnet-patterns.md)
- [sysml-memnet-cookbook-bridge.md](references/sysml-memnet-cookbook-bridge.md)
- [mcp-memnet](mcp-memnet/SKILL.md), [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc)
- [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md)
