---
name: sysml-memnet-documentation
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
# SysML MemNet (design memory + model snap)

**Layout:** `SKILL.md` + references (load order below).

**Entry point for "use MemNet as cache":** [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) -- specialist `sysml-*` skills defer read/write there.

**Durable graph memory** for SysML v2 projects: symbol index with file/line locators, ports, connections, behaviour, design rationale, and documentation atoms. Complements `mcp-sysml-v2` (loaded-file validation, parsing, and symbol navigation).

Tip MemNet is not a model SSOT. Two model SSOTs: repo SysML vs SysMLEdge bound desk (README states which). MemNet stores **structure + atomic facts** (not full prose). **Do not re-read `deploy*.sysml` for topology** when pin_map has PRT/CON -- see [sysml-memnet-read-policy.md](references/sysml-memnet-read-policy.md). Tools: [mcp-memnet](../mcp-memnet/SKILL.md); GQL wire: [memnet-format](../memnet-format/SKILL.md). Thin SysML bridge: [sysml-gql](../sysml-gql/SKILL.md). Nest cuts: [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md).

## Read policy (mandatory)

**Discovery:** `pin_map` from a cue -> PRT / CON / SYM / REQ. leftover `query_warm` / `anchor=` named leftover.  
**Edit:** `Read(path, offset=line-12, limit=35)` at SYM.line only.  
**Forbidden per turn:** full deploy read; re-grep names already in warm; multi-file read without warm miss.

Full rules: [sysml-memnet-read-policy.md](references/sysml-memnet-read-policy.md).

## Reference load order

1. [references/sysml-memnet-snap.md](references/sysml-memnet-snap.md) -- **mandatory** 6-step sequence, grep, delta, `.snap`
2. [references/sysml-memnet-read-policy.md](references/sysml-memnet-read-policy.md) -- **when to read `.sysml`** vs warm (anti-patterns, read budget)
3. [references/sysml-memnet-pipeline.md](references/sysml-memnet-pipeline.md) -- **pipeline handoffs** (GQL/shaped step atoms)
4. [references/sysml-memnet-patterns.md](references/sysml-memnet-patterns.md) -- canonical 19-kind map, construct table, closed rel list
5. [references/relatives-cache-map.md](references/relatives-cache-map.md) -- **which specialist skill writes which kinds**
6. [references/sysml-memnet-cookbook-bridge.md](references/sysml-memnet-cookbook-bridge.md) -- upstream cookbook pointer, unified-kind policy
7. [sysml-gql](../sysml-gql/SKILL.md) -- thin turn loop + construct abbrev
8. Upstream cookbook -- MemNet `docs/application-notes/system/llm-sysml-v2-modeling.md` (worked turns)

Pair with [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) and [memnet-codebase-snap](../memnet-codebase-snap/SKILL.md).

## Prerequisites

1. **Package and PyPI 0.19.5** (honesty `c` on 0.19 -- not a usage-method `b`; tag `v0.19.5`; extras 0.10-0.19 unchanged). **Install:** `pip install 'memnet-llm[mcp]'` or `pip install 'memnet-llm[mcp]==0.19.5'`. Optional `[neo4j]` (live claimed 0.14; drivers only). **1.0** unclaimed.
2. Cursor MCP key **`memnet`** / namespace **`user-memnet`** (`mcp.json` owns URL) -- [mcp-memnet](../mcp-memnet/SKILL.md). Tip MemNet = agent working memory, not the SysML graph. Multitask **MUST NOT** in-process ([memnet-multitask](../memnet-multitask/SKILL.md)). MUST NOT cite `:18766` / `:18765` / `10.0.0.10` or a SKILL.md URL as the live tip. MUST NOT treat old `memnet-pi` / `user-memnet-pi` as live.
3. MemNet MCP tools visible in the session catalog. If absent: treat as serve down -- no `pin_map` / mutate.
4. `serve_status` when unsure. Skip that probe only under single-agent in-process.

## When to use

- Opening or resuming work on a SysML project root. New house default is `sysml-models/` (legacy opt-in: `sysml-v2-models/projects/<slug>/`).
  - House / system repo (`modelbasedPrj-*`): `sysml-models/` (NCU-LEO anchor `TSK_model_leo_cubesat`)
  - Multi-project pack (legacy): `sysml-v2-models/projects/<slug>/`
- Recording design decisions, assumptions, backlog not fully expressed in `.sysml`
- Maintaining `outputs/*.md` / system-design-report atoms (ART/SEC/CLM)
- Multi-turn refactors, requirement audits, report updates

**Skip MemNet** when: one-shot question with no edit; comment-only `.sysml` change; MemNet MCP missing from catalog; or `serve_status` false.

## Atomisation (docs + model)

Model elements: PRT/POR/CON/BEH/ITM/REQ + SYM (path, line) + MOD per file. Conventions: CONV. Open forks: DEC. Backlog: ISSUE. Docs: ART/SEC/CLM. Campaign: TSK_model_<short>.

ITM is a **node** only (item definition / flow item); see [the ITM pattern](references/sysml-memnet-patterns.md#itm-is-a-node).

## Pairing

- **sysml-modeling-workflow** -- encodes the 6-step sequence
- **system-design-report-generator** -- full pack generate/maintain: pin_map before prose, ART/SEC/CLM after sync ([memnet-report-pipeline.md](../system-design-report-generator/references/memnet-report-pipeline.md))
- **sysml-view-doc-sync** -- sync outputs, then atomise key claims as CLM
- **sysml-refactorer**, **sysml-traceability**, **sysml-requirements-audit** -- persist findings after work
- **memnet-format** -- MemNet GQL wire; thin SysML x MemNet kind/id pointer only
- **mcp-memnet** -- base MCP mechanics
- **memnet-nested-sessions** -- catalog / look loop (do not copy here)
- **memnet-multitask** -- shared tip HTTP (`user-memnet`) when Task workers run

## Quick anchors

| Anchor | Use when |
|--------|----------|
| `TSK_model_<short>` | Campaign cue (catalog). Interiors: MCP `session=` per [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md) |
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
- [mcp-memnet](../mcp-memnet/SKILL.md), [memnet-nested-sessions](../memnet-nested-sessions/SKILL.md), [memnet-goldfish-loop.mdc](../rules/memnet-goldfish-loop.mdc)
- [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md)
