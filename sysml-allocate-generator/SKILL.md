---
name: sysml-allocate-generator
description: >-
  Add or list allocate statements mapping software part usages to hardware part usages in deploy-*.sysml.
  Triggers: allocate, runs on, software to hardware, firmware to MCU, PatControlSoftware to compute.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first
  pairs_with: [mcp-sysml-v2, sysml-software-part-generator, sysml-traceability]
token_guardrails: |
  - Both usages must exist in the same deployment composite (or clarify scope).
  - Validate after adding allocate; match part def types to allocation intent.
---

# SysML allocate generator

**When:** **`allocate`** software/firmware parts **to** hardware parts in a **deployment** block.

## Pipeline

1. **Ask first** — Software **part usage** name(s), hardware **part usage** name(s), one-to-one mapping.

2. **Locate** — **`part def`** deployment composite in **`deploy-<project>.sysml`**; find existing **`allocate`** lines for pattern.

3. **Generate** — For each pair:
   ```text
   allocate <softwareUsage> to <hardwareUsage>;
   ```
   Use exact SysML usage names as declared under the deployment **part**.

4. **Imports** — No extra import usually; same package.

5. **Verify** — **SysML v2 MCP validate**.

**Example:** `allocate patSoftware to compute;` in LEO PAT deploy.
