---
name: d2-pid
description: >-
  Anti-pattern: do not draw P&ID in D2. Prefer pyDEXPI. This skill exists to
  catch bad defaults and redirect agents away from D2 P&ID sketches.
metadata:
  pattern: tool-wrapper
  version: "1.0.2"
---
# D2 P&ID (anti-pattern -- do not use)

**Anti-pattern.** Do **not** draw P&ID in D2. Prefer [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) (DEXPI -> graph). Strings -> [SFILES 2.0](../sfiles2/SKILL.md) / [GGILES](../ggiles/SKILL.md). D2 remains for **architecture posters only** (out-of-pack), never plant P&ID.

This skill stays in the pack so agents that find `d2-pid` are steered away -- not as a viable choose-lane.

User rule (2026-09-10): **D2 is not a good idea for drawing P&ID.**

## When

- Essentially **never** for P&ID work.
- If somehow invoked (stale prompt, old habit, explicit "use d2-pid"): **immediately hand off** to [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md). Refuse a D2 P&ID deliverable; redirect.

## When not (always)

- Any P&ID / DEXPI / Proteus / smart P&ID / GraphRAG / MemNet topology task -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md)
- Flowsheet / general graph strings -> [SFILES 2.0](../sfiles2/SKILL.md) / [GGILES](../ggiles/SKILL.md)
- Architecture posters -> out-of-pack D2 architecture skill if installed locally (not this skill)

## Legacy assets (not a green light)

`symbols/` and [ISA-5.1-tags.md](references/ISA-5.1-tags.md) remain only as historical / migration references. Do not use them to produce new P&ID in D2.

## Hand off

- Real P&ID -> [pyDEXPI P&ID](../pydexpi-p-id/SKILL.md) (**immediate**)
- Strings -> [SFILES 2.0](../sfiles2/SKILL.md) / [GGILES](../ggiles/SKILL.md)
- Routing -> [Diagram routing](../diagram-routing/SKILL.md)
