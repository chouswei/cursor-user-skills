# Ground Architecture Review — FP-Derived Checklist

## Bedrock Principles

- **Return path impedance (Z = R + jωL):** Resistance + inductance; high impedance = noise
- **Loop area minimization:** Inductance ∝ loop area; smaller loop = lower di/dt noise
- **Current continuity:** All return currents must find path back to source
- **Star point:** Single-point reference at lowest impedance (optimal at low freq)

## User Inputs (Example: AGND ≠ DGND, isolation > 60dB @ 1MHz)

**From user:**
- Ground separation: Analog vs Digital (AGND ≠ DGND)
- Isolation requirement: 60dB @ 1MHz (implies crosstalk < 1mV from 1V source)
- Critical signals: Which nets switch fast (high di/dt)?
- Board stack-up: How many layers? Planes available?

**Derived constraints:**
- Return path impedance: Z_return < 10mΩ (typical rule: < voltage_budget / critical_current)
- Star point location: Lowest impedance node = PSU bulk cap or isolated power entry
- Ground separation: Physical distance or shielding needed to achieve 60dB isolation
- Critical traces: High di/dt nets (SPI clock, PWM, LVDS) must be isolated from analog return

## Checklist (Principle-Traceable)

### Ground Planes

- [ ] **Continuous GND plane(s):** No gaps or slots that break current paths
  - Examine PCB layer stack-up
  - Evidence: PCB design file or layer image
  - **Falsification:** Isolated GND regions (e.g., slot cutting plane in half)

- [ ] **Plane stitching (via stitching):** Vias connect planes if multi-layer
  - Via spacing: < 50mm between vias to maintain continuity at high freq
  - Evidence: Via map in PCB layout
  - **Falsification:** Via spacing > 100mm

### AGND vs DGND Separation

- [ ] **Physical separation or shielding:** Prevent coupled noise
  - Option A: Separate planes (AGND plane separate from DGND plane)
  - Option B: Single plane with isolation trace (< 5mm gap between zones)
  - Option C: Shield trace between zones
  - Evidence: PCB layer image with annotated zones
  - **Falsification:** AGND and DGND traces intermingled with no isolation

- [ ] **Isolation return point:** One star point (or two if fully isolated)
  - For isolated system: Star point = isolated PSU return node
  - For shared system: Star point = PSU bulk cap return (single point for lowest impedance)
  - Evidence: Schematic or PCB layout pointing to star point location
  - **Falsification:** Multiple return paths at same voltage level (bottleneck)

- [ ] **Return path continuity (AGND → PSU GND):** Trace all analog return current
  - Start: Analog IC GND pin
  - Path: Through GND trace or plane back to PSU return
  - Impedance: Measure or calculate trace R + plane R < 10mΩ
  - Evidence: Schematic trace or PCB continuity check
  - **Falsification:** No dedicated return path (relies on shared trace)

- [ ] **Return path continuity (DGND → PSU GND):** Same as above, separate path from AGND
  - Evidence: Schematic + PCB showing DGND path distinct from AGND
  - **Falsification:** DGND and AGND sharing return traces

### High di/dt Current Isolation

- [ ] **Identify high di/dt nets:** Switching supplies, clock lines, PWM, LVDS
  - Example: SPI clock @ 10MHz with 2A output → di/dt ≈ 2A / 10ns ≈ 200 A/µs
  - Return loop inductance couples noise
  - Evidence: Schematic annotation or design spec
  - **Falsification:** High-speed nets mixed with analog traces on same layer

- [ ] **Isolation strategy:** Route high di/dt returns separately
  - Option A: Dedicated return plane layer
  - Option B: Star-point return (all high-speed currents return to one node, then to PSU)
  - Option C: Shielding trace around high-speed path
  - Evidence: PCB layout showing isolation
  - **Falsification:** High-speed return mixed with analog GND

### Star Point

- [ ] **Single star point identified:** Location of lowest impedance node
  - Typical location: PSU bulk capacitor return (lowest impedance)
  - Alternate: Isolated power entry (if system is isolated)
  - Evidence: Schematic + PCB location marked
  - **Falsification:** Multiple equal-priority return nodes (ambiguous star point)

- [ ] **Critical frequency calculation:** Star point ↔ multi-point transition
  - f_critical = ~1 / (L_plane × C_plane) where L, C are plane parameters
  - Below f_critical: single-point optimal; above: multi-point optimal
  - Typical PCB: f_critical ≈ 10–100 MHz
  - Evidence: Calculation or design note
  - **Falsification:** No frequency guidance (default to single-point at low freq)

---

## Residual Assumptions (Must Accept or Mitigate)

| Assumption | Risk | Mitigation |
|-----------|------|-----------|
| GND plane continuous (no manufacturing defects) | Void under plane → impedance spike | X-ray inspection or continuity test on first samples |
| Via stitching maintains low impedance | Via opens → impedance jumps | Test first samples; electrical continuity check |
| Crosstalk coupling < 1% isolation target | Mutual L/C higher than expected | Increase separation; add shielding trace if crosstalk measured |
| Plane layer thickness nominal | Thin copper → higher R | Confirm copper weight (1oz vs 2oz) with fab |
| Switching frequency stable (predictable di/dt) | If di/dt varies widely, noise varies | Design margin: assume 1.5× nominal di/dt |

---

## Falsification Tests (What Would Prove Us Wrong?)

1. **Isolation measured < 60dB @ 1MHz** → Coupling too high; increase separation or shielding
2. **Voltage ripple on AGND > 50mV** during DGND switching → Star point location suboptimal or plane gap
3. **Crosstalk on analog net > 10mV** from adjacent digital switching → Return path impedance too high; add dedicated GND trace
4. **Measured plane impedance > 50mΩ** → Via stitching gaps or plane voids

---

## Verdict Logic

- **All separation checks pass + star point clear + high di/dt isolated** → **Go**
- **1–2 isolation items yellow + fixable in layout** → **Hold**
- **Fundamental issue** (e.g., no GND plane, AGND/DGND mixed at source) → **No-go**
