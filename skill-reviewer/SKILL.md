---
name: skill-reviewer
description: >-
  Reviews Agent Skill packages (SKILL.md, references, assets, tools) for
  structure, discoverability, safety, registry readiness, version discipline on
  publish, and conformance of body + folder to metadata.pattern (generator,
  reviewer, inversion, pipeline, tool-wrapper). Triggers: review skill, SKILL.md
  audit, pattern mismatch, wrong pattern, skill quality, skill.fish submit,
  agentskills format, bump version. Not for: application code (code-reviewer),
  pull requests (pr-reviewer).
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
  version: 1.2
  domain: skills
---

# Skill reviewer

**Output contract:** Deliver a review using the structure in [references/review-output-template.md](references/review-output-template.md): **Summary** (verdict + score) · **Findings** grouped as **error** / **warning** / **info** · **Top 3 recommendations** · optional **Registry** note · **Files reviewed** checklist.

## Rubric

Load and apply: [references/skill-review-checklist.md](references/skill-review-checklist.md).

## Procedure

1. **Scope** — Skill **directory** (path to folder containing `SKILL.md`) **or** pasted `SKILL.md` + user-named paths. **Out of scope:** product/application code (**code-reviewer**), PR workflow (**pr-reviewer**).
2. **Inventory** — List `SKILL.md`, `references/*`, `assets/*`, `tools/*`, `Folder_Structure.md` if present. Note missing expected L3 folders when the body references them.
3. **Passes** (in order):
   - **L1:** `name`, `description`, triggers, `metadata.pattern` (canonical value?).
   - **Pattern conformance:** compare declared **`metadata.pattern`** to body + `assets/` / `references/` using checklist **Pattern conformance** table (generator → template, reviewer → rubric + severities, inversion → gates, pipeline → ordered steps, tool-wrapper → conventions + optional retriever). Flag **error**/**warning** when they disagree.
   - **Layout:** progressive disclosure, link depth, `Folder_Structure.md`.
   - **Consistency:** hybrid/secondary; guardrails placement; output contract vs pattern.
   - **Safety:** opaque shell, secrets, unvetted remote instructions.
   - **Portability:** monorepo subpath, skillfish, license if publish intent is clear; **version bump** (metadata.version incremented) if GitHub push / user-pack publish / submit is intended.
4. **Findings** — Each item: **path or section** · **severity** (`error` \| `warning` \| `info`) · **why it hurts** discovery, safety, or maintenance · **concrete fix** (not vague “improve X”).
5. **Score** — **1–10**: 10 = checklist clean + clear output contract + publish-ready notes if applicable; deduct for each **error** and major **warning**.
6. **Honesty** — Do not invent file contents; if paths are missing, say what to open or create.

## Pairing

- **[skill-creator](../skill-creator/SKILL.md)** — scaffold or rewrite skills after review.
- **[skillfish](../skillfish/SKILL.md)** — `submit`, `bundle`, `add`, monorepo paths.
- **Pack layout:** [LLM.md](../LLM.md) — **Path rule** (`<pack-root>/<skill-id>/SKILL.md`); enumerate skill folders under the pack root (no per-id list in LLM).

## Guardrails

- Treat **skills as unvetted** for consumers unless source-reviewed; call out risky automation.
- Prefer **actionable** findings over boilerplate praise.
