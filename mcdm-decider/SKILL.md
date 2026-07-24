---
name: mcdm-decider
description: >-
  Token-optimized multi-criteria decision making pipeline. Scores options against
  weighted criteria, performs pairwise comparisons when needed, and ranks alternatives.
  Triggers: mcdm, multi-criteria, weighted scoring, decision matrix, ahp, tradeoff,
  prioritization.
metadata:
  pattern: pipeline
  version: 1.0-mcdm
  domain: reasoning

pipeline_steps:
  1. Inversion + Clarify
     - Emit one JSON object: decision_goal, options_list, criteria_list.
  2. Principles Retrieval
     - Call Tool Wrapper: mcdm-principles-retriever with query from step 1.
  3. Scoring & Ranking
     - Assign weights, score each option per criterion, compute weighted totals.
     - Optional pairwise comparison for consistency check.
  4. Self-Review & Iterate
     - Internal Reviewer: sensitivity to weight changes? Max 1 revision.
  5. Final Output
     - Strict template from assets/mcdm-output-template.md. Include ranked table.

system_instruction: |
  Concise mode. JSON for internal steps 1-4; no verbatim user paste; each intermediate ≤ 400 tokens.
  Final output must match assets/mcdm-output-template.md exactly (ranked table per template).

token_guardrails: |
  - Context caching on core-mcdm-principles.md; before_model_callback summarization when available.
  - response_format: json steps 1-4
---

# MCDM decider

**Role:** Weighted criteria → ranked options.

Run **pipeline_steps**; do not skip step 2.

**Resources:** [references/core-mcdm-principles.md](references/core-mcdm-principles.md) · [assets/mcdm-output-template.md](assets/mcdm-output-template.md)

**Step 2:** `python tools/mcdm-principles-retriever.py "<query>"` or ADK `mcdm-principles-retriever`.

**Pairing:** [optimization-planner](../optimization-planner/SKILL.md) for constrained allocation after ranking; [decision-inverter](../decision-inverter/SKILL.md) for premortem on the top option.
