---
name: sysml-eagle-netlist-bridge
description: >-
  Consolidate EAGLE netlist (.scr, .pl) into SysML v2 signal item definitions and connector port mappings.
  Use when integrating real PCB designs (hardware under design) with full netlist traceability.
  Extracts connector pin assignments, signal names, power distribution, and component usage.
  Run after sysml-hardware-part-generator to add detailed signal flow.
  Triggers: EAGLE netlist, PCB design integration, signal consolidation, connector mapping,
  netlist to SysML, design traceability, 86ewy6qck, hardware netlist consolidation.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first (clarify EAGLE file paths and connector/signal scope)
token_guardrails: |
  - **EAGLE files:** `.scr` (netlist) + `.pl` (parts list) from same design version.
  - **Connector scope:** Clarify which connectors are user-facing (include signal names) vs internal (omit details).
  - **Signal item strategy:** Power rails, control signals, and multi-channel buses (SPI, SAI) get `item def`; single-pin signals documented in comments only.
  - **Design traceability:** Always reference EAGLE design ID (e.g., 86ewy6qck) in SysML attributes and file naming.
  - **Existing part updates:** If updating a `part def` from sysml-hardware-part-generator, run sysml-part-reviewer first to confirm under-design status.
---

# SysML EAGLE Netlist Bridge

**Goal:** Consolidate EAGLE netlist (`.scr`, `.pl`) into SysML v2 signal definitions and connector port mappings, bridging real hardware design with model-based architecture.

## Workflow

0. **Clarify scope** — Ask user:
   - EAGLE file paths (`.scr`, `.pl`, design code)
   - Which connectors are **external** (need detailed signal names) vs **internal** (summary only)
   - **Analysis depth:** minimal (signals only) vs detailed (power budgets, grounding, EMI)?
   - Are we updating an existing `part def` (run sysml-part-reviewer first) or creating new signals?

1. **Read EAGLE files**
   - Parse `.pl` (parts list) for BOM, component count, key ICs
   - Parse `.scr` (netlist script) for:
     - Signal names (power rails, control, data channels)
     - Connector pin assignments
     - Net connectivity (which pins connect to which signals)
     - Common-mode chokes, filtering networks
   - **For `.sch` (schematic) files:** Use grep/ripgrep only (see [EAGLE-FILES-ANALYSIS-GUIDE.md](../../hardware/EAGLE-FILES-ANALYSIS-GUIDE.md))

2. **Organize signals by category**
   - **Power distribution** — voltage rails, ground planes, isolated domains
   - **Control signals** — active-low reset, chip-select, clock, start/stop
   - **Data channels** — SPI (multiple instances), SAI, UART, GPIO
   - **Analog signals** — ADC input, DAC output, modulation
   - **Connectors** — user-facing pin assignments grouped by connector (J1, J5, J6, etc.)

3. **Create SysML item definitions** — for:
   - Power rails (`PowerSupply5V`, `PowerSupply12V`, etc.)
   - Ground references (`GroundSignal`, `GroundIsolated`)
   - Signal primitives (e.g., `SpiChipSelect`, `SpiClock`, `StartSignal`)
   - Multi-pin signal groups (`SpiChannel` composite)

4. **Create connector port definitions** — map to existing `part def` from sysml-hardware-part-generator:
   - Each external connector → `port def` with nested ports for signals
   - Name ports with actual netlist signal names (e.g., `!CS_1`, `SCLK_1`, `SDI_1`, `SDO_1`)
   - Document J-pin references in comments

5. **Document connector signal maps** — add to signals file or analysis doc:
   - For each connector: pin assignments, resistor conditioning networks, jumper routing
   - MCU pin allocations (if MCU is on design)
   - IC signal connections (AD9837 DDS, op-amps, etc.)

6. **Create analysis document** — reference file with:
   - Component summary (count, key ICs, form factors)
   - Power budget notes
   - Grounding architecture
   - Signal integrity / EMI filtering notes

7. **Update `config.yaml`** — add signals file to model_files (after `part def`, before `deploy`)

8. **Validate** — SysML v2 MCP getDiagnostics on new signals file + full project

## Outputs

### Main outputs
- **`signals-<design-code>.sysml`** — SysML v2 item defs + connector port definitions (ready to insert into project models/)
- **`<design-code>-ANALYSIS.md`** — Human-readable netlist summary (if analysis_depth ≥ detailed); if minimal, provide brief inline comments only

### Secondary outputs
- **Updated `part def`** from sysml-hardware-part-generator — now includes design-phase attributes:
  - `designRevisionCode`, `designStatus`, `eagleVersion`, `designDate`
  - Enhanced documentation with netlist references

## Pairing

- **sysml-hardware-part-generator** — create `part def` first; this skill adds signal detail.
- **sysml-physical-port-generator** — for custom connector definitions if not in HardwarePorts.
- **sysml-part-reviewer** — if updating existing part, classify maturity first.
- **sysml-connections** — wire signals in deploy model after port definitions exist.
- **sysml-view-doc-sync** — after signals/part creation, sync pinmap tables to `outputs/*.md` interconnection docs.

## Inputs to gather

- **EAGLE design code** (e.g., 86ewy6qck, Control-system-design_V6)
- **File paths** — `.scr` (netlist), `.pl` (parts list)
- **Connector scope** — which connectors are user-facing?
- **Existing part** — are we updating a known `part def`, or creating signals from scratch?
- **Analysis depth** — minimal (signals only) vs detailed (power budgets, grounding, EMI)?

## Post-generation

1. **Place signals file** in `sysml-v2-models/projects/<name>/models/signals-<design-code>.sysml`
2. **Place analysis doc** in `hardware/<design-code>-ANALYSIS.md`
3. **Copy EAGLE files** to `hardware/<design-code>.{pl,scr}` for archival
4. **Update config.yaml** — add signals file to model_files
5. **Update existing `part def`** if one exists — add design attributes
6. **Validate** — `sysml v2 mcp getDiagnostics` + full project
7. **Wire in deploy** — use sysml-connections to route signals to/from HAT

## Example: 86ewy6qck (PAT MCU HAT PCBA)

**Input:** EAGLE files `86ewy6qck.{pl,scr}` (NUCLEO-H753ZI + AD9837 DDS + QPD multiplexer)

**Outputs:**
- `signals-86ewy6qck.sysml` — 8× power items, SPI primitives, beacon DDS signals, connector maps
- `86ewy6qck-ANALYSIS.md` — BOM, J1 (30-pin) / J5 (20-pin FFC) pinout, power distribution, EMI filtering
- Updated `pat-breakout-mcu-hat.sysml` — port defs with signal names (!CS_1, SCLK_1, etc.)

**Integration:** Added to `leo-cubesat-laser-comm` project; now full netlist is traceable from SysML model to EAGLE design.

---

## Notes

- **Design under development?** Attribute `designStatus: "under-design"` allows future netlist updates without breaking traceability.
- **Multiple design versions?** Create separate `.sysml` and `.md` per version (V4, V5, V6) if needed; config.yaml selects active version.
- **Missing HardwarePorts types?** Use sysml-physical-port-generator to extend HardwarePorts with custom connector definitions.
- **Isolated grounds?** Document separately (`DGND`, `DGND1–5`, `GND`, `AGND`) — important for power integrity and EMI analysis.
