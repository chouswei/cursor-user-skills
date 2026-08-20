# System design report pack — layout (normative)

Applies to **LLM-navigable** system design narratives under `sysml-v2-models/projects/<name>/outputs/`. Complements [PROJECT_OUTPUT_ARTICLE_STANDARD.md](~/.cursor/skills/project-output-article/references/PROJECT_OUTPUT_ARTICLE_STANDARD.md) (monolith rules) — **same alignment and Mermaid doctrine**, different **on-disk shape**.

## Goals

- **Small hub, low LOC** — One **index** file lists all sections with **`llm_toc` + `file`** so agents **open only the section file** they need (token-efficient).
- **Stable section files** — Each file is one **cohesive topic** (part tree, interconnection, behaviour, …); avoid ten tiny fragments.
- **Single source of truth** — Still **`deploy-*.sysml`** / connections / behaviour; markdown is **reference**, not a parallel design authority.

## Folder location and name

**Recommended pack root:**

```text
sysml-v2-models/projects/<name>/outputs/system-design-report/
```

- **Alternative:** `system-design/` if the project already uses that name — **pick one** per project and **do not** duplicate two packs.
- **Optional:** `README.md` **or** `index.md` as hub — **one** hub file only (not both with divergent TOCs).

## Hub file (`index.md` or `README.md`)

**Required content:**

1. **`#` title** — Project + “System design” (or equivalent).
2. **Source line** — Which `models/*.sysml` files back the report (same as monolith standard).
3. **One fenced block** (`yaml` or `json`) with **`llm_toc`**, each entry **must** include:
   - **`id`** — Anchor fragment; must match the **primary `##`** heading in the section file (slug rules per renderer).
   - **`title`** — Human-readable; should match that heading text.
   - **`file`** — Path **relative to pack root** (e.g. `scope-and-sources.md`). This is the **LLM routing key**: agents **read hub**, then **`read_file` on `file`** only.

**Optional in the same fence:** **`llm_keywords`** — keyword → **`id`** (same as monolith standard; ids may live in section files).

**Optional — MemNet routing (recommended when serve is up):**

```yaml
memnet:
  anchor: TSK_model_<short>
  art_id: ART_<short>-design
  session: mn_…          # from AGENT-CONTEXT.md; omit if unknown
  cross_artifacts:       # manuals / external ART graphs
    - art_id: ART_asco8262
      session: mn_…
      note: de-facto valve manual
```

Agents cue **`pin_map`** on the hub `TSK_*` / `ART_*` before opening section files. leftover `anchor=` named leftover. Full procedure: [memnet-report-pipeline.md](memnet-report-pipeline.md).

**Optional:** Short Markdown bullet TOC linking `[title](./file.md#id)`.

**Hub size:** Keep under **~120 lines** if possible (overview + fence + optional TOC only). **No** long tables of parts in the hub — put those in section files.

## Section files

- **One main `##` per file** matching an **`llm_toc` `id`** (exception: intentional subsections as `###` under the same topic).
- **File naming:** `kebab-case.md`, **prefix optional** (`01-scope-and-sources.md`) if sort order must match reading order independent of filename sort — **mirror order in hub `llm_toc`** (authoritative order is **hub list**, not `ls`).
- **Mermaid:** In the section file that owns the diagram; follow [repo-mermaid-rules](~/.cursor/skills/mermaid/references/repo-mermaid-rules.md) and **project-output-article** / **sysml-view-doc-sync** interconnection rules.
- **Front matter:** Not required; if YAML metadata is used, keep it **minimal** to avoid duplicating `llm_toc`.

## Relationship to monolithic `*-system-design.md`

- **Either** a single large `*-system-design.md` **or** a **`system-design-report/`** pack — **not** two competing full narratives. If migrating, **deprecate** the monolith with a one-line pointer at the top: `Superseded by: [system-design-report/index.md](system-design-report/index.md)`.
- **Interconnection-only** or **behaviour-only** standalone docs may remain as separate `*-interconnection.md` files **outside** the pack if the project already ships them; link from hub **Related docs** if needed.

## LOC / LLM discipline

- **Read order:** Hub → **`pin_map(TSK_model_*|ART_*-design)`** (if MemNet up) → **one** `file` from `llm_toc` for the current task.
- **Do not** rely on **line numbers** inside section files for routing — use **`#id`** and **`file`** paths.
- **Grep:** `llm_toc` / `llm_keywords` in hub first; then section-local headings; deploy grep when warm miss on a symbol.

## MemNet atoms (outputs graph)

After section sync, atomise per [memnet-report-pipeline.md](memnet-report-pipeline.md):

| Markdown | MemNet |
|----------|--------|
| Pack hub `index.md` | `@ART` kind=`report` |
| Each `llm_toc` entry | `@SEC` (order = list index) |
| Table row / key fact in section | `@CLM` type=`fact` + `@EDG` `mentions` → `@CON`/`@PRT`/`@REQ` |
| De-facto BOM note | `@CLM` type=`convention` + optional `dependsOn` → external `@ART` |

**Do not** store full section prose or Mermaid in MemNet rows.

## Pandoc / md-to-tex

- Build input list from **hub `llm_toc` order** (see [md-to-tex](../../md-to-tex/SKILL.md)):  
  `pandoc index.md?` — Usually **exclude** hub from PDF body or use **merge** of **section files only** in `llm_toc` order; hub is often title page only — project choice.

## Portability

Copy this skill folder to another repo; keep pack root under `projects/<name>/outputs/` for consistency.
