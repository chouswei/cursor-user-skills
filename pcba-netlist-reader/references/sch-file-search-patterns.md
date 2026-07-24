# Large Schematic File (.sch) Search Patterns

## Problem

Eagle `.sch` schematic files are XML-based and can exceed **100KB+** in size (thousands of lines). Reading the entire file into LLM context is inefficient and wasteful.

**Example:** `86ex0w7kx.sch` is **491,043 characters** (~9,500 lines) - too large to read directly.

## Solution: Use Grep/Ripgrep

Always use **`grep`** or **`ripgrep` (`rg`)** to search for specific patterns, then read only the extracted sections.

```bash
# Search for connector definitions
rg "part name=\"J1\"|part name=\"J2\"|part name=\"J3\"" design.sch

# Find signal connections to specific connector
rg "pinref part=\"J11\".*pin" design.sch

# Find UART/SPI signals
rg "Signal.*TX|Signal.*RX|Signal.*UART5|Signal.*SPI6" design.scr

# Find ground star points
rg "pinref part=\"J11\".*DGND|pin=\"1\"|pin=\"3\"|pin=\"5\"" design.sch

# Find labels (e.g., "To NUCLEO-H753ZI")
rg "text.*NUCLEO|text.*MCU|text.*interHat" design.sch
```

## Common Search Patterns

### Connectors & Headers

```bash
# All J connectors
rg "part name=\"J[0-9]" design.sch

# Specific connectors
rg "J1|J2|J3|J11" design.sch

# P1 (40-pin HAT)
rg "P1|RPI|40.pin|Header" design.sch

# Ground pins
rg "DGND|GND.*pin" design.sch
```

### Signals & Nets

```bash
# UART signals
rg "TX|RX|UART0|UART5" design.sch

# SPI signals
rg "MOSI|MISO|SCLK|SPI1|SPI6|NSS" design.sch

# I2C signals
rg "SDA|SCL|I2C" design.sch

# Power signals
rg "\+3V3|\+5V|\+12V|DGND|GND" design.sch
```

### Inter-HAT Bridges

```bash
# Find inter-HAT connectors
rg "To NUCLEO|To MCU|interHat|bridge" design.sch

# Find signal conditioning networks (resistors)
rg "instance part=\"R[0-9]+\".*gate|instance part=\"RN[0-9]+\"" design.sch

# Find specific pin assignments
rg "pinref part=\"J11\".*pin=\"[0-9]+\"" design.sch
```

## Workflow

1. **Identify search target:** What connector/signal/net are you looking for?
2. **Construct pattern:** Use one of the patterns above
3. **Search:** `rg "pattern" design.sch`
4. **Extract context:** Use `-A` (after) and `-B` (before) flags
   ```bash
   rg -A 5 "part name=\"J11\"" design.sch
   ```
5. **Read extracted section:** Only read the relevant 50-200 lines returned by grep, not the whole file

## Example Walkthrough

**Find J11 inter-HAT connector pins:**

```bash
# Search for J11 connector definition
rg -A 10 "part name=\"J11\"" design.sch

# Output: Shows J11 is a 14-pin header (3220-14-0200-00)

# Find all nets connected to J11
rg "pinref part=\"J11\"" design.sch

# Output: Shows which nets (SPI6, UART5, DGND) connect to which pins
# Pins 2,4,6,8,10,12 = signals
# Pins 1,3,5,7,9,11,13 = DGND

# Read extracted context (~50 lines) to understand signal flow
# Don't read the entire 9,500-line file!
```

## Tools

- **grep:** Standard Unix tool (slower on large files)
- **ripgrep (`rg`):** Much faster, preferred choice
- **VS Code Find:** Can also use IDE search, but terminal is more scriptable
- **Read tool:** Only after grep/rg has extracted relevant sections

## Token Efficiency

**Without grep:** Reading 491K characters ~= 122K tokens
**With grep:** Reading 100 lines ~= 25 tokens

**Savings: 80-95% reduction in token usage!**
