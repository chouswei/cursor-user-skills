# Markdown → `.tex` — mechanics

## Pandoc (recommended)

Install: [Pandoc](https://pandoc.org/installing.html) on the PATH.

### One Markdown file

```bash
pandoc "path/to/input.md" -o "path/to/output.tex" -s
```

### Multiple Markdown files → one `.tex`

Pandoc **concatenates** input files **in the order given**, then parses the result as one Markdown document:

```bash
pandoc "intro.md" "design.md" "appendix.md" -o "combined.tex" -s
```

- **Section structure:** Each file often starts with `#` or `##`. If every file begins with `#`, you get multiple top-level titles — fine for a **report** with “chapters”; for **article** style you may want per-file heading demotion (see below).
- **YAML front matter:** Typically only metadata from the **first** file is applied. Remove or strip duplicate `---` blocks from subsequent files **before** merging, or use a **wrapper** `.md` that sets `title`/`author` once and uses `\include`-style workflow instead.
- **Order:** The user (or `llm_toc` in **project-output-article**) should define canonical order — filenames sort order is rarely correct for narrative.

**Useful flags** (single or multi input):

| Flag | Purpose |
|------|---------|
| `-s` / `--standalone` | Full document with preamble. |
| `--metadata title="..."` | Title; also `author`, `date`. |
| `-V documentclass=...` | e.g. `article`, `report`. |
| `--toc` | Table of contents. |
| `--top-level-division=chapter` | When using `book` / `report`-like classes (check Pandoc version). |

**Windows:** Quote paths; forward slashes work in many shells.

### Heading levels across files

If each part file uses `# Title` and you want parts to become `\section` instead of multiple `\part`/top-level chapters:

- **Option A:** Edit Markdown so only the **first** file has `#` and later files use `##` / `###` as needed.
- **Option B:** Pandoc filters / `--shift-heading-level-by` (see Pandoc manual) to demote headings in specific inputs — automation varies by version; when in doubt, normalize headings in `.md` once.

### Merge-first pattern (duplicate YAML)

1. Build `merged.md`: first file including its YAML; following files **without** front matter, only body, separated by `\n\n` (or horizontal rules if desired).
2. `pandoc merged.md -o out.tex -s`
3. Delete `merged.md` if it was scratch-only.

### Master `.tex` with `\input`

When you need separate LaTeX maintenance per chapter:

1. For each `chapter.md`, run Pandoc to a **fragment** (body only — depends on template; often omit `-s` or use a custom template that outputs `\chapter{...}...\n`).
2. One **hand-written** `main.tex` with `\documentclass`, preamble, `\begin{document}`, `\input{ch1}`, `\input{ch2}`, …

This repo skill treats **one-shot Pandoc multi-input** as the default; `\input` is for advanced layout control.

## What Pandoc handles well

- Headings → `\section`, `\subsection`, …
- Emphasis, inline code, fenced code blocks
- Lists, block quotes, pipe tables (version-dependent)

## Mermaid

Pandoc does **not** render Mermaid to figures automatically.

1. **Placeholder** — `% TODO: diagram — see source .md`
2. **Verbatim** — Keep fenced code as `verbatim` / `lstlisting`
3. **Pre-render** — **[mmdc](../../mmdc/SKILL.md)** → SVG/PNG → `\includegraphics` in `figure`

## Limitations

- Internal `#anchors` across concatenated files: ensure heading text is unique for `\label` hygiene.
- Complex HTML in Markdown may not map cleanly.

## Without Pandoc

- **Short combined doc:** **[mcp-latex](../mcp-latex/SKILL.md)** — create skeleton, then paste sections in order (does not scale to many files).
- **Better:** Install Pandoc and use multi-input or merge-first.

## Verification

- `output.tex` exists; `\documentclass` present with `-s`.
- PDF: user runs `pdflatex` / `latexmk` locally with a TeX distribution installed.
