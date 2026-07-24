# SysML v2 MCP — tool arguments (daltskin/sysml-v2-lsp)

Verified against **npm `sysml-v2-lsp`** MCP as wired in [.cursor/mcp.json](../../../../.cursor/mcp.json) (`node …/mcpServer.js`). Cursor may show the same schema in **MCP server tool descriptors**; if a release differs, follow the descriptor.

## Inline model text: `code`

Pass **full SysML v2 source** as a string in **`code`** for:

| Tool | Typical `code` use |
|------|---------------------|
| **validate** | Required for inline validation (otherwise use whatever `uri`/workspace fields the descriptor allows). |
| **parse** | Same. |
| **getDiagnostics** | Same. |
| **getSymbols** | Same. |
| **getModelSummary** | Same. |
| **preview** | Same; set **`view`** (e.g. `general`, `interconnection`, `state`) per descriptor. |
| **getComplexity** | Same; call **only** when the user asked for complexity/metrics ([cursor-mcp-rules.md](cursor-mcp-rules.md)). |

If the tool returns **Input validation error** / **`code` expected string**, the model text was omitted or the wrong key was used.

## Symbol / element lookup: `name` (not `symbolName`)

These tools expect the **symbol or element simple name** in **`name`**:

| Tool | `name` meaning |
|------|----------------|
| **getDefinition** | Definition to resolve (e.g. `SamplePart`, `NetgearGS728TPv3`). |
| **getReferences** | Symbol whose references to list (definition or usage name, per server behaviour). |
| **getHierarchy** | Element whose containment chain to return (e.g. a `part` usage name). |

Do **not** use `symbolName`, `elementName`, or `qualifiedName` unless the MCP descriptor for your build explicitly shows them.

## Upstream / install

- Source & releases: [daltskin/sysml-v2-lsp](https://github.com/daltskin/sysml-v2-lsp).
- npm package **`sysml-v2-lsp`**; MCP CLI bin **`sysml-mcp`** (same script as `mcpServer.js`).
- **No** supported `npx sysml-v2-lsp validate` CLI.
- **Windows:** `npm install` may fail in **postinstall**; use **`--ignore-scripts`**.
- **Project load** in repo: `python sysml-v2-models/scripts/exam_model.py --project <folder>` (optional `--visualize` for BDD+IBD PNG smoke test). Diagrams: `visualize.py` when needed.

## Noise: `mcpServer.js`

The published **`mcpServer.js`** is a **large minified bundle**. Do not `@`-edit it; follow the troubleshooting guidance in the `mcp-sysml-v2` skill and [.cursorignore](../../../../.cursorignore).
