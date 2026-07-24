# Mermaid for system / interconnection views (`outputs/*.md`)

**Canonical skill:** [sysml-interconnection-mermaid](../../sysml-interconnection-mermaid/SKILL.md) — full pipeline (MemNet `TSK_diagram_*`, placement, materialise, `mmdc`).

This file retains **layout and label** quick reference; deep placement: [mermaid-placement-by-degree](../../mermaid/references/mermaid-placement-by-degree.md).

Use when updating **deployment-aligned** diagrams: part tree companions, **flowchart** IBD-style views, or scale-out “fabric only” figures. General prose rules: [repo-mermaid-rules](../../mermaid/references/repo-mermaid-rules.md). **Narrow preview / PCBA splits:** [viewport-and-layout](../../mermaid/references/viewport-and-layout.md). **Layers / legend detail:** [sysml-interconnection-mermaid/references/layout-and-labels.md](../../sysml-interconnection-mermaid/references/layout-and-labels.md).

## Core principles

1. **Model is the label source** — Before drawing, load **[sysml-interconnection-mermaid](../../sysml-interconnection-mermaid/SKILL.md)** and inventory connections per **[architecture-diagrams.md](../../mermaid/references/architecture-diagrams.md)**; build placement graph per **[mermaid-placement-by-degree.md](../../mermaid/references/mermaid-placement-by-degree.md)** (`config.yaml` → `deployment_part` → `rg connection link` in deploy; MemNet `TSK_diagram_*` or Markdown `DiagramPlan`). Node titles = **part usage names**; canvas edge labels = short tokens; full `link*` in legend.

2. **Layer by topology** — Typical **top-to-bottom** bands:
   - **Office / core LAN** — router, hosts that attach only there (dashboard, MQTT broker, NAS, operator PC, …).
   - **Field** — access switch and **uplink** to the operator PC (often SFP, distinct from PR60X→switch routing).
   - **Plant / tank / edge** — parallel **LAN path** vs **CAM path** (or other field legs), fed by **separate switch ports** (e.g. `poeEthernet2` / `poeEthernet3`).

   Separating layers stops office, field uplink, and station I/O from visually collapsing into one undifferentiated cluster.

3. **Short on the canvas, long in the legend** — Edge labels: **one SysML link id** or short token per edge (`linkPduToControlPcba5V`, `UART`, `Ethernet`). No `\n` or Unicode (`→`) inside `\|edge labels\|` — [edge-label-parser-safety.md](../../mermaid/references/edge-label-parser-safety.md). Bind notes, uart map, and `5V/12V` detail go in caption or connections table.
   - Prefer parser-safe ASCII; use the legend for port lists and wildcards (`linkPcbaToQpd*`).

4. **One diagram ≈ one question** — Example split:
   - Full **single-tank** deploy: core + field + both field chains.
   - **Scale-out** office fabric only: router + shared services + N workstations + N field switches — **omit** per-tank M12 stacks to avoid clutter.

5. **Optional `classDef`** — Color **office / field / terminal** nodes for quick scanning; keep semantics in the model, not only in color.

6. **Directed edges where they help** — From the field switch **down** to each field leg, `-->` can read clearer than bidirectional `<-->` for “fan-out.” Script-generated IBD HTML may still use `<-->` for grouped SysML edges; **semantics** stay the same.

7. **Title comment** — First line `%% <Project> – <deploymentPart> (<scope>)` so exports and diffs stay identifiable.

8. **Regenerate script IBD when appropriate** — If the project has `visualize.py` + `ibd_html_path` in `config.yaml`, regenerate HTML after deploy changes so **SysML-driven** Mermaid stays in sync; **manual** figures in `outputs/*.md` are still updated by hand for layout and annotations.

## Preview compatibility (Cursor / GitHub / older Mermaid)

Some **embedded** Markdown previews ship an **older Mermaid** build. **Nested subgraphs** (e.g. tank region containing LAN/CAM columns) and **Unicode** in labels are valid in current Mermaid and pass **`mmdc`**, but a preview may still error.

**Prefer keeping** the nested structure when it matches the topology; do not flatten solely for the preview.

If the preview fails: render with **`mmdc`** or open **script-generated** `visualize.py` HTML (often newer Mermaid), or update the preview extension / IDE Mermaid version.

Full repo prose rules still apply: [repo-mermaid-rules](../../mermaid/references/repo-mermaid-rules.md).

## Checklist (before marking doc sync done)

- [ ] **[sysml-interconnection-mermaid](../../sysml-interconnection-mermaid/SKILL.md)** pipeline followed; MemNet `TSK_diagram_*` or Markdown `DiagramPlan` before fenced block
- [ ] Part names / ports match **deploy** (grep `connection` / `part` lines).
- [ ] Spare PR60X / switch ports and **site convention** bullets in `Network::*` **doc** match if you cite them.
- [ ] Legend or **Connections** table lists SysML **link** names where operators need traceability.
- [ ] Edge labels: single-line ASCII, no `\n` / `→` in `\|...\|` ([edge-label-parser-safety](../../mermaid/references/edge-label-parser-safety.md)).
- [ ] `mmdc` validation if the project renders diagrams in CI or the user asked for PNG/SVG export ([mermaid](../../mermaid/SKILL.md) / [mmdc](../../mmdc/SKILL.md)).

## Contrasts

| Concern | Manual Mermaid in `outputs/*.md` | `visualize.py --diagram ibd --format html` |
|--------|-------------------------------------|--------------------------------------------|
| Layout | Curated layers, optional `classDef` | Subgraphs from `config.yaml` `ibd_subgraphs` |
| Edges | May use `-->` for readability | Typically `<-->` grouped by part-pair |
| Source | Editor | Extracted from deployment composite |

Both should agree on **who connects to whom** and **which physical port** when the model fixes it.
