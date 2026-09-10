---
name: diagram-routing
description: >-
  Use first when diagram format is unclear. Mermaid for SysML; D2 for
  architecture; pyDEXPI for real P&ID; SFILES2/GGILES for graph↔string; D2 P&ID
  only if explicitly requested.
metadata:
  pattern: pipeline
  version: "1.0.1"
---
# Diagram routing

Pick one path, then open that skill. Do not invent a third text-to-diagram language unless the user named it.

## Project policy (locked)

| Lane | Tool | When |
|------|------|------|
| **In-repo SysML figures** | **Mermaid** | `outputs/**`, report fences, IBD/state/activity |
| **Stakeholder architecture SVG** | **D2** | Slides / posters — [D2 architecture](sand-workflow:d2-architecture) |
| **Real P&ID / DEXPI topology** | **pyDEXPI** | Proteus/DEXPI → NetworkX — [pyDEXPI P&ID](sand-workflow:pydexpi-p-id) (**AGPL** — flag before proprietary redistribute) |
| **Flowsheet ↔ SFILES string** | **SFILES2** | PFD/P&ID unit strings — [SFILES 2.0](sand-workflow:sfiles2) (MIT) |
| **General graph ↔ string** | **GGILES** | Arbitrary typed NetworkX sequences — [GGILES](sand-workflow:ggiles) (MIT) |
| **D2 P&ID sketch** (demoted) | **D2** | Explicit non-DEXPI sketch only — [D2 P&ID](sand-workflow:d2-pid) |
| **Data charts** | Python | matplotlib/plotly |

SysML desk: **model → MemNet → Mermaid in `outputs/**` → `mmdc`**.

P&ID desk: **DEXPI → pyDEXPI → graph** → optional SFILES2/GGILES. Prefer DEXPI/pyDEXPI graph over D2 sketches; stop redraw loops without a clear target.

## Choose

| Signal | Skill |
|--------|--------|
| P&ID / DEXPI / Proteus / smart P&ID / plant graph | [pyDEXPI P&ID](sand-workflow:pydexpi-p-id) |
| SFILES / flowsheet string / PFD tokens | [SFILES 2.0](sand-workflow:sfiles2) |
| GGILES / graph sequence / tokenize graph string | [GGILES](sand-workflow:ggiles) |
| Explicit “D2 P&ID sketch only” | [D2 P&ID](sand-workflow:d2-pid) |
| SysML interconnection / IBD in report | [SysML interconnection Mermaid](sand-workflow:sysml-interconnection-mermaid) |
| SysML behaviour in report | [Mermaid diagrams](sand-workflow:mermaid) |
| Stakeholder architecture SVG | [D2 architecture](sand-workflow:d2-architecture) |
| D2 sequence / ERD / export | [D2 sequence](sand-workflow:d2-sequence), [D2 ERD](sand-workflow:d2-erd), [D2 export](sand-workflow:d2-export) |
| Unclear SysML lane | [SysML diagram routing](sand-workflow:sysml-diagram-routing) |
| SysML topology from P&ID graph/string | [sfiles-pydexpi-sysml-bridge](sand-workflow:sfiles-pydexpi-sysml-bridge) |

## Defaults

1. SysML / report → Mermaid.
2. Architecture poster → D2.
3. P&ID → pyDEXPI; strings → SFILES2 (flowsheet) or GGILES (general); D2 P&ID only on explicit ask.
4. Never invent parts / `link*` / instrument tags.

## CLI / install

- D2: `d2` on PATH (or local go install)
- Mermaid: `mmdc` or `npx @mermaid-js/mermaid-cli`
- pyDEXPI / SFILES2 / GGILES: venv + `pip install pydexpi` / `SFILES2` / `ggiles`
