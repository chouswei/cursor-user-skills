---
name: mcp-markitdown
description: >-
  MarkItDown MCP (user-markitdown): convert Office/PDF/HTML and other files to Markdown
  via convert_file, convert_directory, or list_supported_formats. Triggers: markitdown,
  convert to markdown, pdf to md, docx to markdown, markitdown mcp.
metadata:
  pattern: tool-wrapper
  specialization: mcp-integration
  domain: publishing
  mcp_key: markitdown
  version: "1.2"
token_guardrails: |
  - GetMcpTools(server=user-markitdown) before CallMcpTool.
  - Prefer convert_file for one path; convert_directory only when the user wants a batch.
  - Do not dump huge converted bodies into chat — summarise or write to an agreed path.
  - For PCBA datasheets under parts/*/hardware/*/datasheets/, convert then cite page/section — do not paste whole PDFs.
---

# MCP: MarkItDown (`user-markitdown`)

## When to use

- Turn PDF, DOCX, PPTX, XLSX, HTML, images (OCR-capable setups), or similar into Markdown
- Batch-convert a folder of supported files
- Check which formats the server supports before converting

## Tool discovery and auth

1. `GetMcpTools(server="user-markitdown")` before calling.
2. Auth is uncommon for local MarkItDown; if `needsAuth` / 401, call `mcp_auth` once then retry.

## Tools

| Tool | Use |
|------|-----|
| `list_supported_formats` | Capability check |
| `convert_file` | One file: `file_path` **or** `file_content` (base64) + `filename` |
| `convert_directory` | `input_directory`; optional `output_directory` |

## Typical workflow

1. Optional: `list_supported_formats` if unsure the type is supported.
2. `convert_file` with an absolute `file_path` when possible.
3. Return a short summary + path to output Markdown if written to disk; avoid pasting multi-page dumps unless asked.

## Pitfalls

- Scanned PDFs need OCR-capable MarkItDown extras; plain convert may return empty/weak text.
- Huge binaries: prefer path over base64 `file_content`.
- Datasheet PDFs (e.g. W5500): convert once, keep a short extract in-repo if needed; avoid re-dumping multi-MB Markdown into chat.
- Pair with `mdtohtml` / `md-to-tex` only when the user wants a further export — MarkItDown stops at Markdown.
---
