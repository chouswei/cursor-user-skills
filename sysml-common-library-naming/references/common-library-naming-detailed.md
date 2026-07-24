# SysML common library — naming rules (detailed)

**Syntax and normative library:** Use [**Systems-Modeling/SysML-v2-Release**](https://github.com/Systems-Modeling/SysML-v2-Release?tab=readme-ov-file) as the primary reference for SysML v2 language and libraries. This reference covers **naming conventions** only (parts, ports, connections, composites) for this repo’s common lib.

---

## 1. Packages

- **PascalCase**
- One top-level package per file
- Avoid names that shadow OMG/Kernel (e.g. do not use `Ports` if the standard library defines it; use `HardwarePorts` or similar)
- **Part packages (examples):** HardwarePorts, PowerSwitching, DevelopmentBoards, Optoelectronics, VisionNetwork
- **Connections:** SharedConnections
- **Composites:** PoeEdgeComputer, EdgeAI, Optoelectronic

## 2. File names

- **snake_case**
- Name should reflect the package: `ports.sysml` → HardwarePorts, `development_boards_kits_programmers.sysml` → DevelopmentBoards, `relays_semiconductors.sysml` → PowerSwitching
- **File size:** soft line-count guardrails and when to add a **sibling file** (one primary package per file) — Cursor skill [sysml-common-file-scale](../../sysml-common-file-scale/SKILL.md) and [references/scale-policy.md](../../sysml-common-file-scale/references/scale-policy.md).

## 3. Port definitions (in the ports package)

- **PascalCase**, suffix **Port**
- Name by role/interface: PowerIn5VPort, PowerOut12VPort, SpiPort, GpioExpansionPort, M2InterfacePort, AnalogLinePort, EthernetPort
- **Nested ports:** SysML v2 allows ports that contain other ports (e.g. an interface end whose type is a port definition, with nested `port` usages inside the end’s body). Use the same naming (camelCase for nested port names). Example (from OMG Release): `end port suppliedBy : SpigotBank { port hot : Spigot; port cold : Spigot; }`; connections then use dotted paths: `connect suppliedBy.hot to deliveredTo.hot`. See `sysml-v2-models/libs/omg/SysML-v2-Release/sysml/src/training/11. Interfaces/Interface Decomposition Example.sysml`.
- **Multi-pin connector (e.g. RPi5 40-pin GPIO):** Model the connector as one port (e.g. `Gpio40PinPort`) with **nested ports** for pin groups: `power3v3`, `power5v`, `gnd`, `i2c`, `spi0`, `uart0`, or per-pin if needed. Example: `port gpio40p : Gpio40PinPort { port power3v3 : PowerIn3V3Port; port i2c : I2cTwoPinPort; port spi0 : SpiPort; }`. Connections use dotted paths: `rpi5.gpio40p.spi0`. Validated with SysML MCP.

## 4. Part definitions

- **PascalCase**
- **Off-the-shelf (OTS):** product or type name — e.g. RaspberryPi5, PolarFireSoCDiscoveryKit, Hailo8M2, RelaySPST, LoadSwitch5V, GroupGetC12880MABreakout
- **Custom / in-house (IMD):** descriptive name + optional ID — e.g. FourChannelPdFrontEnd86eunnxhq, PatSpiI2cBreakoutHat, Rpi5SigBreakout  
  **IPN (InvenTree):** **MfrPart#@MfrAbbr** (manufacturer part number @ manufacturer abbreviation). For self-made PCBAs (InstruMeasure Dynamics): **partNumber** attribute = ClickUp task ID; IPN = **partNumber@IMD** (e.g. 86ewdvt0r@IMD). Keep part name the same in ClickUp and InvenTree. In part doc: "Self-made PCBA, InstruMeasure Dynamics (IMD). partNumber = X (= ClickUp task ID). InvenTree IPN: partNumber@IMD (X@IMD). Name aligned with ClickUp and InvenTree."

## 5. Attributes and members

- **camelCase** for attributes and for port/part member names: productCategory, partNumber, estimatedCostUsd, currentDraw5V, powerIn12V, pdOutA, hgpio
- Do not reuse the same name for an attribute and a port/part in the same classifier (causes shadowing)

## 6. Connection definitions

- **PascalCase**, often with **Link** or role: Power5VLink, SpiLink, AnalogLineLink, Power12VLink

## 7. Classification (optional)

- **OTS:** DigiKey-style `productCategory` string (e.g. `"Development Boards, Kits, Programmers > Single Board Computers"`)
- **IMD:** category aligned with your inventory (e.g. InvenTree); part IPN **MfrPart#@MfrAbbr** (for IMD: **partNumber@IMD**)

## 8. Doc statements

- Use `doc /* ... */` — no semicolon after the block comment

## 9. Qualified types (tool-dependent)

- If the tool does not resolve port types from `import PackageName::*`, use qualified names for port types: **HardwarePorts::PowerIn12VPort**, **HardwarePorts::SpiPort**, etc.

---

**Summary:** PascalCase for packages, port/part/connection *definitions*; camelCase for attributes and member names; snake_case for file names; avoid shadowing standard/library names; custom parts use a consistent **partNumber** and optional **@IMD** (or equivalent) in external systems. Optional **estimatedCostUsd** (Real, unit USD): OTS catalog list price; **IMD custom PCBA** all-in unit estimate (layout, bare PCB, components, placement), planning floor **5 USD** minimum unless quote says otherwise—see [libs/common/parts/README.md](../../../../sysml-v2-models/libs/common/parts/README.md).
