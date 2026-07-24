# LaTeX MCP — agent notes

## When to use

- User wants **`.tex`** creation/editing, **structure** or **light validation** via MCP.
- **Final** deliverable is **LaTeX/PDF** while **`projects/<name>/outputs/*.md`** remains source of truth for system design — use after content is stable, or in parallel for a formal export track.
- **Not** the default path for SysML/model docs; see **project-output-article** / **sysml-view-doc-sync** for markdown outputs.

## Tools (typical names — confirm in MCP panel)

| Tool | Role |
|------|------|
| `create_latex_file` | New document from parameters (document class, title, packages, body). |
| `edit_latex_file` | Replace / insert / append / prepend by search or line. |
| `read_latex_file` | Read `.tex` content. |
| `list_latex_files` | Discover `.tex` under a directory. |
| `validate_latex` | Basic checks (not a full engine run). |
| `get_latex_structure` | Sections / outline extraction. |

## Host and paths

- Server **`cwd`** is **`tools/mcp-latex-server`** in this repo; file paths in tools follow the **upstream** server rules (sandbox under allowed roots — see [github.com/RobertoDure/mcp-latex-server](https://github.com/RobertoDure/mcp-latex-server)).
- Optional **`LATEX_BASE_PATH`** env: see [docs/mcp/LATEX_MCP.md](../../../../docs/mcp/LATEX_MCP.md).

## Prerequisites

- **Python venv** with `mcp` + deps (per repo doc).
- **Full TeX distribution** for PDF compilation workflows the user requests outside the MCP (or any compile step the server documents).

## Secrets

- No API keys for this server; avoid pasting sensitive **paths** or **document content** into public logs.

## Pairing

- **project-output-article** — markdown section order / `llm_toc` first; LaTeX as optional export.
- **md-to-tex** — convert **one or several** `.md` → **one** `.tex` (usually **pandoc** multi-input or merge-first); use this MCP to **edit/create** `.tex` when Pandoc is absent or for touch-ups.
- **tech-report-generator** — narrative engineering report; LaTeX only if the user wants a `.tex`/print pipeline.
