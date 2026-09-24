---
name: diagram-routing
description: >-
  Use first when diagram format is unclear. Mermaid for SysML; D2 for
  architecture posters only (never P&ID); pyDEXPI for real P&ID topology;
  SFILES2/GGILES for graph<->string; PIDcircuitTikZ for LaTeX ISO 14617 drawings;
  TikZ for general LaTeX figures.
metadata:
  pattern: pipeline
  version: "1.0.3"
---
# Diagram routing

Pick one path, then open that skill. Do not invent a third text-to-diagram language unless the user named it.

## Project policy (locked)

| Lane | Tool | When |
|------|------|------|
| **In-repo SysML figures** | **Mermaid** | `outputs/**`, report fences, IBD/state/activity |
| **Stakeholder architecture SVG** | **D2** | Slides / posters -- out-of-pack D2 architecture skill if installed locally; **never P&ID** |
| **Real P&ID / DEXPI topology** | **pyDEXPI** | Proteus/DEXPI -> NetworkX -- [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) (**AGPL** -- flag before proprietary redistribute) |
| **Flowsheet <-> SFILES string** | **SFILES2** | PFD/P&ID unit strings -- [SFILES 2.0](../sfiles2/SKILL.md) (MIT) |
| **General graph <-> string** | **GGILES** | Arbitrary typed NetworkX sequences -- [GGILES](../ggiles/SKILL.md) (MIT) |
| **LaTeX ISO 14617 P&ID drawing** | **PIDcircuitTikZ** | Publication TeX/PDF glyphs -- [pid-circuit-tikz](../pid-circuit-tikz/SKILL.md) (MIT); topology SSOT stays pyDEXPI |
| **General TikZ figure** | **TikZ** | Non-P&ID LaTeX graphics -- [tikz](../tikz/SKILL.md) |
| **Do not: D2 for P&ID** | -- | Wrong tool. Use pyDEXPI (topology) or PIDcircuitTikZ (LaTeX ISO drawing) or SFILES2/GGILES (strings). Anti-pattern stub: [d2-pid](../d2-pid/SKILL.md) |
| **Data charts** | Python | matplotlib/plotly |

SysML desk: **model -> MemNet -> Mermaid in `outputs/**` -> `mmdc`**.

P&ID desk: **DEXPI -> pyDEXPI -> graph** (SSOT) -> optional SFILES2/GGILES; LaTeX ISO drawing -> PIDcircuitTikZ. Never D2 for P&ID; stop redraw loops without a clear target.

## Choose

| Signal | Skill |
|--------|--------|
| P&ID / DEXPI / Proteus / smart P&ID / plant graph | [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) |
| SFILES / flowsheet string / PFD tokens | [SFILES 2.0](../sfiles2/SKILL.md) |
| GGILES / graph sequence / tokenize graph string | [GGILES](../ggiles/SKILL.md) |
| TikZ P&ID / ISO 14617 / PIDcircuitTikZ | [pid-circuit-tikz](../pid-circuit-tikz/SKILL.md) |
| TikZ / PGF / Overleaf (non-P&ID) | [tikz](../tikz/SKILL.md) |
| User asks for "D2 P&ID" / D2 plant sketch | **Refuse / redirect** to [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) (topology) or [pid-circuit-tikz](../pid-circuit-tikz/SKILL.md) (LaTeX ISO). Cite [d2-pid](../d2-pid/SKILL.md) only as anti-pattern docs |
| SysML interconnection / IBD in report | SysML interconnection Mermaid (out-of-pack) |
| SysML behaviour in report | [Mermaid diagrams](../mermaid/SKILL.md) |
| Architecture SVG / stakeholder poster | D2 architecture (out-of-pack) or local D2 skill |
| SysML from P&ID graph | out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally; see [SysML topology handoff](../pydexpi-p-id/references/sysml-topology-handoff.md) |

## Defaults

1. SysML / report -> Mermaid.
2. Architecture poster -> D2 (**never P&ID**).
3. P&ID topology -> pyDEXPI; LaTeX ISO drawing -> PIDcircuitTikZ; strings -> SFILES2/GGILES; **never D2 for P&ID**.
4. Never invent parts / instrument tags.

## CLI / install

- D2 on PATH -- architecture only
- Mermaid: `mmdc` or `npx @mermaid-js/mermaid-cli`
- pyDEXPI / SFILES2 / GGILES: venv + pip (see each skill)
- PIDcircuitTikZ / TikZ: TeX Live + libs under `pid-circuit-tikz/lib/`
