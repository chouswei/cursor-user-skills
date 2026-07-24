# Mermaid diagram rules (repo)

**Very important:** Follow these rules for all Mermaid state and flow diagrams so labels do not overlap when rendered (Markdown preview, HTML, or PNG for ClickUp).

---

## 1. Short labels on arrows

Long transition labels (e.g. `ReedTopTriggered`, `TargetDepthReached`, `CarReachedTopAfterReturn`) overlap in the rendered diagram.

- **Do:** Use short labels on the arrows, e.g. `ReedTop`, `TargetDepth`, `AtTop`.
- **Don’t:** Use full event/attribute names on the diagram if they are long (unless the diagram is very sparse).

---

## 2. Set direction (stateDiagram-v2)

Without an explicit direction, layout can be cramped and labels overlap.

- **Do:** Add `direction TB` for lifecycle / firmware state machines (especially when a **reconnect** or **error** loop returns to an earlier state).
- **Do:** Use `direction LR` only for ≤4 states with **no** long return arcs.
- **Don't:** Nest `state X { idle --> idle: ... }` with multiple self-loops — Mermaid draws one awkward arc; list events in a **table** instead ([state-diagram-layout.md](state-diagram-layout.md)).
- **Example:**
  ```mermaid
  stateDiagram-v2
    direction TB
    [*] --> travelling
    travelling --> atTop: ReedTop
  ```

---

## 3. One-line legend (traceability)

Short labels must be traceable back to the model (e.g. SysML behaviour).

- **Do:** Add a one-line legend under the diagram, e.g.  
  *Events (short): ReedTop = ReedTopTriggered, TargetDepth = TargetDepthReached, AtTop = CarReachedTopAfterReturn.*
- This keeps the diagram readable while preserving traceability to the behaviour model.

---

## 4. Flowcharts and interconnection diagrams

### 4.1 Always set flowchart type and direction

- **Do:** Start with `flowchart TB` or `flowchart LR` (and optionally a title comment).
- **Example:** `%% PAT data flow` then `flowchart LR`

### 4.2 Subgraphs: avoid redundant naming

- **Do:** Give the **subgraph** a distinct role (e.g. `["Breakout HAT (bridge)"]`) and the **node inside** a short name (e.g. `[HAT]`), so the same phrase is not repeated as both box title and node label.
- **Don’t:** Use the same label for the subgraph and its only node (e.g. `subgraph hat["Breakout HAT"]` with `breakout[breakout HAT]` inside).

### 4.3 Edge labels: short, directional, unambiguous

- **Do:** Use **one line** per edge label: SysML **link** name or short protocol token (e.g. `linkCm5ToPatPduUart`, `UART`, `Ethernet`). Full port lists, bind notes, and `5V/12V` detail go in the **caption or table** — not on the edge.
- **Do not:** Put `\n` or Unicode arrows (`→`, `↔`) inside `\|edge labels\|` — causes **Lexical error** in preview and some `mmdc` builds. See [edge-label-parser-safety.md](edge-label-parser-safety.md).
- **Do:** Use directed edges: `-->` for one-way, `<-->` for bidirectional. Arrowheads come from syntax, not from characters inside the label.
- **Do:** Add a legend under the figure when abbreviations need traceability (e.g. *switchOutBeacon5V bind powerOutBeacon_5V*).
- **Do:** Prefer parser-safe ASCII. Avoid `*`, `!`, unquoted `/`, `\`, `:` in edge labels unless validated with `mmdc -i <file>.md`.

### 4.4 Diagram title (for context)

- **Do:** Add a Mermaid comment at the top of the block, e.g. `%% LEO Laser Comm PAT – data flow (acquisition-MCU variant)`, so the diagram is identifiable in exports and diffs.
- Optionally repeat the same in the surrounding doc (e.g. a heading or caption above the code block).

### 4.5 Subgraph order and overlap

- For multi-subgraph diagrams, **prefer `flowchart TB`** so groups stack vertically and labels (e.g. I2C daisy chain) do not overlap other blocks. Use distinct subgraph IDs and differentiate similar edge labels (e.g. "QPD ADC" vs "ADC to MCU").
- In `flowchart LR`, subgraphs are laid out left-to-right; define **Host** then **Breakout HAT** then **QPD path** then **MEMS** then **I2C** and keep names short.

### 4.6 Narrow viewport (Markdown preview / system design reports)

- If the diagram **scrolls horizontally** in preview (~900px width), switch to **`flowchart TB`** or **split** into 2–4 figures (power / compute / edge / data path) instead of shrinking font alone.
- Optional **init** block for density: `fontSize` 13–15px, `nodeSpacing` 14–22, `rankSpacing` 22–32 — full table in [viewport-and-layout.md](viewport-and-layout.md).
- PCBA / control-board starters: [../templates/narrow-viewport-pcba.md](../templates/narrow-viewport-pcba.md).

---

## Summary checklist

**State diagrams (stateDiagram-v2):**

1. [ ] Use **short labels** on transitions (e.g. ReedTop, TargetDepth, BatteryFull).
2. [ ] Add **`direction TB`** for lifecycle + recovery loops; LR only for small acyclic charts ([state-diagram-layout.md](state-diagram-layout.md)).
3. [ ] **Flat** top-level states; self-loops (>1 event) in **table**, not multiple diagram edges.
4. [ ] Add a **legend** under the diagram mapping short → full names.
5. [ ] Optional themed SVG: [pretty-mermaid-bridge.md](pretty-mermaid-bridge.md) after `mmdc` pass.

**Flowcharts (interconnection / data flow):**

1. [ ] Set **flowchart TB** (prefer for many subgraphs to avoid overlap) or **flowchart LR**, and add a **%% title** comment.
2. [ ] **Subgraph** label ≠ same as inner node (e.g. "Breakout HAT (bridge)" + node "HAT").
3. [ ] **Edge labels** one line, ASCII, no `\n` / `→` / `*` in `\|...\|` ([edge-label-parser-safety.md](edge-label-parser-safety.md)).
4. [ ] **Legend** under the diagram when short labels need traceability (bind, uart map, power rails).
5. [ ] **No horizontal scroll** in narrow preview (or split + numbered figure captions).
6. [ ] **`mmdc -i <section>.md`** passes before doc sync is done.

---

## References

- [tasks/lessons.md](../../../../tasks/lessons.md) — Same rule in lessons (review at session start).
- [tools/clickup/](../../../../tools/clickup/) — scripts for ClickUp; Mermaid→PNG when exporting to Docs.
- [Mermaid flowchart docs](https://mermaid.js.org/syntax/flowchart.html) — Subgraphs, direction, edge syntax.
- [viewport-and-layout.md](viewport-and-layout.md) — TB vs LR, split figures, init tuning, markdown workflow.
- [edge-label-parser-safety.md](edge-label-parser-safety.md) — `\n` ban, lexical errors, SysML link ids on edges.
