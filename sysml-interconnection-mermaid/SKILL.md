---
name: sysml-interconnection-mermaid
description: >-
  Build deployment-aligned interconnection Mermaid flowcharts in outputs (system-design-report,
  interconnection view, IBD-style wiring). MemNet TSK_diagram graph first, typedBy intent split,
  placement-by-degree (rank_span, barycenter), materialise to .md, mmdc validate. Use when drawing
  interconnection view, edgeSide/L2/power figures, or wiring diagrams from deploy connection link*.
metadata:
  pattern: pipeline
  version: 1.0
  domain: sysml
  pairs_with: [sysml-memnet-documentation, mermaid, mmdc, sysml-view-doc-sync, sysml-modeling-workflow]
---

# SysML interconnection view (Mermaid)

**Audience:** LLM editing **`outputs/**/*.md`** interconnection / wiring **flowcharts** from **`deploy-*.sysml`**.

**Source of truth:** model (`part`, `connection link*`, nested PCBA `link*`) — never invent nodes or links in `.md` alone.

---

## When to use

| User intent | This skill |
|-------------|------------|
| Interconnection view, wiring diagram, IBD-style deploy figure | **Yes** — primary |
| Behaviour sequence / state machine | **No** — [mermaid](../mermaid/SKILL.md) behaviour refs |
| SysML MCP preview / validate only | **No** — [mcp-sysml-v2](../mcp-sysml-v2/SKILL.md) |
| Full report section prose + tables | Pair [sysml-view-doc-sync](../sysml-view-doc-sync/SKILL.md) |

---

## Skill stack (load order)

1. **`sysml-modeling-workflow`** — if `.sysml` also changes this turn
2. **`sysml-memnet-documentation`** — `TSK_diagram_*` wire, `typedBy`, `figure_includes` / `figure_uses`
3. **This skill** — interconnection pipeline below
4. **`mmdc`** — validate fenced blocks in section `.md` before done

Serve down: TRON `DiagramPlan` per [mermaid-placement-by-degree](../mermaid/references/mermaid-placement-by-degree.md) § Serve down; backfill MemNet before materialise.

---

## Pipeline (mandatory)

```text
1. Inventory   config.yaml deployment_part → rg "connection link" in deploy-*.sysml
2. Classify    typedBy / intent bucket per link (L2, power, control, field) — p0:types
3. Split       one intent family per figure (≤6 nodes, hub degree ≤6) — split gate
4. Scope       MemNet TSK_diagram_<figureId> — figure_includes / figure_uses — p1:scope
5. Place       anchor, ranks, mates, lanes, rank_span audit — p2 / p2b / p2c
6. Edge order  spokes → chains → chords → uplinks — p3:edges
7. Materialise patch section .md (%% figure-id); legend + Connections table — p4
8. Validate    mmdc -i <section>.md — p5:review (max 2 layout iterations on graph only)
```

**Rule:** Steps 1–6 touch **MemNet only** (or TRON in-prompt). Do **not** hand-edit fenced ` ```mermaid ` until pre-materialise gate passes.

On layout failure: rewind **p2/p3** on graph — never patch crossings in `.md`.

---

## Figure rules (summary)

| Rule | Detail |
|------|--------|
| **Nodes** | Part **usage** names from deploy (`gs305EP`, `relayChainPcba`, …) |
| **Edges** | Short canvas token (`P1`, `24 V`, `HDMI`); full `link*` in legend or table |
| **Labels** | ASCII, single line in `\|...\|` — [edge-label-parser-safety](../mermaid/references/edge-label-parser-safety.md) |
| **Layers** | `subgraph` per composite or intent band (core LAN / field / plant) — [layout-and-labels](references/layout-and-labels.md) |
| **Star hub** | Anchor = max degree; leaves + mates at leaf rank; HDMI/mate chord **last** |
| **Power chain** | Source rank 0 → +1 per hop along `-->` |
| **Uplink** | Only edge allowed `rank_span > 1`; declare **last** |
| **Nested PCBA** | Internal links from `part def`; boundary links from deploy |
| **Title** | First line `%% <figureId>` matching MemNet `TSK_diagram_*` |

Full placement algorithm: [mermaid-placement-by-degree](../mermaid/references/mermaid-placement-by-degree.md).  
Model inventory steps: [architecture-diagrams](../mermaid/references/architecture-diagrams.md).  
Narrow / overloaded figures: [viewport-and-layout](../mermaid/references/viewport-and-layout.md).

---

## Section file pattern

Typical path: `outputs/system-design-report/04-interconnection.md`.

Each figure: heading → fenced `mermaid` with `%% <figureId>` first line → one-line legend mapping short tokens to `link*`.

**Worked example:** `vedan-foam-detection-lite-ver2` → `04-interconnection.md` (`vfdl2-edgeside-panel-eth`) and TRON `DiagramPlan` in [mermaid-placement-by-degree](../mermaid/references/mermaid-placement-by-degree.md) § Serve down.

After section edits: regenerate merged export if the project uses one (`merge_markdown.py` per hub `llm_toc`).

---

## Checklist

- [ ] `connection link*` inventory matches deploy (grep, not memory)
- [ ] `typedBy` on `@CON` (or backfill + `@CLM` assumptions)
- [ ] `TSK_diagram_*` scoped; split gate passed
- [ ] `p2c:spans` clean (`rank_span ≤ 1` except uplink)
- [ ] `p3:edges` order: spokes → chains → chords
- [ ] Legend / **Connections** table lists `link*` for traceability
- [ ] `mmdc -i <section>.md` pass
- [ ] MemNet `p6:settle` + report `@CLM` if serve up ([sysml-view-doc-sync](../sysml-view-doc-sync/SKILL.md) step 7)

---

## Anti-patterns

| Bad | Good |
|-----|------|
| Draw from screenshot / memory | Inventory deploy + warm MemNet `@CON` |
| One figure mixing L2 + power + GPIO | Split by `typedBy` intent |
| Mate (HDMI) at rank 2 in star | Mates at **leaf rank**, chord last |
| Unicode `→` in edge labels | ASCII tokens + legend |
| Edit `.md` before placement graph | `TSK_diagram_*` or TRON first |

---

## References

- [layout-and-labels.md](references/layout-and-labels.md) — layers, legend, manual vs script IBD
- [mermaid-placement-by-degree](../mermaid/references/mermaid-placement-by-degree.md) — MemNet / TRON placement
- [architecture-diagrams](../mermaid/references/architecture-diagrams.md) — model-first inventory
- [interconnection-mermaid (view-doc-sync)](../sysml-view-doc-sync/references/interconnection-mermaid.md) — sync-time doc pairing
