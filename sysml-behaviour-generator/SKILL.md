---
name: sysml-behaviour-generator
description: >-
  Scaffold SysML v2 behaviour packages: state def (states, transitions, events as attribute def),
  optional actions/activities, doc on states; align with deploy and requirements (satisfy, package imports).
  Triggers: behaviour model, state machine, transitions, PatApplicationStates, lifecycle states,
  behaviour-*.sysml, add state to SysML project.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first (gather inputs before generating)
  pairs_with: [mcp-sysml-v2, sysml-software-part-generator]
token_guardrails: |
  - Ask for missing names/events before generating large state machines.
  - After inserting behaviour: SysML v2 MCP validate; update root imports and config load order if new file.
  - Load references/behaviour-style-guide.md when generating; avoid pasting full OMG examples into chat.
  - After substantive .sysml changes: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) delta (`@BEH`/`@SYM`); workflow step 6.
  - Before multi-file refactor: pin_map(TSK_model_*).
---

# SysML behaviour generator

**When:** User wants a **`behaviour-<project>.sysml`** package or extensions: **state machines** (`state def`), **events** (`attribute def`), transitions, docs; optionally links to **requirements** and **deploy** parts.

## Pipeline

1. **Ask first** — If missing: **project folder name**, **behaviour package name** (e.g. `LeoLaserCommBehaviour`), **state machine name**, **list of states**, **events/triggers**, **initial state**, **terminal or error states**. One short question per gap.

2. **Conventions** — Read [references/behaviour-style-guide.md](references/behaviour-style-guide.md): file name, load order after `deploy-*`, `root-*` imports, `private import` of deploy/requirements packages.

3. **Generate** — Use [assets/state-machine-stub.sysml](assets/state-machine-stub.sysml) as structural template:
   - **`attribute def`** per event/signal (with `doc /* ... */`).
   - **`state def`** with `entry; then <initialState>;`, **`state`**, **`transition`** `first` / `accept` / `then`.
   - **`doc`** on `state def` and each material state.

4. **Integrate** — Ensure **root** package imports the behaviour package **after** deploy (per [sysml-modeling-workflow](../../sysml-modeling-workflow/SKILL.md)). Add **`config.yaml`** entry for `behaviour-<project>.sysml` before `root-<project>.sysml` if the file is new.

5. **Requirements (optional)** — If user names requirement defs, add **`satisfy`** or reference in `doc` only when the project already uses that pattern; do not invent requirement IDs without user confirmation.

6. **Verify** — **SysML v2 MCP validate**. **Preview** state diagram only if user asked (follow [mcp-sysml-v2 references/cursor-mcp-rules.md](../mcp-sysml-v2/references/cursor-mcp-rules.md)).

7. **Outputs** — Align **`projects/<name>/outputs/*.md`** behaviour sections from the model when the user wants docs updated.

## Pairing

- **sysml-software-part-generator** — software parts that *host* behaviour (threads, state machine parts in deploy); behaviour file often *references* states by name in docs or separate concern.
- **sysml-connections** — logical software `connection` in deploy when behaviour drives data flow between parts.

**Repo:** [sysml-modeling-workflow](../../sysml-modeling-workflow/SKILL.md) · Example: `sysml-v2-models/projects/sysmledgraph/models/behaviour-sysmledgraph.sysml`
