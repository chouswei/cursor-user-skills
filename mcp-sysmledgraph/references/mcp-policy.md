# sysmledgraph MCP -- retarget policy

Live routing guide. Engine is **MemNet**. **Kuzu is rejected.**

## Live (SysMLEdge / MemNet MCP)

Use these P0 names only:

- `rev_status` -- SHA + STALE
- `gql_read` -- bounded GQL; `staleOk` is read-only
- `gql_context` -- neighbourhood of one qname/path
- `gql_impact` -- blast radius along mapped connections
- `list_scope` -- indexed roots / package qnames
- `propose` -- `sysml-models/proposals/<id>/` only
- `reproject` -- rebuild projection from current SysML; not SSOT

Day loop: [../sysmledge-workflow/SKILL.md](../../sysmledge-workflow/SKILL.md). Contracts: [P0-contracts.md](https://github.com/chouswei/SysMLEdge/blob/main/docs/P0-contracts.md).

**MUST NOT** run Kuzu, Cypher, or `graph.kuzu` as a live command.

## Historical abandoned / Kuzu -- refuse

Do not run these. They belonged to codebase-sysmledgraph (Kuzu file lock + Cypher).

| Old name | Why refuse |
|----------|-----------|
| `indexDbGraph` | Wrote Kuzu; not MemNet reproject |
| `cypher` / `query` / `context` / `impact` | Cypher against Kuzu, not GQL |
| `rename` as graph edit | SysMLEdge rename is a proposal (`delta.sysml` + `PATCH.md`) |
| `worker start/stop` | TCP daemon for Kuzu lock -- not applicable |
| `npm run sysmledgraph:setup-lsp` | Legacy LSP bootstrap for the abandoned indexer |

Lineage (accuracy only): path-only `.sysml` index via sysml-v2-lsp, graph in Kuzu. SysMLEdge does not continue that DB.

Retrieval seeds: retarget MemNet SysMLEdge MCP, never Kuzu, rev_status, gql_read, propose, graph.kuzu refuse
