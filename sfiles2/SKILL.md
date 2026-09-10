---
name: sfiles2
description: >-
  Use when converting PFD/P&ID flowsheets to/from SFILES 2.0 strings (NetworkX ↔
  SFILES). Prefer pyDEXPI for DEXPI/smart P&ID SSOT; GGILES for non-flowsheet
  graphs. MIT.
metadata:
  pattern: tool-wrapper
  version: "1.0"
---
# SFILES 2.0

Convert **PFD / P&ID flowsheets ↔ SFILES 2.0 strings** (and NetworkX), via TU Delft Process Intelligence Research.

Upstream: https://github.com/process-intelligence-research/SFILES2  
Paper: Vogel et al., *SFILES 2.0: an extended text-based flowsheet representation* (Optimization and Engineering, 2023).  
Licence: **MIT**. Package: `pip install SFILES2` (import path `Flowsheet_Class.flowsheet`).

## When

- Compact text/token representation of a process flowsheet (PFD or simplified P&ID)
- Round-trip: SFILES string ↔ NetworkX `MultiDiGraph`
- ML / LLM context cheaper than XML or images
- After a process-level graph exists (often from [pyDEXPI P&ID](sand-workflow:pydexpi-p-id)), encode topology as SFILES

## When not

- Full DEXPI smart P&ID SSOT -> [pyDEXPI P&ID](sand-workflow:pydexpi-p-id)
- Arbitrary non-flowsheet graphs -> [GGILES](sand-workflow:ggiles)
- SysML report -> Mermaid; architecture posters -> D2
- No clear target / user halt on P&ID redraws -> stop

## Hard rules

1. Prefer **DEXPI graph (pyDEXPI)** as topology SSOT when Proteus/DEXPI exists; SFILES is a **derived** string view.
2. Do not invent unit tags or streams beyond locks / graph / SFILES input.
3. Use `version="v2"` unless legacy v1 is required.
4. Install in a **venv**, not system pip.
5. D2 glyph sketches remain demoted.

## Pipeline

```python
from Flowsheet_Class.flowsheet import Flowsheet

fs = Flowsheet()
fs.create_from_sfiles("(raw)(hex)(prod)")  # must be valid SFILES
G = fs.state  # nx.MultiDiGraph

fs2 = Flowsheet(OntoCapeConformity=True)
fs2.create_from_nx(G)
fs2.convert_to_sfiles(version="v2", canonical=True)
s = fs2.sfiles
```

Also: `sfiles_list` tokens; GraphML via `Flowsheet(xml_file=...)`; upstream demos `run_demonstration.py` / `demonstration.ipynb`.

## Stack

1. DEXPI -> [pyDEXPI P&ID](sand-workflow:pydexpi-p-id) -> NetworkX  
2. Process-level string -> **SFILES 2.0** (this skill)  
3. Custom-typed graphs -> [GGILES](sand-workflow:ggiles)  
4. Never default to [D2 P&ID](sand-workflow:d2-pid)

Prefer DEXPI/pyDEXPI graph over D2 sketches; stop redraw loops without a clear target.

## SysML mapping (handoff)

Topology from this stack is **evidence** for the product SysML model. Structural SSOT stays **SysML v2 `.sysml`**.

| Graph / string element | Lands in SysML as | If missing in model |
|------------------------|-------------------|---------------------|
| Equipment / instrument node | existing `part` (+ ports) | **gap** -- do not invent equipment |
| Piping / process edge | `port` + `item`/`flow` + `connection`/`bind` | gap / ISSUE |
| Signal / control edge | ports + connections per locks | gap |
| SFILES / GGILES token only | same after decode to graph | never invent from string alone |

**Locks win** (user/PDF-named topology and assay locks). Conflict with locks -> **contradict** if `.sysml` does the opposite, else gap.

Owner of the landing: [sfiles-pydexpi-sysml-bridge](sand-workflow:sfiles-pydexpi-sysml-bridge) (Sysmler). Diagram owns load/encode/draw; SysML owner edits `.sysml` and reviews this section. Prefer conceptual/process graph over complete DEXPI for SoI wiring. No invented mL/λ/size. MemNet delta only **after** `.sysml` validate -- do not treat NetworkX as MemNet SSOT.

## Hand off

- SysML topology mapping -> [sfiles-pydexpi-sysml-bridge](sand-workflow:sfiles-pydexpi-sysml-bridge)
- Routing -> [Diagram routing](sand-workflow:diagram-routing)
- DEXPI -> [pyDEXPI P&ID](sand-workflow:pydexpi-p-id)
- General graph↔string -> [GGILES](sand-workflow:ggiles)

## Refs

- [STACK.md](references/STACK.md)
