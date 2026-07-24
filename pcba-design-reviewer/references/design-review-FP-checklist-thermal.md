# Thermal Budget Review — FP-Derived Checklist

## Bedrock Principles

- **Junction temperature (T_j = T_a + P·θ_ja):** Dissipation raises IC internal temperature
  - θ_ja = thermal resistance (°C/W); determined by package, layout, airflow
- **Thermal runaway (dP/dT > 0):** Some devices get worse as they heat (positive feedback)
  - Resistance increases with temp → more dissipation → more heat → runaway (needs derating)
- **Derating:** Device specs degrade at elevated temperature
  - Leakage current increases; maximum clock frequency decreases; noise margin shrinks

## User Inputs (Example: LM358 op-amp + DSP in SMD, 25°C lab ambient)

**From user:**
- Ambient temperature: 25°C typical (or 55°C worst-case industrial)
- PCB thermal conditions: Free air convection, or with heatsink/fan?
- Operating profile: Continuous or intermittent?
- Critical ICs: Which devices have tight thermal margins?

**Derived constraints (Example: LM358 @ 25°C ambient, free air):**
- Max junction temperature: T_j,max = 150°C (from datasheet)
- Thermal resistance (air): θ_ja ≈ 200°C/W (typical 8-pin DIP or SOIC, free air)
- Power dissipation budget: P_max = (T_j,max − T_ambient) / θ_ja = (150 − 25) / 200 = 0.625W
- Worst-case (55°C ambient): P_max = (150 − 55) / 200 = 0.475W (lower margin!)
- **Design margin:** Keep actual P < 50% of P_max for derating headroom

## Checklist (Principle-Traceable)

### Device Selection & Derating

- [ ] **Operating temperature range specified:** Device rated for intended ambient?
  - Standard: 0–70°C commercial (lab/office)
  - Industrial: −40–85°C
  - Automotive: −40–125°C
  - Evidence: Datasheet operating range
  - **Falsification:** Commercial device in −40°C environment (outside spec)

- [ ] **Derating curve applied:** Power dissipation derated with temperature
  - Most datasheets show P_max(T) curve
  - At 55°C, typical derating = 50% of 25°C rating
  - Evidence: Datasheet derating table or curve applied to design calculation
  - **Falsification:** Using 25°C rating at 55°C ambient

### Power Dissipation Calculation

- [ ] **Power per IC identified:** Sum of I·V for all rails
  - Example: Op-amp with ±12V supply, 100mA output → P = I_supply · V_supply
  - Detailed: P = (I_quiescent × V_supply) + (I_output · V_load); often manufacturer spec provides P_dissipation
  - Evidence: Datasheet specs + design calculations
  - **Falsification:** Power calculation missing or wrong units

- [ ] **Total board dissipation budgeted:** Sum of all IC power
  - Example: 5 ICs at 0.5W each = 2.5W total
  - Evidence: Power budget table in design doc
  - **Falsification:** No power budget summary

- [ ] **Margin applied:** Design power ≤ 50% of max rating
  - At 50%, device has room for temp derating and variation
  - Example: IC rated 1W at 25°C → design target P ≤ 0.5W
  - Evidence: Design note stating margin assumption
  - **Falsification:** Operating at 100% of rating (no margin)

### Thermal Resistance Assessment

- [ ] **Thermal resistance (θ_ja) from datasheet:** Package-dependent value
  - Examples:
    - 8-pin DIP (through-hole): θ_ja ≈ 200–300°C/W
    - SOIC-8 (SMD, free air): θ_ja ≈ 150–200°C/W
    - BGA (large, with plane): θ_ja ≈ 30–60°C/W
  - Evidence: Datasheet thermal specs
  - **Falsification:** θ_ja not checked or wrong package assumed

- [ ] **PCB thermal conditions matched:** Layout decision affects θ_ja
  - Free air convection: Use θ_ja from datasheet
  - With copper plane under IC: θ_ja improved by 20–40% (typical)
  - With heatsink: θ_ja significantly reduced (must model)
  - Evidence: Design note stating thermal design (plane? heatsink?)
  - **Falsification:** No PCB thermal planning

### Temperature Margin

- [ ] **Junction temperature calculated:** T_j = T_ambient + P · θ_ja
  - Example: T_a = 55°C (worst-case), P = 0.3W, θ_ja = 150°C/W
  - T_j = 55 + 0.3 × 150 = 100°C
  - Evidence: Calculation in design doc
  - **Falsification:** T_j not calculated

- [ ] **Margin to max rating ≥ 10°C:** Headroom for variation and transients
  - T_j,max − T_j ≥ 10°C
  - Example: T_j,max = 150°C, T_j = 100°C → margin = 50°C ✓
  - Evidence: Design note stating margin
  - **Falsification:** T_j only 5°C below max (too tight)

- [ ] **Worst-case ambient used:** Not nominal 25°C
  - Worst-case: 55°C (industrial), −40°C (cold-start), or 125°C (vehicle interior)
  - Evidence: Design assumes specified worst-case ambient
  - **Falsification:** Design uses 25°C only (ignores extremes)

### Thermal Runaway Risk

- [ ] **Runaway check (if applicable):** Devices with positive dP/dT
  - Examples: Some diodes, resistors, BJTs increase P with temp
  - Most IC controllers have stable or negative dP/dT (OK)
  - Evidence: Datasheet I-V curves at multiple temps
  - **Falsification:** Runaway-risk device used without derating

- [ ] **Temperature coefficient reviewed:** Rate of spec change with temp
  - Example: Op-amp offset voltage temp coeff = 5µV/°C (small effect)
  - Op-amp input bias current doubles every ~50°C (larger effect at high T)
  - Evidence: Datasheet temp coeff table
  - **Falsification:** Temp coeff not reviewed; spec assumed constant

### Heatsinking (if needed)

- [ ] **Heatsink required?** Check if T_j exceeds acceptable even with derating
  - If T_j,max − T_j < 10°C margin, add heatsink or reduce P
  - Heatsink θ_sink (IC to ambient) = θ_junction_case + θ_case_sink + θ_sink_ambient
  - Evidence: Thermal calculation or prototype testing
  - **Falsification:** Inadequate cooling; T_j exceeds spec

- [ ] **Heatsink material & mounting:** Thermal path from IC to sink
  - Thermal interface: thermal paste or pad (typical 1–5°C/W)
  - Mounting: Screwed or glued? Pressure contact?
  - Evidence: Heatsink assembly drawing or photo
  - **Falsification:** Loose mounting; air gap between IC and sink

---

## Residual Assumptions (Must Accept or Mitigate)

| Assumption | Risk | Mitigation |
|-----------|------|-----------|
| Ambient exactly as specified (no local hotspots) | Component in enclosed box → T_a > ambient | Thermal simulation or prototype temp measurement |
| Datasheet θ_ja applies to actual PCB layout | Layout without plane or poor soldering → higher θ_ja | X-ray inspection; thermal test on first samples |
| Power dissipation steady-state (not transient spikes) | Brief high-power events → local T_j spike | Check transient I-V curves in datasheet; use peak power if spike-dominated |
| Derating factor conservative | Actual device may be less sensitive | Use datasheet derating curve; test is best |
| All thermal calculations correct (formula, units) | Math error → overestimated margin | Double-check units (°C/W, W, °C); use calculator or spreadsheet |

---

## Falsification Tests (What Would Prove Us Wrong?)

1. **Measured IC junction temperature > T_j,max** → Thermal model wrong; heatsink needed or power must be reduced
2. **IC spec drift with time** (offset voltage, bias current increase) → Temperature too high; derating insufficient
3. **Device shutdown or latch-off during operation** → Thermal throttling activated; operating beyond design margin
4. **Thermal image shows IC > 20°C above neighboring components** → Concentrated hotspot; likely transient power spike or poor thermal contact

---

## Verdict Logic

- **T_j ≤ T_j,max − 10°C (all ICs, worst-case ambient) + derating applied** → **Go**
- **T_j ≤ T_j,max − 5°C or no derating margin reviewed** → **Hold** (add heatsink or reduce clock speed)
- **T_j > T_j,max or no thermal analysis done** → **No-go** (design must change)
