# De Facto PCBA-to-SysML Alignment: Skill Improvement Guide

## Problem Statement

When modeling PCBAs for SysML v2 designs, there is a **systematic gap between conceptual port definitions and ground-truth hardware netlist data**. Without rigorous netlist parsing discipline, the model remains **incomplete, inferential, and disconnected from actual design intent**.

**Key Failure Modes Observed:**
- Incomplete port discovery (e.g., I2C1 enabled in CubeMX but overlooked in SysML)
- Missing signal conditioning details (resistor references, jumper logic, fanout patterns)
- Uncertain resistor network assignments (which signals, which pins, correct R-values?)
- Unverified MCU pin mappings (assumed alt-function vs. confirmed from CubeMX .ioc)
- No traceability from SysML doc comments back to netlist line numbers

## De Facto Alignment Workflow (Systematic)

### Phase 1: Inventory All Connectors & Signals

**Input:** EAGLE design files (`.pl`, `.scr`, `.sch`)

**Steps:**
1. Read **`.pl` (parts list)** — extract all J# connectors, their packages, and component references
2. Grep **`.scr` (netlist)** for all J# signals — identify pin-level connectivity
3. For each J#, build a **pin-to-signal map** (e.g., J1-2 = !CS_1, J1-3 = SDI_1, etc.)
4. Cross-index resistor and jumper networks on each signal

**Deliverable:** Connector pinout inventory (example below)

```
J1 (30-pin):
  Pin 1: DGND
  Pin 2: !CS_1 (via R18) ← PA4
  Pin 3: SDI_1 (via R17) ← PG11
  Pin 5: SCLK_1 (via R16) ← PD7 [also JP2-3]
  Pin 6: SDO_1 (via R15) ← PG9 [also JP1-3]
  ...
```

### Phase 2: Extract Resistor & Jumper Networks

**Input:** Netlist signals and signal conditioning details

**Process:**
1. For each signal N$# on a connector pin, trace backwards through resistors:
   - `N$9 ← J2-2` means the signal N$9 appears on J2 pin 2
   - `N$9 ← R23[1]` means pin 1 of resistor R23 connects to this signal
   - `R23[2] ← ?` identifies the other end (e.g., MCU pin PA5)

2. Document jumper selectors (JP1, JP2, JP3, JP5, JP9):
   - Which signals they affect?
   - What are the "1" and "2" configuration options?
   - Current netlist: is the jumper connected or open?

3. Verify resistor values and functions:
   - 0Ω (short): impedance matching / routing
   - 22Ω: level protection, series termination
   - 10K: pull-up/pull-down

**Deliverable:** Signal-to-resistor matrix (example below)

```
SPI6_SCK:
  Path: MCU PA5 (CN12_11) ← R23[2] ← N$9 ← J2-2
  Resistor: R23 (series conditioning, assumed 0Ω)
  Jumper: (none)
  
SPI1_SCK_1:
  Path: MCU PD7 (CN11_45) ← R16[2] ← SCLK_1 ← JP2-3, J1-5
  Resistor: R16 (0Ω impedance)
  Jumper: JP2 connects SCLK_1 path (position 2 likely closes, position 1 open?)
```

### Phase 3: Cross-Reference CubeMX Configuration

**Input:** STM32CubeMX `.ioc` file

**Steps:**
1. Extract pin mode and signal assignments:
   - `PB6.Mode=I2C` → `PB6.Signal=I2C1_SCL`
   - `SPI6.Mode=SPI_MODE_SLAVE` → `SPI6.VirtualType=VM_SLAVE`
   - `UART5.IPParameters=...` → extract baud rate, data format

2. Build MCU peripheral manifest:
   - Which SPIs are masters vs. slaves?
   - Which UARTs are active?
   - Are there alternate peripherals?

3. Verify alignment:
   - Does CubeMX PA5 = SPI6_SCK match netlist SPI6_SCK?
   - If not, flag as **design mismatch** (CubeMX vs. PCB netlist conflict)

**Deliverable:** MCU Peripheral Mapping (example below)

```
STM32H753 (CubeMX v11 26_4_8.ioc):
  SPI1: Master
    PA4(NSS) → J1-2 [!CS_1]
    PD7(SCK) → J1-5 [SCLK_1]
    PG11(MOSI) → J1-3 [SDI_1]
    PG9(MISO) → J1-6 [SDO_1]
  
  SPI6: Slave
    PA5(SCK) ← J2-2 [SPI6_SCK from PolarFire master]
    PG12(MISO) → J2-6 [SPI6_MOSI out]
    PG14(MOSI) ← J2-4 [SPI6_MISO in from PolarFire]
    PG8(NSS) ← J2-8 [SPI6_NSS from PolarFire]
  
  UART5: Asynchronous (921600 bps, 8N1)
    PC12(TX) → J2-10 [UART5_TX]
    PD2(RX) ← J2-12 [UART5_RX]
```

### Phase 4: Build SysML Port Definitions

**Input:** Inventories from Phases 1–3

**Guidelines:**

1. **Each port `doc` block MUST contain:**
   - Exact connector name/package (J#, package code)
   - Complete pin-to-signal map (all pins, not just active ones)
   - Signal conditioning (resistor references, jumper logic)
   - MCU pin assignments (from CubeMX)
   - EAGLE netlist references (line numbers in `.scr`, signal names N$#)
   - CubeMX peripheral config (mode, baud rate, etc.)

2. **Each port sub-element MUST reference:**
   - EAGLE signal name (e.g., SDI_1, SPI6_SCK, UART5_TX)
   - Resistor path (e.g., "PG11 R17[2]→J1-3")
   - CubeMX alt-function (e.g., SPI1_MOSI, I2C1_SDA)

3. **Port discovery process:**
   - Start with `.pl` (connector list) — how many connectors exist?
   - Check `.scr` for every J# signal — is there a port for it?
   - Cross-reference CubeMX — is every enabled peripheral exposed?
   - Ask: Is this connector meant to be external (for users) or internal (on-HAT only)?

**Example:**
```sysml
port def PatMcuHatP1McuPort {
  doc /*
    **[J1 - P1_MCU]** 30-pin Samtec TSW-108 on 86ewy6qck v78.
    
    **Netlist mapping (86ewy6qck.scr):**
      J1-2:  !CS_1   ← R18[2] ← PA4 (CN11_32) via Signal '!CS_1' line 8
      J1-3:  SDI_1   ← R17[2] ← PG11 (CN11_70) via Signal 'SDI_1' line 906
      ...
    
    **CubeMX (STM32CubeMX v11 26_4_8.ioc):**
      PA4.Mode=NSS_Signal_Hard_Output, PA4.Signal=SPI1_NSS
      ...
  */
  port spi1 : HardwarePorts::SpiFourPinPort {
    port cs : HardwarePorts::GpioExpansionPort;  // !CS_1 (PA4 R18[2]→J1-2)
    ...
  }
}
```

### Phase 5: Validate & Iterate

**Steps:**
1. Run SysML v2 MCP `validate` — all grammar/import errors resolved?
2. Cross-check: For every external connector (J#), is there a port instance?
3. Verify resistor counts:
   - Expected R1–R18 for J1? Count all `.scr` references.
   - Missing or unexpected resistors? Flag for design review.
4. Ask: Are all enabled CubeMX peripherals exposed or internal?

## Checklist: De Facto Alignment Verification

- [ ] All connectors from `.pl` have SysML port definitions?
- [ ] Every active signal in `.scr` is traced back to a MCU pin?
- [ ] Resistor references match between model doc and `.scr` line numbers?
- [ ] CubeMX peripheral modes (Master/Slave/Disabled) match model assumptions?
- [ ] I2C/SPI/UART baud rates and config match CubeMX settings?
- [ ] Jumpers (JP#) documented with their configuration and effect?
- [ ] Ground distribution (GND pin count, star topology) noted?
- [ ] Power supply pins (±3V3, ±5V, ±12V) and regulatory devices (L#, C#) referenced?
- [ ] SysML model validates with zero diagnostics?

## Key Lessons Learned

### Lesson 1: Netlist is Source of Truth
- **Never assume** port connectivity based on conventions.
- **Always extract** from `.scr` and `.pl` files.
- When in doubt, search for the signal name in `.scr` (e.g., `grep "SCLK_1"` shows all references).

### Lesson 2: CubeMX ↔ Netlist Reconciliation
- CubeMX `.ioc` defines **intended** MCU usage (mode, baud, alt-function).
- EAGLE `.scr` defines **actual** PCB connectivity (which pins really go to which connectors).
- If they disagree → **design mismatch** (e.g., SPI6 assigned but not routed).

### Lesson 3: Resistor Networks Are Part of the Interface
- Don't document "PG12 → J2 pin 6" alone.
- Document the full path: "PG12 (CN11_65) ← R29[2] ← N$13 ← J2-6".
- This traceability prevents unexpected signal integrity issues later.

### Lesson 4: Hidden Interfaces (Internal-Only)
- I2C1 enabled in CubeMX but J9 reserved → **internal interface only**.
- Don't create physical ports for internal interfaces unless they have on-HAT I2C devices.
- Document this decision explicitly in the model.

### Lesson 5: Jumper Selectors Require Site Knowledge
- JP1, JP2, JP3, JP5, JP9: What is the **current configuration**?
- Is this configurable (user selects), or factory-set?
- Model the **de facto** (current) setup, not all possibilities.

## Recommended Tool Chain

1. **EAGLE file reading:** Use provided `EAGLE-FILES-ANALYSIS-GUIDE.md`
   - `.pl` → read entire file (small)
   - `.scr` → read entire file (medium, ~1KB)
   - `.sch` → use `grep`/`ripgrep` only (large XML, 100KB+)

2. **CubeMX `.ioc` parsing:** Text editor + grep for peripheral assignments
   - Search `SPI6.Mode=`, `UART5.IPParameters=`, `PB6.Signal=`, etc.

3. **SysML modeling:** Follow port definition template (Phase 4 above)

4. **Validation:** SysML v2 MCP `validate` + manual checklist

## Future Skill Improvements

1. **Automated netlist-to-SysML generator:** Python script consuming `.scr` + `.ioc` → generates port templates
2. **Netlist diff alerter:** Detect when EAGLE netlist changes break SysML model assumptions
3. **CubeMX→SysML sync:** Periodically regenerate port definitions from CubeMX exports
4. **Jumper configurator:** UI/CLI to toggle JP# settings and auto-update model

---

**Version:** 1.0  
**Date:** 2026-04-08  
**Author:** De facto alignment workflow (after MCU HAT rebuild)  
**Status:** Active — used for `pat-breakout-mcu-hat.sysml` v78 netlist traceability
