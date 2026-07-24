# Power Distribution Review — FP-Derived Checklist

## Bedrock Principles

- **Kirchhoff's Current Law (KCL):** Current must flow continuously, no sinks or sources
- **Ohm's Law (V=IR):** Every trace has nonzero resistance; voltage drop = I × R
- **Capacitor filtering (V_ripple = I·Δt / C):** Capacitors supply transient current
- **Thermal feedback (P=I²·R):** Self-heating can cause runaway

## User Inputs (Example: ±12V ±5%, 2A max)

**From user:**
- Rail voltage: ±12V
- Tolerance: ±5%
- Max current: 2A
- Load profile: transient or steady?

**Derived constraints:**
- Voltage drop budget: 5% × 12V = **0.6V max**
- Max trace resistance: R_max = 0.6V / 2A = **0.3Ω**
- Decoupling time constant: τ = L·C, must settle in < 100ns (user specifies or assume)
- Bulk capacitor: V_ripple = I·Δt / C → C_bulk = 2A × 50ns / 0.5V = **200µF minimum**

## Checklist (Principle-Traceable)

### Power Traces

- [ ] **Trace resistance < 0.3Ω**
  - Measure (via 4-point LCR) or calculate: R = ρ·L / (W×T)
    - ρ = copper resistivity (1.7×10⁻⁸ Ω·m)
    - L = trace length (mm), W = width (mm), T = thickness (oz/35µm)
  - Evidence: KiCad trace calc or lab measurement
  - **Falsification:** Measured R > 0.4Ω

### Decoupling Capacitors (Near IC)

- [ ] **Placement:** Within 5mm of IC power pins (minimize loop L)
  - Measure on PCB layout or schematic
  - Evidence: PCB screenshot with dimensions
  - **Falsification:** Caps > 10mm from IC

- [ ] **ESL < 100pH:** Low equivalent series inductance for high-freq response
  - Check datasheet (e.g., Samsung, Murata specs list ESL)
  - Typical: 0603 ceramics ≈ 50pH, 0805 ≈ 80pH
  - Evidence: Capacitor datasheet ESL column
  - **Falsification:** ESL > 150pH

- [ ] **ESR < 10mΩ:** Low equivalent series resistance for current handling
  - Check datasheet ESR @ 1MHz
  - Typical: 0603 ceramic ≈ 5mΩ
  - Evidence: Capacitor datasheet
  - **Falsification:** ESR > 20mΩ

- [ ] **Minimum count:** One decoupling cap per 2-3 IC power pins
  - Example: 8-pin IC (2 power pins) → 1 cap minimum, 2 recommended
  - Evidence: BOM count
  - **Falsification:** Fewer than 1 per 3 pins

### Bulk Capacitor (PSU Entry)

- [ ] **Capacitance ≥ 200µF** (derived from V_ripple budget)
  - Check BOM value
  - Evidence: Component datasheet
  - **Falsification:** C < 150µF

- [ ] **Placement:** Near PSU input connector or regulator output
  - Measure on layout
  - Evidence: PCB screenshot
  - **Falsification:** > 20mm from PSU entry

- [ ] **ESR < 50mΩ:** Controls ripple voltage (V_ripple ≈ I × ESR during transient)
  - Check datasheet; typical aluminum electrolytic ≈ 30mΩ @ 1kHz
  - Evidence: Capacitor datasheet ESR curve
  - **Falsification:** ESR > 100mΩ

### Power Vias

- [ ] **Via count ≥ 2 per power pin:** Low-resistance connection IC → PCB
  - Measure on netlist or PCB
  - One via ≈ 5–10mΩ; two vias in parallel ≈ 2.5–5mΩ
  - Evidence: Netlist or PCB layout
  - **Falsification:** 1 via per power pin

- [ ] **Via diameter ≥ 10mil (0.25mm):** Standard size; smaller = higher R
  - Check design rules
  - Evidence: PCB design rule or layout screenshot
  - **Falsification:** Via diameter < 8mil

### Return Path

- [ ] **Ground return path exists:** Every +12V current must have return to GND
  - Trace from load IC back to PSU GND pin
  - Evidence: PCB schematic or layout continuity check
  - **Falsification:** Floating net (no return path)

- [ ] **GND trace or plane:** Return path must have low impedance
  - Option A: Dedicated GND trace (measured R < 0.3Ω)
  - Option B: GND plane (continuous copper, lowest impedance)
  - Evidence: Layout screenshot or trace resistance measurement
  - **Falsification:** No dedicated GND trace or broken plane

---

## Residual Assumptions (Must Accept or Mitigate)

| Assumption | Risk | Mitigation |
|-----------|------|-----------|
| PCB copper thickness nominal (1oz/35µm) | Thin copper → higher R | Specify 2oz copper in fab notes; confirm receipt |
| No solder voids under caps | Void → open connection | X-ray inspection of mass production or sample lot |
| Capacitor ESL/ESR match datasheet nominal | Variation possible | Test first samples (LCR meter @ 1MHz) |
| 25°C ambient (no thermal derating) | At 55°C, R increases ~10% | Recalculate worst-case: R_hot = 1.1 × R_nominal |
| Capacitor leads soldered with minimal inductance | Long leads add ESL | Surface-mount (not through-hole); minimize lead length |

---

## Falsification Tests (What Would Prove Us Wrong?)

1. **Ripple voltage > 0.6V** at 2A load step → Decoupling inadequate or R too high
2. **Measured trace resistance > 0.4Ω** → Trace width or copper quality insufficient
3. **IC crashes or resets on load transient** → Voltage droop below IC min spec
4. **Thermal image shows IC > 60°C** at 25°C ambient → Excessive power dissipation or thermal resistance

---

## Verdict Logic

- **All items pass + all assumptions acceptable** → **Go**
- **1–2 items yellow (warning) + fixable** → **Hold** (resolve before layout)
- **Fundamental violation** (e.g., no decoupling caps, R_trace > 1Ω) → **No-go**
