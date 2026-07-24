# MCU type playbook

## Basement goal

Blink / hello + board config stub + documented flash path.

## Ask (if unknown)

- Board / MCU family (e.g. W6300-EVB-Pico, Pico 2)
- Toolchain: Pico SDK CMake vs PlatformIO vs vendor IDE
- Host OS for build (Windows/WSL/Linux)

## Create

- `src/main.c` (or `.cpp`) — minimal init + loop
- `include/` or `config/` — board pins as named constants / TBD placeholders
- `CMakeLists.txt` **or** `platformio.ini` (one build system)
- `README.md` — build, flash (UF2/SWD), serial monitor

## Hybrid notes

- Live under `firmware/` when hybrid
- Network/MQTT app logic stays thin; socket/driver stubs only if Ethernet chip named by user

## Pairing

- PolarFire Discovery: [polarfire-soc-setup](../../polarfire-soc-setup/SKILL.md)
- Do not invent pinouts; mark TBD
