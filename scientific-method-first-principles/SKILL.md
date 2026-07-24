---
name: scientific-method-first-principles
description: >-
  Implements the **entire** scientific method for system engineering, fused with first-principles bedrock:
  frame the question; survey background and prior evidence; form falsifiable hypotheses; design or specify
  the smallest decisive experiment; run or prescribe it; analyze outcomes; conclude; **iterate** (what would
  change the answer, next test if inconclusive). Bedrock invariants (physics, SLOs, org constraints) bound
  analysis and conclusions. Triggers: scientific method, hypothesis, falsifiable test, measurement vs theory,
  telemetry, benchmark, lab data, evidence-based architecture.

metadata:
  pattern: pipeline
  version: 1.1-scientific-method-fp
  domain: reasoning

pipeline_steps:
  1. Frame + evidence (JSON)
     - Maps to **question/problem** + **background evidence**: emit objective, evidence_summary (what data/tests exist or "unknown"), stated_constraints, open_questions (string[]).
  2. Principles retrieval
     - From this skill directory: `python tools/empirical-fp-principles-retriever.py "<query>" -n 7`, or ADK tool `empirical-fp-principles-retriever` with query from step 1.
     - If tool unavailable, read references/core-empirical-fp-principles.md and apply same keyword overlap as the retriever script.
  3. Fuse + deconstruct + rebuild (JSON then short prose plan)
     - Maps to **hypothesis -> experiment/test -> analyze -> conclude** (and **iterate** if inconclusive): classify key claims as E/T/O; list conflicts; produce fused numbered design or decision steps (no fabricated numbers); state what would falsify and what to run next if still uncertain.
  4. Self-review
     - Compliance: no invented data; conflicts named; invariants respected.
     - Decision quality: answers the stated objective (yes/no + one line); correlation-vs-mechanism check (one line); stakeholder_blind_spot (one line).
     - pass (bool); max 1 revision.
  5. Final output
     - Strict template from assets/empirical-fp-output-template.md only.

system_instruction: |
  You run the **full** scientific method for engineering work—do not shortcut problem framing, falsifiable
  hypotheses, experimental logic, or honest analysis. First-principles invariants are the **theoretical bedrock**
  used when interpreting results and closing conclusions (via E/T/O tagging), not a side track you can omit.
  Be concise. Step 4 JSON must include decision-quality fields (objective_fit, correlation_vs_mechanism, stakeholder_blind_spot) plus compliance checks.
  Use JSON for steps 1, 3 (internal), and 4 as appropriate; final user-facing block must match
  assets/empirical-fp-output-template.md exactly. Never fabricate measurements, logs, or test outcomes;
  use placeholders and name the missing experiment. Intermediate steps ≤ 400 tokens each.

token_guardrails: |
  - Prefer empirical-fp-principles-retriever; max_results 5-7; short query. No full paste of core-empirical-fp-principles.md.
  - response_format: json internal steps; final = empirical-fp-output-template only.
---

# Scientific method and first-principles

**Role:** Full scientific method + first-principles bedrock for engineering decisions; detail in `pipeline_steps` and `system_instruction`.

Run **pipeline_steps**; do not skip step 2.

**Resources:** [references/core-empirical-fp-principles.md](references/core-empirical-fp-principles.md) · [assets/empirical-fp-output-template.md](assets/empirical-fp-output-template.md)

**Step 2:** `python tools/empirical-fp-principles-retriever.py "<query>"` or ADK `empirical-fp-principles-retriever`.

**Pairing:** [empirical-paradox-synthesis](../empirical-paradox-synthesis/SKILL.md) when both poles are evidence-backed; [mcdm-decider](../mcdm-decider/SKILL.md) for weighted option ranking; [decision-inverter](../decision-inverter/SKILL.md) for premortem on the chosen plan.
