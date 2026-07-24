# PCBA First Principles (Bedrock Laws)

These laws are invariant and govern all PCBA design decisions.

## 1. Power Distribution

**Kirchhoff's Current Law (KCL):** Current in = Current out at every node. No current "disappears."
- Implication: Every power rail must have a complete return path (no floating nets)

**Ohm's Law (V = I·R):** Every conducting path has nonzero resistance.
- Implication: Voltage drop across traces = I × R; must budget V_drop < spec (e.g., < 5%)

**Capacitor charging (V_ripple = I·Δt / C):** Capacitor supplies transient current when PSU cannot.
- Implication: If cap opens → ripple spikes → IC brownout

**Thermal feedback (P = I²·R):** Current dissipation in resistance creates heat, which increases resistance.
- Implication: Self-heating → runaway possible in poorly designed circuits (requires derating)

---

## 2. Ground Architecture

**Return path impedance (Z_return = R_trace + jωL_loop):** Return path has both resistance and inductance.
- Implication: Minimize loop area (L_loop ∝ area) to minimize di/dt noise

**Current continuity:** All return currents must find a path back to source. Single-point bottleneck = high impedance.
- Implication: Star point (one low-Z reference node) optimal at low freq; multi-point only above critical frequency

**Plane continuity:** Solid ground or power plane = distributed capacitance + low impedance.
- Implication: Breaks in plane (via stitching gaps, isolation slots) create impedance spikes and crosstalk

---

## 3. Signal Integrity & Isolation

**Near-end crosstalk (V_ne ≈ L_m/L_s × di/dt):** Mutual inductance couples circuits.
- Implication: Fast switching (high di/dt) → large noise on adjacent traces

**Far-end crosstalk (V_fe ≈ C_m/C_s × dv/dt):** Mutual capacitance couples circuits.
- Implication: High-speed transitions → capacitive coupling to nearby nets

**Common-mode rejection (CMRR ∝ impedance ratio):** Differential circuits reject common-mode if impedances balanced.
- Implication: Unbalanced impedances → poor CMRR → common-mode noise bleeds into signal

---

## 4. Thermal

**Junction temperature (T_j = T_ambient + P·θ_ja):** Heat dissipation raises IC junction temperature.
- θ_ja = thermal resistance (°C/W); determined by package, board layout, airflow
- Implication: If T_j exceeds max rating → permanent damage or thermal shutdown

**Derating:** Device specs degrade with temperature (resistance increases, leakage increases).
- Implication: Design margin must account for 25°C → 55°C (or worst-case ambient)

---

## 5. EMC / Noise

**Di/dt noise (V_noise = L × di/dt):** Current spikes through inductance create voltage spikes.
- Implication: Fast switching → large noise unless inductance minimized (short traces, low ESL)

**Decoupling effectiveness (ESL, ESR, placement):** Capacitor must respond quickly to transients.
- ESL (equivalent series inductance) dominates at high freq; ESR (equivalent series resistance) limits current
- Placement within 5mm of IC minimizes loop L; distant caps are ineffective at high freq
- Implication: Nominal (distant) capacitors may not decouple in practice

**Radiation:** High-impedance loops radiate; fast di/dt + large area = antenna.
- Implication: Layout with minimal loop area = lower EMI radiation

---

## Design Corollaries

| Law | → Implication for Design |
|-----|--------------------------|
| KCL | No floating nets; complete return paths |
| V=IR | Budget voltage drop; minimize trace R |
| C filtering | Decoupling mandatory; calc C from di/dt |
| Thermal runaway | Derating required; T_j margin ≥ 10°C |
| Z_return | Minimize loop area; star point placement |
| Crosstalk | Isolation by spacing or shielding; balance impedances |
| ESL/ESR | Low-ESL caps near IC; ESR trade-off (filtering vs stability) |

