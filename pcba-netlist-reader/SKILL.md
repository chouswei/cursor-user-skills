---
name: pcba-netlist-reader
description: >-
  Parse Eagle/FUSION 360 (`.scr`, `.net`, `.sch`, `.csv` BOM) and KiCad (`.scr`, `.kicad_sch`) netlists. Trace signal connectivity, cross-reference parts to datasheets via MCP, identify unresolved references and pin conflicts. **Large `.sch` files (>100KB) must be searched with grep/ripgrep, not read directly.** Pre-audit before pcba-design-reviewer gate.
metadata:
  pattern: reviewer
  specialization: netlist-validation
  domain: pcba-design
  mcp_key: pcbparts
---

# pcba-netlist-reader

Audit KiCad or Eagle netlists + BOM for connectivity and completeness before design review.

## Workflow (5 steps, ~150 tokens)

| Step | Action | Inputs | Outputs |
|------|--------|--------|---------|
| 0 | **Intake** | Ask: netlist file path (`.scr`/`.net`), parts list (`.csv`/`.txt`), signals to trace (optional) | User inputs |
| 1 | **Format check** | Load `references/netlist-formats.md` | Format specs (Eagle vs KiCad) |
| 2 | **Parse** | Extract: part references, signal nets, pin assignments from files | Parsed data (part list, signals) |
| 3 | **Cross-ref** | Call MCP: `jlc_get_pinout`, `board_get`, `jlc_find_alternatives` for each part | Pinout specs, alternatives |
| 4 | **Report** | Generate: signal trace table, BOM checklist, unresolved parts, pin conflicts | Go/no-go audit report |

## Output Format

**Signal trace table:**
- Net name | Components | Pin assignments | Status (resolved/unresolved/conflict)

**BOM audit:**
- Part ref | Datasheet link | Stock status | Alternatives (if any)

**Findings:**
- Unresolved parts (in netlist but not in BOM, e.g., "U1 mystery device")
- Pin conflicts (same signal on incompatible pins)
- Missing components

**Recommendation:** → pcba-design-reviewer (design gate)

## Handling Large Schematic Files (.sch)

**`.sch` files (EAGLE schematic XML) can exceed 100KB and contain thousands of lines.**

### ❌ **DO NOT:**
- Try to read entire `.sch` file into LLM context
- Use `cat`, `head`, `tail`, `Read` tool on large `.sch` files
- Attempt pattern matching on full file content

### ✅ **DO:**
- Use **`grep` / `ripgrep` (`rg`)** to search for specific patterns:
  ```bash
  grep "J1\|J2\|J3\|P1" design.sch
  rg "Signal.*TX\|Signal.*RX" design.scr
  rg "pinref.*J11\|part.*J11" design.sch
  ```
- Search for **specific connector labels** (`J1`, `P1`, `RPI`, `HAT`, etc.)
- Search for **signal names** (UART, SPI, I2C, GND, power pins)
- Extract **relevant context** (10-20 lines around matches) using `-A`, `-B` flags
- Read only the **extracted sections** (~50-100 lines), not the whole file

**📖 Full guide:** See [EAGLE-FILES-ANALYSIS-GUIDE.md](../../hardware/EAGLE-FILES-ANALYSIS-GUIDE.md) for complete analysis workflow, file reading strategy matrix, and advanced grep patterns for `.pl`, `.scr`, `.sch`, and `.nl` files.

## Pairing

- **Before:** No prerequisite
- **After:** pcba-design-reviewer (gate readiness)

## MCP Tools Used

- `jlc_get_pinout` — pinout for part number
- `board_get` — reference board schematics
- `jlc_find_alternatives` — cross-reference parts
