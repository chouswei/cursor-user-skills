# sysmledgraph MCP — historical agent notes

This file documents an abandoned MCP and is not a live routing guide. Do not run these commands.

- **indexDbGraph** when the graph may be stale after `.sysml` changes; use **paths** relative to repo root.
- **impact** / **context** / **query** / **cypher** for “who references”, blast radius, and graph exploration.
- **Do not** index the full OMG release tree for routine work (huge) — see [docs/mcp/SYSMLEDGRAPH_MCP.md](../../../../docs/mcp/SYSMLEDGRAPH_MCP.md).
- One-time LSP setup may be required: `npm run sysmledgraph:setup-lsp` from repo root (see doc).
