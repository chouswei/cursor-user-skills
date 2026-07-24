# Project output article standard

Normative rules for **long-form Markdown** under `sysml-v2-models/projects/<name>/outputs/` (e.g. `*-system-design.md`, interconnection, behaviour). Intended for **LLM navigation** and **human reading** without duplicating a second standard in `docs/`.

## Goals

- One predictable **section order** across projects.
- A **machine-readable outline** (`llm_toc`) so agents jump to the right `##` without scanning the whole file; optional **`llm_keywords`** (synonyms/part names → same `#id`s) in the **same** top fence for partial-read routing.
- **Mermaid** as the default diagram dialect inside `.md` (~/.cursor/skills/mermaid/SKILL.md)).
- **De facto alignment**: names and port paths match **`deploy-*.sysml`** (and connections packages), not stale labels.

## LLM-first table of contents (`llm_toc`)

**Required** for new or heavily revised output articles when agents are expected to edit or review them.

Place **after** the document `#` title and **source line** (which `.sysml` files back the doc), and **before** the main body sections.

Use **one** fenced block, language tag `yaml` or `json`. The block may contain **`llm_toc` only** or **`llm_toc` plus `llm_keywords`** (see below).

**YAML example (TOC only):**

```yaml
llm_toc:
  - id: part-tree
    title: Part tree
  - id: interconnection-view
    title: Interconnection view
```

**YAML example (TOC + optional keywords in the same fence):**

```yaml
llm_toc:
  - id: part-tree
    title: Part tree
  - id: interconnection-view
    title: Interconnection view
llm_keywords:
  fieldPoESwitch: interconnection-view
  GS728TPv3: part-tree
```

**JSON example:**

```json
{
  "llm_toc": [
    { "id": "part-tree", "title": "Part tree" },
    { "id": "interconnection-view", "title": "Interconnection view" }
  ]
}
```

**JSON with keywords (same object as `llm_toc`):**

```json
{
  "llm_toc": [
    { "id": "part-tree", "title": "Part tree" },
    { "id": "interconnection-view", "title": "Interconnection view" }
  ],
  "llm_keywords": {
    "fieldPoESwitch": "interconnection-view",
    "GS728TPv3": "part-tree"
  }
}
```

### Rules for `id` and `title`

- **`title`** — Plain text; should match the corresponding **`##` heading** (or the visible heading text).
- **`id`** — Fragment for deep links (`#id`). Must match the **anchor** your renderer generates for that heading (e.g. GitHub-style slug: lowercase, spaces to hyphens, strip most punctuation). If unsure, use the heading text without `##` and slugify: `Part tree` → `part-tree`.
- **Order** — List `llm_toc` entries in **document order** (top to bottom).

## Optional keyword index (`llm_keywords`)

**Optional.** Add in the **same** top `yaml` / `json` fence as `llm_toc`, as a second root key **`llm_keywords`**.

- **Shape** — Flat map: **keyword string → `id` string** (the heading fragment only, no `#`). Keys are **synonyms, part names, acronyms**, or other terms readers might search for; values must match an **`id`** from `llm_toc` or any **`##`** heading in the file.
- **Purpose** — Lets agents resolve **non-title** terms to a section **before** reading long body text (works best with partial reads: grep, jump to `#id`). A **large keyword index at the bottom** of the file does **not** help early routing and adds tokens after the main content; avoid duplicating a full keyword index for agents there.
- **Size** — Keep **small** (on the order of **15 entries**). Prefer high-signal names only; do not list every part string from the doc.
- **YAML keys** — Quote keys that contain spaces or special characters (e.g. `"X710-DA2": interconnection-view`).

## Optional human TOC

Below `llm_toc`, you may add a short **Markdown** list:

```markdown
- [Part tree](#part-tree)
- [Interconnection view](#interconnection-view)
```

Keep it in sync when sections move or rename.

## Recommended section order

Use only what applies; omit empty sections. Typical system-design articles:

1. **Title** — `# …` plus one paragraph **scope** and **source** (model paths, key packages).
2. **Part tree** — Hierarchical tree (fenced text or list) aligned with deploy nesting.
3. **Connections / interconnection** — Tables or diagrams; **exact** port paths from deploy.
4. **Behaviour** — States, actors, or summary table if `behaviour-*.sysml` exists.
5. **Power / estimates** — If relevant (budgets, assumptions).
6. **References** — Datasheets, external specs, repo paths.

Large topics (e.g. scale-out variant) may use **`##`** subsections; add each to `llm_toc` if agents need direct jumps.

## Mermaid

- **Canonical:** Mermaid **source** lives in the **`.md`** file.
- Follow [repo-mermaid-rules](~/.cursor/skills/mermaid/references/repo-mermaid-rules.md) (short labels, direction, subgraph rules).
- **Rendering** to PNG/SVG/HTML is **optional** and tooling-specific; use the **mmdc** skill when the user asks for assets.

## Alignment with the model

- **Authoritative:** `deploy-*.sysml`, `connections-*.sysml`, `behaviour-*.sysml`, `requirements-*.sysml`.
- **Procedure:** [sysml-view-doc-sync/SKILL.md](../../sysml-view-doc-sync/SKILL.md); traceability: [sysml-traceability](../../sysml-traceability/SKILL.md).
- **Pin maps:** Physical pin numbering stays in **`.md`** or dedicated pinmap files, not as the only description of logical ports in the model.

## Multi-file system design report pack (optional)

When a single `*-system-design.md` is **too large** for efficient agent reads, use a **folder pack** with a **hub** and **section files**. Normative layout, **`llm_toc` with `file`**, and **LOC** rules: **[system-design-report-generator/references/SYSTEM_DESIGN_REPORT_LAYOUT.md](~/.cursor/skills/system-design-report-generator/references/SYSTEM_DESIGN_REPORT_LAYOUT.md)**.

- **Hub** — Small `index.md` or `README.md` under e.g. `outputs/system-design-report/` lists sections with **`llm_toc`** entries `{ id, title, file }`; agents **read hub first**, then **one** `file` per task.
- **Sections** — One topic per `.md` file; **same** alignment and Mermaid rules as this standard.
- **Either/or** — Do not maintain **both** a full monolith and a full duplicate pack; migrate with a one-line supersession note if needed.
- **Merging into single `.md`:** Before final merge, **remove all inter-file cross-references** (e.g. `[./filename.md#section](./filename.md#section)`). Replace with **same-document anchor links**: `[§ Section Title](#section-anchor)`. Use section search/replace to batch-update all links at once. The merged file becomes self-contained with no relative path refs to sibling `.md` files.

## Portability

See [portability.md](portability.md) for copying this skill to another repo.
