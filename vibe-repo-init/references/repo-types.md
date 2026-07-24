# Repo types (vibe init)

## Single types

| Code | Signals (triggers) | Default stack hint |
|------|--------------------|--------------------|
| `mcu` | firmware, Pico, STM32, ESP, bare-metal, RTOS, flash, UF2 | C/C++ + vendor SDK + CMake/PlatformIO |
| `linux-pc` | CLI, daemon, systemd, local Linux tool | Python or Go/Rust; `src/` + `tests/` |
| `online-server` | API, VPS, Docker, PaaS, webhook, MQTT broker side | HTTP/MQTT service + `.env.example` + deploy stub |
| `html-ui` | browser, SPA, static site, dashboard web | HTML/CSS/JS or light Vite; no backend required |
| `pc-ui` | desktop app, GUI, tray, Tauri, Qt, WPF | Toolkit-specific; separate from `html-ui` |

## Hybrid

`hybrid` is **not** a seventh stack — it is an **ordered list** of the above.

Rules:

1. Name types explicitly: `hybrid: mcu + online-server + html-ui`.
2. Scaffold **shared root** once (README, `.gitignore`, AGENTS/cursor hints).
3. Each type gets a **slice** dir (e.g. `firmware/`, `server/`, `web/`) — see basement-layout.
4. Document the **runtime contract** between slices (UART/MQTT/HTTP) in README in one short section.
5. Do not merge MCU and server build systems into one opaque root.

## Classification procedure

1. Extract nouns from user phrase (board, deploy, UI surface).
2. Pick strongest single type; if ≥2 surfaces → hybrid list.
3. If ambiguous between `html-ui` and `pc-ui`: ask one question (browser vs installable desktop).
4. If ambiguous MCU board: leave board as `TBD` in plan; do not invent pin maps.

## Anti-patterns

- Scaffolding full features (auth, billing) during init
- Copying an unrelated sibling repo without user saying "mirror X"
- One mega-CMake for firmware + Node server without slices
