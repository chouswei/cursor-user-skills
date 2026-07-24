---
name: decision-inverter
description: >-
  Structured premortem / inversion on a **named decision or plan**. Triggers: premortem, what would fail,
  blind spots, decision risks, inversion before deciding.
metadata:
  pattern: inversion
  interaction: multi-turn
---

# Decision inverter

Structured decision inversion. **Do not synthesize recommendations until all phases complete.**

## Phase 1 - Failure discovery (one question per turn, in order)

- Q1: "What would cause this decision or plan to fail completely?"
- Q2: "What assumptions are we making that, if false, would make this a bad decision?"
- Q3: "What second-order or unintended consequences could occur?"

## Phase 2 - Risk exploration (after Phase 1)

- Q4: "Which of these failure modes is most likely or most damaging?"
- Q5: "Are there stakeholders, edge cases, or external factors we haven't considered?"

## Phase 3 - Synthesis (after all answers)

Load `assets/decision-inversion-template.md`; summarize risks/assumptions; prioritized failure modes and safeguards; confirm with user; iterate until satisfied.
