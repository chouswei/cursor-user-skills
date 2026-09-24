---
name: tikz
description: >-
  Use when authoring LaTeX TikZ figures (paths, nodes, Overleaf). Not for SysML
  Mermaid, D2 architecture posters, or DEXPI graph SSOT. For ISO 14617 P&ID
  symbols use pid-circuit-tikz.
---
# TikZ (LaTeX graphics)

Author vector figures in LaTeX with **TikZ** (`tikzpicture`). Prefer this when the deliverable is a `.tex` figure or Overleaf/PDF pipeline -- not as a substitute for Mermaid (SysML reports) or D2 (architecture posters).

Docs: https://www.overleaf.com/learn/latex/TikZ_package

## When

- User asks for TikZ / PGF / LaTeX drawing / Overleaf figure
- Publication-quality vector art inside a TeX document

## When not

- SysML / `outputs/**` Mermaid -> Mermaid skills
- Architecture SVG posters -> D2 architecture
- DEXPI / plant graph SSOT -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md)
- ISO 14617 P&ID symbols -> [PIDcircuitTikZ](../pid-circuit-tikz/SKILL.md)

## Hard rules

1. Every TikZ path ends with `;`.
2. Load `\usepackage{tikz}` and only needed `\usetikzlibrary{...}`.
3. Do not invent equipment tags beyond locks / SSOT.
4. Prefer named `\node` + `positioning` when the figure will grow.
5. Compile with pdflatex/lualatex when available; else deliver `.tex` + deps.

## Minimal skeleton

```latex
\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{positioning}
\begin{document}
\begin{tikzpicture}[
  box/.style={draw, thick, minimum width=2cm}
]
  \node[box] (a) {A};
  \node[box, right=of a] (b) {B};
  \draw[->] (a) -- (b);
\end{tikzpicture}
\end{document}
```

## Core vocabulary

| Need | Pattern |
|------|---------|
| Line | `\draw (x,y) -- (u,v);` |
| Curve | `\draw (a) .. controls (c1) and (c2) .. (b);` |
| Circle | `\filldraw[black] (0,0) circle (2pt);` |
| Rectangle | `\draw (0,0) rectangle (3,2);` |
| Relative place | `positioning` library + `[above=of name]` |
| Arrow | `\draw[->] (a.east) -- (b.west);` |

## Hand off

- Routing -> [Diagram routing](../diagram-routing/SKILL.md)
- ISO P&ID -> [PIDcircuitTikZ](../pid-circuit-tikz/SKILL.md)
- DEXPI graph -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md)
