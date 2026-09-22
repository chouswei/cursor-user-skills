---
name: sysmledge-workflow
description: >-
  Day loop via sysmledge WWW. Multitask → sysmledge-cursor-multitask.
  tip memnet-pi never product.
metadata:
  pattern: pipeline
  version: "1.1"
---
# SysMLEdge workflow

**SysMLEdge hosts `model@rev`.** Day loop via product MCP **`sysmledge` WWW** (not tip MemNet).

## Invariants

| Rule | |
|------|--|
| Host | SysMLEdge product MCP **`sysmledge`** (WWW droplet face) |
| Tip | `memnet-pi` OPS-ONLY — **never product** |
| SSOT | Two model SSOTs. MUST NOT substitute. Bound desk when overlay + `rev_status` `working_ssot=graph`; else repo `sysml-models/`. README states which kind. Tip MemNet is not a model SSOT. |
| Identity | graph = model @ git SHA; reads return `rev.sha` + `rev.stale` |
| Face tools | `openProject` / `closeProject` / `rev_status` / `ask` / `gql` / `pin_map` / `propose` |
| Agents | propose under `proposals/<id>/` only |
| Honesty | after Save, face must STALE until reproject |

## Day loop

```
bound+graph: rev_status/gql/ask -> propose -> human Save -> sync sysml-models/ backup
unbound/repo-based: edit .sysml -> validate -> outputs/parts -> human Save -> reproject if a face exists
```

## Multitask

If Cursor also shows `memnet-pi`, still use **`sysmledge` only** for product. See **`sysmledge-cursor-multitask`**. tip≠face.

## Soft-pass kills

tip-as-host · tip-as-face · skip-face-because-graph-lags-files · file-watch sync · never-STALE face · agent SSOT write · invent_2 as proof_pass · tunnel-as-day-1

## Pair

`sysmledge-cursor-multitask` · `mcp-sysmledge` · `sysmledge-host-model-at-rev`
