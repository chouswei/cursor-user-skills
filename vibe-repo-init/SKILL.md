---
name: vibe-repo-init
description: >-
  Initialise a blank repo for Cursor vibe coding: classify target type(s) (mcu,
  linux-pc, online-server, html-ui, pc-ui, hybrid), confirm scope, scaffold
  basement plus Cursor project files (.cursor/rules, .cursor/skills, AGENTS.md),
  then type playbooks. Triggers: blank repo, empty repo, vibe coding init, Cursor
  project init, scaffold basement, initialise project, greenfield repo, MCU
  firmware basement, hybrid app scaffold.
metadata:
  pattern: pipeline
  version: 1.2-vibe-repo-init
  domain: repo-bootstrap
  secondary: "hybrid: confirm-scope gate + Cursor basement (.cursor/skills required) + type playbooks; optional project-planner"
pipeline_steps:
  1. Detect blankness
     - Confirm workspace is empty or near-empty (no meaningful src). If not blank, stop and ask: init-in-place vs new folder.
  2. Classify type(s)
     - Map user intent → one or more types from references/repo-types.md (mcu | linux-pc | online-server | html-ui | pc-ui | hybrid).
     - Hybrid = ordered list of primary + secondary types (e.g. mcu+online-server+html-ui).
  3. Confirm scope (gate)
     - One short question unless confirm-system-before-build skip conditions apply.
     - Capture: purpose, primary type(s), language/toolchain prefs, deploy target, non-goals.
  4. Emit init plan
     - Fill assets/init-plan-template.md; show user; wait for OK before writing files (unless user said "just scaffold").
  5. Scaffold basement
     - Apply references/basement-layout.md + references/cursor-basement.md + type playbook(s) under references/types/.
     - Create only basement files (README, ignore, build stub, src skeleton, AGENTS.md, `.cursor/rules/`, **`.cursor/skills/`**) — not full product features.
  6. Optional deep plan
     - If requirements still fuzzy after scaffold: hand off to ../project-planner/SKILL.md once.
  7. Verify + settle
     - Checklist in references/init-checklist.md; report tree + next vibe step in Cursor.
system_instruction: |
  Concise British English. IDE is Cursor — scaffold Agent + rules + **project `.cursor/skills/`** (required).
  Confirm before scaffold. Basement only — no feature sprawl.
  Load one type playbook at a time. Hybrid: shared root first, then each type slice.
  Do not invent board/cloud credentials. Prefer ASCII paths.
  Do not omit `.cursor/skills/`; seed from assets/repo-context-skill-stub.md unless user names another first skill.
token_guardrails: |
  - Open references/repo-types.md once for classification; open only matched type playbook(s).
  - Open references/cursor-basement.md once per scaffold.
  - Do not paste sibling skill bodies; link ids only.
  - Intermediate handoffs: short TOON; final user report = assets/init-report-template.md.
---

# Vibe repo init (Cursor)

**Role:** Turn a blank (or near-blank) folder into a **Cursor vibe-coding basement** — runnable skeleton + **Cursor** project files (`AGENTS.md`, `.cursor/rules/`, **`.cursor/skills/`**) — for MCU, Linux PC, online server, HTML UI, PC UI, or **hybrid** mixes.

**IDE assumption:** [Cursor](https://cursor.com) (Agent, project rules, **project skills**, user-pack skills). Do not scaffold VS Code–only or JetBrains layouts unless the user asks.

**Not this skill:** full product features, SysML modeling (use SysML hubs), or deep requirements interviews (use `project-planner` after basement exists).

## Execution contract

1. Follow `pipeline_steps` in order; **do not write files before step 4 OK** (unless user waived).
2. Honor [confirm-system-before-build](~/.cursor/rules/confirm-system-before-build.mdc).
3. Always apply [references/cursor-basement.md](references/cursor-basement.md) on scaffold — **`.cursor/skills/` is mandatory**.
4. Seed `.cursor/skills/repo-context/` from [assets/repo-context-skill-stub.md](assets/repo-context-skill-stub.md) unless the user names a different first project skill.
5. One primary type playbook; hybrid adds secondary slices without duplicating shared root.
6. After scaffold: one clear "next vibe step" in Cursor (build/flash/run/open UI).

## Type codes

| Code | Meaning |
|------|---------|
| `mcu` | Bare-metal / RTOS firmware (Pico, STM32, …) |
| `linux-pc` | Native Linux/desktop CLI or daemon |
| `online-server` | Hosted API/worker (VPS, PaaS, container) |
| `html-ui` | Browser UI (static or light web app) |
| `pc-ui` | Desktop GUI (native toolkit / Tauri / Electron-class) |
| `hybrid` | Two or more of the above (ordered) |

Full taxonomy: [references/repo-types.md](references/repo-types.md).

## Delegated skills

| Skill | When |
|-------|------|
| [project-planner](../project-planner/SKILL.md) | Step 6 — requirements still fuzzy |
| [polarfire-soc-setup](../polarfire-soc-setup/SKILL.md) | MCU/SoC path needs PolarFire kit setup |
| [api-client-pattern](../api-client-pattern/SKILL.md) | Server/client HTTP basement conventions |
| [mcp-memnet](../mcp-memnet/SKILL.md) | Persist `@USR` scope / `@TSK` init when serve up |

## Resources

- [references/cursor-basement.md](references/cursor-basement.md) — Cursor files (rules + **skills** required)
- [references/repo-types.md](references/repo-types.md) — taxonomy + hybrid rules
- [references/basement-layout.md](references/basement-layout.md) — shared tree
- [references/types/](references/types/) — per-type playbooks
- [references/init-checklist.md](references/init-checklist.md)
- [assets/init-plan-template.md](assets/init-plan-template.md)
- [assets/init-report-template.md](assets/init-report-template.md)
- [assets/repo-context-skill-stub.md](assets/repo-context-skill-stub.md) — default project skill seed

## Pairing

User-pack skills: `~/.cursor/skills/`. **Project skills:** `.cursor/skills/` (required in every scaffold). Route via [SKILL-GRAPH.md](../SKILL-GRAPH.md) / repo `AGENTS.md`. Memory: [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc).
