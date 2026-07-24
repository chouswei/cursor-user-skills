---
name: project-output-article
description: >-
  Canonical structure and LLM-first table of contents for long-form project output articles under
  projects/<name>/outputs/*.md (system design, interconnection, behaviour). Pair with sysml-view-doc-sync for
  deploy alignment; mermaid + mmdc for diagrams. Triggers: outputs article, system design doc, project markdown
  standard, llm_toc, llm_keywords, outputs TOC, foam detection style doc.
metadata:
  pattern: pipeline
  pairs_with:
    - sysml-view-doc-sync
    - system-design-report-generator
    - mermaid
    - mmdc
    - md-to-tex
    - skill-creator
token_guardrails: |
  - Normative article rules live in references/PROJECT_OUTPUT_ARTICLE_STANDARD.md — do not fork a second source of truth under docs/.
  - Model/deploy is authoritative; article text and Mermaid labels must match deploy part and port paths (de facto wiring).
  - These outputs are primarily for **human reading**: keep prose concise, precise, and concrete. Prefer tables, bullets, and short captions over long narrative blocks.
  - Avoid repeating the same fact in multiple places. Say it once in the clearest section, then reference it.
  - Do not paraphrase the model with extra adjectives or filler; if the model already expresses a detail cleanly, mirror it tersely or omit it.
  - Prefer one top **nav fence** (YAML or JSON) immediately after title + source: `llm_toc` plus optional `llm_keywords` in the **same** block; keep keyword map small (~15); optional human markdown TOC below. For token efficiency use **partial reads** (first fenced block at top, or grep `llm_toc` / `llm_keywords`) and **`#id` anchors** — do **not** bake in line numbers (they change when the file edits).
  - Mermaid: embed in .md; validate with mermaid skill; use mmdc only when rendering assets is requested.
  - Submodule / canonical repo: [project-in-another-repo.mdc](../../../.cursor/rules/project-in-another-repo.mdc). Scope: [AGENTS.md](../../../AGENTS.md).
---

# Project output article

**When:** Authoring or restructuring a **long** `projects/<name>/outputs/*.md` article (system design, PAT doc, interconnection) so humans and agents share one **section order** and **navigable outline**.

These articles are usually read by people first. Favor compact section prose, crisp headings, and traceable tables over model-echoing paragraphs.

## Pairing

- **sysml-view-doc-sync** — content must match **`.sysml`** deploy/behaviour; apply that skill for diffs and port paths.
- **system-design-report-generator** — **folder + section `.md` files + hub `llm_toc` with `file`** when the report is split for LLM partial reads; still follow this standard’s section semantics.
- **mermaid** / **mmdc** — diagram text vs CLI render.
- **md-to-tex** — optional export to **one** `.tex` from **one** or **several** `outputs/*.md` (pandoc multi-input or merge-first; use **`llm_toc`** order when bundling); not a substitute for article structure rules here.
- **skill-creator** — only when promoting this pattern into another repo’s skill pack ([portability](references/portability.md)).

## Pipeline

1. **Read the standard** — [references/PROJECT_OUTPUT_ARTICLE_STANDARD.md](references/PROJECT_OUTPUT_ARTICLE_STANDARD.md) (section order, `llm_toc`, optional `llm_keywords`, Mermaid rules).
2. **Choose shape** — **Monolith:** start from [assets/article-shell.md](assets/article-shell.md). **Multi-file pack:** [system-design-report-generator](~/.cursor/skills/system-design-report-generator/SKILL.md) (`outputs/system-design-report/`, hub + sections).
   - **Multi-file packs:** Section files are inputs to merge, NOT standalone documents. **Remove all inter-section cross-references** ("See section X", "See chapter Y") before final merge. Replace `[./filename.md#anchor](./filename.md#anchor)` with `[§ Section Name](#anchor)` (same-file anchor links).
3. **Emit top nav fence** — Right after title and source line, add **one** fenced **`yaml`** or **`json`** block containing:
   - **`llm_toc`** (required): list of `{ id, title }`; `id` must match heading anchors in the target renderer.
   - **`llm_keywords`** (optional): same fence, flat map keyword → existing heading `id` (~15 entries max). See [PROJECT_OUTPUT_ARTICLE_STANDARD.md](references/PROJECT_OUTPUT_ARTICLE_STANDARD.md).
   Agents should **read this block first** (partial read or search); use **`#id`** to jump to sections — not fixed line numbers (unstable across edits).
4. **Optional human TOC** — Markdown bullet list linking `#id` for readers.
5. **Fill sections** — From model: part tree, connections, behaviour, estimates, references — not from memory alone.
6. **Mermaid** — Blocks in `.md` per [mermaid skill](~/.cursor/skills/mermaid/SKILL.md); render via [mmdc](~/.cursor/skills/mmdc/SKILL.md) only if the user wants SVG/PNG/PDF.
7. **Sync check** — Run **sysml-view-doc-sync** before calling the article done.

**Workflow:** [sysml-modeling-workflow](../sysml-modeling-workflow/SKILL.md) (model first, then outputs).
