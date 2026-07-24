---
name: sysml-eagle-netlist-bridge
description: >-
  DEPRECATED stub. EAGLE netlist to SysML workflow lives in
  sysml-pcba-de-facto-alignment. Triggers: EAGLE netlist, netlist to SysML,
  PCB design integration (resolve to sysml-pcba-de-facto-alignment).
metadata:
  pattern: generator
  domain: sysml-v2
  status: deprecated
  version: "2.0-deprecated"
  pairs_with: [sysml-pcba-de-facto-alignment, sysml-eagle-netlist-parser-tool, pcba-netlist-reader]
---

# DEPRECATED -- use sysml-pcba-de-facto-alignment

**Status:** merged. Do not load this skill for work.

Open **[sysml-pcba-de-facto-alignment](../sysml-pcba-de-facto-alignment/SKILL.md)** for EAGLE `.scr`/`.pl` (and broader de-facto) alignment. Optional JSON feeder: [sysml-eagle-netlist-parser-tool](../sysml-eagle-netlist-parser-tool/SKILL.md). Pre-audit connectivity: [pcba-netlist-reader](../pcba-netlist-reader/SKILL.md).
