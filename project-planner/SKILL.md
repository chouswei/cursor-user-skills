---
name: project-planner
description: >-
  Requirements interview then filled plan template. Triggers: plan a project, design a system, I want to build,
  new project roadmap.
metadata:
  pattern: inversion
  interaction: multi-turn
---

# Project planner

Structured requirements. **Do not design/build until all phases done.**

## Phase 1 - Problem discovery (one question per turn)

- Q1: "What problem does this solve for users?"
- Q2: "Who are primary users? Technical level?"
- Q3: "Expected scale? (users/day, data volume, request rate)"

## Phase 2 - Constraints (after Phase 1)

- Q4: "Deployment environment?"
- Q5: "Stack requirements or preferences?"
- Q6: "Non-negotiables? (latency, uptime, compliance, budget)"

## Phase 3 - Synthesis (after all answers)

Load `assets/project-plan-template.md`; fill from answers; present; ask what to change; iterate until confirmed.
