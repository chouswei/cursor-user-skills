---
name: analytical-mechanics-propose
description: >-
  Proposes or reviews an analytical-mechanics framing for any domain:
  resident configuration versus inventory, role split, discrete honesty,
  dissipative forgetting, controls and hard caps, three surfaces, gauge,
  instantiations on one phase space, and falsifiable predictions. The LLM
  STM thesis is the worked example, not the only target. Use when transferring
  Lagrangian / Hamiltonian / KKT / Noether language onto a new plant.
  Triggers: analytical mechanics propose, apply Lagrangian to, Hamiltonian
  framing, KKT cap diagnostic, Noether gauge propose. Skip: STM-only harness
  or triage (llm-stm-analytical-mechanics); MemNet install/wire
  (mcp-memnet, memnet-format).
metadata:
  pattern: pipeline
  version: "1.0"
  domain: user
pipeline_steps:
  1. Usefulness -- name resident configuration W versus inventory S; usefulness is action A on a trajectory, not a dump of S.
  2. Role split -- integrator / steering / plant. Do not collapse roles.
  3. Configuration honesty -- native discrete versus continuous instrument; round back if you relax.
  4. Open / dissipative -- if the system forgets, name dissipation; do not pretend closed Hamiltonian flow.
  5. Controls and caps -- name control u; hard inequality caps; KKT / shadow-price as diagnostic, not a buyable knob.
  6. Three surfaces -- log proposal, admission, and eviction separately.
  7. Gauge / symmetry -- rename invariance on unobservables; order of admission is physical.
  8. Instantiations -- same phase space, different controls; STM ShapeWalk is one example.
  9. Falsifiable predictions -- at least one claim that can fail, with failure condition.
  10. Firewalls -- method-transfer MUST NOTs; no product SemVer claims.
  11. Emit -- fill assets/propose-card.md.
system_instruction: |
  General method-transfer propose. STM thesis is the worked example, not the only plant.
  Not a MemNet SemVer claim. Pack metadata.version is this skill only. MemNet 1.0 unclaimed.
  British English. ASCII. If the job is STM harness or STM debug only, stop and open llm-stm-analytical-mechanics.
token_guardrails: |
  - L2 = this checklist. L3 = GitHub thesis headings / playbooks. MUST NOT paste thesis math or playbook body.
  - MUST NOT duplicate mcp-memnet install or memnet-format GQL grammar.
  - MUST NOT invent MemNet 1.0 or treat honesty c as a SemVer cut.
  - Final user-facing block matches assets/propose-card.md.
---

# Analytical mechanics propose (any domain)

**Method transfer.** Doctrine SSOT: [llm-stm-mechanics](https://github.com/chouswei/llm-stm-mechanics) (`thesis/analytical-mechanics-of-llm-stm.md`). This skill is the **general propose checklist** (L2). Section pointers: [references/l3-sources.md](references/l3-sources.md). Thin dictionary: [references/core-am-propose-principles.md](references/core-am-propose-principles.md).

**Worked example, not the only target.** LLM STM / ShapeWalk / `pin_map` is one instantiation on the same phase-space idea. For STM-only wire or triage, stop and open [llm-stm-analytical-mechanics](../llm-stm-analytical-mechanics/SKILL.md).

**Not a MemNet SemVer claim.** Pack `metadata.version` is this skill folder only. Do **not** claim MemNet **1.0**. Thesis package pins (for example `memnet-llm` 0.19.x) are source citations, not this pack's version.

**Pair (do not duplicate):** STM specialist [llm-stm-analytical-mechanics](../llm-stm-analytical-mechanics/SKILL.md). Not MemNet install or GQL wire: [mcp-memnet](../mcp-memnet/SKILL.md), [memnet-format](../memnet-format/SKILL.md).

## When to load

| Job | This skill | Then |
|-----|------------|------|
| Propose or review AM framing on an arbitrary plant (cache, RAG, planner, hardware loop, org process) | Pipeline below | Fetch L3 section that the step names |
| STM harness, W vs S, ShapeWalk debug, thesis triage | **Stop** | [llm-stm-analytical-mechanics](../llm-stm-analytical-mechanics/SKILL.md) |
| MemNet tools / GQL grammar | **Stop** | mcp-memnet / memnet-format |

## Pipeline

Run in order. Each step writes one short block (table or bullets). Intermediate steps <= 400 tokens. Do not skip 9 or 10.

1. **Resident versus inventory.** Name the plant's inventory S (cabinet, corpus, weights, session graph, ledger). Name the resident configuration W (what is actually in the active window / state). Usefulness is action A along a trajectory of W, not a dump of S. Store is the manifold of admissible configurations, not the phase point.
2. **Role split.** Integrator realises the next step under W. Steering chooses H, a force, or a constraint (control u). Plant / inventory is what W is selected from. The same software component may occupy two roles on different turns; log them separately.
3. **Configuration honesty.** Admission is discrete (in or out). A smooth / attention-mass relaxation is an instrument for gradients; implementations must round back to a discrete W. Do not pretend the native plant is a smooth manifold.
4. **Open / dissipative.** If the plant forgets, evicts, compresses, or summarises, it is open. Closed Hamiltonian flow is volume-preserving and cannot account for that loss. Name the dissipative channel (discrete force on the hard window, and/or a continuous resistive account). Do not run two competing eviction stories as if they were one step.
5. **Controls and caps.** Name u (never a coordinate). Inequality caps (window, hop, row count, rate) stay **hard** in the engine. A KKT / shadow-price estimator (`lambda-hat_M`) is an **account diagnostic**: biting cap versus slack. It is not a buyable knob. Task fail + slack => wrong Shape / wrong u, not "buy more M".
6. **Three surfaces.** Log separately: **proposal** (offered Shape X-tilde), **admission** (what entered W, order preserved), **eviction** (what left W). A ranker may only propose. Collapsing the three into one score fails inspectability. Offered X-tilde is a subset of W only if the whole Shape is admitted.
7. **Gauge / symmetry.** Identity is the element, not a hidden name. Rename invariance: isomorphic relabelling of unobservables must not change observables, action estimates, or task scores (up to declared noise). Admission **order is physical** -- do not sort by hidden id to "clean" a test. If labels leak into ranking, that is a gauge anomaly, not noise.
8. **Instantiations.** Map the domain's loaders / policies onto **one** phase space as different controls (worked STM examples: bounded walk, RAG-style load, KV eviction). Do not treat each product as a new memory ontology. Fetch thesis section 9 only if you need the STM worked example.
9. **Falsifiable predictions.** State at least one claim, protocol sketch, and **failure condition**. A dictionary that always fits after the fact is not a mechanism. Point at thesis section 10 for the STM scoreboard; do not copy experiment tables into this pack.
10. **Firewalls.** Apply [references/core-am-propose-principles.md](references/core-am-propose-principles.md) MUST NOTs. Analysis symbols (L, H, p, m, lambda, coverage) are not product fields. Do not paste section-13 math onto a wire.
11. **Emit** the propose card from [assets/propose-card.md](assets/propose-card.md).

## MUST NOT

- Route STM-only harness / debug here; use the STM specialist.
- Duplicate mcp-memnet install or memnet-format GQL.
- Claim MemNet **1.0** or treat honesty `c` as a SemVer a/b cut.
- Paste thesis or playbook body into the card.
- Put analysis fields on a product read (momentum / coverage / lambda / m as emitted state).
- Soften hard caps inside the engine to make a diagnostic pretty.
- Collapse proposal / admission / eviction; dump S as the memory API.
- Confuse action A with inventory S; confuse product cue q with analysis control u without one named map.

## Pairing

| Need | Skill |
|------|--------|
| STM turn loop / debug tree | [llm-stm-analytical-mechanics](../llm-stm-analytical-mechanics/SKILL.md) |
| Which STM playbook file | [memnet-stm-harness](../memnet-stm-harness/SKILL.md) |
| Feedback / stability (not AM propose) | [control-theory-planner](../control-theory-planner/SKILL.md) |
| Constrained allocation (not AM propose) | [optimization-planner](../optimization-planner/SKILL.md) |
| Experiment design after a prediction | [scientific-method-first-principles](../scientific-method-first-principles/SKILL.md) |
| MemNet tools / wire | **Not this skill** -- mcp-memnet / memnet-format |

## Steps

1. If STM-only, stop and open the specialist.
2. Run pipeline 1-10. Fetch L3 by heading only ([references/l3-sources.md](references/l3-sources.md)).
3. Fill the propose card. Stop.
