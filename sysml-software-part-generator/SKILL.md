---
name: sysml-software-part-generator
description: >-
  Define SysML v2 software part structures (part def with ports, attributes, nested parts) for threads,
  state machines, services, and composites in deploy or behaviour packages. Use when adding software
  components that consume/produce logical data flow. Run sysml-software-port-generator first for port
  and connection types. If editing an existing software part or maturity is unclear, run sysml-part-reviewer
  first. Triggers: software part, thread def, state machine part, deploy software block.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first (gather inputs before generating)
token_guardrails: |
  - MemNet cache: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) — query_warm before edit; `@PRT`/`@SYM` delta after validate.
---

# SysML Software Part Generator

1. **Ask first** — If missing: part name, role (thread/state-machine/service/composite), ports (names and types), optional attributes (rate, baud), nested parts for composites — ask user. One short question per gap.
2. Load `references/part-style-guide.md` for naming, structure, and attribute patterns.
3. Load `assets/part-def-template.sysml` for required structure.
4. Ensure port and connection types exist (use sysml-software-port-generator first if needed).
5. Fill template; part def must appear; doc, ports, and optional attributes required.
6. Return **only** the completed SysML part definition(s) (ready to insert into deploy package) unless user asked for commentary.

## Pairing

- **sysml-part-reviewer** — before changing baselined or unclear-maturity software parts.
- **sysml-software-port-generator** — port and connection types before this part def.
- **sysml-item-generator** — logical payloads on software ports when needed.
- **sysml-allocate-generator** — software to hardware after deploy shape exists.
- **sysml-view-doc-sync** — after **well-design** changes when the project keeps behaviour/deploy docs in `outputs/`.

## Inputs to gather

- **Part name** (e.g. CameraThread, QpdThread, PatApplicationStateMachine)
- **Role** — thread, state machine, service, composite
- **Ports** — name, type (e.g. SoftwareDataOutPort, StateCommandInPort), direction
- **Attributes** (optional) — e.g. imageRateHz, positionUpdateRateHz, hostUartBaud
- **Nested parts** (for composites) — member names and types, connections between them

## Post-generation

1. Insert defs into project deploy or behaviour package
2. Add `allocate` statements if part runs on hardware
3. Add `connect` in composite or parent block for data flow
4. Validate: SysML MCP validate
