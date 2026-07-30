---
name: sysml-modeling-workflow
description: >-
  Primary SysML workflow skill: MemNet-first 6-step turn sequence, model-first edits, validate, outputs sync,
  and routing to specialist sysml-* skills. Triggers: modeling workflow, file roles, load order, project setup,
  outputs sync, workflow questions, memnet sysml.
metadata:
  pattern: pipeline
  domain: sysml-v2
  version: "1.2"
  pairs_with: [sysml-memnet-cache, sysml-memnet-documentation, sysml-modeling-session-checklist, sysml-root-config, sysml-import-order-helper, sysml-view-doc-sync, mcp-sysml-v2, mcp-memnet, project-planner, sysml-traceability]
token_guardrails: |
  - MUST follow the 6-step MemNet turn sequence below on every substantive modeling turn.
  - pin_map before edit; MemNet delta + line refresh after validate (see sysml-memnet-snap.md).
  - Pipeline handoffs: shared dialect mutate when MemNet is up (sysml-memnet-pipeline.md); plain Markdown when down (not TOON/TRON).
  - MUST follow sysml-memnet-read-policy.md: no full deploy read for topology; <=2 narrow Read windows per turn.
  - After .sysml edits, validate with mcp-sysml-v2; route to specialist sysml-* skills for depth.
---

system_instruction: |
  Prefer plain Markdown or MemNet shared dialect; do not use TOON/TRON. JSON only at tool boundaries.


# SysML modeling workflow

Use this skill when the user asks how to structure SysML work, which skill to use, or how to sequence a modeling session.

## Mandatory turn sequence (6 steps)

Every substantive turn on the project model tree **MUST** follow this order. Default pack path is `sysml-v2-models/projects/<slug>/`; if the open repo's root **`AGENTS.md`** names another tree (e.g. `sysml-models/`), use that. Full rules: [sysml-memnet-snap.md](../sysml-memnet-documentation/references/sysml-memnet-snap.md).

| Step | Action | MemNet |
|------|--------|--------|
| **1** | `serve_status`. If `running: false` -> edit `.sysml` only; skip 2 and 6; note stale graph. | -- |
| **2** | Pin map: `pin_map(anchor=TSK_model_<short>, depth=2, max_rows=50)` | **READ** |
| **3** | Locate symbol -> edit `models/*.sysml` ([read policy](../sysml-memnet-documentation/references/sysml-memnet-read-policy.md): pin map first; Read +/-15 lines at SYM.line only) | -- |
| **4** | `mcp-sysml-v2 validate` until pass | -- |
| **5** | `sysml-view-doc-sync` **iff** outputs exist and structure changed. Interconnection figures: **[sysml-interconnection-mermaid](../sysml-interconnection-mermaid/SKILL.md)** before fenced Mermaid. | -- |
| **6** | MemNet delta + SYM.line refresh; step atoms + settle turn ([pipeline](../sysml-memnet-documentation/references/sysml-memnet-pipeline.md)) | **WRITE** |

**Warm miss** -> initial snap per [sysml-memnet-documentation](../sysml-memnet-documentation/SKILL.md), then step 3.

**Skip step 6** only: comment/whitespace-only edit; MemNet down; user question with no edit.

### Read budget (step 3)

| Do | Don't |
|----|-------|
| Pin map on `TSK_model_*` then SYM window | `Read` entire `deploy-*.sysml` each turn |
| One `Grep` per unknown symbol | Re-grep names already on the pin map |
| `mcp-sysmledgraph` before cross-file rename | Re-read all requirements + root for one link |

Full policy: [sysml-memnet-read-policy.md](../sysml-memnet-documentation/references/sysml-memnet-read-policy.md).

Also: confirm project/scope; derive plans from the model when needed.

## Routing

- MemNet cache (relatives read/write): `sysml-memnet-cache` -> `mcp-memnet` tools
- MemNet policy / snap procedure: `sysml-memnet-documentation`
- Session preflight: `sysml-modeling-session-checklist`
- New project root/config or load order: `sysml-root-config`, `sysml-import-order-helper`
- Requirements, traceability, audits: `sysml-requirements-generator`, `sysml-traceability`, `sysml-requirements-audit`
- Ports, parts, items: `sysml-physical-port-generator`, `sysml-hardware-part-generator`, `sysml-software-port-generator`, `sysml-software-part-generator`, `sysml-item-generator`
- Wiring, interconnection, outputs sync: `sysml-connections`, `sysml-view-doc-sync`
- Behaviour or state machines: `sysml-behaviour-generator`, `sysml-view-doc-sync`
- Rename, migration, blast radius: `sysml-refactorer`, `mcp-sysmledgraph`
- Shared library changes or file splits: `sysml-common-lib-contribution`, `sysml-common-file-scale`
- Part maturity gate: `sysml-part-reviewer`
- Long-form outputs packs: `project-output-article`, `system-design-report-generator`
- EAGLE / de-facto PCBA alignment: `sysml-pcba-de-facto-alignment`

## File rules

- File names: lowercase with hyphens, using `requirements`, `deploy`, `root`, and optionally `connections` or `behaviour`.
- Package names: project-specific PascalCase; root package is `Project<ProjectNamePascalCase>`.
- Load order: Kernel -> optional ISQ/SI -> libs -> requirements -> optional connections -> deploy -> optional behaviour -> root last.
- Root file: `root-<project>.sysml` imports all project packages and stays last in `config.yaml`.
- Common protocol ports use nested pins; physical pin maps stay in `.md`.
- `AGENT-CONTEXT.md`: thin human stub (session, anchor, summary); agents use MemNet for topology/backlog.

## Pipeline atoms (between steps)

When MemNet is up, each step writes MemNet atoms in the **shared dialect** -- not chat scratch encodings.

Template: [sysml-memnet-pipeline.md](../sysml-memnet-documentation/references/sysml-memnet-pipeline.md).

## Validation and sync

- After any `.sysml` edit, run `mcp-sysml-v2 validate`.
- Use `preview` for Mermaid or BDD/IBD checks when a diagram is needed.
- Keep `projects/<name>/outputs/` aligned with the model.

## See also

- [AGENTS.md](../../../AGENTS.md)
- [sysml-memnet-snap.md](../sysml-memnet-documentation/references/sysml-memnet-snap.md)
- [sysml-memnet-read-policy.md](../sysml-memnet-documentation/references/sysml-memnet-read-policy.md)
- [sysml-modeling-session-checklist](../sysml-modeling-session-checklist/SKILL.md)
- [mcp-sysml-v2](../mcp-sysml-v2/SKILL.md)
