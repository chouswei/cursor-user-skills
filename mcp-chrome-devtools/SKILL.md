---
name: mcp-chrome-devtools
description: >-
  Cursor MCP chrome-devtools-mcp: drive Chrome — snapshots, screenshots, click, type, network, performance.
  Triggers: browser automation, devtools mcp, page inspect chrome.
metadata:
  pattern: tool-wrapper
  specialization: mcp-integration
  domain: browser
  mcp_key: chrome-devtools
---

# MCP: Chrome DevTools

1. **Config:** [.cursor/mcp.json](../../../.cursor/mcp.json) key `chrome-devtools`; see [docs/mcp/CHROME_DEVTOOLS_MCP.md](../../../docs/mcp/CHROME_DEVTOOLS_MCP.md).
2. **Before heavy use:** load [references/mcp-policy.md](references/mcp-policy.md).
3. Call MCP tools **only** as needed; read each tool schema in the MCP descriptor before invoking.

**Repo:** [tools/mcp/README.md](../../../tools/mcp/README.md) (server map).
