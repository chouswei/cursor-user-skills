---
name: tech-report-generator
description: >-
  Engineering-facing reports: status, investigation, evaluation, architecture snapshot, handoff - **not** RFC
  ballot doc, **not** scholarly IMRaD. Pipeline with clarify, style load, draft, rubric self-review, then template-only
  markdown. Triggers: tech report, engineering write-up, status doc, findings doc, handoff narrative.
metadata:
  pattern: pipeline
  version: 2.0-tech-report
  domain: technical-writing

pipeline_steps:
  1. Clarify (JSON)
     - Emit: audience (team|leadership|handoff|string), purpose (string), scope_window (string), facts_available (string), sensitivity (string or none).
  2. Load references
     - Read references/tech-report-style-guide.md (do not paste full file into user channel; apply when drafting). Skim section headings only if context-constrained.
  3. Draft
     - Fill assets/tech-report-template.md structure; gaps -> `[bracket placeholders]`; **no invented metrics**.
  4. Self-review
     - Apply references/tech-report-quality-rubric.md; emit JSON: pass (bool), violations (string[]), revision_note (string). Max 1 revision of step 3-4.
  5. Final output
     - Single markdown document matching assets/tech-report-template.md filled sections only (no JSON).

system_instruction: |
  JSON steps 1 and 4 only; steps 2-3 internal. Final user-visible output is markdown from tech-report-template.md only.
  No fabricated metrics; call out gaps. Each JSON emit <= 400 tokens.

token_guardrails: |
  - Do not dump full style guide into chat; use it while drafting only.
  - response_format: json for steps 1,4; final = filled template markdown only.
---

# Tech report generator

**Role:** Structured engineering reports with a quality gate before delivery.

Run **pipeline_steps**; step 4 is mandatory before final.

**Resources:** [references/tech-report-style-guide.md](references/tech-report-style-guide.md) · [references/tech-report-quality-rubric.md](references/tech-report-quality-rubric.md) · [assets/tech-report-template.md](assets/tech-report-template.md)

**Pairing:** [tech-report-reviewer](../tech-report-reviewer/SKILL.md) after draft.
