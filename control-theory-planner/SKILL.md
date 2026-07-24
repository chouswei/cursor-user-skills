---
name: control-theory-planner
description: >-
  Token-optimized control systems pipeline. Designs feedback loops, ensures stability,
  and applies control principles to dynamic systems and processes.
  Triggers: control theory, feedback loop, PID, stability, observability, setpoint, regulation.
metadata:
  pattern: pipeline
  version: 1.0-control
  domain: reasoning

pipeline_steps:
  1. Inversion + Clarify
     - Emit one JSON object: system_description, desired_state, current_deviation, constraints.
  2. Principles Retrieval
     - Call `control-principles-retriever` via `python tools/control-principles-retriever.py "<query>"`, or load references/core-control-principles.md if the tool is unavailable.
  3. Control Design
     - Recommend feedback mechanisms, controller type, parameters.
  4. Self-Review & Iterate
     - Check for stability risks and observability. Max 1 revision.
  5. Final Output
     - Strict template from assets/control-output-template.md.

system_instruction: |
  Concise mode. JSON for internal steps 1-4; no verbatim user paste; each intermediate ≤ 400 tokens.
  Final output must match assets/control-output-template.md exactly.

token_guardrails: |
  - Context caching on core-control-principles.md
  - response_format: json steps 1-4
---

# Control theory planner

**Role:** Feedback, stability, regulation toward setpoints.

Run **pipeline_steps**.

**Resources:** [references/core-control-principles.md](references/core-control-principles.md) · [assets/control-output-template.md](assets/control-output-template.md)

**Step 2 tool:** `python tools/control-principles-retriever.py "<query>"` or ADK `control-principles-retriever`.

**Pairing:** [optimization-planner](../optimization-planner/SKILL.md) for constrained control; [scientific-method-first-principles](../scientific-method-first-principles/SKILL.md) when measurement design is unclear.
