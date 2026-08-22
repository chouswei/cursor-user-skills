---
name: sysml-requirements-audit
description: >-
  Read-only or light-touch audit of SysML v2 requirements: inventory requirement defs, refine/derive
  trees, satisfy links in deploy, orphaned requirements, duplicate IDs, missing Req types. Outputs a
  compact matrix / gap list—not full traceability authoring or outputs/*.md sync. Triggers: requirements
  audit, req matrix, gap analysis light, which reqs lack satisfy, refine/derive coverage, R1 R2 coverage
  check, requirements sanity check before release.
metadata:
  pattern: pipeline
  domain: sysml-v2
  version: "1.2"
  pairs_with: [mcp-sysml-v2, sysml-traceability, sysml-requirements-generator]
token_guardrails: |
  - **Scope:** Audit and report; do not bulk-add satisfy / allocate / refine unless the user asks to fix gaps (then hand off to sysml-traceability or sysml-requirements-generator).
  - Use **Grep / Read** on live `requirements-*.sysml` and `deploy-*.sysml`; then use Cursor **`user-sysml-v2` MCP** (`parse` / `validate` / `getSymbols` / `getDefinition` / `getReferences`) on the file or code just loaded. Do not use abandoned `sysmledgraph` or treat an MCP workspace URI index as model SSOT.
  - After user requests fixes: sysml-traceability for satisfy/allocate/docs; sysml-requirements-generator for new or derived requirement defs.
  - exam_model.py requirement consistency check when available.
  - After substantive .sysml changes: sysml-memnet-cache delta (`@ISSUE`/`@CLM` findings); workflow step 6.
  - Before multi-file refactor: pin_map(TSK_model_*).
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML requirements audit

**When:** A **structured picture** of requirements vs **refine** / **derive** / **satisfy** (and optionally **allocate**) **without** a full traceability pass or rewriting **`outputs/*.md`**.

**Not for:** Full **traceability** implementation, **de facto** port audits, or **view-doc sync** → **sysml-traceability** + **sysml-view-doc-sync**.

## Pipeline

1. **Locate** — Project **`requirements-*.sysml`**, **`deploy-*.sysml`** (and **`behaviour-*.sysml`** if it references reqs). Confirm **`config.yaml`** load order includes requirements before deploy.

2. **Inventory defs** — Grep **`requirement def`** and **`requirementId`**; table: **id**, short **doc** / title.

3. **Inventory hierarchy** — Grep **`refine`** / **`derive`**; map **parent → child** requirementIds. Flag theme parents with no children when behaviour docs imply nested obligations; flag children with missing/broken parent links.

4. **Inventory usages** — Grep **`requirement`** usages and **`satisfy`**: map **usage → requirement def type**.

5. **Gaps** — No satisfy; broken satisfy refs; **duplicate** ids; **flat peers** that should derive from one parent; hierarchy orphans.

6. **Optional allocate** — If user asks: shallow list of software→hardware pairs.

7. **Output** — [references/audit-output-template.md](references/audit-output-template.md): counts, tables, **next skill** (**sysml-traceability**, **sysml-requirements-generator**). Note if **`10-requirements-traceability.md`** is stale vs model (do not rewrite unless asked).

8. **Verify** — **mcp-sysml-v2** validate **only if** edits were requested.

**Repo:** [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) · [sysml-traceability/references/de-facto-modeling.md](../sysml-traceability/references/de-facto-modeling.md)

**Detail:** [references/audit-output-template.md](references/audit-output-template.md)
