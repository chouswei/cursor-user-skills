# SysML v2 MCP — Cursor server rules (strict)

These mirror the **MCP server use instructions** for this workspace:

1. Call **exactly** the tool(s) the user asked for — do not add extra MCP calls.
2. **preview** means **only** the preview tool. **Do not** call `getComplexity` alongside preview unless the user asked for complexity or metrics.
3. `getComplexity` **only** when the user literally asks for **complexity** or **metrics**.
4. After **preview**, if the client supports diagram rendering, pass returned Mermaid to the client’s diagram renderer as configured — **do not** paste large raw JSON or markup as the only output when a visual was requested.
5. If the user asks to **visualise/visualize** a file, use preview / visualize / `visualiseFile` / `visualizeFile` per server — **not** `getDefinition` or `getComplexity` for that request.
6. **Repo policy:** do **not** run `visualize.py` unless the user explicitly asks ([AGENTS.md](../../../../AGENTS.md)).
7. **Tool parameters:** for **getDefinition**, **getReferences**, and **getHierarchy**, pass the symbol/element simple name as **`name`** (string). For inline model text use **`code`**. See [tool-parameters.md](tool-parameters.md).
8. **Do not** treat **`node_modules/sysml-v2-lsp/dist/server/mcpServer.js`** as user source: it is a minified MCP bundle; ignore editor noise or stack traces pointing at it.

**Setup:** [docs/mcp/SYSML_V2_MCP_SETUP.md](../../../../docs/mcp/SYSML_V2_MCP_SETUP.md).
