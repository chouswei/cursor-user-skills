---
name: sysml-behaviour-generator
description: >-
  Scaffold SysML v2 behaviour packages: state def (states, transitions, events as attribute def),
  optional actions/activities; patterns for power-down/up, sticky DHCP, reconnect, multi-edge join,
  ordered commissioning when asked; align with deploy and requirements (satisfy, refine/derive).
  Triggers: behaviour model, state machine, transitions, lifecycle states, behaviour-*.sysml,
  power-cycle behaviour, plant commissioning flow, sticky DHCP reconnect, multi-edge join.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first (gather inputs before generating)
  version: "1.1"
  pairs_with: [mcp-sysml-v2, sysml-software-part-generator, sysml-requirements-generator, sysml-view-doc-sync]
token_guardrails: |
  - Ask for missing names/events before generating large state machines.
  - After inserting behaviour: SysML v2 MCP validate; update root imports and config load order if new file.
  - Load references/behaviour-style-guide.md when generating; avoid pasting full OMG examples into chat.
  - Prefer generic patterns (sticky MAC reservation, ordered commissioning, reconnect backoff) -- do not hard-code site IPs in skill stubs.
  - After substantive .sysml changes: sysml-memnet-cache delta (`@BEH`/`@SYM`); workflow step 6; sync outputs/diagrams when user wants operator flows.
  - Before multi-file refactor: pin_map(TSK_model_*).
---

# SysML behaviour generator

**When:** User wants a **`behaviour-<project>.sysml`** package or extensions: **state machines**, **events**, transitions, docs; optionally links to **requirements** and **deploy**.

## Pipeline

1. **Ask first** — If missing: **project folder**, **behaviour package name**, **state machine name**, **states**, **events/triggers**, **initial** / **error** states. One short question per gap.

2. **Conventions** — [references/behaviour-style-guide.md](references/behaviour-style-guide.md): file name, load order after `deploy-*`, root imports.

3. **Generate** — [assets/state-machine-stub.sysml](assets/state-machine-stub.sysml):
   - **`attribute def`** per event/signal (with `doc /* ... */`).
   - **`state def`** with `entry; then <initialState>;`, **`state`**, **`transition`** `first` / `accept` / `then`.
   - **`action def`** when the project uses named actions for operator or host sequences.
   - **`doc`** on `state def` and each material state.

4. **Plant / multi-edge patterns (when user asks)** — Prefer reusable patterns (no site-specific addresses in stubs):
   - **Ordered commissioning** — DHCP / sticky reservations → transport ready → switch visibility → inventory table commit.
   - **Sticky DHCP** — reserved MAC keeps IPv4 across reconnect; guest pool for unknown bring-up only; promote guest → reservation.
   - **Power-down / power-up** — link down → renew/rebind → MQTT reconnect (backoff) → resume; inventory rows persist.
   - **Multi-edge join** — per-site bands / role offsets; many edge actors join the same plant LAN and MQTT namespace.
   Cross-link parent requirementIds in **doc**; ask **sysml-requirements-generator** to **refine** / **derive** children when new obligations appear.

5. **Integrate** — Root imports behaviour **after** deploy; **`config.yaml`** entry before root if new file ([sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md)).

6. **Requirements (optional)** — **`satisfy`** or **doc** refs only when the project already uses that pattern; do not invent requirement IDs without confirmation.

7. **Verify** — **SysML v2 MCP validate**. **Preview** state diagram only if user asked.

8. **Outputs** — Align behaviour sections and, for commissioning/setup, **`outputs/diagrams/`** plant-setup style flowcharts (**sysml-view-doc-sync**).

## Pairing

- **sysml-software-part-generator** — software parts that host behaviour.
- **sysml-connections** — logical software connections when behaviour drives data flow.
- **sysml-requirements-generator** — refine/derive commissioning or power-cycle children.

**Repo:** [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) · Example: `sysml-v2-models/projects/sysmledgraph/models/behaviour-sysmledgraph.sysml`
