---
name: sysml-requirements-audit
description: >-
  Read-only or light-touch audit of SysML v2 requirements: inventory requirement defs, satisfy links in deploy,
  orphaned requirements, duplicate IDs, missing Req types. Outputs a compact matrix / gap list—not full
  traceability authoring or outputs/*.md sync. Triggers: requirements audit, req matrix, gap analysis light,
  which reqs lack satisfy, R1 R2 coverage check, requirements sanity check before release.
metadata:
  pattern: pipeline
  domain: sysml-v2
  pairs_with: [mcp-sysml-v2, mcp-sysmledgraph, sysml-traceability, sysml-requirements-generator]
token_guardrails: |
  - **Scope:** Audit and report; **do not** bulk-add **satisfy** / **allocate** unless the user asks to fix gaps (then hand off to **sysml-traceability** or **sysml-requirements-generator**).
  - Use **grep** / **sysmledgraph** on **`requirements-*.sysml`** and **`deploy-*.sysml`**; avoid loading entire model into chat.
  - After user requests **fixes:** **sysml-traceability** for **satisfy**/**allocate**/**docs** alignment; **sysml-requirements-generator** for new **requirement def** scaffolding.
  - **exam_model.py** requirement consistency check: projects with **requirements** + **satisfy** may already be validated—run when available.
  - After substantive .sysml changes: [sysml-memnet-cache](../sysml-memnet-cache/SKILL.md) delta (`@ISSUE`/`@CLM` findings); workflow step 6.
  - Before multi-file refactor: query_warm(TSK_model_*).
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML requirements audit

**When:** You need a **structured picture** of requirements vs **satisfy** (and optionally **allocate**) **without** doing a full traceability pass or rewriting **`outputs/*.md`**.

**Not for:** Full **traceability** implementation, **de facto** port audits, or **view-doc sync** → **sysml-traceability** + **sysml-view-doc-sync**.

## Pipeline

1. **Locate** — Project **`requirements-*.sysml`**, **`deploy-*.sysml`** (and **`behaviour-*.sysml`** if it references reqs). Confirm **`config.yaml`** load order includes requirements before deploy.

2. **Inventory defs** — Grep **`requirement def`** and **`requirementId`** (or project naming); build table: **id**, **short doc / title** (from **`doc`** if present).

3. **Inventory usages** — Grep **`requirement`** usages and **`satisfy`** in deploy (and elsewhere): map **usage → requirement def type**.

4. **Gaps** — Requirements with **no satisfy** target; **satisfy** referencing **unknown** requirement usage or type; **duplicate** requirement ids if project convention forbids.

5. **Optional allocate** — If user asks: grep **`allocate`**; list software→hardware pairs that reference requirements context (keep shallow unless user expands).

6. **Output** — Use [references/audit-output-template.md](references/audit-output-template.md): summary counts, tables, **recommended next skill** (**sysml-traceability**, **sysml-requirements-generator**).

7. **Verify** — **mcp-sysml-v2** validate on touched files **only if** edits were requested; otherwise read-only.

**Repo:** [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) · [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md) (when audit touches nominal vs de facto wording in **doc**)

**Detail:** [references/audit-output-template.md](references/audit-output-template.md)
