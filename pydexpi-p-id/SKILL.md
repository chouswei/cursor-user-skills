---
name: pydexpi-p-id
description: >-
  Use for real P&ID via pyDEXPI (DEXPI/Proteus -> NetworkX -> MemNet/GraphRAG).
  Prefer over D2. AGPL-3.0 -- flag before proprietary redistribute. Pair with
  SFILES2/GGILES for graph↔string.
metadata:
  pattern: pipeline
  version: "1.0.1"
---
# pyDEXPI P&ID (primary)

Real P&ID path: **DEXPI -> pyDEXPI -> NetworkX** (then MemNet / GraphRAG / optional SFILES or GGILES strings). Do **not** default to D2 glyph sketches.

Upstream: https://github.com/process-intelligence-research/pyDEXPI  
DEXPI **1.3**. Citation: Goldstein et al., ESCAPE-35 (2025), doi:10.69997/sct.139043.  
ChatP&ID (AIChE e70540) uses this stack for GraphRAG.

## Licence (hard gate)

**AGPL-3.0** (copyleft). OK for in-house / open collaboration.

**Before any proprietary or closed-source redistribute** (or AGPL-incompatible bundling): stop and flag the user / CEO -- commercial/custom licence may be needed from PI Research (`a.schweidtmann@tudelft.nl`). Do not silently ship pyDEXPI inside a closed product.

SFILES2 and GGILES are **MIT** and do not inherit this gate; pyDEXPI-derived code/binaries do.

## When

- Smart P&ID / Proteus `.xml` / DEXPI model / plant topology graph
- Once DEXPI data exists (first consumer for plant topology)
- Bounded MemNet pin maps from P&ID topology
- Optional DEXPI SVG export (`DrawDiagram`) when graphics exist in the model

## When not

- SysML deploy interconnection in `outputs/**` -> Mermaid interconnection skill
- Software architecture posters -> D2 architecture
- User stop / no clear P&ID target -> do nothing
- Classic flowsheet **string** encoding only -> [SFILES 2.0](sand-workflow:sfiles2) after you have a process graph
- Arbitrary graph↔string -> [GGILES](sand-workflow:ggiles)

## Hard rules

1. **Graph is SSOT for P&ID reasoning** -- query the graph; never dump full XML/image into the LLM context.
2. **No invention** of equipment, tags, nozzles, or lines beyond locks / DEXPI model.
3. Prefer pyDEXPI over D2. [D2 P&ID](sand-workflow:d2-pid) only on explicit non-DEXPI sketch ask.
4. AGPL flag before proprietary redistribute (see above).
5. Install in a **venv**: `python3 -m venv … && pip install pydexpi`.

## Pipeline

```python
from pydexpi.loaders import ProteusSerializer, GraphLoader, GraphAbstractor, JsonSerializer

dexpi_model = ProteusSerializer().load(directory_path, filename)

# Persist model (json or pickle serializers)
JsonSerializer().save(dexpi_model, "out", "model")

plant = GraphLoader().parse_dexpi_to_graph(dexpi_model)  # MultiDiGraph, every DexpiBaseModel as node
process = GraphAbstractor.build_process_graph(plant)     # collapse piping internals
conceptual = GraphAbstractor.build_conceptual_graph(plant)
# also: GraphAbstractor.build_complete_graph(plant)
```

Optional SVG (when DEXPI graphics present): `DrawDiagram` / `DrawRepresentationGroup` from pyDEXPI SVG loader -- not hand-rolled D2 cards.

Agent path: export a **bounded** graph slice to MemNet (equipment + piping edges + instruments) -- pin_map, never whole-file paste. Report node/edge counts; ground answers in graph ids.

Downstream strings:

- Process flowsheet vocabulary -> [SFILES 2.0](sand-workflow:sfiles2)
- Custom typed graphs -> [GGILES](sand-workflow:ggiles)

## Features checklist (deepen)

| Capability | Module / note |
|------------|----------------|
| Pydantic DEXPI classes | `pydexpi.dexpi_classes` |
| Proteus XML load | `ProteusSerializer` (drawing info often not fully parsed) |
| JSON / pickle serialize | `JsonSerializer` / `PickleSerializer` |
| Full / process / conceptual graphs | `GraphLoader` + `GraphAbstractor` |
| SVG export | `SvgRenderer`, `DrawDiagram`, … |
| Synthetic P&ID | upstream generative helpers (only if asked) |

## Related

- DEXPI2graphML (TUDoAD) -- alternate GraphML export
- ChatP&ID -- GraphRAG on DEXPI graphs
- LLM-CodeGen-Image -- examples only, not runtime

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

- Routing -> [Diagram routing](sand-workflow:diagram-routing)
- SFILES string -> [SFILES 2.0](sand-workflow:sfiles2)
- General sequence -> [GGILES](sand-workflow:ggiles)
- SysML topology mapping -> [sfiles-pydexpi-sysml-bridge](sand-workflow:sfiles-pydexpi-sysml-bridge)
- D2 sketch only -> [D2 P&ID](sand-workflow:d2-pid) (demoted)

## Refs

- [STACK.md](references/STACK.md)
