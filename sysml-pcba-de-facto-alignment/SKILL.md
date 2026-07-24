---
name: sysml-pcba-de-facto-alignment
description: >-
  Convert EAGLE netlists and CubeMX exports into de facto SysML port definitions with full
  pin, resistor, jumper, and MCU traceability. Use when PCBAs must be modeled from ground-truth
  hardware instead of nominal assumptions.
metadata:
  pattern: reviewer
  specialization: de-facto-alignment
  domain: pcba-design
  severity-levels: warning, error, info
  pairs_with:
    - pcba-netlist-reader
    - pcba-design-reviewer
    - sysml-physical-port-generator
    - sysml-hardware-part-generator
---

# sysml-pcba-de-facto-alignment

Bridge PCB netlist reality into SysML port definitions with explicit, auditable traceability.
Use this skill when a model must reflect the actual board wiring, not the nominal design intent.

## When To Use

- A PCBA has connectors, jumpers, or resistor networks that must be modeled in SysML
- CubeMX configuration and PCB routing must be reconciled
- A port block is missing signals that exist in the netlist
- You need de facto connector mapping, not abstract interface names
- You need model comments that point back to netlist evidence

## Workflow

1. Inventory all connectors and signals from the EAGLE `.pl` and `.scr` files.
2. Trace each signal through resistors, jumpers, and fanout paths.
3. Cross-reference the current CubeMX `.ioc` configuration.
4. Build SysML port definitions with complete doc blocks and explicit pin mapping.
5. Validate the model with SysML v2 MCP and a de facto alignment checklist.

## Required Outputs

- Connector pinout inventory
- Signal-to-resistor matrix
- MCU peripheral mapping from CubeMX
- SysML port definitions with full traceability in `doc` blocks
- Mismatch report for any netlist, CubeMX, or model disagreement

## Rules

- Treat the netlist as the source of truth for actual connectivity.
- Model the current jumper configuration, not all possible jumper states.
- Document resistor values and signal-conditioning purpose whenever known.
- Record exact signal names and, when available, netlist line references.
- Do not invent ports for hidden or internal-only interfaces without evidence.
- For large `.sch` files, search with `rg` or `grep` instead of reading the entire file.

## Checklist

- Every external connector in `.pl` appears in the SysML model
- Every active signal in `.scr` traces to a MCU pin or deliberate internal sink
- Every jumper and resistor on a connector path is documented
- CubeMX peripheral mode matches the PCB implementation
- SysML port comments include the actual connector, pin, and evidence trail
- Validation passes without unresolved imports or syntax errors

## Reference Guide

The detailed workflow and examples are kept in
[`SKILL_IMPROVEMENT_GUIDE.md`](SKILL_IMPROVEMENT_GUIDE.md).
