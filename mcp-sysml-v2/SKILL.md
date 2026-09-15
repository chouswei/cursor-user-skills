---
name: mcp-sysml-v2
description: >-
  Cursor MCP sysml-v2 (npm sysml-v2-lsp from daltskin/sysml-v2-lsp): validate, parse, getDiagnostics,
  getSymbols, getDefinition, getReferences, getHierarchy, getModelSummary, preview, getComplexity. Use
  code= for inline SysML; name= for
  getDefinition/getReferences/getHierarchy. Triggers: .sysml validate, preview diagram, symbols, sysml-v2 mcp.
metadata:
  pattern: tool-wrapper
  specialization: mcp-integration
  domain: sysml-v2
  mcp_key: sysml-v2
  version: "1.3"
token_guardrails: |
  - After workspace .sysml edits: call validate (and preview if diagram requested).
  - Obey references/cursor-mcp-rules.md for preview vs visualizeFile and complexity.
  - Before getDefinition / getReferences / getHierarchy: use argument name (string), not symbolName.
---

# MCP: SysML v2 (sysml-v2-lsp)

1. **Upstream:** [daltskin/sysml-v2-lsp](https://github.com/daltskin/sysml-v2-lsp) — npm package **`sysml-v2-lsp`**; MCP entry = **`node_modules/.../mcpServer.js`** or npm bin **`sysml-mcp`**. Grammar and parser ship inside **`dist/`** at publish time.
2. **User-pack install:** `~/.cursor/tools/sysml-v2-mcp` (Windows: `$env:USERPROFILE\.cursor\tools\sysml-v2-mcp`); install with `npm install --ignore-scripts`. Version 0.23.0 has a POSIX-only `postinstall` that makes ordinary `npx` installation exit on Windows.
3. **Config:** user-level `~/.cursor/mcp.json` (Windows: `$env:USERPROFILE\.cursor\mcp.json`), key **`sysml-v2`** (Cursor MCP namespace **`user-sysml-v2`**), launches `node` with the installed `dist/server/mcpServer.js` directly. Avoid a duplicate project-level key.
4. **Tool arguments:** read **[references/tool-parameters.md](references/tool-parameters.md)** — **`code`** (inline SysML text) for validate/parse/preview/…; **`name`** for **getDefinition**, **getReferences**, **getHierarchy**. For rename, impact, or search, query the file or code just loaded; never treat the MCP workspace URI index as model SSOT. If Cursor’s MCP descriptor disagrees with a new release, follow the descriptor.
5. **Mandatory:** read [references/cursor-mcp-rules.md](references/cursor-mcp-rules.md) before **preview** / **visualize** / **complexity** calls.
6. **Repo workflow:** [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) — **MCP validate** after model edits. In `modelbasedPrj-*` system repos, SysML models live under `sysml-models/`.
7. **De facto:** Grammar-valid SysML can still misrepresent **as-built** wiring. For port renames and COTS interface style, cross-check deploy + outputs per [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md).
8. **Version check:** compare the pinned dependency in `~/.cursor/tools/sysml-v2-mcp/package.json` with `npm view sysml-v2-lsp version`.

## Grammar / LSP reference

- The published `sysml-v2-lsp` package bundles the grammar, parser, validation, symbols, and MCP entry point.
- Cursor talks to the server locally over stdio through `~/.cursor/mcp.json` (key `sysml-v2`, namespace `user-sysml-v2`); it is not a REST API.
- If Cursor opens `node_modules/sysml-v2-lsp/dist/server/mcpServer.js`, that bundle is expected and should not be edited directly.
- Use `npm view sysml-v2-lsp version` to check against `~/.cursor/tools/sysml-v2-mcp/package.json` for updates, and restart Cursor after upgrades.
- **Usage questions** (how to express constructs, not MCP tools): [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) — SysML Forum / FAQ before inventing.
