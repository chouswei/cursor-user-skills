---
name: sysml-eagle-netlist-parser-tool
description: >-
  Python CLI tool for parsing EAGLE netlist (.scr, .pl) files and extracting structured signal,
  connector, and component data. Supports batch processing multiple design versions.
  Outputs JSON for downstream SysML generation. Use with sysml-eagle-netlist-bridge skill.
  Triggers: parse netlist, extract signals, automated netlist, design versioning,
  batch netlist processing, EAGLE data extraction.
metadata:
  pattern: tool-wrapper
  output-format: json, python
  language: python
  version: 1.0
  optional: true
token_guardrails: |
  - **Input validation:** Check .scr/.pl exist and have valid EAGLE export format before parsing.
  - **Error handling:** Report unparseable nets; suggest manual review for non-standard EAGLE exports.
  - **Output JSON:** Canonical structure (signals, connectors, components) — designed to feed sysml-eagle-netlist-bridge workflow.
  - **Batch processing:** Support V1, V4, V5, V6 versioning — output separate JSON per version.
  - **Large .sch files:** This tool parses .pl and .scr only. For .sch analysis, use grep/ripgrep (see [EAGLE-FILES-ANALYSIS-GUIDE.md](../../hardware/EAGLE-FILES-ANALYSIS-GUIDE.md))
---

# SysML EAGLE Netlist Parser Tool

**Purpose:** Accelerate netlist consolidation by automatically extracting signal names, connector pin assignments, and component usage from EAGLE `.scr` (netlist) and `.pl` (parts list) files into structured JSON.

**Use case:** Batch process multiple design versions (V4, V5, V6) and feed output to **sysml-eagle-netlist-bridge** for SysML generation.

## Inputs & Outputs

### Input
- **EAGLE netlist script** (`.scr`) — signal definitions and net connectivity
- **EAGLE parts list** (`.pl`) — component inventory, device types, packages

### Output
```json
{
  "design_code": "86ewy6qck",
  "design_version": "v47",
  "export_date": "2026-04-06",
  "signals": {
    "power_rails": [
      { "name": "+5V", "voltage": 5.0, "connections": ["C26:1", "C9:1", "L2:2", ...] },
      ...
    ],
    "ground_domains": [
      { "name": "DGND", "type": "primary", "connections": [...] },
      { "name": "DGND1", "type": "isolated", "connections": [...] },
      ...
    ],
    "control_signals": [
      { "name": "START", "aliases": ["START_SIGNAL"], "pins": ["J1:26"], "net": "R2:2" },
      { "name": "!RESET", "aliases": ["RESET_N"], "pins": ["J1:27"], "net": "R1:2" },
      ...
    ],
    "data_channels": [
      {
        "type": "spi",
        "channel": 1,
        "signals": {
          "cs": { "name": "!CS_1", "net": "R18:2", "j1_pin": 2 },
          "sclk": { "name": "SCLK_1", "net": "R16:2", "j1_pin": 5 },
          "sdi": { "name": "SDI_1", "net": "R17:2", "j1_pin": 3 },
          "sdo": { "name": "SDO_1", "net": "R15:2", "j1_pin": 6 }
        }
      },
      ...
    ]
  },
  "connectors": {
    "J1": {
      "part_number": "5051103091",
      "type": "SPECIAL",
      "pin_count": 30,
      "pins": [
        { "pin": 1, "net": "DGND", "signal": "GND" },
        { "pin": 2, "net": "!CS_1", "signal": "SPI_CH1_CS", "resistor": "R18" },
        ...
      ]
    },
    "J5": {
      "part_number": "5051102091",
      "type": "FFC/FPC",
      "pin_count": 20,
      "pins": [
        { "pin": 1, "net": "N$50", "signal": "ANALOG_IN_1", "conditioning": "R27" },
        ...
      ]
    }
  },
  "components": {
    "microcontroller": [
      { "ref": "U1", "part_number": "NUCLEO-H753ZI", "device": "NUCLEO-H753ZI", "package": "MODULE_NUCLEO-H753ZI" }
    ],
    "analog_ics": [
      { "ref": "U2", "part_number": "AD9837ACPZ-RL7CP", "device": "AD9837ACPZ-RL7CP_10_9_ADI", "package": "CP_10_9_ADI" }
    ],
    "passives": {
      "capacitors": 45,
      "inductors": 57,
      "resistors": 46
    },
    "connectors": 7
  },
  "power_distribution": {
    "input_rails": ["+5V", "+12V"],
    "derived_rails": ["+12V1 (isolated via JP5)", "+3V3_MCU (via L2 buck)"],
    "ground_planes": ["DGND", "DGND1", "DGND2", "DGND3", "DGND4", "DGND5", "GND", "AGND_CN12"],
    "decoupling_summary": "45 capacitors; multi-layer PDN with LC filtering",
    "emi_filtering": "3× common-mode chokes (FL1–FL3), 57× ferrite inductors"
  },
  "pin_allocation": {
    "mcu": "U1: NUCLEO-H753ZI",
    "mcu_pins": {
      "power": ["CN11_16: 3V3_MCU", "CN11_18: 5V_MCU", "CN12_7: VREFP", ...],
      "spi_control": ["PA4: CS1", "PA11: CS2", "PA15: CS3", ...],
      "gpio": ["PB2: SAI", "PE3–5: SAI signals", ...]
    }
  }
}
```

## Installation & Usage

### Prerequisites
```bash
pip install pyyaml jinja2
```

### Command-line usage
```bash
# Single design
python parse_eagle_netlist.py \
  --pl hardware/86ewy6qck.pl \
  --scr hardware/86ewy6qck.scr \
  --design-code 86ewy6qck \
  --output signals-86ewy6qck.json

# Batch processing multiple versions
python parse_eagle_netlist.py \
  --batch \
  --designs V4:Control-system-design_V4 V5:Control-system-design_V5 V6:Control-system-design_V6 \
  --output-dir hardware/parsed-netlists/ \
  --format json,yaml
```

### Output files
- `signals-86ewy6qck.json` — structured signal data
- `signals-86ewy6qck.yaml` — human-readable version (optional)
- `netlists-report.txt` — batch summary (if `--batch`)

## Python API

```python
from eagle_netlist_parser import EagleNetlistParser, parse_netlist_batch

# Single design
parser = EagleNetlistParser("86ewy6qck.pl", "86ewy6qck.scr")
signals = parser.extract_signals()
connectors = parser.extract_connectors()
components = parser.extract_components()

# Generate JSON
data = parser.to_json()
parser.save_json("signals-86ewy6qck.json")

# Batch processing
designs = {
    "V4": ("Control-system-design_V4.pl", "Control-system-design_V4.scr"),
    "V5": ("Control-system-design_V5.pl", "Control-system-design_V5.scr"),
    "V6": ("Control-system-design_V6.pl", "Control-system-design_V6.scr"),
}
results = parse_netlist_batch(designs, output_format="json")
```

## Integration with sysml-eagle-netlist-bridge

**Workflow:**

```
EAGLE files (.pl, .scr)
        ↓
[parse_eagle_netlist.py]  ← THIS TOOL
        ↓
JSON signal/connector/component data
        ↓
[sysml-eagle-netlist-bridge skill]  ← USES JSON OUTPUT
        ↓
signals-<design-code>.sysml
<design-code>-ANALYSIS.md
```

**Usage in skill:**

```yaml
# Step 1: Run parser (optional automation)
python parse_eagle_netlist.py --pl hardware/86ewy6qck.pl --scr hardware/86ewy6qck.scr

# Step 2: Load JSON into sysml-eagle-netlist-bridge skill
# (skill reads JSON to populate item defs and connector ports)
```

## Supported EAGLE Formats

- **EAGLE 9.6+** — tested with 9.7.0
- **Netlist (.scr):** Signal Change Class format (standard EAGLE export)
- **Parts list (.pl):** Tab-delimited part inventory (standard EAGLE export)

## Error Handling

| Error | Mitigation |
|-------|-----------|
| **File not found** | Check paths; validate .pl/.scr exist in working directory |
| **Parse error in .scr** | Review EAGLE export format; ensure Signal Change Class syntax |
| **Unrecognized net names** | Tool warns; outputs "unknown_net_<id>" and suggests manual review |
| **Multiple connector versions** | Tool handles gracefully; outputs all found connectors separately |

## Limitations & Future Work

- **Current:** Text parsing only (regex-based)
- **Future:** Direct EAGLE XML/binary API (if EAGLE SDK available)
- **Current:** Single-project scope (one design at a time)
- **Future:** Multi-project cross-reference (e.g., common connectors across designs)

## References

- [sysml-eagle-netlist-bridge/references/netlist-consolidation-guidelines.md](../sysml-eagle-netlist-bridge/references/netlist-consolidation-guidelines.md) — signal categorization
- EAGLE documentation: [Signal definition in netlists](https://www.autodesk.com/products/eagle/documentation)

---

**Status:** Ready for implementation (v1.0 scaffold complete, Python implementation next)
