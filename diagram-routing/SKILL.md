---
name: diagram-routing
description: >-
  Use first when diagram format is unclear. Mermaid for SysML; D2 for
  architecture posters only (never P&ID); pyDEXPI for real P&ID; SFILES2/GGILES
  for graph<->string.
metadata:
  pattern: pipeline
  version: "1.0.2"
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
| **Do not: D2 for P&ID** | -- | Wrong tool. Use pyDEXPI (or SFILES2/GGILES for strings). Anti-pattern stub: [d2-pid](../d2-pid/SKILL.md) |
| **Data charts** | Python | matplotlib/plotly |

SysML desk: **model -> MemNet -> Mermaid in `outputs/**` -> `mmdc`**.

P&ID desk: **DEXPI -> pyDEXPI -> graph** -> optional SFILES2/GGILES. Never D2 for P&ID; stop redraw loops without a clear target.

## Choose

| Signal | Skill |
|--------|--------|
| P&ID / DEXPI / Proteus / smart P&ID / plant graph | [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) |
| SFILES / flowsheet string / PFD tokens | [SFILES 2.0](../sfiles2/SKILL.md) |
| GGILES / graph sequence / tokenize graph string | [GGILES](../ggiles/SKILL.md) |
| User asks for "D2 P&ID" / D2 plant sketch | **Refuse / redirect** to [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) (or SFILES2/GGILES for strings). Cite [d2-pid](../d2-pid/SKILL.md) only as anti-pattern docs (what not to do) |
| SysML interconnection / IBD in report | SysML interconnection Mermaid (out-of-pack) |
| SysML behaviour in report | [Mermaid diagrams](../mermaid/SKILL.md) |
| Stakeholder architecture SVG | out-of-pack D2 architecture skill if installed locally |
| D2 sequence / ERD / export | out-of-pack D2 sequence / ERD / export skills if installed locally |
| Unclear SysML lane | SysML diagram routing (out-of-pack) |
| SysML topology from P&ID graph/string | out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally; see [SysML topology handoff](../pydexpi-p-id/references/sysml-topology-handoff.md) |

## Defaults

1. SysML / report -> Mermaid.
2. Architecture poster -> D2 (architecture only; never P&ID).
3. P&ID -> pyDEXPI only; strings -> SFILES2 (flowsheet) or GGILES (general); **never D2** for P&ID.
4. Never invent parts / `link*` / instrument tags.

## CLI / install

- D2: `d2` on PATH (or local go install) -- architecture posters only
- Mermaid: `mmdc` or `npx @mermaid-js/mermaid-cli`
- pyDEXPI / SFILES2 / GGILES: venv + `pip install pydexpi` / `SFILES2` / `ggiles`
