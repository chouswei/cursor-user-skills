---
name: chemengkg-assist
description: >-
  Use when ChemEngKG (kgtool) may assist reagent/process reasoning --
  SPARQL/graph assist only; never invent user/PDF-locked assay coefficients;
  lecture-coding for patterns not note dumps; optional MemNet via memnet-use (no
  Layer pipe).
metadata:
  pattern: pipeline
  version: "1.0.1"
---
# ChemEngKG assist (reagent / process reasoning)

Use when a **Chemical Engineering Knowledge Graph** lookup could assist chem/process reasoning -- via [ChemEngKG_kgtool](https://github.com/process-intelligence-research/ChemEngKG_kgtool) (kgtool / ChemKG).

## When

- Exploring process/chem relationships already stored in ChemEngKG (SPARQL / graph dump).
- Uploading curated Turtle for a **non-locked** process sketch to a **dev** ChemEngKG instance.
- Contrasting KG suggestions with **user- or PDF-locked** assay / process numbers.

## When not

- **Locked chem / assay numbers** -- concentrations, stocks, UV path length, volumes, and similar stay **user/PDF-locked only**. KG must **not** invent mL, epsilon, pump maps, or reagent stocks.
- Dumping lecture notebooks from [AI-in-Bio-Chemical-Engineering-Lecture-Coding](https://github.com/process-intelligence-research/AI-in-Bio-Chemical-Engineering-Lecture-Coding) as answers -- **patterns only** (hybrid/PINN structure, GNN property-prediction workflow, ML pipeline shape).
- Treating GraphQL/getGraph dumps as measured lab data.
- Naming customer / company / lane projects inside this skill -- keep tooling generic.

## Tool shape (kgtool)

from kgtool.interface import ChemKG
chemkg = ChemKG(url="<graphql_api>", graph="<graph_name>")  # or ChemKG.dev() -> localhost:4001
chemkg.runSparql("SELECT * WHERE { ?s ?p ?o } LIMIT 10")

Install: pip install git+https://github.com/process-intelligence-research/ChemEngKG_kgtool
Backend local: see ChemEngKG_backend. Responses are GraphQL {data|errors} dicts.

## Pipeline

1. **State the lock wall** -- what is user/PDF locked vs open process question.
2. **Query** ChemEngKG with a tight SPARQL (limit rows); cite graph name + query.
3. **Label provenance** -- every triple is KG-assist, not assay fact.
4. **Refuse invention** -- if KG is empty/unreachable, say so; do not fabricate process edges.
5. **Optional MemNet landing** -- if the user wants durable working memory, use pack MemNet skills (memnet-use / mcp-memnet): cue -> pin_map -> sparse mutate; no Layer pipe; do not silently fork a second SSOT.
6. **Lecture patterns** -- optional: mirror hybrid-model / GNN structure from lecture-coding; never paste lecture note dumps.

## Related

- P&ID / DEXPI graphs: pydexpi-p-id (prefer over demoted d2-pid)
- Physics-consistent surrogates: physics-constrained-surrogate-routing

## Emit shape

- Query + graph name + row budget
- Provenance label (KG-assist vs lock)
- Gaps / empty / errors honestly
- Firewall: no invented locked coefficients

## Quality bar

- Generic tooling only; no project / lane names in the recipe
- ASCII in LLM English (--, ->)
- British English
