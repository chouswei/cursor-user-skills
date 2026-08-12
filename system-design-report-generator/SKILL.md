---
name: system-design-report-generator
description: >-
  Scaffold or maintain a system design report as a folder of section .md files plus a small hub index with
  llm_toc (file paths for LLM partial reads). MemNet-first when serve is up: pin_map(TSK_model_*)
  before prose, atomise @ART/@SEC/@CLM after sync. Triggers: system design report pack, split outputs sections,
  outputs folder system design, multi-file system design, hub index llm_toc file, memnet report sync.
metadata:
  pattern: pipeline
  domain: mbse-outputs
  version: "2.4"
  pairs_with:
    - project-output-article
    - sysml-view-doc-sync
    - sysml-memnet-documentation
    - sysml-modeling-workflow
    - mermaid
    - mmdc
    - md-to-tex
    - mdtohtml
token_guardrails: |
  - **Hub first:** agents read **`index.md`** (or `README.md`) only for full-file list — **low line count (LOC)** — then open **one** `file` from `llm_toc` per task; do not load every section `.md` into context by default.
  - **MemNet before prose (when serve up):** `serve_status` → `pin_map(TSK_model_<short>)` → then hub → **one** section file. Do not grep-deploy from memory when warm rows exist.
  - **Normative layout:** [references/SYSTEM_DESIGN_REPORT_LAYOUT.md](references/SYSTEM_DESIGN_REPORT_LAYOUT.md) — do not invent a second competing root under `docs/`.
  - **MemNet pipeline:** [references/memnet-report-pipeline.md](references/memnet-report-pipeline.md) -- ART/SEC/claim atoms after sync; G/M step codes per [sysml-memnet-pipeline.md](../sysml-memnet-documentation/references/sysml-memnet-pipeline.md) (GQL / openCypher-shaped only).
  - **Model wins:** deploy/connections/behaviour/requirements `.sysml` stay authoritative; **sysml-view-doc-sync** after edits. Keep `10-requirements-traceability` and `outputs/diagrams/` plant-setup flows aligned with refine/derive + behaviour.
  - Report sections are **human-first**: write compact, precise prose. Prefer tables, bullets, and short notes; avoid long introductory filler and avoid restating the same fact in multiple sections.
  - If a section can be understood from a table plus one short sentence, do that instead of a paragraph.
  - **UTF-8 encoding:** All `.md` files **must** be UTF-8 encoded (no mixed encoding, no BOM). Merge using Python (see skill): read each file with explicit `encoding='utf-8'`, combine in order, write merged output as UTF-8. **No Unicode sanitization needed** — proper UTF-8 handles all special characters (–, →, ↔, ×, §) correctly.
  - **Section files are merge inputs only:** Remove all inter-section cross-references ("See chapter X", "See section Y") before merging. Individual files are not meant to be read standalone.
  - **Do not commit merged files to git** — keep only section `.md` files as authoritative source; generate exports (merged `.md`, HTML, LaTeX) on-demand using Python merge script.
---

# System design report generator (multi-file pack)

**When:** A **system design** (or similar) narrative is large enough that **one monolithic `*-system-design.md`** is hard for agents to navigate, or the team wants **sections as separate files** with a **machine-readable map** (`llm_toc` with **`file`** entries).

These packs are for human readers too, so keep each section tight and purposeful. The hub should orient the reader; the section files should explain only what is needed.

## Pairing

- **project-output-article** — same section semantics and Mermaid rules; this skill adds **folder + file split** + **hub `llm_toc`**.
- **sysml-view-doc-sync** — update **every** touched section file after deploy changes.
- **sysml-memnet-documentation** — **pin_map** before generate/maintain; **atomise** `@ART`/`@SEC`/`@CLM` after sync ([memnet-report-pipeline.md](references/memnet-report-pipeline.md)).
- **sysml-modeling-workflow** — validate `.sysml` before report delta; report maintenance is step 5 follow-on, not a substitute for model snap.
- **md-to-tex** — pass **hub `llm_toc` order** as Pandoc input list for multi-file → one `.tex`.
- **mdtohtml** — export section files to HTML (Mermaid rendering, UTF-8 safe, handles encoding correctly).

## Pipeline

### A — Generate or refresh full pack

1. **MemNet preflight** — `serve_status`. If up: read `AGENT-CONTEXT.md` → `pin_map(TSK_model_<short>, depth=2)`. Warm miss → initial model snap per **sysml-memnet-documentation** before writing prose.
2. **Read layout** — [references/SYSTEM_DESIGN_REPORT_LAYOUT.md](references/SYSTEM_DESIGN_REPORT_LAYOUT.md) (folder name, hub schema, section filenames, **LOC** discipline).
3. **Create or adopt folder** — Under `sysml-v2-models/projects/<name>/outputs/`, use pack root **`system-design-report/`** (or legacy `system-design/` if the project already started — one pack per project, **documented in hub**).
4. **Hub file** — From [assets/hub-index-template.md](assets/hub-index-template.md): project title, **source** line (model paths), **`llm_toc`** with **`file`**, optional **`llm_keywords`**, optional **`memnet:`** block (anchor, `art_id`, session, cross-artifact manuals).
5. **Section files** — From [assets/section-template.md](assets/section-template.md): content from **warm graph + deploy grep** — exact `link*` names, requirement ids (parent/child via refine/derive), behaviour action names, de-facto part notes from model `doc` comments.
6. **Sync** — Run **sysml-view-doc-sync**; validate **mermaid** / **mmdc** only when rendering assets. Include **`outputs/diagrams/`** commissioning / plant-setup flowcharts when behaviour defines them; keep **`10-requirements-traceability`** in step with the requirements package.
7. **MemNet report delta** — [references/memnet-report-pipeline.md](references/memnet-report-pipeline.md): `@ART` + `@SEC` per hub section + key `@CLM` facts with `mentions` EDGs to `@CON`/`@PRT`/`@REQ`. Skip only if `serve_status` false.
8. **Pointers** — Update `outputs/README.md`; keep `AGENT-CONTEXT.md` thin (session + anchor + `ART_*` ids, not topology).

### B — Maintain one section (incremental)

1. `query_warm` on touched model ids.
2. Hub → pick **one** `llm_toc.file`.
3. Patch section from model; **sysml-view-doc-sync** for that file's diagrams.
4. MemNet: update/add `@CLM` + EDGs for changed claims only.

## Exporting to merged views (HTML, LaTeX, PDF)

**Policy: Do not commit merged files to git.** Keep only section `.md` files; generate exports on-demand.

### HTML Export Workflow (Recommended)

**Step 1: Merge section files using Python (UTF-8 safe)**

Use the **Python merge script** for explicit UTF-8 encoding and Unicode preservation:

```bash
# Copy merge_markdown.py from skill references (one-time setup)
cp .cursor/skills/mdtohtml/references/merge_markdown.py tools/merge_markdown.py

# Merge all sections in llm_toc order
cd sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report
python ../../../tools/merge_markdown.py leo-laser-comm-PAT-system-design-merged.md \
  01-abstract-introduction.md 02-architecture.md 02b-interconnection.md \
  02b1-mcu-pinmap.md 02b2-inter-hat-bridges.md 02b3-software-allocation.md \
  02b4-connector-inventory.md 03-software-allocation.md 04-state-machine.md \
  05-tracking.md 06-calibration.md 07-storage.md 08-faults.md \
  09-device-thread-states.md 10-optics.md 11-power.md 12-references.md
```

**Why Python over PowerShell?**
- ✅ Explicit UTF-8 encoding (no mixed encodings or BOM)
- ✅ Unicode characters (–, →, ↔, ×, §) preserved intact through pipeline
- ✅ Cross-platform (Windows, macOS, Linux) identical behavior
- ✅ No character sanitization needed; proper encoding handles it all

**Before merge (optional for individual section inspection):**

Individual `.md` files should **NOT contain cross-references** (e.g., "See section X" or "See chapter 3") since they are inputs to merge, not standalone documents. Remove all inter-section links before merging.

**Step 2: Validate Mermaid diagrams (MANDATORY)**

```bash
# Validate merged markdown for Mermaid parse errors
mmdc -i leo-laser-comm-PAT-system-design-merged.md

# If errors occur, fix them in source section files, then re-merge and re-validate
```

**Step 3: Convert to HTML**

```bash
cd c:\Projects\SystemDesign
python tools/md_to_html.py sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report/leo-laser-comm-PAT-system-design-merged.md
```

**Result:** `leo-laser-comm-PAT-system-design-merged.html` with:
- ✅ Mermaid diagrams rendered inline (no separate rendering step)
- ✅ Syntax highlighting for code blocks
- ✅ Dark theme applied by default
- ✅ UTF-8 special characters preserved (→, –, ·, §) — no corruption
- ✅ Responsive mobile/desktop layout
- ✅ Fully self-contained (no external CSS/JS dependencies)

### LaTeX/PDF Export Workflow

1. **Merge section files** (same PowerShell as above)
2. **Convert to LaTeX** — Use [md-to-tex](../md-to-tex/SKILL.md) skill:
   ```bash
   python tools/md_to_tex.py leo-laser-comm-PAT-system-design-merged.md
   ```
   - Pandoc with `-f utf-8 -t latex` flags (handles special characters)
   - Output: `leo-laser-comm-PAT-system-design-merged.tex`
3. **Compile PDF**:
   ```bash
   pdflatex leo-laser-comm-PAT-system-design-merged.tex
   ```
   Or use [mcp-latex](../mcp-latex/SKILL.md) skill for Cursor integration

### Diagrams in Exports

- **HTML:** Mermaid.js renders all diagrams live in browser
- **LaTeX:** Mermaid blocks output as verbatim; optionally pre-render to SVG with **mmdc** skill and embed via `\includegraphics{diagram.svg}`

### Automation & Tooling

Write a shell script or Makefile to regenerate exports on-demand:

```bash
#!/bin/bash
# export-report.sh — regenerate merged HTML + LaTeX on-demand

cd sysml-v2-models/projects/leo-cubesat-laser-comm/outputs/system-design-report

# Merge sections (see PowerShell script above, or write in Bash)
# [merge logic here]

# Convert to HTML
python ../../../tools/md_to_html.py leo-laser-comm-PAT-system-design-merged.md

# Convert to LaTeX
python ../../../tools/md_to_tex.py leo-laser-comm-PAT-system-design-merged.md

# Compile PDF (if TeX available)
# pdflatex leo-laser-comm-PAT-system-design-merged.md

echo "✓ HTML, LaTeX, and optionally PDF exported"
```

**Encoding Guardrail:**
- When merging UTF-8 `.md` files, **use Python** for explicit UTF-8 mode (see `tools/merge_markdown.py`)
- ✅ Python: `encoding='utf-8'` at read and write
- ❌ PowerShell UTF-8 can have encoding issues; not recommended
- **Result:** Special characters (→, –, ·, §) display correctly; prevents `?` or `â†'` corruption
- **Rule:** Section files should NOT have inter-section cross-references (since they're merge inputs, not standalone)

**Standard (monolith vs pack):** [project-output-article / PROJECT_OUTPUT_ARTICLE_STANDARD.md](~/.cursor/skills/project-output-article/references/PROJECT_OUTPUT_ARTICLE_STANDARD.md) § Multi-file pack.

## References

- [SYSTEM_DESIGN_REPORT_LAYOUT.md](references/SYSTEM_DESIGN_REPORT_LAYOUT.md)
- [memnet-report-pipeline.md](references/memnet-report-pipeline.md)
- [hub-index-template.md](assets/hub-index-template.md)
- [section-template.md](assets/section-template.md)
