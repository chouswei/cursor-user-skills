# Signal Isolation Review — FP-Derived Checklist

## Bedrock Principles

- **Near-end crosstalk (V_ne ≈ L_m/L_s × di/dt):** Mutual inductance between loops couples noise
- **Far-end crosstalk (V_fe ≈ C_m/C_s × dv/dt):** Mutual capacitance couples noise
- **Common-mode rejection (CMRR ∝ Z_+ / Z_−):** Unbalanced impedances degrade CMRR
- **Return path impedance (Z = R + jωL):** High impedance → noise injection

## User Inputs (Example: I²C isolation 60dB, differential SPI < 100mV crosstalk)

**From user:**
- Signal type: Single-ended (I²C, RS-485) or differential (LVDS, CAN)
- Isolation target: dB (CMRR requirement) or mV (crosstalk limit)
- Critical nets: Which signals must not interfere? (e.g., ADC input vs PWM return)
- PCB environment: EMI source nearby? (switching supply, high di/dt)

**Derived constraints (Example: I²C 60dB CMRR):**
- Crosstalk induced voltage: V_crosstalk = CMRR_target × V_common_mode / 1000
  - If V_common = 5V, CMRR_target = 60dB (1000:1) → V_crosstalk_max = 5mV
- Mutual inductance coupling: V_ne = L_m/L_s × di/dt; must keep < 5mV
  - Example: di/dt = 1A/10ns = 100 A/µs; L_s ≈ 3nH (single IC pin); L_m < 1pF → need separation
- Mutual capacitance coupling: V_fe = C_m/C_s × dv/dt; must keep < 5mV
  - Example: dv/dt = 3V/10ns = 300 V/µs; C_m = 1pF @ 1mm spacing; need > 5mm or shielding

## Checklist (Principle-Traceable)

### Single-Ended Signals (I²C, RS-485, SPI, etc.)

- [ ] **Net separation:** Critical nets > 5mm from high di/dt nets
  - Measure on PCB layout
  - High di/dt: SPI clock, PWM output, switching supply switching node
  - Evidence: PCB layer image with measurements
  - **Falsification:** Spacing < 2mm

- [ ] **Return path for critical signal:** Each signal has dedicated return (not shared with switching supply)
  - Example: ADC input GND → star point (not through SPI return)
  - Evidence: Schematic tracing
  - **Falsification:** ADC GND shared with DGND (high di/dt return)

- [ ] **Shielding (if needed):** Ground trace or plane between critical signal and noise source
  - Ground shield connects to star point or local GND plane
  - Evidence: PCB layer showing shield trace
  - **Falsification:** No shielding, tight spacing

### Differential Signals (LVDS, CAN, RS-485 diff pair)

- [ ] **Impedance matching:** Both lines (+ and −) must have equal impedance to GND
  - Typical: Z+ ≈ Z− ± 5% for good CMRR
  - Measure or simulate using PCB stack-up and trace geometry
  - Evidence: PCB impedance simulation or measurement
  - **Falsification:** Z+ and Z− differ > 10%

- [ ] **Length matching:** + and − traces equal length (avoid phase skew)
  - Max skew: < λ/20 at highest freq (λ = wavelength in PCB)
  - Example: 1GHz LVDS → λ ≈ 30cm in PCB → max skew < 1.5cm
  - Measure: Trace length in layout (diff pair router auto-matches in most EDA tools)
  - Evidence: PCB routing report or screenshot showing length match
  - **Falsification:** Length mismatch > 2cm

- [ ] **Spacing from other signals:** Diff pair isolated from high-noise nets
  - Minimum spacing: > 3 × (trace separation within pair)
  - Example: Diff pair traces 10mil apart → spacing from others > 30mil
  - Evidence: PCB layer image with measurements
  - **Falsification:** Other signals < 10mil from diff pair

- [ ] **Return path for diff pair:** Common-mode return (GND) must be local
  - Vias to GND plane spaced every 1/4 wavelength or < 5mm (whichever is smaller)
  - Evidence: PCB showing via placement
  - **Falsification:** Vias > 10mm apart

- [ ] **Termination (if applicable):** Series termination (source) or parallel termination (load)
  - LVDS: typically 100Ω series, 100Ω parallel load (standard)
  - RS-485: 120Ω termination at both ends (twisted pair impedance)
  - Evidence: Schematic showing termination resistors
  - **Falsification:** Missing or incorrect termination resistor value

### ADC/DAC Isolation

- [ ] **Analog signal ≠ Digital GND:** Separate return paths AGND and DGND
  - Analog input traces → AGND return (isolated from digital switching)
  - Digital output traces → DGND return (separate from analog)
  - Evidence: Schematic + PCB routing showing separation
  - **Falsification:** Analog signal return routed through DGND

- [ ] **Reference voltage shielded:** Analog reference (VREF) isolated from noise
  - VREF trace shielded or routed on separate layer away from high-speed nets
  - Decoupling caps close to VREF input (within 5mm)
  - Evidence: PCB showing VREF path
  - **Falsification:** VREF adjacent to clock or switching supplies

- [ ] **Input filtering:** Low-pass RC or LC filter on ADC input (if noisy environment)
  - Cutoff frequency: f_c < signal bandwidth but > Nyquist × 2
  - Example: 10kHz signal → f_c = 20–50kHz; R·C = 1/(2πf_c)
  - Evidence: Schematic showing filter
  - **Falsification:** No filter or cutoff too high (attenuates signal)

---

## Residual Assumptions (Must Accept or Mitigate)

| Assumption | Risk | Mitigation |
|-----------|------|-----------|
| PCB stack-up & trace geometry match design intent | Variation → actual impedance differs | Impedance test or simulation with actual stack-up |
| Mutual inductance/capacitance match book values | Real coupling may be higher | Crosstalk test with first prototype |
| Shielding trace not broken | Break → loss of shielding effectiveness | Continuity test on all shield vias/traces |
| Return path inductance negligible at signal freq | At high freq, inductance dominates | Use local GND vias; keep return path < 10mm |
| Termination resistor value exact | Tolerance affects CMRR and signal integrity | Use 1% tolerance (E24 series) resistors |

---

## Falsification Tests (What Would Prove Us Wrong?)

1. **Crosstalk measured > 10mV** on sensitive net (e.g., ADC input) → Separation inadequate or return path noisy
2. **CMRR measured < 60dB** (differential signal) → Impedance mismatch or termination error
3. **Signal integrity eye diagram shows jitter > 10%** (high-speed signal) → Crosstalk or impedance mismatch
4. **ADC reading drifts during PWM switching** → Insufficient filtering or AGND/DGND coupling

---

## Verdict Logic

- **All separation checks pass + matched impedances (if diff) + isolated returns** → **Go**
- **1–2 items yellow (e.g., slightly tight spacing) + can be addressed in revision** → **Hold**
- **Fundamental issue** (e.g., ADC return through digital GND, no termination) → **No-go**
