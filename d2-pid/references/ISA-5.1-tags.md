# ISA-5.1 instrument tags (cheat sheet for P&ID text diagrams)

Not a substitute for ANSI/ISA-5.1. Use for stakeholder D2 P&IDs when tagging loops.

## Tag shape

`XX-NNN` or `XXX-NNN` — letter code + loop number (e.g. `FT-101`, `FIC-101`, `PSHH-301`).

## First letter (measured / initiating variable) — common

| Letter | Meaning |
|--------|---------|
| F | Flow |
| L | Level |
| P | Pressure / vacuum |
| T | Temperature |
| A | Analysis (composition, pH, conductivity, …) |
| S | Speed / frequency |
| W | Weight / force |
| V | Vibration |
| Z | Position / dimension |
| H | Hand (manual) |
| X | Unclassified / multi |
| Y | Event / state |

## Succeeding letters (function) — common

| Letter | Meaning |
|--------|---------|
| E | Primary element (sensor) |
| T | Transmit |
| I | Indicate |
| R | Record |
| C | Control |
| V | Valve (final element) |
| S | Switch |
| A | Alarm |
| Y | Relay / compute / convert |
| H / L | High / Low modifiers (e.g. PSHH, LAL) |

## Frequent combinations

| Tag | Meaning |
|-----|---------|
| FT / PT / LT / TT | Flow / pressure / level / temperature transmitter |
| FE / TE | Flow / temperature primary element |
| FI / PI / LI / TI | Local indicator |
| FIC / PIC / LIC / TIC | Indicating controller |
| FCV / PCV / LCV / TCV | Control valve for that variable |
| XV | On/off shutoff valve |
| PSV | Pressure safety valve |
| AIT / AI | Analyzer transmitter / indicator |
| ZSO / ZSC | Position switch open / closed |

## Line kinds (stakeholder shorthand)

| Kind | Draw as (D2) |
|------|----------------|
| Process | solid `->` |
| Utility / minor | solid, thinner label `utility` |
| Electric / 4–20 mA | dashed `->` label `elec` |
| Pneumatic | dashed `->` label `air` |
| Software / DCS | dotted or dashed label `sw` |

## Equipment class tags (PIP-ish shorthand)

Prefix by family when useful: `T-` tank, `P-` pump, `E-` exchanger, `V-` vessel/valve (disambiguate), `R-` reactor, `F-` filter — always prefer the project's locked tag list over inventing numbers.
