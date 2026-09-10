---
name: diagram-routing
description: >-
  Use first when diagram format is unclear. Mermaid for SysML; D2 for
  architecture; pyDEXPI for real P&ID; SFILES2/GGILES for graph<->string; D2 P&ID
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
| **Stakeholder architecture SVG** | **D2** | Slides / posters -- out-of-pack D2 architecture skill if installed locally |
| **Real P&ID / DEXPI topology** | **pyDEXPI** | Proteus/DEXPI -> NetworkX -- [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) (**AGPL** -- flag before proprietary redistribute) |
| **Flowsheet <-> SFILES string** | **SFILES2** | PFD/P&ID unit strings -- [SFILES 2.0](../sfiles2/SKILL.md) (MIT) |
| **General graph <-> string** | **GGILES** | Arbitrary typed NetworkX sequences -- [GGILES](../ggiles/SKILL.md) (MIT) |
| **D2 P&ID sketch** (demoted) | **D2** | Explicit non-DEXPI sketch only -- [D2 P&ID](../d2-pid/SKILL.md) |
| **Data charts** | Python | matplotlib/plotly |

SysML desk: **model -> MemNet -> Mermaid in `outputs/**` -> `mmdc`**.

P&ID desk: **DEXPI -> pyDEXPI -> graph** -> optional SFILES2/GGILES. Prefer DEXPI/pyDEXPI graph over D2 sketches; stop redraw loops without a clear target.

## Choose

| Signal | Skill |
|--------|--------|
| P&ID / DEXPI / Proteus / smart P&ID / plant graph | [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) |
| SFILES / flowsheet string / PFD tokens | [SFILES 2.0](../sfiles2/SKILL.md) |
| GGILES / graph sequence / tokenize graph string | [GGILES](../ggiles/SKILL.md) |
| Explicit "D2 P&ID sketch only" | [D2 P&ID](../d2-pid/SKILL.md) |
| SysML interconnection / IBD in report | SysML interconnection Mermaid (out-of-pack) |
| SysML behaviour in report | [Mermaid diagrams](../mermaid/SKILL.md) |
| Stakeholder architecture SVG | out-of-pack D2 architecture skill if installed locally |
| D2 sequence / ERD / export | out-of-pack D2 sequence / ERD / export skills if installed locally |
| Unclear SysML lane | SysML diagram routing (out-of-pack) |
| SysML topology from P&ID graph/string | out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally; see [SysML topology handoff](../pydexpi-p-id/references/sysml-topology-handoff.md) |

## Defaults

1. SysML / report -> Mermaid.
2. Architecture poster -> D2.
3. P&ID -> pyDEXPI; strings -> SFILES2 (flowsheet) or GGILES (general); D2 P&ID only on explicit ask.
4. Never invent parts / `link*` / instrument tags.

## CLI / install

- D2: `d2` on PATH (or local go install)
- Mermaid: `mmdc` or `npx @mermaid-js/mermaid-cli`
- pyDEXPI / SFILES2 / GGILES: venv + `pip install pydexpi` / `SFILES2` / `ggiles`
