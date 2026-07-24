# Hardware part definition style guide

## Purpose

Hardware part definitions (development boards, HATs, modules, breakout boards, custom PCBAs) in SysML v2. Use **sysml-physical-port-generator** for connector structures (Gpio40PinPort, mikroBUS, etc.); this skill produces part defs that use those ports. Port types live in `HardwarePorts`.

## Naming

- **Part defs:** PascalCase — OTS by product name (RaspberryPi5, PolarFireSoCDiscoveryKit, NucleoH753zi); custom/IMD by descriptive name + optional ID (PatSpiI2cBreakoutHat, FourChannelPdFrontEnd86eunnxhq)
- **Ports:** camelCase (powerIn, p1, ethernet, gpio40p, hatInterface)
- **Attributes:** camelCase (productCategory, partNumber, currentDraw5VMax, formFactor)

See [common-library-naming-detailed.md](../../sysml-common-library-naming/references/common-library-naming-detailed.md) §4, §5.

## OTS vs custom

| Type | Naming | Attributes |
|------|--------|------------|
| **OTS** | Product/type name | productCategory, partNumber, estimatedCostUsd, currentDraw*, formFactor |
| **Custom/IMD** | Descriptive + ID | productCategory, partNumber (= ClickUp task ID); IPN = partNumber@IMD |

## Common attributes

| Attribute | Type | Use |
|-----------|------|-----|
| productCategory | String | DigiKey-style or InvenTree category |
| partNumber | String | Mfr part # (OTS) or ClickUp task ID (IMD) |
| estimatedCostUsd | Real | OTS: list price. IMD PCBA: all-in unit (layout + bare PCB + components + placement), not component sum only; planning floor **5 USD** unless quote says otherwise |
| memoryGB | Integer | RAM |
| currentDraw5VMax, currentDraw5VTypical | ElectricCurrentValue | Power |
| formFactor | String | Physical size |
| output5VMax, output12VMax | ElectricCurrentValue | Power-out capability |

## Port types (HardwarePorts)

Power: PowerIn5VPort, PowerOut5VPort, PowerIn12VPort, PowerOut12VPort, PowerIn3V3Port, PowerOut3V3Port  
Bus: SpiPort, I2cTwoPinPort, UartTwoPinPort, QwiicPort, PcieBusPort, EthernetPort  
Headers: Gpio40PinPort, MikroBusPort, GpioPassThroughPort, GpioExpansionPort  
Custom: AcquisitionMcuHatPort (for Nucleo-on-HAT)

## Structure (simple part)

```
part def XxxBoard {
  doc /* Product, key specs, pinout ref. */
  attribute productCategory : String;
  attribute partNumber : String;
  port powerIn : HardwarePorts::PowerIn5VPort;
  port p1 : HardwarePorts::Gpio40PinPort;
  port ethernet : HardwarePorts::EthernetPort;
}
```

## Structure (composite / breakout HAT)

- Nested ports with project-specific port defs (e.g. PatBreakoutComputeInPort) or inline nesting
- Power in/out, enable GPIOs
- Optional internal parts (e.g. ad9833) and connections

## Output location

- **Common lib:** `sysml-v2-models/libs/common/parts/` (development_boards.sysml, optoelectronics.sysml, etc.)
- **Project-specific:** Project models (e.g. pat-breakout-hat.sysml in leo-cubesat-laser-comm)

## Examples (reference)

- **PolarFireSoCDiscoveryKit** — compute board: p1, ethernet, mikrobus, powerIn
- **PatSpiI2cBreakoutHat** — custom HAT: computeIn, memsOut, nucleo, qpdOut, powerIn/Out, powerEnable*
- **QpdAcquisitionMcu** — MCU type: hatInterface (AcquisitionMcuHatPort), hostI2c
