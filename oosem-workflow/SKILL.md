---
name: oosem-workflow
description: >-
  Object-Oriented Systems Engineering Method (OOSEM) cycle for SysML work:
  scenario-driven, top-down, iterative needs through V&V; allocate behaviour
  to interacting objects rather than a single-pass functional split.
  Triggers: OOSEM, object-oriented systems engineering, scenario-driven MBSE,
  oosem.opensysml.org, OOSEM cycle. Skip: Harmony or RUP SE as the named method;
  generic SysML file edits with no method language.
metadata:
  pattern: pipeline
  version: "1.0"
  domain: sysml
  secondary: "hybrid: one OOSEM activity per turn; delegates one sysml-* specialist"
  pairs_with: [sysml-modeling-workflow, sysml-stakeholder-use-case, sysml-requirements-generator, sysml-nested-structure-modeling, sysml-behaviour-generator, sysml-connections, mcdm-decider, sysml-hardware-part-generator, sysml-software-part-generator, sysml-traceability, sysml-requirements-audit, sysmledge-workflow, sysml-part-reviewer]
token_guardrails: |
  - Method source is https://oosem.opensysml.org/. MUST NOT invent a seventh activity.
  - Cycle is iterative. MUST NOT treat the six activities as a one-pass waterfall.
  - Black-box behaviour and scenarios before logical objects; logical objects before physical parts.
  - One specialist SKILL.md per turn. MUST NOT paste sibling skill bodies.
  - .sysml edits follow sysml-modeling-workflow. SysMLEdge repos also follow sysmledge-workflow.
  - Load references/cycle.md only when mapping an activity or citing sources.
pipeline_steps:
  1. Bind activity
     - Name which of the six OOSEM activities this turn is in. If unknown, start at needs analysis.
     - Emit the handoff in assets/activity-handoff.md (short fields only).
  2. Scenario first
     - Operational scenarios and black-box required behaviour before structure.
     - If the user jumped to parts or ports, pull back to scenarios / black-box requirements.
  3. Delegate one specialist
     - Open exactly one row from the Delegated skills table. Follow that SKILL.md.
  4. Model-first edit
     - If editing .sysml, follow ../sysml-modeling-workflow/SKILL.md (six-step turn).
     - SysMLEdge tree: also ../sysmledge-workflow/SKILL.md (propose-only; human Save).
  5. Trade or V&V gate
     - Candidate architectures: ../mcdm-decider/SKILL.md against measures of effectiveness.
     - Claiming done: ../sysml-traceability/SKILL.md then ../sysml-requirements-audit/SKILL.md.
  6. Cycle note
     - Record activity completed, iteration index, and which activity repeats next.
     - V&V lessons feed earlier activities; do not close the cycle as finished-forever.
system_instruction: |
  Concise British English. ASCII in skill prose. OOSEM is method; SysML v2 text is the model.
  Follow pipeline_steps in order. One specialist per turn. JSON only at tool boundaries.
---

# OOSEM cycle

**When:** The user names **OOSEM** (Object-Oriented Systems Engineering Method), object-oriented systems engineering, or scenario-driven MBSE, or points at [oosem.opensysml.org](https://oosem.opensysml.org/).

**Not:** Harmony or RUP SE as the asked method. Not a replacement for [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) file/MemNet sequence.

**Pairing:** Method overlay on the SysML hub. Textual SysML v2 in this pack -- not Cameo, MagicDraw, Sparx, or Papyrus GUI. SysMLEdge day loop: [sysmledge-workflow](../sysmledge-workflow/SKILL.md).

**Source:** [OOSEM primer](https://oosem.opensysml.org/) (INCOSE OOSEM Working Group method; tool-neutral). Detail and citations: [references/cycle.md](references/cycle.md).

## Cycle (repeat, do not complete once)

```text
needs -> requirements -> architecture -> trades -> design -> V&V -> (repeat)
```

| # | Activity | Owns |
|---|----------|------|
| 01 | Needs analysis | Problem and stakeholders before solution language |
| 02 | Requirements analysis | Black-box system requirements from needs and operational scenarios |
| 03 | Architecture and logical decomposition | Allocate behaviour to interacting logical objects, then physical components |
| 04 | Trade studies and analysis | Compare candidate architectures / parameters against measures of effectiveness |
| 05 | Design synthesis | Physical architecture specific enough to implement, test, and integrate |
| 06 | Verification and validation | Requirements then original needs; feed lessons back |

Top-down and scenario-driven: black-box first, then logical objects, then physical design. Each pass decomposes further and writes requirements implementers can use.

## Delegated skills (one per turn)

| Activity | Open | When |
|----------|------|------|
| Needs | [sysml-stakeholder-use-case](../sysml-stakeholder-use-case/SKILL.md) | Stakeholders, goals, use cases, operational context |
| Requirements | [sysml-requirements-generator](../sysml-requirements-generator/SKILL.md) | Black-box requirements; refine/derive children |
| Architecture | [sysml-nested-structure-modeling](../sysml-nested-structure-modeling/SKILL.md) | Logical objects and nested structure |
| Architecture | [sysml-behaviour-generator](../sysml-behaviour-generator/SKILL.md) | Allocate behaviour / state to those objects |
| Architecture | [sysml-connections](../sysml-connections/SKILL.md) | Interactions between objects (ports and connectors) |
| Trades | [mcdm-decider](../mcdm-decider/SKILL.md) | Weighted comparison of candidate architectures |
| Design | [sysml-hardware-part-generator](../sysml-hardware-part-generator/SKILL.md) or [sysml-software-part-generator](../sysml-software-part-generator/SKILL.md) | Physical / software components |
| V&V | [sysml-traceability](../sysml-traceability/SKILL.md) then [sysml-requirements-audit](../sysml-requirements-audit/SKILL.md) | satisfy/allocate coverage; then audit |
| Maturity | [sysml-part-reviewer](../sysml-part-reviewer/SKILL.md) | Part ready for implementers |

## Gates

| MUST | MUST NOT |
|------|----------|
| Name the activity this turn | Skip to physical parts before black-box requirements exist |
| Keep the cycle iterative | Treat 01-06 as a waterfall that finishes once |
| Cite the primer URL when the method is the answer | Invent OOSEM activities or copy Friedenthal chapter prose |
| Follow sysml-modeling-workflow on `.sysml` edits | Duplicate that 6-step sequence here |

Handoff shape: [assets/activity-handoff.md](assets/activity-handoff.md).

## See also

- Method primer: https://oosem.opensysml.org/
- Modeling hub: [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md)
- Activity map and sources: [references/cycle.md](references/cycle.md)
