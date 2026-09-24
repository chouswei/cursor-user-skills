---
name: service-proposal
description: >-
  Author or recast a customer-facing commercial service proposal (what we offer the
  customer) as markdown using the PandaDoc service-proposal section order. Use when
  the user asks for a service proposal, customer offer, PandaDoc proposal, or to
  recast a plan into a proposal -- not for internal SOPs, lab cal notes, engineering
  design dumps, RFCs, or tech reports.
metadata:
  pattern: generator
  version: "1.0"
  domain: doc
  pairs_with: [project-planner, tech-report-generator, prompt-writing-discipline]
---

# Service proposal

**Role:** Produce one **customer offer** markdown document. Not an internal SOP, lab calibration note, engineering design dump, RFC, or tech report.

## When

| Load | Skip |
|------|------|
| Service proposal / customer offer / PandaDoc proposal | Internal SOP or procedure |
| Recast plan -> proposal | Lab cal note or design dump as the deliverable |
| Commercial scope + pricing placeholders | RFC / tech-report / IMRaD |

## Steps

1. **Classify** -- Confirm the artefact is a **customer offer**. If the user wants an SOP, cal note, or design doc, stop and route to the matching skill.
2. **Model gate** -- If the host repo is model-based (`sysml-models/models/*.sysml` or `AGENTS.md` names SysML as SSOT) and ratings / scope are design SHALLs: MUST edit the model first, then the proposal. Else write from stated closed facts only.
3. **Load** -- Apply [references/offer-rules.md](references/offer-rules.md). Fill [assets/service-proposal-template.md](assets/service-proposal-template.md).
4. **Split offer** -- Every Scope / Executive Summary MUST separate **We offer** from **Customer furnishes (CFE)**.
5. **Emit** -- Return the filled markdown (or write the path the user named). Gaps -> `[bracket placeholders]`. Pricing -> **TBD** only.

## Section order (PandaDoc)

MUST use these headings in order (source: [PandaDoc service proposal template](https://www.pandadoc.com/service-proposal-template/)). MUST NOT invent a substitute outline.

1. Introduction  
2. Our Background  
3. Executive Summary  
4. Purpose  
5. Opportunity  
6. Solution  
7. Our Proposal  
8. Scope of Work  
9. Rationale  
10. Pricing  
11. Delivery  
12. Terms and Conditions  
13. Approval  

Cover block (Prepared by / Prepared for) precedes Introduction. Optional short TOC may list the same titles. Deliverables live under Executive Summary and Scope of Work -- not a freestanding invented heading.

## Closed MUST / MUST NOT

| MUST | MUST NOT |
|------|----------|
| Split **We offer** vs **Customer furnishes (CFE)** | Sell CFE as our SKUs |
| Name a PCBA **subsystem** as such when that is the work | Write a boxed instrument / standalone PSU cover for a subsystem |
| Use **TBD** for currency figures | Invent prices |
| Keep hazards as offer **constraints / exclusions** | Dump hazard procedures into the proposal |
| Strip competitor / reference-vendor names and catalogue SKUs from the customer text | Leak internal engineering reference SKUs into the offer |
| Keep on-board sense (ADC/TIA) as ours; site DMM as optional customer check-only | Invent a "COTS bench monitor" product SKU |

Full checklist: [references/offer-rules.md](references/offer-rules.md).

## Pairing

- [project-planner](../project-planner/SKILL.md) -- intake before commercial scope is closed  
- [tech-report-generator](../tech-report-generator/SKILL.md) -- engineering reports, not customer offers  
- [prompt-writing-discipline](../prompt-writing-discipline/SKILL.md) -- LLM-facing prose when editing this skill  
- Model-based hosts: follow repo `AGENTS.md` / SysML default stack before rewriting ratings in the proposal
