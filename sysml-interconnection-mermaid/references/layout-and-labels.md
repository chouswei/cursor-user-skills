# Interconnection layout and labels

**Audience:** LLM using [sysml-interconnection-mermaid](../SKILL.md). Pair with [mermaid-placement-by-degree](../../mermaid/references/mermaid-placement-by-degree.md).

---

## Layer bands (flowchart TB)

Typical top-to-bottom separation — use **`subgraph`** so office, field, and plant do not collapse into one cluster:

| Band | Examples | Notes |
|------|----------|-------|
| **Core / office LAN** | `topLevelNetworkSwitch`, `mqttBroker`, `industrialPc` | Site router as hub; spokes inside subgraph |
| **Field uplink** | Panel switch port 5 → core | Declare **last**; only `rank_span > 1` |
| **Plant / edge** | Power chain, valve, imaging light | One intent per figure when possible |

**Directed edges:** `-->` for power chains and switch fan-out; `---` for symmetric L2 attachment when direction does not matter.

---

## Canvas vs legend

| On canvas | In legend / Connections table |
|-----------|--------------------------------|
| `P1`, `P2`, `eth1`, `24 V`, `HDMI` | Full `linkEdgePcToGs305epPort2`, port paths |
| Part usage id (`gs305EP`) | Optional type / de-facto in caption |
| `bind` | Dotted edge `-.->` + note in table |

**Parser safety:** no `\n`, `→`, `—` inside `\|edge labels\|` — [edge-label-parser-safety](../../mermaid/references/edge-label-parser-safety.md).

---

## One diagram ≈ one question

| Figure scope | Example |
|--------------|---------|
| Panel L2 + HMI | `vfdl2-edgeside-panel-eth` |
| Plant power + valve | `vfdl2-edgeside-plant-power` |
| PCBA internal | `vfdl2-relay-pcba-internal` |
| System L2 edge + core | `vfdl2-ethernet-interconnection` |
| Scale-out fabric only | Core + N field switches — omit per-tank stacks |

Split when: mixed `typedBy` families, `|nodes| > 6`, or `max(degree) > 6` — [viewport-and-layout](../../mermaid/references/viewport-and-layout.md).

---

## Nested PCBA

| Layer | Source | In diagram |
|-------|--------|------------|
| Deploy boundary | `deploy-*.sysml` composite | Harness, PSU, valve field links |
| On-board | `part def FoamLiteVer2RelayChainPcba` | Coil/contact path inside `subgraph` |

Do not merge deploy `linkRelayControllerGpio40ToRelayChainHarness` with internal `linkMcuCoilToBufferLogicIn` without showing the PCBA boundary.

---

## Manual `.md` vs script IBD

| | Manual Mermaid in `outputs/*.md` | `visualize.py` IBD HTML |
|--|----------------------------------|-------------------------|
| Layout | Placement-by-degree, curated layers | `ibd_subgraphs` from config |
| Edges | `-->` where readable | Often `<-->` grouped |
| When | Operator report, split intents | Auto-sync after deploy |

Both must agree on **who connects to whom** and **which port**.

---

## Optional styling

- `classDef` for office / field / terminal (semantics still in model)
- `%%{init: ...}%%` for `fontSize`, `nodeSpacing`, `rankSpacing` — match project siblings
- Themed SVG export: [pretty-mermaid](../../pretty-mermaid/SKILL.md) **after** `mmdc` pass

---

## Preview vs export

Nested subgraphs and current Mermaid syntax may fail in **old embedded previews** but pass **`mmdc`**. Do not flatten topology for preview alone; validate with CLI.
