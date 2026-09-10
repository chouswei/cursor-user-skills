---
name: chemengkg-assist
description: >-
  Use when ChemEngKG (kgtool) may assist reagent or process reasoning via
  SPARQL/graph lookup -- never invent assay or PDF locks; lecture-coding for
  patterns only, not note dumps; coordinate MemNet ingest when a process graph
  becomes working memory.
metadata:
  pattern: pipeline
  version: "1.0.0"
---
# ChemEngKG assist (reagent / process reasoning)

Use when a **Chemical Engineering Knowledge Graph** lookup could assist chemistry or process reasoning -- via [`ChemEngKG_kgtool`](https://github.com/process-intelligence-research/ChemEngKG_kgtool) (`kgtool` / `ChemKG`).

## When

- Exploring process or chemistry relationships already stored in ChemEngKG (SPARQL / graph dump).
- Uploading curated Turtle for a **non-locked** process sketch to a **dev** ChemEngKG instance.
- Contrasting KG suggestions with PDF or user-named locks (assays, design SHALLs, etc.).

## When not

- **Named assay / PDF locks** -- concentrations, stocks, optical path lengths, volumes, and similar remain **source-locked only**. The KG must **not** invent millilitres, molar absorptivities, pump maps, or reagent stocks.
- Dumping lecture notebooks from [AI-in-Bio-Chemical-Engineering-Lecture-Coding](https://github.com/process-intelligence-research/AI-in-Bio-Chemical-Engineering-Lecture-Coding) as answers -- **patterns only** (hybrid/PINN structure, GNN property-prediction workflow, ML pipeline shape).
- Treating GraphQL/`getGraph` dumps as measured laboratory data.

## Tool shape (kgtool)

```python
from kgtool.interface import ChemKG
chemkg = ChemKG(url="<graphql_api>", graph="<graph_name>")  # or ChemKG.dev() -> localhost:4001
chemkg.runSparql("SELECT * WHERE { ?s ?p ?o } LIMIT 10")
chemkg.getGraph() / getGraphs()
# curated only: uploadTurtle(...), uploadFile(path, URI)
```

Install: `pip install git+https://github.com/process-intelligence-research/ChemEngKG_kgtool`  
Backend local: see `ChemEngKG_backend` (process-intelligence-research). Responses are GraphQL `{data|errors}` dicts.

## Workflow

1. **State the lock wall** -- what is PDF or user-named locked vs open process question.
2. **Query** ChemEngKG with a tight SPARQL (limit rows); cite graph name + query.
3. **Label provenance** -- every triple is KG-assist, not assay fact.
4. **Refuse invention** -- if KG is empty or unreachable, say so; do not fabricate process edges.
5. **MemNet** -- if a chemistry process graph should become working memory, coordinate ingest via [chemistry-memnet-session](sand-workflow:chemistry-memnet-session) before forking a second source of truth.
6. **Lecture patterns** -- optional: mirror hybrid-model / GNN *structure* from lecture-coding; never paste lecture note dumps.

## Related skills

- Plant topology / P&ID graphs: [pyDEXPI P&ID](sand-workflow:pydexpi-p-id)
- Diagram format choice: [diagram-routing](sand-workflow:diagram-routing)
- Physics-consistent surrogates (not inventing assay numbers): [physics-constrained-surrogate-routing](sand-workflow:physics-constrained-surrogate-routing)

## Hard rules

- ChemEngKG assists reasoning; it does not override named PDF or user locks.
- Empty or unreachable KG -> report the gap; never invent edges or numeric SHALLs.
- Do not mint assay coefficients, path lengths, stock volumes, or pump maps from KG suggestions alone.
- Keep this skill generic -- no project, company, or lane names in the recipe.
