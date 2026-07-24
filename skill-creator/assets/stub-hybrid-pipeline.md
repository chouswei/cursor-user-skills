# Stub: hybrid pipeline SKILL.md (pipeline + embedded routing / other skills)

Use when the new skill is a **pipeline** that **orchestrates** other skills or patterns (selector, reviewer tail, nested phases). Primary pattern stays **pipeline**; document the mix in one line and in `pipeline_steps`.

```yaml
---
name: <skill-name>
description: >-
  <Third-person WHAT + WHEN. Mention orchestration: e.g. routes via reasoning-strategy-selector,
  then runs specialist skills, or ends with reviewer. Triggers: ...>
metadata:
  pattern: pipeline
  version: 1.0-<slug>
  domain: <domain>
  secondary: "hybrid: <e.g. selector mid-pipeline + generator final | reviewer step | call N sibling skills>"

pipeline_steps:
  1. <Intake / frame> (JSON or structured)
     - Distill objective; list constraints; optional flags for sub-flows.
  2. Routing (optional but typical for hybrid)
     - Run **reasoning-strategy-selector** per ../reasoning-strategy-selector/SKILL.md with a short query;
       then open only the `order` skills it returns (or fixed list if product requires it).
  3. <Domain core step>
     - Execute local logic, retrieval, or delegated specialist steps in order.
  4. <Optional: reviewer / validation step>
     - Load references/<checklist>.md or delegate to a reviewer-pattern subsection; max 1 revision.
  5. Final output
     - Strict template from assets/<output-template>.md (or plain markdown contract as specified).

system_instruction: |
  You are a hybrid pipeline orchestrator: follow pipeline_steps in order; do not skip routing gates.
  When step 2 applies, use reasoning-strategy-selector output as binding for which sibling skills to invoke next.
  Concise mode; intermediate JSON only where steps say so; final output matches the template exactly.

token_guardrails: |
  - Do not paste full sibling SKILL.md bodies; path links and skill ids only.
  - Prefer retriever tools per sub-skill; keep selector query short.
  - response_format: per-step; final step = user-visible format only.
---
```

## Body sections (markdown under frontmatter)

- **Role** — What this meta-pipeline owns vs what it delegates.
- **Execution contract** — Order, gates, when selector runs (once vs per sub-task).
- **Delegated skills** — Table: skill id | relative path to SKILL.md | when invoked.
- **Resources** — Links to `references/`, `assets/`, optional `tools/`.
- **Pairing** — If this skill wraps the pack’s selector, link `../reasoning-strategy-selector/SKILL.md` once.

## Files to create alongside

- `references/core-<domain>-principles.md` (orchestration rules, delegation, token notes).
- `assets/<output-template>.md` (final artifact shape).
- Optional `tools/<name>-principles-retriever.py` with `tool_spec` if heavy principles exist.
- `Folder_Structure.md`
- If the skill is added to this skills pack: set `wants_selector_update: true` in skill-creator intake so selector files get consistent `related_skills` / template edits.
