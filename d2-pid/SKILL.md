---
name: d2-pid
description: >-
  Demoted last-resort D2 stakeholder P&ID sketch only. Prefer pyDEXPI P&ID for
  real work. Do not use after user stop/token-waste unless they explicitly ask
  for a D2 sketch.
metadata:
  pattern: tool-wrapper
  version: "1.0.1"
---
# D2 P&ID (demoted -- last resort)

**Demoted.** Prefer [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) (DEXPI -> graph). Use this skill **only** when the user explicitly asks for a non-DEXPI D2 stakeholder sketch.

User rule (2026-09-10): stop P&ID redraw loops that waste tokens; do not touch P&ID without a clear target.

## When

- User says D2 / quick sketch / no DEXPI XML available **and** accepts "not real P&ID"
- Never as the default for "make a P&ID"

## When not

- Any DEXPI / Proteus / smart P&ID / GraphRAG / MemNet topology task -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md)
- After user stop / token-waste feedback -> stop

## Hard rules (if used)

1. Symbols from `symbols/` only -- **no** architecture box-lists. Tags: [ISA-5.1-tags.md](references/ISA-5.1-tags.md).
2. Locks-only; label output as **stakeholder sketch**, not ISO/DEXPI.
3. One pass unless user asks for a specific delta -- no multi-round redraw spam.
4. `d2 --pad=40 --layout=tala`; width `<1400`.

## Hand off

- Real P&ID -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md)
- Routing -> [Diagram routing](../diagram-routing/SKILL.md)
