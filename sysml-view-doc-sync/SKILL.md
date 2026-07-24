---
name: sysml-view-doc-sync
description: >-
  After SysML structure/behaviour changes: align projects/<name>/outputs/*.md (system design, interconnection,
  behaviour) and optional Mermaid; use SysML v2 MCP preview for BDD/IBD checks—not visualizeFile unless user
  asks. Preserve de facto alignment: markdown must use the same port names and site conventions as deploy
  (see sysml-traceability/references/de-facto-modeling.md). Interconnection Mermaid: layered topology, short
  edge labels + legend, one diagram per intent—see references/interconnection-mermaid.md. Triggers: sync doc
  to model, update outputs from deploy, diagram from sysml, IBD markdown, operator-facing wiring table.
metadata:
  pattern: pipeline
  pairs_with: [mcp-sysml-v2, mermaid, mmdc, sysml-connections, sysml-behaviour-generator, project-output-article, system-design-report-generator]
token_guardrails: |
  - Model is source of truth; do not invent structure only in .md.
  - Obey mcp-sysml-v2 references/cursor-mcp-rules.md for preview vs visualizeFile.
  - For interconnection flowcharts: follow references/interconnection-mermaid.md; prefer short Mermaid; validate with mmdc when user wants rendered assets or CI checks diagrams.
  - Submodule / canonical repo: [project-in-another-repo.mdc](../../../.cursor/rules/project-in-another-repo.mdc), [DOCS_INDEX.md](../../../docs/DOCS_INDEX.md). MBSE vs implementation: [AGENTS.md](../../../AGENTS.md) scope table.
  - `outputs/*.md` are for human reading: keep prose short, precise, and non-redundant. Use tables or bullets for dense wiring detail instead of long paragraphs.
  - **UTF-8 encoding:** All `.md` files must be saved as UTF-8 (no BOM, no mixed encoding). When syncing from model, preserve UTF-8 throughout. If editing `.md` in an editor, ensure UTF-8 is the output encoding.
  - After substantive .sysml changes: run sysml-modeling-workflow step 6 (MemNet delta + line refresh).
  - Before multi-file refactor: query_warm(TSK_model_*).
  - **Special character sanitization:** When merging or exporting `.md` files, replace Unicode special chars with ASCII to prevent Mermaid parser errors:
    - En-dash `–` → hyphen `-`
    - Em-dash `—` → hyphen `-`
    - Right arrow → keep as `->` (ASCII)
    - Double arrow `↔` → `<->`
    - Multiplication `×` → `x`
    - Section symbol `§` → `s.`
  - **Mermaid parser safety:** Validate merged `.md` files with `mmdc` before publication; if parse error occurs in a diagram with labels, sanitize Unicode chars in labels first.
---

system_instruction: |
  Prefer plain Markdown tables or domain wire; do not use TOON/TRON. JSON only at tool boundaries.


# SysML view & doc sync

**When:** User updated **`.sysml`** and **`outputs/*.md`**, diagrams, or HTML exports should **match** the model.

This skill should help the report read cleanly, not just stay mechanically synced.

**Pairing:** For long-form **`outputs/*.md`** structure, TOC, and section order, see **[project-output-article](../project-output-article/SKILL.md)** (references `PROJECT_OUTPUT_ARTICLE_STANDARD.md`). For **split** system design packs (**hub + section files**), see **[system-design-report-generator](../system-design-report-generator/SKILL.md)** — sync **every** section file after deploy edits; then run report MemNet delta (`@ART`/`@SEC`/`@CLM`) per [memnet-report-pipeline.md](../system-design-report-generator/references/memnet-report-pipeline.md) when serve is up.

**Interconnection / IBD-style Mermaid:** See **[sysml-interconnection-mermaid](../sysml-interconnection-mermaid/SKILL.md)** (canonical pipeline) and **[references/interconnection-mermaid.md](references/interconnection-mermaid.md)** (layout quick ref). Repo-wide prose rules: [repo-mermaid-rules](../mermaid/references/repo-mermaid-rules.md).

## Pipeline

1. **Identify outputs** — `projects/<name>/outputs/` — which `.md` (or **`system-design-report/`** hub + `*.md` sections) reference deploy part names, connections, states (see project README or DOCS_INDEX). For packs, read **hub `llm_toc`** first, then the **section `file`** you need.

2. **Diff narrative** — Update sections: architecture, part tree, connection summary, behaviour states — **from** grep/read of deploy and behaviour files, not from memory. Copy **exact** qualified port paths from deploy for tables (de facto wiring).
   Keep prose terse and factual; avoid repeating port lists in multiple paragraphs when one table or caption suffices.

3. **Mermaid (system / interconnection)** — Load **[sysml-interconnection-mermaid](../sysml-interconnection-mermaid/SKILL.md)** first. Model-first inventory: [architecture-diagrams](../mermaid/references/architecture-diagrams.md). Placement: MemNet `TSK_diagram_*` or Markdown `DiagramPlan` per [mermaid-placement-by-degree](../mermaid/references/mermaid-placement-by-degree.md) **before** fenced blocks. Layout/legend: [interconnection-mermaid.md](references/interconnection-mermaid.md):
   - **Traceability:** part usage names and **exact `link*` edge labels** from deploy (and nested PCBA def for `linkMcuTo*` / `linkPowerTo*`).
   - **Clarity:** prefer one labeled edge per block pair in overview diagrams; collapse repeated channels into a single summary edge when the channel list is already captured in the caption or table.
   - **Mounted controller rule:** if the controller is on a HAT or carrier, show only the physical HAT-to-controller links in the interconnect figure; keep software telemetry links in text or a software-flow diagram.
   - **Layers:** separate **core LAN**, **field uplink**, and **station / edge chains** in distinct subgraphs or vertical bands.
   - **Labels:** short on arrows; expand in a **legend** line or the **Connections** table (SysML `link*` names).
   - **Scope:** split **full deploy** vs **scale-out fabric-only** mini-diagrams instead of one overloaded chart.
   - **`%%` title** line for export/diff identity.
   - **Optional:** `classDef` for office vs field vs terminal; directed `-->` from switch to field legs where it aids reading.
   - **Validate AFTER edit:** Run `mmdc -i <diagram>.mmd` to catch parse errors before rendering or export. **Fix all errors before finalizing.**

4. **SysML diagrams** — **SysML v2 MCP preview** for structural sanity; **not** **visualizeFile** / **visualize.py** unless user explicitly asks ([cursor-mcp-rules](../mcp-sysml-v2/references/cursor-mcp-rules.md)).

5. **Optional HTML IBD** — If the project defines `ibd_html_path` in `config.yaml`, run `visualize.py --diagram ibd --format html` after deploy edits so **generated** Mermaid matches the model; align **manual** diagrams in `.md` per step 3.

6. **Index** — If new doc area: consider **`docs/DOCS_INDEX.md`** per repo rules (user-directed).

7. **MemNet report atoms (pack only)** — If project has `outputs/system-design-report/` and `serve_status` is true: after step 2–3, batch `@CLM` for new/changed table rows + `mentions` EDGs ([memnet-report-pipeline.md](../system-design-report-generator/references/memnet-report-pipeline.md)). Skip if comment-only model edit or serve down.

**Workflow ref:** [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) — model first, then outputs
