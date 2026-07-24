---
name: mcp-sysmledgraph
description: >-
  Cursor MCP sysmledgraph: indexDbGraph, context, impact, cypher, query, clean, rename, list indexed paths;
  Kuzu graph under .sysmledgraph-local. Triggers: cross-file sysml, who references, graph query, index project, sysmledgraph mcp.
metadata:
  pattern: tool-wrapper
  specialization: mcp-integration
  domain: sysml-v2
  mcp_key: sysmledgraph
---

# MCP: sysmledgraph

1. **Config:** [.cursor/mcp.json](../../../.cursor/mcp.json) key `sysmledgraph`; storage `SYSMEDGRAPH_STORAGE_ROOT=.sysmledgraph-local`.
2. **Setup & index roots:** [docs/mcp/SYSMLEDGRAPH_MCP.md](../../../docs/mcp/SYSMLEDGRAPH_MCP.md) — typical roots `sysml-v2-models/libs/common`, `sysml-v2-models/projects`.
3. Load [references/mcp-policy.md](references/mcp-policy.md) before **indexDbGraph** or destructive **clean** calls.

**Repo:** [tools/mcp/README.md](../../../tools/mcp/README.md).
