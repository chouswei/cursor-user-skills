---
name: hardware-custom-pcba-workflow
description: >-
  DEPRECATED pack stub. Full custom PCBA hardware/ workflow is a system-repo skill under
  .cursor/skills/, not this user pack. Triggers: hardware custom pcba, custom PCBA workflow,
  hardware slug PCBA (resolve to pcba-design-reviewer in user pack; open repo skill when present).
metadata:
  pattern: pipeline
  domain: pcba
  status: deprecated
  version: "1.0-deprecated"
  pairs_with: [pcba-design-reviewer, pcba-netlist-reader, sysml-pcba-de-facto-alignment, fusion-electronics-fetch]
---

# DEPRECATED -- repo skill; pack hub is pcba-design-reviewer

**Status:** not shipped as a full workflow in the user pack. Do not invent pack-local PCBA layout steps from this stub.

**Prefer (user pack):** [pcba-design-reviewer](../pcba-design-reviewer/SKILL.md), [pcba-netlist-reader](../pcba-netlist-reader/SKILL.md), [sysml-pcba-de-facto-alignment](../sysml-pcba-de-facto-alignment/SKILL.md), [fusion-electronics-fetch](../fusion-electronics-fetch/SKILL.md).

**When a system repo is open:** load that repo's `.cursor/skills/hardware-custom-pcba-workflow/SKILL.md` if present (see [system-models-sysml-pack-note.md](../system-models-sysml-pack-note.md)).
