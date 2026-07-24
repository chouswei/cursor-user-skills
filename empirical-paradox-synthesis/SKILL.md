---
name: empirical-paradox-synthesis
description: >-
  Resolves opposing valid pulls (paradox) with a both/and synthesis **anchored in evidence**: tests, metrics,
  telemetry, incidents, SLOs, or explicit org constraints. Use when measurements or hard requirements support
  both sides of a tension and you need one coherent mechanism (phasing, scoping, guardrails, seams) — not
  a hand-wavy compromise. Triggers: empirical paradox, measured tradeoff, both true from data, SLO conflict,
  latency vs reliability with numbers, synthesis from experiments, dialectic with telemetry.
metadata:
  pattern: pipeline
  version: 1.1-empirical-paradox
  domain: reasoning

pipeline_steps:
  1. Frame + tension (JSON)
     - Emit: objective, pole_a_summary, pole_b_summary, known_evidence (string or "unknown"), non_negotiables (string[]).
  2. Principles retrieval
     - `python tools/empirical-paradox-principles-retriever.py "<query>" -n 7` from this directory, or ADK `empirical-paradox-principles-retriever`.
     - Fallback: keyword filter over references/core-empirical-paradox-principles.md (same scoring as script).
  3. Anchor + synthesize (JSON)
     - Tag E/O per pole; state paradox in one line; produce numbered synthesis mechanism; list falsifiable predictions (no invented metrics).
  4. Self-review + reflection (JSON)
     - Compliance: each pole supported or marked hypothesis; synthesis checkable; predictions falsifiable.
     - Reflection (same JSON object): residual_assumptions (string[]), what_would_falsify (string[]), what_new_data_would_flip (one string; no fabricated data).
     - pass (bool); max 1 revision of steps 3-4.
  5. Final output
     - assets/empirical-paradox-output-template.md only.

system_instruction: |
  You perform empirical paradox synthesis: tensions grounded in data or explicit constraints, then both/and
  mechanisms. Step 4 must include reflection fields (residual assumptions, falsifiers, what evidence would flip the call)
  before pass. JSON for internal steps where useful; final block matches assets/empirical-paradox-output-template.md
  exactly. Never fabricate measurements or incidents. ≤ 400 tokens per intermediate step.

token_guardrails: |
  - Prefer empirical-paradox-principles-retriever; max_results 5-7; short query.
  - response_format: json internal when specified; final = template only.
---

# Empirical paradox synthesis

**Role:** Evidence-anchored both/and synthesis when opposing pulls share data or hard constraints.

| Need | Skill |
|------|--------|
| Evidence + bedrock invariants (full method) | [scientific-method-first-principles](../scientific-method-first-principles/SKILL.md) |
| Weighted options / criteria table | [mcdm-decider](../mcdm-decider/SKILL.md) |
| Both poles backed by data/constraints; need explicit mechanism | **this skill** |

Run **pipeline_steps**; do not skip step 2.

**Resources:** [references/core-empirical-paradox-principles.md](references/core-empirical-paradox-principles.md) · [assets/empirical-paradox-output-template.md](assets/empirical-paradox-output-template.md)

**Step 2:** `python tools/empirical-paradox-principles-retriever.py "<query>"` or ADK `empirical-paradox-principles-retriever`.

**Pairing:** [scientific-method-first-principles](../scientific-method-first-principles/SKILL.md) for full experiment framing; [mcdm-decider](../mcdm-decider/SKILL.md) when ranking synthesis options.
