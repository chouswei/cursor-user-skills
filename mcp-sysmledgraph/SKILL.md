---
name: mcp-sysmledgraph
description: >-
  Retarget to MemNet/SysMLEdge MCP (rev_status, gql_read, gql_context,
  gql_impact, list_scope, propose, reproject); never Kuzu, Cypher, or graph.kuzu.
  Triggers: sysmledgraph, sysmledgraph mcp, indexDbGraph, Kuzu sysml, graph.kuzu.
  Skip: Mermaid or D2 viz-only.
metadata:
  pattern: tool-wrapper
  version: "2.0"
  domain: sysml
  specialization: mcp-integration
  mcp_key: sysmledgraph
  pairs_with: [sysmledge-workflow, mcp-memnet, sysml-gql, mcp-sysml-v2]
token_guardrails: |
  - Live route is SysMLEdge/MemNet MCP P0 tools. MUST NOT install or invoke Kuzu sysmledgraph.
  - MUST NOT run cypher, indexDbGraph, or a Kuzu worker. Historical names below are refuse-only.
  - Day loop and STALE: sysmledge-workflow.
---

# MCP: sysmledgraph (retarget)

**Live work:** use **SysMLEdge / MemNet MCP**. Do not treat this folder as a Kuzu tool-wrapper.

Day loop, STALE, and propose-only: [sysmledge-workflow](../sysmledge-workflow/SKILL.md).

Policy: [references/mcp-policy.md](references/mcp-policy.md).

## Live tools (P0 names)

| Tool | Role |
|------|------|
| `rev_status` | `current.sha`, `rev.sha`, `rev.stale` |
| `gql_read` | Bounded GQL read (STALE / `staleOk` as in SysMLEdge P0) |
| `gql_context` | Neighbourhood of one qname/path |
| `gql_impact` | Upstream/downstream along mapped connections |
| `list_scope` | Indexed roots / package qnames in the bound projection |
| `propose` | Write only `sysml-models/proposals/<id>/{PATCH.md, delta.sysml}` |
| `reproject` | Rebuild MemNet from current SysML; not SSOT |

Engine is **MemNet + GQL**. Contracts: [P0-contracts.md](https://github.com/chouswei/SysMLEdge/blob/main/docs/P0-contracts.md), [P1-acceptance.md](https://github.com/chouswei/SysMLEdge/blob/main/docs/P1-acceptance.md), [SysMLEdge AGENTS.md](https://github.com/chouswei/SysMLEdge/blob/main/AGENTS.md).

## Historical abandoned / Kuzu -- refuse

The former **sysmledgraph** MCP (Kuzu + Cypher, `graph.kuzu`, TCP worker for a Kuzu file lock) is abandoned.

**MUST NOT** install, configure, invoke, or recommend:

- `indexDbGraph`, `list_indexed`, `clean_index`, `cypher`, `query`, `context`, `impact`, `rename` (as a graph edit), `generate_map`
- CLI `worker start/stop`, `graph export` / `graph map` against Kuzu
- `npm run sysmledgraph:setup-lsp` as a live setup path
- Treating an MCP workspace URI index as model SSOT

Those names are historical schema only. Live rename/impact/search is GQL on MemNet via the P0 tools above.

Loaded-file SysML **syntax** (`parse` / `validate` / symbols) remains [mcp-sysml-v2](../mcp-sysml-v2/SKILL.md) -- that is not a graph SSOT.
