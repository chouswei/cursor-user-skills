---
name: ggiles
description: >-
  Use when converting NetworkX graphs to/from GGILES sequential strings
  (generalized SFILES). Prefer SFILES2 for classic PFD/P&ID unit strings;
  pyDEXPI for DEXPI SSOT. MIT.
metadata:
  pattern: tool-wrapper
  version: "1.0.1"
---
# GGILES

**Generalized Graph Input Line Entry System** -- NetworkX graph <-> sequential string (SFILES generalized beyond flowsheets).

Upstream: https://github.com/process-intelligence-research/Generalized-graph-line-entry-system  
PyPI: `pip install ggiles`  
Licence: **MIT**.

## When

- Need graph<->string for **arbitrary** typed NetworkX graphs (not only chemical flowsheets)
- Canonical sequences via graph invariants; tokenization for ML
- Bridging a pyDEXPI / custom process graph into a compact string when SFILES unit vocabulary does not fit

## When not

- Classic PFD/P&ID unit strings with SFILES vocabulary -> prefer [SFILES 2.0](../sfiles2/SKILL.md)
- DEXPI load / plant SSOT -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md)
- Architecture posters -> out-of-pack D2 architecture skill if installed locally; SysML report -> Mermaid

## Hard rules

1. Same converter settings must be used for `graph_to_sequence` and `sequence_to_graph` (and matching `GGILESTokenizer` config).
2. Do not invent node/edge types or attributes beyond the source graph.
3. Install in a **venv**.
4. Useful alongside pyDEXPI graphs; does not replace DEXPI.

## Pipeline

```python
import networkx as nx
from ggiles.graph_invariant import GraphInvariantProcessor, MorganAlgorithm, AlphabeticNodeOrdering
from ggiles import make_converter, GGILESTokenizer, GraphTokenConfig
from ggiles.attribute_encoding import AttributeConfig

G = nx.DiGraph()
# ... nodes/edges with type (and optional attributes) ...

invariant = GraphInvariantProcessor(layers=[MorganAlgorithm(), AlphabeticNodeOrdering("type")])
attr_config = AttributeConfig(node_attributes=["id"])  # optional
token_config = GraphTokenConfig()  # customize node_type_attribute / default_edge_type as needed

conv = make_converter(invariant=invariant, attribute_config=attr_config, graph_token_config=token_config)
seq = conv.graph_to_sequence(G)
G2 = conv.sequence_to_graph(seq)

tokens = GGILESTokenizer().tokenize(seq)
```

Markers (from upstream docs): `v(.)` node, `e(.)` edge, `[.]` branch, `<&|.&.|` converge, cycles `1.<1`, `|n` new subgraph.

## Stack position

pyDEXPI plant/process graph -> (optional) abstract -> **GGILES** when you need a general sequence; use **SFILES2** when the domain is standard flowsheet units.

Prefer DEXPI/pyDEXPI graph over D2 sketches; stop redraw loops without a clear target.

## SysML mapping (handoff)

See shared mapping: [sysml-topology-handoff.md](../pydexpi-p-id/references/sysml-topology-handoff.md).

SysML topology landing is owned by the SysML specialist (out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally). Diagram owns load/encode/draw; SysML owner edits `.sysml`.

## Hand off

- SysML topology mapping -> [sysml-topology-handoff.md](../pydexpi-p-id/references/sysml-topology-handoff.md) (out-of-pack bridge skill `sfiles-pydexpi-sysml-bridge` when present locally)
- Flowsheet SFILES -> [SFILES 2.0](../sfiles2/SKILL.md)
- DEXPI -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md)
- Routing -> [Diagram routing](../diagram-routing/SKILL.md)

## Refs

- [STACK.md](references/STACK.md)
