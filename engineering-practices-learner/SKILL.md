---
name: engineering-practices-learner
description: >-
  Learns, classifies, labels, and retrieves engineering practices with optional relation
  edges between entries (depends_on, conflicts_with, complements, etc.). Every practice gets a
  stable **id** (slug) for relations and corpus lines. JSON steps 1-4.
  Triggers: engineering practices, taxonomy, label practices, knowledge graph, related
  practices, playbook, lessons learned, classify practice, practice library,
  export to skill, tool-wrapper from practices, promote playbook to skill.
metadata:
  pattern: pipeline
  version: 1.3-eng-practices
  domain: reasoning

pipeline_steps:
  1. Ingest / clarify
     - Emit JSON only: {"objective": "string", "inputs": [{"id": "string|null", "practice": "string", "conditions": "string", "result": "string", "source": "string"}]}. User may supply **id**; if null, assign in step 2 per references/core-engineering-practices.md.
  2. Classify / normalize / label / relate
     - Emit JSON only: {"entries": [{"id": "string", "label": "string", "practice": "string", "conditions": "string", "observed_result": "string", "confidence": "high|med|low", "tags": ["string"], "taxonomy_path": ["optional","facet"]}], "relations": [...]}. **Required:** unique **id** per entry (stable slug); relations reference ids only. Cap: <=12 relation edges per emit; omit empty arrays.
  3. Retrieve (+ relation closure)
     - Call `engineering-practices-retriever` via `python tools/engineering-practices-retriever.py "<query>" -n 7`, or keyword-filter references/core-engineering-practices.md. Emit JSON only: {"query": "string", "retrieved": ["string"], "expanded_via_relations": ["id"], "rank_note": "string"}. **retrieved**: lines or parsed **id:** values from corpus; **expanded_via_relations**: at most **5** ids, **1-hop** only from top retrieved hits (see references/core-engineering-practices.md).
  4. Review / iterate
     - Emit JSON only: {"pass": true|false, "cycles_used": 0-3, "method_check": true|false, "delta": "string"}. Max 3 revision cycles total for step 4; if method_check true, main agent may run [scientific-method-first-principles](../scientific-method-first-principles/SKILL.md) once before final pass.
  5. Final output
     - Strict template from assets/engineering-practices-output-template.md only.

system_instruction: |
  Concise mode. Steps 1-4: JSON only (no prose between steps). No verbatim user paste; each intermediate emit <= 400 tokens.
  Step 5: markdown matching assets/engineering-practices-output-template.md exactly.
  Combined single JSON for steps 1-4 allowed if it includes all required keys in one object.
  Every entry must have a **stable unique id** before emitting relations. Use stable entry ids in relations; never invent cross-links without a typed edge from the vocabulary in core-engineering-practices.md.

token_guardrails: |
  - Prefer engineering-practices-retriever over pasting full references/core-engineering-practices.md.
  - max_results 5-7; short query for step 3; relation expansion max 5 ids, 1-hop only.
  - Step 2: relations array max 12 edges; use canonical types from core-engineering-practices.md only.
  - response_format: json steps 1-4; final = template only.
---

# Engineering practices learner

**Role:** Structure practices with **labels/tags/taxonomy** and **typed relations** between entries (not a flat tag soup only).

Run **pipeline_steps**; do not skip step 3 when retrieval matters.

**Resources:** [references/core-engineering-practices.md](references/core-engineering-practices.md) · [assets/engineering-practices-output-template.md](assets/engineering-practices-output-template.md)

**Step 3 tool:** `python tools/engineering-practices-retriever.py "<query>"` or ADK `engineering-practices-retriever`.

**Pairing:** [scientific-method-first-principles](../scientific-method-first-principles/SKILL.md) when step 4 sets `method_check: true`; [skill-reviewer](../skill-reviewer/SKILL.md) then [skill-creator](../skill-creator/SKILL.md) when promoting practices to a repo skill (see below).

## Export: practices -> new skill

A **coherent subset** of classified practices (stable ids, clear conditions, solid observed results) can become a **new Agent Skill**. Typical fit:

- **`tool-wrapper`** when the bundle is **conventions + when to apply** (load `references/` and follow when coding or reviewing); optional small `tools/*-retriever.py` over a **trimmed** principles file copied from this output.
- **`pipeline`** only if the workflow stays **ordered steps** (gates, JSON phases); not required for most practice libraries.

**Review before scaffold:** Treat the filled **step-5 template** (tables + relations) as the **source spec**. Run **[skill-reviewer](../skill-reviewer/SKILL.md)** on the draft folder after **skill-creator** emits it, or ask skill-reviewer to audit the **template export** as a virtual skill spec (ids, safety, triggers). Then **skill-creator** ingests that spec to generate `SKILL.md` + `references/` + assets.

**Does not auto-write disk:** This skill only structures knowledge; **skill-creator** creates files.
