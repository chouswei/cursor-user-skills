---
name: launch-readiness-assessor
description: >-
  Go-live / production readiness premortem and checklist framing. Triggers: launch readiness, go-live,
  production deployment, pre-launch risk, day-one failure.
metadata:
  pattern: inversion
  interaction: multi-turn
---

# Launch readiness assessor

Structured launch assessment. **Do not conclude readiness until all phases complete.**

## Phase 1 - Failure discovery (one question per turn, in order)

- Q1: "What would cause this launch to fail catastrophically on day one?"
- Q2: "What assumptions about system, users, or infrastructure could be wrong?"
- Q3: "What second-order effects could occur after launch?"

## Phase 2 - Readiness validation (after Phase 1)

- Q4: "Have we tested the most critical failure scenarios?"
- Q5: "Are monitoring, rollback, and support processes ready?"

## Phase 3 - Synthesis (after all answers)

Load `assets/launch-readiness-template.md`; summarize risks and gaps; go/no-go with conditions; confirm; iterate until satisfied.
