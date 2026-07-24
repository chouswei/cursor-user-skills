---
name: incentive-alignment-reviewer
description: >-
  Reviewer for incentive structures. Identifies misalignments, principal-agent problems,
  perverse incentives, and second-order effects. Triggers: incentives, alignment, skin in the game,
  principal agent, perverse incentive, gaming, second order effects.
metadata:
  pattern: reviewer
  version: 1.0-incentive
  domain: reasoning

pipeline_steps:
  1. Inversion + Clarify
     - Identify the incentive structure, actors, rewards, and potential misalignments.
  2. Principles Retrieval
     - Load references/incentive-review-checklist.md
  3. Incentive Review
     - Apply checklist, identify risks and misalignments.
  4. Self-Review & Iterate
     - Check completeness of analysis. Max 1 revision.
  5. Final Output
     - Structured review using the checklist with findings and recommendations.

system_instruction: |
  Respond in concise mode only. Use structured output. Keep analysis focused on incentives.

token_guardrails: |
  - Context caching on incentive-review-checklist.md
---

# Incentive alignment reviewer

**Role:** Incentives, principal-agent, perverse incentives, second-order effects.

Run **pipeline_steps**; apply [references/incentive-review-checklist.md](references/incentive-review-checklist.md) rigorously.

**Pairing:** [risk-assessor](../risk-assessor/SKILL.md) or [decision-inverter](../decision-inverter/SKILL.md).
