---
name: sysmledge-cursor-multitask
description: >-
  Use when Cursor Multitask/Task sees both product MCP sysmledge and tip MCP
  memnet-pi -- route product asks to sysmledge only; tip!=face forever.
  Also: SysMLEdgePrj-* trees bind on sysmledge, never Foam, never tip-as-face.
metadata:
  pattern: pipeline
  version: "1.1.0"
  pairs_with:
    - sysmledge-workflow
    - memnet-multitask
    - memnet-use
    - mcp-memnet
---
# SysMLEdge Cursor Multitask (tip!=face)

When Cursor Multitask or Task sees both product MCP `sysmledge` and tip MCP `memnet-pi`, route by face.

## Faces

| MCP | Role | Day-1 product path? |
|-----|------|---------------------|
| **sysmledge** | Product face (model@rev host); WWW /mcp + Bearer | YES |
| **memnet-pi** | Tip MemNet engine plumbing (ops bounce / session) | NO |

Product allowlist on `sysmledge` only: `openProject` / `closeProject` / `rev_status` / `ask` / `gql` / `pin_map` / `propose`.

## Routing

| Ask | Route |
|-----|-------|
| Foam archive / historical meter desk | `sysmledge` only if that `projectId` is bound; never as a SysMLEdgePrj face |
| SysMLEdgePrj / product query or propose | `sysmledge` after human `openProject` |
| Bind / unbind / STALE honesty | `sysmledge` |
| MemNet serve bounce, tip session_not_found | `memnet-pi` (ops only) |
| Unbound SysMLEdgePrj | `openProject` then refuse live-SSOT until bound; `sysml-models/` remains author SSOT |

Prefix and migrate: [sysmledge-workflow/references/sysmledge-prj.md](../sysmledge-workflow/references/sysmledge-prj.md). MUST NOT invent `projectId`. MUST NOT reuse `foam-beachhead` for PD or any `SysMLEdgePrj-*` tree.

## Parent coordinator

1. Put `sysmledge` + `projectId@rev` in every worker prompt.
2. Workers call product allowlist only -- never tip as product path.
3. After human Save: face must show `rev.stale=true` until reproject/bind.
4. `propose` != Save.

## Soft-pass kills

- tip-as-face
- invent_2 as proof_pass / keep-using / H2H / sell
- foam-beachhead as general MCP or as a SysMLEdgePrj / PD face
- invent SysMLEdgePrj `projectId` / bind in pack or product AGENTS
- tunnel localhost as current day-1 product face
- tip MemNet on WWW as product

## Pairing

- Day loop: [sysmledge-workflow](../sysmledge-workflow/SKILL.md)
- Face / MCP: product MCP `sysmledge` (not stale `sysmledgraph`)
- MemNet Multitask: [memnet-multitask](../memnet-multitask/SKILL.md)
- MemNet use: [memnet-use](../memnet-use/SKILL.md)
- MemNet tools: [mcp-memnet](../mcp-memnet/SKILL.md)
