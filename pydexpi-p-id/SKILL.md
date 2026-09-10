---
name: pydexpi-p-id
description: >-
  Use for real P&ID via pyDEXPI (DEXPI/Proteus -> NetworkX -> MemNet/GraphRAG).
  Never use D2 for P&ID (anti-pattern d2-pid). AGPL-3.0 -- flag before
  proprietary redistribute. Pair with SFILES2/GGILES for graph<->string.
metadata:
  pattern: pipeline
  version: "1.0.2"
---
# pyDEXPI P&ID (primary)

Real P&ID path: **DEXPI -> pyDEXPI -> NetworkX** (then MemNet / GraphRAG / optional SFILES or GGILES strings). **Never** draw P&ID in D2 (anti-pattern skill [d2-pid](../d2-pid/SKILL.md)).

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

- SysML deploy interconnection in `outputs/**` -> SysML interconnection Mermaid (out-of-pack)
- Software architecture posters -> out-of-pack D2 architecture skill if installed locally
- User stop / no clear P&ID target -> do nothing
- Classic flowsheet **string** encoding only -> [SFILES 2.0](../sfiles2/SKILL.md) after you have a process graph
- Arbitrary graph<->string -> [GGILES](../ggiles/SKILL.md)

## Hard rules

1. **Graph is SSOT for P&ID reasoning** -- query the graph; never dump full XML/image into the LLM context.
2. **No invention** of equipment, tags, nozzles, or lines beyond locks / DEXPI model.
3. **Never** use D2 for P&ID. If asked for D2 P&ID, refuse/redirect here; cite [d2-pid](../d2-pid/SKILL.md) only as anti-pattern docs.
4. AGPL flag before proprietary redistribute (see above).
5. Install in a **venv**: `python3 -m venv .venv && .venv/bin/pip install pydexpi`.

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

- Process flowsheet vocabulary -> [SFILES 2.0](../sfiles2/SKILL.md)
- Custom typed graphs -> [GGILES](../ggiles/SKILL.md)

## Features checklist (deepen)

| Capability | Module / note |
|------------|----------------|
| Pydantic DEXPI classes | `pydexpi.dexpi_classes` |
| Proteus XML load | `ProteusSerializer` (drawing info often not fully parsed) |
| JSON / pickle serialize | `JsonSerializer` / `PickleSerializer` |
| Full / process / conceptual graphs | `GraphLoader` + `GraphAbstractor` |
| SVG export | `SvgRenderer`, `DrawDiagram`, ... |
| Synthetic P&ID | upstream generative helpers (only if asked) |

## Related

- DEXPI2graphML (TUDoAD) -- alternate GraphML export
- ChatP&ID -- GraphRAG on DEXPI graphs
- LLM-CodeGen-Image -- examples only, not runtime

## SysML mapping (handoff)

See shared mapping: [sysml-topology-handoff.md](references/sysml-topology-handoff.md).

SysML topology landing is owned by the SysML specialist (out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally). Diagram owns load/encode/draw; SysML owner edits `.sysml`.

## Hand off

- Routing -> [Diagram routing](../diagram-routing/SKILL.md)
- SFILES string -> [SFILES 2.0](../sfiles2/SKILL.md)
- General sequence -> [GGILES](../ggiles/SKILL.md)
- SysML topology mapping -> [sysml-topology-handoff.md](references/sysml-topology-handoff.md) (out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally)
- Asked for D2 P&ID -> refuse; stay on this skill (or SFILES2/GGILES for strings). Anti-pattern docs only: [d2-pid](../d2-pid/SKILL.md)

## Refs

- [STACK.md](references/STACK.md)
