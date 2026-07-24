---
name: sysml-software-port-generator
description: >-
  Define SysML v2 software/logical port structures (OutPort/InPort + connection def) for interfaces
  between software parts (threads, state machines, services). Use when adding logical data flow,
  command flow, or event interfaces in deploy or behaviour packages. Triggers: software port, logical
  interface, data flow between threads, command flow, deploy package ports.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first (gather inputs before generating)
---

# SysML Software Port Generator

1. **Ask first** — If missing: interface name, flow kind (data / command / event), producer/consumer roles, optional item type — ask user. One short question per gap.
2. Load `references/port-style-guide.md` for naming, structure, and connection patterns.
3. Load `assets/port-def-template.sysml` for required structure.
4. Fill template; port pair (Out/In) and connection def must appear.
5. Return **only** the completed SysML port and connection definitions (ready to insert into deploy package) unless user asked for commentary.

## Inputs to gather

- **Interface name** (e.g. SoftwareData, StateCommand, ImageFrame)
- **Flow kind** — data, command, event (affects doc text)
- **Connection end roles** — e.g. `source`/`sink`, `fromStateMachine`/`toComponent`, `producer`/`consumer`
- **Item type** (optional) — FlowItems type when port conveys explicit item (e.g. Power3V3); omit for pure logical flow

## Post-generation

1. Insert defs into project deploy package (e.g. `deploy-<project>.sysml`)
2. Add ports to part defs (threads, state machines) as needed
3. Add `connect` statements for the new connection def
4. Validate: SysML MCP validate
