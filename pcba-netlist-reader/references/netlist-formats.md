# KiCad and Eagle Netlist Formats

## Eagle (FUSION 360)

### `.scr` (Script file — netlist)

**Structure:**
```
Signal <signal_name>
  <part_ref> <pin>
  <part_ref> <pin>
  ...
```

**Example:**
```
Signal +12V
  U1 5
  C1 1
  PS1 3

Signal GND
  U1 2
  C1 2
  R1 1
```

**Parsing:**
- Each `Signal` line starts a net
- Subsequent indented lines are connections (part_ref pin)

### `.pl` (Part list — BOM)

**Structure:**
```
Part <part_ref> <value> <device> <package>
```

**Example:**
```
Part U1 LM358 OPAMP SOIC8
Part C1 100µF CAP CHIP0805
Part R1 10k RES CHIP0603
```

**Parsing:**
- Each `Part` line = one component
- Columns: reference | value | device | package

### `.csv` BOM Export

**Common format:**
```
Reference,Value,Datasheet,MPN,Qty
U1,LM358,http://...,LM358N,1
C1,100µF,http://...,GRM21BR61C107KA12L,1
R1,10k,http://...,ERJ-6ENF1002V,1
```

**Parsing:** Standard CSV; columns vary by export tool

---

## KiCad

### `.scr` (Netlist script)

**Structure:** Similar to Eagle (text-based)

**Example:**
```
(signal +12V
  (pin U1 5)
  (pin C1 1)
)
```

**Parsing:** S-expression format; parse signal name + pin pairs

### `.kicad_sch` (Schematic file)

**Format:** Custom KiCad text format (not recommended for automated parsing; use `.net` or `.csv` instead)

### `.net` (Netlist export)

**Structure:**
```
(net (code 1) (name +12V)
  (node (ref U1) (pin 5))
  (node (ref C1) (pin 1))
)
```

**Parsing:** S-expression; extract net name, nodes (ref, pin)

---

## Cross-Reference with pcbparts MCP

**For each part in BOM:**
1. Extract MPN (datasheet MPN, not internal reference)
2. Call `jlc_get_pinout(MPN)` → pinout diagram (verify pin assignments in netlist match datasheet)
3. Call `jlc_find_alternatives(MPN)` → alternates (stock, cost)
4. Call `board_get(IC_name)` → reference schematics (learn best practices)

**Example flow:**
- Netlist: "U12 pin 6 on DGND"
- BOM: U12 = "TCA9548A I2C Mux"
- `jlc_get_pinout("TCA9548A")` → Pin 6 is A0 address input
- **Finding:** U12 A0 on DGND → I²C address 0x60 ✓ (confirms V6 audit fix)
