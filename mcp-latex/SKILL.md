---
name: mcp-latex
description: >-
  Cursor MCP LaTeX Server (local Python, tools/mcp-latex-server): create/edit/read/validate .tex,
  list files, document structure. Optional final PDF path needs a TeX distribution (MiKTeX, TeX Live, MacTeX).
  Triggers: latex mcp, tex file, final pdf, compile latex, robertodure-mcp-latex-server, LobeHub latex.
metadata:
  pattern: tool-wrapper
  specialization: mcp-integration
  domain: publishing
  mcp_key: robertodure-mcp-latex-server
token_guardrails: |
  - **Scope:** use for **LaTeX artifacts** and **final-document** workflows — not a substitute for `projects/<name>/outputs/*.md` as the primary design record (pair with **project-output-article** / **sysml-view-doc-sync** when exporting from markdown).
  - **Paths:** tool paths are resolved by the server relative to its **base path** (see upstream); stay within allowed directories — do not exfiltrate or write outside the user’s agreed LaTeX workspace.
  - **Compile:** full **pdflatex** / engine runs are **not** guaranteed by the MCP alone; confirm TeX is installed when the user needs PDF output.
---

# MCP: LaTeX Server

1. **Config:** [.cursor/mcp.json](../../../.cursor/mcp.json) key **`robertodure-mcp-latex-server`** — venv Python + `latex_server.py`; see [docs/mcp/LATEX_MCP.md](../../../docs/mcp/LATEX_MCP.md) for **Windows vs macOS/Linux** `command` paths and **LobeHub** `mcp view` (manual install, not generic `npx` alone).
2. **Upstream / smoke test:** [tools/mcp-latex-server/](../../../tools/mcp-latex-server/) — optional local check: `python tools/mcp-latex-server/test_latex_mcp_stdio.py` from repo root.
3. Load [references/mcp-policy.md](references/mcp-policy.md) for tools list and pairing with markdown outputs.

**Repo map:** [tools/mcp/README.md](../../../tools/mcp/README.md).
