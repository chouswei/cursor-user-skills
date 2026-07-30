# Port definition style guide

## Naming

- **Protocol port defs:** `{{ConnectorName}}Protocol` (e.g. `Gpio40PinPowerProtocol`, `MikroBusSpiProtocol`)
- **Connector port def:** `{{ConnectorName}}Port` (e.g. `Gpio40PinPort`, `MikroBusPort`)
- **Pin ports:** `pinN` where N = physical pin number (e.g. `pin3`, `pin8`)

See [common-library-naming-detailed.md](../../sysml-common-lib-contribution/references/common-library-naming-detailed.md) §3.

## Port types (HardwarePorts)

| Type | Use for |
|------|---------|
| GpioExpansionPort | Single GPIO/signal |
| PowerOut3V3Port, PowerOut5VPort | Power pins |
| GndPort | Ground |
| AnalogLinePort | ADC, analog in/out |
| SpiPort | SPI (extend for pin-level) |
| I2cTwoPinPort | I2C (extend + redefines sda/scl) |
| UartTwoPinPort | UART (extend + redefines tx/rx) |

## Protocol compatibility (redefines)

To connect via `I2cLink`, `UartLink`, or `SpiLink`, protocol sub-ports must satisfy the connection's port type. Use `redefines`:

- **I2C:** `port pinN : GpioExpansionPort redefines sda;` and `redefines scl;`
- **UART:** `port pinN : GpioExpansionPort redefines tx;` and `redefines rx;`
- **SPI:** No redefines; extend SpiPort and add pin ports typed as GpioExpansionPort

## Doc strings

- Use `doc /* ... */` for connector and each protocol
- Document signal mapping in protocol doc (e.g. `pin3=SDA`, `pin8=TX`)
- No semicolon after doc block

## Connections

Add `I2cLink`, `UartLink` in `connections.sysml` when needed. `SpiLink` already exists. Update deploy model to use `connector.protocol` (e.g. `compute.p1.spi0`).

## Output location

Add port defs to `sysml-v2-models/libs/common/parts/hardware_ports.sysml` (package `HardwarePorts`). Validate with SysML MCP after edits.

## Examples (reference)

- **Gpio40PinPort** — RPi-style 40-pin: power, i2c, uart, spi0, id, gpio
- **MikroBusPort** — mikroBUS 16-pin: spi, i2c, uart, power, other
- **AcquisitionMcuHatPort** — Custom (not RPi pinout): spi1..4, hostUart, startOut, resetNOut, memsFclkOut
