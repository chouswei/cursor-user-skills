---
name: md-to-tex
description: >-
  Markdown to one LaTeX (.tex): one .md or several .md files (sections/chapters) combined into a single .tex.
  Pandoc-first when available; MCP LaTeX or manual skeleton as fallback. Triggers: md to tex, multiple md one tex,
  combine markdown latex, chapters md tex, pandoc merge md, outputs md bundle tex, foam detection md latex.
metadata:
  pattern: pipeline
  domain: publishing
  pairs_with:
    - mcp-latex
    - mermaid
    - mmdc
    - project-output-article
    - system-design-report-generator
token_guardrails: |
  - **One output .tex** per run unless the user names several output paths explicitly.
  - **Inputs:** either **one** `.md` or an **ordered list** of `.md` paths (sections) — confirm order before converting; do not merge unrelated folders without user confirmation.
  - **Do not** paste huge multi-file bodies into chat; read files incrementally or convert via shell **pandoc** on disk.
  - **Mermaid** is not auto-rendered to figures in LaTeX — see references (placeholder, verbatim, or **mmdc** + `\includegraphics`).
  - **Model truth** remains SysML / `outputs/*.md`; combined `.tex` is **derived**.
  - **UTF-8 encoding:** All input `.md` files must be UTF-8. When merging multiple `.md` files into one `.tex`, use Pandoc with explicit UTF-8: `pandoc -f utf-8 -t latex input1.md input2.md input3.md -o output.tex`. Check output for encoding corruption (e.g., `â†'` instead of `→`); if found, re-encode inputs.
---

# Markdown → one LaTeX (.tex)

**When:** Export to **one** `.tex` from **one** Markdown file **or** from **several** Markdown files that represent **sections/chapters** (e.g. split `outputs/` files).

## Pipeline — single `.md`

1. **Lock paths** — Input `file.md`, output `file.tex` (or derive basename).
2. **Pandoc** — `pandoc input.md -o output.tex -s` — [references/md-to-tex-conversion.md](references/md-to-tex-conversion.md). For **system-design-report** packs, build the input list from **hub `llm_toc`** `file` order (often **section files only**, not the hub) — [system-design-report-generator](../system-design-report-generator/SKILL.md).
3. **No Pandoc** — Short doc: **[mcp-latex](../mcp-latex/SKILL.md)**; else recommend installing Pandoc.
4. **Mermaid** — Per references § Mermaid.
5. **Check** — `\documentclass` in output; optional user-side `pdflatex`.

6. **Pairing** — Project outputs: [project-output-article](../project-output-article/SKILL.md) / `llm_toc` for stable section order.

## Pipeline — multiple `.md` (sections) → one `.tex`

1. **Ordered list** — User supplies **`path1.md`, `path2.md`, …** in **document order** (or a glob with explicit sort rule). One output **`combined.tex`** (or user path). If files use overlapping heading levels, note whether to shift levels (see references).

2. **Pandoc (preferred)** — Concatenate inputs in order:

   ```bash
   pandoc "sec01.md" "sec02.md" "sec03.md" -o "book.tex" -s
   ```

   Details, metadata, and heading pitfalls: [references/md-to-tex-conversion.md](references/md-to-tex-conversion.md) § **Multiple inputs**.

3. **Alternatives** — (a) Concatenate to a **temporary single `.md`** (strip duplicate YAML from non-first files), then run single-file Pandoc; (b) **master `.tex`** with `\input{part1.tex}` … after generating each part with Pandoc to **fragment** (`-s` off or custom template) — more control, more steps.

4. **Mermaid / assets** — Same as single-file; each source `.md` may contain diagrams — track which file needs **mmdc** pre-render.

5. **Sanity check** — One coherent preamble; sections read in order; fix duplicate `\label`s if Pandoc warns.

**Docs hub:** [docs/mcp/LATEX_MCP.md](../../../docs/mcp/LATEX_MCP.md) · **MCP skill:** [mcp-latex](../mcp-latex/SKILL.md)
