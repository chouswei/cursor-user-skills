---
name: risk-assessor
description: >-
  General risk assessment and premortem (not launch-specific). Triggers: risk assessment, premortem,
  blind spots, failure modes, what could go wrong.
metadata:
  pattern: inversion
  interaction: multi-turn
---

# Risk assessor

Structured risk interview. **Do not synthesize mitigations until all phases complete.**

## Phase 1 - Failure discovery (one question per turn, in order)

- Q1: "What would cause this project/plan to fail completely?"
- Q2: "What assumptions are we making that, if false, would collapse the plan?"
- Q3: "What second-order effects could turn success into failure?"

## Phase 2 - Prioritization (after Phase 1)

- Q4: "Which failure modes are most likely or most severe?"
- Q5: "Any blind spots or stakeholders we missed?"

## Phase 3 - Synthesis (after all answers)

Load `assets/risk-assessment-template.md`; summarize risks; prioritized mitigations; confirm; iterate until satisfied.
