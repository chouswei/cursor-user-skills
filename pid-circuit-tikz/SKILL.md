---
name: pid-circuit-tikz
description: >-
  Use when drawing ISO 14617 P&ID symbols in LaTeX with PIDcircuitTikZ (TikZ
  circuits.pid). Prefer pyDEXPI for topology SSOT; never D2 for P&ID. MIT.
---
# PIDcircuitTikZ

Draw **ISO 14617** P&ID symbols in LaTeX via TikZ `circuits.pid` / `circuits.pid.ISO14617`.

Upstream: https://github.com/jellespijker/PIDcircuitTikZ  
License: **MIT**.

## Role vs other P&ID tools

| Need | Skill |
|------|--------|
| Topology SSOT / Proteus / GraphRAG | [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) (**primary**) |
| Flowsheet <-> string | [SFILES 2.0](../sfiles2/SKILL.md) / [GGILES](../ggiles/SKILL.md) |
| LaTeX / PDF drawing with ISO 14617 glyphs | **This skill** |
| D2 plant sketch | **Refuse** -- [d2-pid](../d2-pid/SKILL.md) anti-pattern |

Prefer **DEXPI graph** for reasoning; use this when the user wants a **TeX/PDF symbol drawing**. Do not invent tags beyond locks / graph.

## When

- TikZ P&ID, ISO 14617 symbols, or PIDcircuitTikZ by name
- Deliverable is `.tex` + PDF with standard process glyphs
- Annotating known topology (locks or pyDEXPI graph) as a publication figure

## When not

- No clear target / halt redraw spam -> stop
- Machine-readable plant graph -> pyDEXPI first
- Architecture posters -> D2; SysML report -> Mermaid

## Install

Copy next to the main `.tex` (or into `$TEXMFHOME/tex/latex/PIDcircuitTikz/`):

- `tikzlibrarycircuits.pid.code.tex`
- `tikzlibrarycircuits.pid.ISO14617.code.tex`
- `pgflibraryshapes.gates.pid.code.tex`
- `pgflibraryshapes.gates.pid.ISO14617.code.tex`

Vendored with this skill: `lib/` (same four files).

## Minimal example

```latex
\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{circuits}
\usetikzlibrary{circuits.pid.ISO14617}
\usetikzlibrary{positioning,calc}

\begin{document}
\begin{tikzpicture}[
  circuit pid ISO14617,
  every info/.style={font=\tiny}
]
  \draw (0,0)
    to [pump={name=P1,info=$P_1$}] (2,0)
    to [valve={name=V1,info'=$V_1$}] (4,0)
    to [tank={name=T1}] (5,0);
  \node[turning actuator, at={V1.center}{1}]{};
\end{tikzpicture}
\end{document}
```

Style: `circuit pid ISO14617`. Path: `\draw ... to [pump=...] ...;`. Attach actuators with `\node[turning actuator, at={V1.center}{1}]{};`.

## Coverage

ISO 14617 parts 1-15 (connections, actuators, measurement, valves, pumps, heat, separation, ...). Catalog: upstream `example.tex` / `PIDcircuitTikZ.pdf`. Missing symbol -> extend library; do not fake with D2 boxes.

## Hard rules

1. Locks / pyDEXPI graph are SSOT -- TikZ is a **drawing**.
2. No invented equipment, tags, or setpoints.
3. Name components (`name=...`) so instruments/actuators can attach.
4. One clear figure pass; no redraw spam without a named delta.
5. If `pdflatex` missing, deliver `.tex` + library file list.

## Compile

```bash
pdflatex -interaction=nonstopmode figure.tex
```

## Hand off

- Routing -> [Diagram routing](../diagram-routing/SKILL.md)
- General TikZ -> [TikZ](../tikz/SKILL.md)
- DEXPI -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md)
- SysML from graph -> out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally; see [SysML topology handoff](../pydexpi-p-id/references/sysml-topology-handoff.md)

## Refs

- `lib/` (vendored PIDcircuitTikZ libraries)
- `references/STACK.md`
