# Mermaid placement by degree (MemNet graph first)

**Audience:** LLM editing **interconnection / architecture flowcharts** in `outputs/**/*.md`. **Canonical skill:** [sysml-interconnection-mermaid](../sysml-interconnection-mermaid/SKILL.md). **Do not** write fenced ` ```mermaid ` blocks until a **placement graph** exists in MemNet (or a **Markdown `DiagramPlan`** when serve is down).

Pair with: [architecture-diagrams.md](architecture-diagrams.md) (model-first blocks), [viewport-and-layout.md](viewport-and-layout.md) (split figures), [edge-label-parser-safety.md](edge-label-parser-safety.md), [sysml-memnet-pipeline.md](~/.cursor/skills/sysml-memnet-documentation/references/sysml-memnet-pipeline.md) (wire rows).

---

## Layers

| Layer | Role | Mutable when |
|-------|------|----------------|
| **SysML** `deploy-*.sysml` | Topology authority (`part`, `connection link*`) | Model edits |
| **MemNet** `TSK_diagram_*` | Scope, degree, types, rank, lane, rank_span, edge order | Each diagram sync turn |
| **`outputs/*.md`** | Presentation — fenced Mermaid derived from graph | After `p5:review=ok` + `mmdc` |

**Rule:** Steps through **p5:review** touch **MemNet only** — no `.md` edit until pre-materialise gate passes.

---

## Mandatory pipeline

```text
pin_map(TSK_model_*)
  → p0:types (typedBy histogram → intent bucket)
  → split gate (one intent family per figure)
  → p1:scope (figure_includes / figure_uses)
  → p2:place (ranks, anchor, mates)
  → p2b:bary (lane iteration ≤2)
  → p2c:spans (rank_span audit)
  → p3:edges (spokes → chains → chords)
  → p4:materialise (.md + mmdc)
  → p5:review (visual; max 2 iterations)
  → p6:settle
```

On **p5** failure: rewind to **p2** or **p3** on graph only — never hand-patch crossings in `.md`.

---

## `typedBy` backfill (before p0)

Current project snaps may have `@CON` + `ends` but **no `typedBy` EDG**. Before any placement task:

1. `query_warm` `@CON_*`; for each missing `typedBy`:
2. Grep `connection link<Name>\s*:\s*<DefName>` in `deploy-*.sysml`.
3. Add `@EDG … typedBy … CONDEF_<DefName>` in the **same batch** as snap delta.
4. Fallback (grep miss only): name-prefix heuristic (`linkEdgePanelAc*` → power, `link*ToGs305epPort*` → L2) as `@CLM` type=`assumption`.

Subsequent `connection` adds **must** include `typedBy` per [sysml-memnet-patterns.md](~/.cursor/skills/sysml-memnet-documentation/references/sysml-memnet-patterns.md).

---

## Split gate (before p1)

Abort single-figure scope when **any** holds:

| Gate | Threshold |
|------|-----------|
| Mixed `typedBy` intent families | >1 family in one `TSK_diagram_*` |
| Node count | `|figure_includes| > 6` |
| Hub degree | `max(degree) > 6` |

**Intent buckets** (example — project connection defs may extend):

| Bucket | Typical `typedBy` / connection defs |
|--------|-------------------------------------|
| **L2 / panel** | `EthernetHostToSwitchPort`, `HdmiHostToTouchDisplay`, `EthernetLink` |
| **Power** | `AcMainsPanelFeed`, `Power12VToAccessory`, `Power5VToAccessory` |
| **Control / GPIO** | `Gpio40PinHarnessLink`, `GpioRelayCoilLogic`, relay harness types |
| **Field / valve** | `RelayTwoPInterfaceToValveController`, `RelayTwoPThrowHarnessLink` |

---

## Glossary

| Term | Definition |
|------|------------|
| **rank** | Integer 0..N, top-to-bottom row in `flowchart TB`. Per `PRT` in `@CLM` stat. |
| **lane** | Integer 1..K, left-to-right within a rank. |
| **declare#** | Order in fenced block. **Anchor = declare# 1** always; not equal to rank order. |
| **rank_span** | `|rank(endA) − rank(endB)|` per CON. ≤ 1 mandatory except uplinks. |
| **spoke** | Edge between **anchor** (hub) and leaf in adjacent rank. |
| **chain** | Edge along directed power path; ranks step +1 per hop. |
| **chord** | Edge between two **non-anchor** nodes at **same rank** (mate pair, e.g. HDMI). |
| **uplink** | Edge to off-figure node — only edge allowed `rank_span > 1`; declare last. |

---

## Degree and anchor (p2:place)

**Degree:** for each `PRT` in `figure_includes`, count `figure_uses` CONs whose `ends` contain that usage.

**Anchor:** `argmax(degree)` within scope; tie-break by dominant `typedBy`:

| Dominant type | Anchor pick |
|---------------|-------------|
| L2 / switch | `gs305EP` or highest-degree switch |
| Power | `edgePanelAc220V` (source) or `relayChainPcba` (hub) |
| Control | PCBA hub |

Mark `@EDG` `anchor_of` from anchor `@PRT` → `TSK_diagram_*`.

---

## Rank assignment (p2:place)

| Topology | Rank rule |
|----------|-----------|
| **Power chain** | Source rank 0 → each hop +1 along `-->` |
| **Star (switch)** | Hub at rank **1**; **all leaves at rank 0** (including mates, e.g. `edgePc`) |
| **Mate pair** | Both mates at **leaf rank (0)**; `adjacent_to` EDG; consecutive declare# |
| **Uplink** | Off-figure; declare last; only `rank_span > 1` allowed |

**Why mates stay at leaf rank:** placing a mate at rank 2 forces its spoke (e.g. `edgePc → gs305EP`) to `rank_span 2` — gate failure.

**p2c:spans audit:** for each CON in `figure_uses`, compute `rank_span`. If any `> 1` (non-uplink): **do not materialise** — re-rank or split.

```cypher
CREATE (c:CLM {id: 'C_span_audit', type: 'pipe', code: 'p2c:spans ok:5 warn:0', status: 'active', recycle: 'delete_on_settle'})
```

---

## Barycenter lanes (p2b:bary)

Max **2 barycenter iterations** on MemNet only:

1. Fix ranks from p2.
2. Seed lanes: anchor centred; leaves by `typedBy` then name.
3. For each rank `R` (top→bottom, then bottom→top): `lane(node) = average(lane(neighbours in R±1))`; ties by name.
4. Write `lane` to `@CLM` stat; set `declare#`: anchor=1, then `(rank asc, lane asc)`.
5. Stop when lane order unchanged or after 2 sweeps.

**Star leaf tie-break:** order rank-0 leaves to match hub port order in `ends` (P1..P4).

**Note:** Mermaid/dagre placement is **best-effort** — `p5:review` remains mandatory.

---

## Edge declaration order (p3:edges)

```text
p3:edges = (hub spokes, leaf lane left→right) → (power chains, rank asc) → (chords / mate edges) → (uplinks)
```

- Declare **mate nodes** consecutively in declare#.
- Declare **mate edge** (HDMI) **after all spokes**, even though it is same-rank (chord).
- Never interleave chord between spokes.

Store ordered `CON_*` list on `TSK_diagram_*` as `@CLM` pipe `p3:edges:…`.

---

## Materialise (p4:materialise)

From `pin_map(TSK_diagram_<figureId>)`:

1. `%% <figureId>` + `init` + `flowchart TB`.
2. Optional `subgraph` per [architecture-diagrams.md](architecture-diagrams.md) §3.
3. **Nodes** in declare# order (`PRT` usage names).
4. **Edges** in `p3:edges` order; canvas = short tokens; legend maps `CON_*` / `link*` / `typedBy`.
5. Patch section `.md` — replace block with same `%% figure-id`.
6. `mmdc -i <section>.md`.

---

## Review (p5:review)

**Pre-materialise gate** (all must pass before first p4):

| Check | Fail action |
|-------|-------------|
| `p2c:spans` clean | Rewind p2 or split |
| Mates same rank + adjacent declare# | Fix `adjacent_to`; p2b |
| `p3:edges` follows global rule | Re-emit p3 |

**Review loop:** max **2 review iterations**. Rewind p2/p3 on graph; re-p4. After 2 failures → split figure — **no fake nodes**.

---

## MemNet wire (serve up)

See [sysml-memnet-pipeline.md](~/.cursor/skills/sysml-memnet-documentation/references/sysml-memnet-pipeline.md) section Diagram placement task. Agent I/O is openCypher-shaped (not pipe `@TAG`).

**Task:**

```cypher
CREATE (t:TSK {id: 'TSK_diagram_vfdl2-edgeside-panel-eth', goal: 'panel L2 graph', phase: 'pipe', status: 'in_progress', recycle: 'delete_on_settle'})
CREATE (t)-[:CHILDOF {id: 'NEW', note: 'diagram', recycle: 'delete_on_settle'}]->(:TSK {id: 'TSK_model_vfdl2'})
CREATE (t)-[:DOCUMENTS {id: 'NEW', note: '04-interconnection.md', recycle: 'delete_on_settle'}]->(:SEC {id: 'SEC_S04'})
```

**Placement stat per node:**

```cypher
CREATE (c:CLM {id: 'C_place_gs305EP', type: 'stat', code: 'PRT_gs305EP deg4 rank1 lane1 declare1', status: 'active', recycle: 'delete_on_settle'})
CREATE (:TSK {id: 'TSK_diagram_vfdl2-edgeside-panel-eth'})-[:OWNS {id: 'NEW', recycle: 'delete_on_settle'}]->(c)
```

**Pipe codes:** `p0:types` · `p1:scope` · `p2:place` · `p2b:bary` · `p2c:spans` · `p3:edges` · `p4:materialise` · `p5:review` · `p6:settle`

---

## Serve down — Markdown `DiagramPlan`

When MemNet is unavailable: keep the same fields in plain Markdown tables between iterations. **Backfill MemNet** when serve returns before p4. Do not use TOON/TRON.

**Canonical example — VFDL2 `vfdl2-edgeside-panel-eth`:**

**Meta**

| field | value |
|-------|-------|
| figureId | `vfdl2-edgeside-panel-eth` |
| intent | panel-L2 |
| anchor | `PRT_gs305EP` |
| spanAudit | ok=5, warn=0 |

**Types**

| typedBy | n |
|---------|---|
| EthernetHostToSwitchPort | 4 |
| HdmiHostToTouchDisplay | 1 |

**Nodes**

| prt | deg | rank | lane | declare | anchor |
|-----|-----|------|------|---------|--------|
| PRT_gs305EP | 4 | 1 | 1 | 1 | true |
| PRT_relayController | 1 | 0 | 1 | 2 | false |
| PRT_poeCameraA | 1 | 0 | 2 | 3 | false |
| PRT_edgePc | 2 | 0 | 3 | 4 | false |
| PRT_edgeTouchScreen | 1 | 0 | 4 | 5 | false |
| PRT_poeCameraB | 1 | 0 | 5 | 6 | false |

**Edges** (order = declare order)

| order | con | typedBy | endA | endB | rank_span |
|-------|-----|---------|------|------|-----------|
| 1 | CON_linkRelayControllerToGs305epPort1 | EthernetHostToSwitchPort | relayController | gs305EP | 1 |
| 2 | CON_linkPoeCameraAToGs305epPort3 | EthernetHostToSwitchPort | poeCameraA | gs305EP | 1 |
| 3 | CON_linkEdgePcToGs305epPort2 | EthernetHostToSwitchPort | edgePc | gs305EP | 1 |
| 4 | CON_linkPoeCameraBToGs305epPort4 | EthernetHostToSwitchPort | poeCameraB | gs305EP | 1 |
| 5 | CON_linkEdgePcToTouchScreen | HdmiHostToTouchDisplay | edgePc | edgeTouchScreen | 0 |

**Mates**

| a | b | reason |
|---|---|--------|
| PRT_edgePc | PRT_edgeTouchScreen | HDMI |

**Layout:** rank 0 = all leaves + mates; rank 1 = hub (`gs305EP`, declare# 1). All spokes `rank_span 1`; HDMI chord `rank_span 0`.

---

## Anti-patterns

| Bad | Good |
|-----|------|
| Edit `.md` before MemNet graph | Build `TSK_diagram_*` first |
| Re-grep deploy to count edges when warm `@CON` exists | Traverse `figure_uses` / `connects` |
| Add Mermaid nodes not in `figure_includes` | Split figure or fix scope |
| Hand-patch crossing in `.md` | Rewind p2/p3 on graph |
| Mate at rank 2 in star topology | Mates at leaf rank 0 |
| Opaque proprietary handoff dialects | Markdown `DiagramPlan` tables (same fields) |

---

## Checklist

- [ ] `typedBy` backfill done (or assumptions recorded)
- [ ] `TSK_diagram_*` with `figure_includes` / `figure_uses`
- [ ] Split gate passed (one intent family)
- [ ] Anchor + degree table on graph
- [ ] `p2c:spans` clean
- [ ] `p3:edges` spokes → chains → chords
- [ ] `p5:review=ok`
- [ ] `mmdc -i <section>.md` pass
- [ ] `p6:settle` + method `@CLM` on `@SEC`
