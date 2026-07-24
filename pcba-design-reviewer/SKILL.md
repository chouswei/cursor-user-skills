---
name: pcba-design-reviewer
description: >-
  Validate PCBA design using first-principles reasoning: state bedrock principles (Kirchhoff's laws, V=IR, thermal, EMC), derive constraints from principles, map to design, emit verdict (Go/Hold/No-go). Gate before layout. Pairs with netlist-reader audit.
metadata:
  pattern: reviewer
  specialization: first-principles-gate
  domain: pcba-design
  severity-levels: error, warning, info
  pairs_with:
    - pcba-netlist-reader
    - decision-inverter
    - risk-assessor
---

# pcba-design-reviewer

Validate PCBA design from **principles → constraints → checklists → verdict**. Gate before layout.

## Workflow (4 phases, ~200 tokens)

```
0. INTAKE
   Ask: design constraints (rails, current, freq, isolation reqs), fundamental problem
   → User articulates bedrock need

1. RETRIEVE PRINCIPLES
   Load: references/pcba-first-principles.md
   → Bedrock laws (KCL, V=IR, Z, thermal, EMC)

2. DECONSTRUCT DESIGN (per domain: Power, Ground, Isolation, Thermal, EMC)
   For each: State constraint → Derive from principle → Map to PCB/schematic
   → Constraint analysis

3. REBUILD CHECKLIST
   Load: design-review-FP-checklist-{domain}.md
   → Principle-traceable items (not generic)

4. VERDICT
   Check: violations? acceptable assumptions? pass rate?
   → Go | Hold | No-go
```

## Output Per Domain (JSON-like structure)

```
Domain: power_distribution
  Principle: KCL + V=IR
  User constraint: "±12V ±5%, 2A max"
  Derived constraint: R_max = 0.3Ω
  Checklist pass rate: 85% (items with evidence)
  Residual assumptions:
    - PCB copper thickness nominal (no voids)
    - Capacitor ESL/ESR = datasheet nominal
  Falsification tests:
    - Measured trace R > 0.5Ω → FAIL
    - Ripple voltage > 0.6V → FAIL
  Confidence: high | med | low
  Severity: error | warning | info
```

## Verdict Logic

- **Go:** All domains pass + assumptions acceptable + confidence ≥ med
- **Hold:** Some warnings (fixable before layout)
- **No-go:** Principle violation or confidence = low

## Pairing

- **Before:** pcba-netlist-reader (audit connectivity)
- **After:** Layout reviewer (if created); decision-inverter or risk-assessor for failure modes (optional)

## Reference Docs (Load Once, Cache)

- `pcba-first-principles.md` — Bedrock laws (KCL, V=IR, Z, thermal, EMC)
- `design-review-FP-checklist-power.md` — Power distribution checklist
- `design-review-FP-checklist-ground.md` — Ground architecture checklist
- `design-review-FP-checklist-isolation.md` — Signal isolation checklist
- `design-review-FP-checklist-thermal.md` — Thermal budget checklist
