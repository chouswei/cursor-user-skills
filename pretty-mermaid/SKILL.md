---
name: pretty-mermaid
description: >-
  Themed Mermaid export via beautiful-mermaid: SVG themes, ASCII/terminal art,
  and batch render. Use when the user asks to beautify, apply a theme, export
  themed SVG, ASCII diagram, or batch-render .mmd files. Not for: authoring or
  fixing Mermaid from scratch (mermaid), mmdc CLI flags (mmdc), or declutter
  layout passes (mermaid-doc-readability). Validate with mmdc first when syntax
  is uncertain.
metadata:
  pattern: tool-wrapper
  version: "1.1"
  domain: documentation
  pairs_with: [mermaid, mmdc]
---

# Pretty Mermaid

Render themed SVG or ASCII from existing Mermaid source. Does **not** replace [mermaid](../mermaid/SKILL.md) authoring or [mmdc](../mmdc/SKILL.md) validation.

**Scripts live in this skill folder** (`~/.cursor/skills/pretty-mermaid/scripts/`).

## When to use

| Goal | Action |
|------|--------|
| Themed SVG (slides, static embed) | `scripts/render.mjs` + `--theme` |
| ASCII / terminal / plain README | `--format ascii` |
| Batch folder of `.mmd` | `scripts/batch.mjs` |
| New diagram or syntax fix | **Defer to** [mermaid](../mermaid/SKILL.md) |
| Plain CLI SVG/PNG/PDF | Prefer [mmdc](../mmdc/SKILL.md) |

Bridge: [mermaid/references/pretty-mermaid-bridge.md](../mermaid/references/pretty-mermaid-bridge.md). Upstream: [Pretty-mermaid-skills](https://github.com/imxv/Pretty-mermaid-skills).

## Quick start

```bash
# List themes
node ~/.cursor/skills/pretty-mermaid/scripts/themes.mjs

# Single themed SVG
node ~/.cursor/skills/pretty-mermaid/scripts/render.mjs \
  --input diagram.mmd \
  --output diagram.svg \
  --format svg \
  --theme github-light

# ASCII
node ~/.cursor/skills/pretty-mermaid/scripts/render.mjs \
  --input diagram.mmd \
  --format ascii \
  --use-ascii

# Batch
node ~/.cursor/skills/pretty-mermaid/scripts/batch.mjs \
  --input-dir ./diagrams \
  --output-dir ./output \
  --format svg \
  --theme tokyo-night \
  --workers 4
```

**First run:** `cd ~/.cursor/skills/pretty-mermaid ; npm install` if auto-install fails.

## Theme picks

| Context | Theme |
|---------|--------|
| Dark docs | `tokyo-night`, `github-dark` |
| Light docs | `github-light`, `zinc-light` |
| High contrast / slides | `zinc-light`, `dracula` |

Full list: `node scripts/themes.mjs` · detail [references/THEMES.md](references/THEMES.md).

## Options (common)

- `--transparent` — transparent background
- `--font "JetBrains Mono"` — custom font
- `--bg` / `--fg` / `--accent` — colour overrides
- `--padding-x` / `--padding-y` — ASCII spacing

## Diagram type templates

Copy from `assets/example_diagrams/` only as starting `.mmd`; syntax and layout rules stay in [mermaid](../mermaid/SKILL.md) and [references/DIAGRAM_TYPES.md](references/DIAGRAM_TYPES.md).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Cannot find module 'beautiful-mermaid'` | `npm install` in this skill folder |
| Parse error | Validate with `mmdc -i file.mmd`; see [mermaid](../mermaid/SKILL.md) error table |
| File not found | Use absolute paths on Windows |

## Resources

- `scripts/render.mjs`, `batch.mjs`, `themes.mjs`
- `references/THEMES.md`, `DIAGRAM_TYPES.md`, `api_reference.md`
- `assets/example_diagrams/*.mmd`
- Local Windows notes: [LOCAL_PATCHES.md](LOCAL_PATCHES.md)
