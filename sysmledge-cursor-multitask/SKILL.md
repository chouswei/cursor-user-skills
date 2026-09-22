---
name: sysmledge-cursor-multitask
description: >-
  Use when Cursor Multitask/Task sees both product MCP sysmledge and tip MCP
  memnet-pi -- route product asks to sysmledge only; tip!=face forever.
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
| SysMLEdge product query or propose | `sysmledge` |
| Bind / unbind / STALE honesty | `sysmledge` |
| MemNet serve bounce, tip session_not_found | `memnet-pi` (ops only) |
| Unbound project | `openProject` then refuse until bound |
| PD / overlay `sysmledge-pd-tree` | SysMLEdge-based when bound; files until `openProject` sticks. MUST NOT skip the face because the graph lags files. |

## Parent coordinator

1. Put `sysmledge` + `projectId@rev` in every worker prompt.
2. Workers call product allowlist only -- never tip as product path.
3. After human Save: face must show `rev.stale=true` until reproject/bind.
4. `propose` != Save.

## Soft-pass kills

- tip-as-face
- skip-face-because-graph-lags-files
- invent_2 as proof_pass / keep-using / H2H / sell
- foam-beachhead as general MCP
- tunnel localhost as current day-1 product face
- tip MemNet on WWW as product

## Pairing

- Day loop: [sysmledge-workflow](../sysmledge-workflow/SKILL.md)
- Face / MCP: product MCP `sysmledge` (not stale `sysmledgraph`)
- MemNet Multitask: [memnet-multitask](../memnet-multitask/SKILL.md)
- MemNet use: [memnet-use](../memnet-use/SKILL.md)
- MemNet tools: [mcp-memnet](../mcp-memnet/SKILL.md)
