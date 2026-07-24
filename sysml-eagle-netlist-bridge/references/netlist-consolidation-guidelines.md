# EAGLE Netlist Consolidation Guidelines

## Signal Categorization

### Power Rails
Define `item def` for each voltage domain:
```sysml
item def PowerSupply5V {
  doc /* Main acquisition MCU supply. */
  attribute voltage : Real = 5.0;
  attribute unit : String = "V";
}
```

**Include:** Rails that appear in multiple places (J1, connectors, decoupling capacitors).
**Skip:** Very local voltages (e.g., bootstraps) unless they affect traceability.

### Ground Planes
Document all ground domains separately:
```sysml
item def GroundSignal {
  doc /* Primary ground plane (DGND). */
}

item def GroundIsolated {
  doc /* Secondary/isolated ground (DGND1–DGND5). */
  attribute isolationLevel : String;
}
```

**Why:** Grounding architecture is critical for power integrity, EMI, and analog signal quality.

### Control Signals
Define primitives for single-pin signals:
```sysml
item def StartSignal {
  doc /* Acquisition trigger/frame sync. */
}

item def ResetSignal {
  doc /* Active-low reset. */
}
```

**Include:** Any signal that appears on multiple connectors or has functional significance (not just GPIO).
**Skip:** GPIO that appears once unless explicitly important.

### Multi-Pin Channels
Use composite item defs for buses:
```sysml
item def SpiChannel {
  doc /* 4-signal SPI group. */
  part cs : SpiChipSelect;
  part sclk : SpiClock;
  part sdi : SpiDataIn;
  part sdo : SpiDataOut;
}
```

**Include:** SPI (multiple instances), SAI (data + clock), UART pairs.
**Pattern:** One composite per functional unit, not per signal line.

## Connector Port Definitions

### Naming Convention
```
port def <ProductName><ConnectorLabel>Port {
  // Signal ports matching netlist names
}
```

**Examples:**
- `PatMcuHatP1McuPort` — connector P1 on PAT MCU HAT
- `PatMcuHatJQpdPort` — connector J_QPD
- `PatMcuHatJBeaconPort` — connector J_Beacon

### Signal Mapping in Comments
Include **resistor network** and **EAGLE net** references:

```sysml
port def PatMcuHatP1McuPort {
  port spi1 : HardwarePorts::SpiFourPinPort {
    port cs : HardwarePorts::GpioExpansionPort;   // !CS_1 (R18)
    port mosi : HardwarePorts::GpioExpansionPort; // SDI_1 (R17)
    port sclk : HardwarePorts::GpioExpansionPort; // SCLK_1 (R16)
    port miso : HardwarePorts::GpioExpansionPort; // SDO_1 (R15)
  }
}
```

**Format:** `// <netlist-signal-name> (<EAGLE-ref>)`

### Documentation String
Reference the EAGLE connector type, pin count, and J-label:

```sysml
doc /* 
  J1 (30-pin 5051103091 SPECIAL connector) — SPI multiplexer for 4 QPD channels.
  Pin pairs: (even) = GND, (odd) = signal.
  See 86ewy6qck netlist for full pin assignments.
*/
```

## Analysis Document Structure

**File:** `<design-code>-ANALYSIS.md`

### Sections
1. **Overview** — what the PCB does, key ICs, design status
2. **Component Summary** — BOM by category (microcontroller, analog, connectors, passives)
3. **Connector Signal Maps** — one subsection per external connector with pin table
4. **Power Distribution Network** — rails, buck converters, decoupling strategy
5. **Key Signal Connections** — MCU pins, AD9837 routes, cross-domain paths
6. **Layout & Assembly Notes** — EMI filtering, multi-layer grounding, jumper config

### Example: J1 Connector Table
| Channel | !CS | SCLK | SDI | SDO | J1 Pins | Resistors |
|---------|-----|------|-----|-----|---------|-----------|
| 1 | R18 | R16 | R17 | R15 | 2, 5, 3, 6 | 4× 10kΩ |
| 2 | R14 | R12 | R13 | R11 | 8, 11, 9, 12 | 4× 10kΩ |

## Design Attributes for `part def`

When updating an existing hardware part, add:

```sysml
attribute designRevisionCode : String = "86ewy6qck";
attribute designStatus : String = "under-design";  // or "well-design", "COTS"
attribute eagleVersion : String = "9.7.0";
attribute designDate : String = "2026-04-06";
```

These allow:
- **Traceability** — model ↔ EAGLE design version
- **Maturity tracking** — under-design can change; COTS is locked
- **Audit trail** — when netlist was last updated

## Cross-Referencing

In SysML files, use **doc comments** to link:

```sysml
doc /*
  Real PCB design (under design): 86ewy6qck (EAGLE v47, 2026-04-06)
  - NUCLEO-H753ZI (U1: STM32H753ZIT6) acquisition MCU
  - AD9837 (U2) for beacon modulation DDS
  - 4× SPI QPD interfaces via J1 (30-pin connector)
  
  See hardware/86ewy6qck-ANALYSIS.md for netlist details and signal mapping.
*/
```

In analysis docs, reference SysML:

```markdown
**SysML Integration:** `LeoLaserComm::PatMcuHat` in `pat-breakout-mcu-hat.sysml`
- Port definitions tied to J1, J5, J6 connectors below
- Signal items defined in `signals-86ewy6qck.sysml`
```

## When to Create Separate Versions

If the design has multiple significant revisions (V4, V5, V6), consider:

1. **Same signals file, versioned EAGLE files:**
   ```
   hardware/86ewy6qck-V4.{pl,scr}
   hardware/86ewy6qck-V5.{pl,scr}
   hardware/86ewy6qck-V6.{pl,scr}
   sysml-v2-models/.../signals-86ewy6qck.sysml  (references all versions)
   ```

2. **Or, separate signals files per version** (if connectors changed):
   ```
   sysml-v2-models/.../signals-86ewy6qck-V5.sysml
   sysml-v2-models/.../signals-86ewy6qck-V6.sysml
   config.yaml: (selects active version)
   ```

**Recommendation:** Use version 1 (separate EAGLE, unified signals) unless connectors fundamentally changed.
