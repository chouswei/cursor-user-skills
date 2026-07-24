---
name: optimization-planner
description: >-
  Token-optimized optimization and constraint satisfaction pipeline. Defines
  objective, constraints, finds feasible solutions, and suggests improvements.
  Triggers: optimize, constraint, linear programming, resource allocation,
  scheduling, knapsack, feasibility.
metadata:
  pattern: pipeline
  version: 1.0-optimization
  domain: reasoning

pipeline_steps:
  1. Inversion + Clarify
     - Emit one JSON object: objective, decision_variables, constraints_list.
  2. Principles Retrieval
     - Call Tool Wrapper: optimization-principles-retriever with query from step 1.
  3. Model & Solve
     - Formulate as optimization problem, enumerate or approximate solution.
  4. Self-Review & Iterate
     - Internal Reviewer: is the solution feasible and near-optimal? Max 1 revision.
  5. Final Output
     - Strict template from assets/optimization-output-template.md. Include solution table.

system_instruction: |
  Concise mode. JSON for internal steps 1-4; no verbatim user paste; each intermediate ≤ 400 tokens.
  Final output must match assets/optimization-output-template.md exactly (solution table per template).

token_guardrails: |
  - Context caching on core-optimization-principles.md; before_model_callback summarization when available.
  - response_format: json steps 1-4
---

# Optimization planner

**Role:** Objectives + constraints → feasible / improved allocations.

Run **pipeline_steps**; do not skip step 2.

**Resources:** [references/core-optimization-principles.md](references/core-optimization-principles.md) · [assets/optimization-output-template.md](assets/optimization-output-template.md)

**Step 2:** `python tools/optimization-principles-retriever.py "<query>"` or ADK `optimization-principles-retriever`.

**Pairing:** [mcdm-decider](../mcdm-decider/SKILL.md) for weighted multi-objective tradeoffs.
