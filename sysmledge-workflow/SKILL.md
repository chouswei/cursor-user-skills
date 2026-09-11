---
name: sysmledge-workflow
description: >-
  SysMLEdge day loop when the author SSOT is sysml-models/: edit the SysML tree,
  wait for a human whole-tree Save, then query the MemNet projection via GQL;
  implement allocated work from that live model; agents propose SysML only.
  STALE: show it and refuse live-SSOT pretence. Triggers: sysmledge workflow,
  sysml edge, SysMLEdge, STALE sysml, sysml propose, gql_read, rev_status,
  reproject. Skip: Mermaid or D2 viz-only; Kuzu, Cypher, or graph.kuzu.
metadata:
  pattern: pipeline
  version: "1.0"
  domain: sysml
  pairs_with: [sysml-modeling-workflow, sysml-gql, mcp-memnet, sysml-new-project, mcp-sysml-v2, mcp-sysmledgraph]
token_guardrails: |
  - Engine is MemNet + GQL. MUST NOT use Kuzu, Cypher, or graph.kuzu.
  - Agents propose only under sysml-models/proposals/<id>/. MUST NOT silently overwrite sysml-models/ SSOT.
  - STALE: show rev.stale; refuse live-SSOT pretence. staleOk is read-only. propose while STALE is refused unless base.sha + human rebase.
  - GQL MUST NOT invent parts, ports, connections, or PLM ids. Bounded reads; no full-tree dump as the only merge story.
  - Load references/day-loop.md for STALE error shape and proposal file rules.
pipeline_steps:
  1. Bind tree
     - Confirm model root is sysml-models/ (or repo AGENTS.md). Call rev_status. If STALE, show it; do not pretend the graph is current.
  2. Edit or read
     - Edit SysML under sysml-models/ as text. Syntax check via mcp-sysml-v2 is allowed. Do not treat GQL as SSOT.
  3. Human Save
     - Whole-tree Save is a human/operator action. MCP MUST NOT save or import silently. After Save, projection binds rev.sha.
  4. GQL
     - When not STALE (or with staleOk on read-only): gql_read, gql_context, gql_impact, list_scope. Every structure answer includes rev.sha and rev.stale.
  5. Implement
     - Implement allocated parts/code from the saved SysML + live GQL. Do not write the graph back as the model.
  6. Propose only
     - SysML changes the agent does not own as SSOT go to propose -> sysml-models/proposals/<id>/{PATCH.md, delta.sysml}.
  7. Self-check
     - STALE shown if true; no Kuzu; no silent SSOT write; proposal has base.sha.
system_instruction: |
  Concise British English. ASCII in skill prose. SysML is author SSOT; MemNet/GQL is the trail.
  Agents propose; humans save. Intermediate steps stay short. JSON only at tool boundaries.
---

# SysMLEdge day loop

**When:** The open system uses **SysMLEdge** with author SSOT under **`sysml-models/`**. Not for Mermaid/D2 viz-only. Not for the abandoned Kuzu `sysmledgraph` stack.

**Pairing:** Textual modeling sequence stays [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md). Working-memory GQL shape: [sysml-gql](../sysml-gql/SKILL.md). MemNet tools: [mcp-memnet](../mcp-memnet/SKILL.md). Greenfield tree: [sysml-new-project](../sysml-new-project/SKILL.md). Old MCP name: [mcp-sysmledgraph](../mcp-sysmledgraph/SKILL.md) (retarget only).

**Contracts (normative, do not paste):** [P0-contracts.md](https://github.com/chouswei/SysMLEdge/blob/main/docs/P0-contracts.md), [P1-acceptance.md](https://github.com/chouswei/SysMLEdge/blob/main/docs/P1-acceptance.md), [SysMLEdge AGENTS.md](https://github.com/chouswei/SysMLEdge/blob/main/AGENTS.md).

## Day loop

```text
edit sysml-models/  ->  human Save (whole tree)  ->  MCP GQL  ->  implement  ->  agent propose only
```

| Step | Who | MUST |
|------|------|------|
| Edit | Agent or human | Change `.sysml` under `sysml-models/`. `proposals/` is not SSOT. |
| Save | Human | Whole-tree overwrite of current + git commit. MCP MUST NOT call this silently. |
| GQL | Agent | Query the MemNet projection bound to `rev.sha`. `graph = model @ rev`. |
| Implement | Agent | Code / `parts/**` from saved SysML. Never serve GQL/MemNet dumps as the model. |
| Propose | Agent | `propose` writes only `sysml-models/proposals/<id>/{PATCH.md, delta.sysml}`. |

**Invariant:** `graph = model @ <rev.sha>`. If the projection cannot name a SHA, fail closed.

## STALE

**STALE** means bound `rev.sha` is not the SHA of **current**.

| Gate | MUST |
|------|------|
| Show | Surface STALE on any structure read. Do not hide it. |
| Live-SSOT pretence | Refuse. Do not call STALE GQL "the current model", "HEAD", or "what is saved". |
| `staleOk` | Read-only. With `staleOk=true`, return the bound-rev projection **and** `rev.stale=true`. Default `staleOk=false`: structure read fails with `code: STALE`. |
| Propose while STALE | Refuse unless the proposal declares `base.sha` **and** a human rebases. `staleOk` does not unlock `propose`. |

Error shape and proposal file rules: [references/day-loop.md](references/day-loop.md).

## P0 MCP tools

Query language is **GQL** against **MemNet**. Resume the *roles* of the old path-index MCP; do not resume Cypher or `graph.kuzu`.

| Tool | Mutates SSOT? | Behaviour |
|------|----------------|-----------|
| `rev_status` | No | `current.sha`, `rev.sha`, `rev.stale`. |
| `gql_read` | No | Bounded GQL read. Needs `staleOk=true` when STALE, else STALE error. |
| `gql_context` | No | Neighbourhood of one qname/path (part/port/connection). Same STALE rules. |
| `gql_impact` | No | Upstream/downstream along mapped connections. Same STALE rules. |
| `list_scope` | No | Indexed project roots / package qnames in the bound projection. |
| `propose` | No (SSOT) | Write only under `sysml-models/proposals/<id>/`. Returns path + `base.sha`. |
| `reproject` | No (SSOT) | Rebuild MemNet from **current** SysML. Human or privileged operator. Agents MAY request; MUST NOT pretend the graph is SSOT. |

**Forbidden on MCP:** silent overwrite of `sysml-models/` SSOT; unattended `save` / `import` / `download`; graph write-back as SSOT; unbounded full-tree dump as the only merge story; Cypher / Kuzu / `graph.kuzu`; `mutate` that adds structure not in SysML at `rev.sha`.

Rename is a **proposal** (`delta.sysml` + `PATCH.md`), not a graph edit.

## Agent proposal path

```text
sysml-models/proposals/<id>/
  PATCH.md      # intent, base.sha, affected qnames
  delta.sysml   # SysML delta; not GQL, Cypher, or a MemNet snapshot
```

Stub: [assets/proposal-stub.md](assets/proposal-stub.md). Human apply: merge `delta.sysml` into the tree, then **Save**. There is no "apply GQL to SSOT".

## Engine

| Live | Refuse |
|------|--------|
| MemNet + GQL | Kuzu, Cypher, `graph.kuzu`, long-lived Kuzu worker |
| SysML zip / `sysml-models/` as downloadable source | Serving the graph as downloadable source |
| v1 map: part, port, connection, `partNumber`, ClickUp/Inventree ids when present in SysML | Invented qnames, packages, requirements, actions, allocations, or PLM placeholders |

## See also

- STALE + propose detail: [references/day-loop.md](references/day-loop.md)
- Modeling hub: [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md)
- Abandoned Kuzu MCP retarget: [mcp-sysmledgraph](../mcp-sysmledgraph/SKILL.md)
