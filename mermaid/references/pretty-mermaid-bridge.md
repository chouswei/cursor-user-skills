# pretty-mermaid bridge (themed SVG / ASCII)

**Skill:** `~/.cursor/skills/pretty-mermaid/` — cloned from [imxv/Pretty-mermaid-skills](https://github.com/imxv/Pretty-mermaid-skills) (MIT).

Use **after** the [mermaid](../SKILL.md) pipeline validates with `mmdc`. pretty-mermaid does **not** replace syntax validation.

---

## When to use

| Goal | Tool |
|------|------|
| Author / fix Mermaid | **mermaid** ([SKILL](../SKILL.md)) |
| Syntax check, CI, plain SVG/PNG/PDF | **mmdc** ([mmdc](../../mmdc/SKILL.md)) |
| Themed SVG for slides, ClickUp, static embed | **pretty-mermaid** |
| ASCII in README / terminal | **pretty-mermaid** `--format ascii` |
| Cluttered / tiny charts | **mermaid-doc-readability** ([SKILL](../../mermaid-doc-readability/SKILL.md)) |
| Prince PDF from HTML | Repo `tools/bake_html_mermaid_for_prince.py` (inline SVG via mmdc) when that tool exists |

---

## Commands

```bash
# List themes
node ~/.cursor/skills/pretty-mermaid/scripts/themes.mjs

# Single diagram
node ~/.cursor/skills/pretty-mermaid/scripts/render.mjs \
  -i path/to/diagram.mmd \
  -o path/to/diagram.svg \
  --theme github-light

# Batch (report diagram folder)
node ~/.cursor/skills/pretty-mermaid/scripts/batch.mjs \
  --input-dir ./diagrams \
  --output-dir ./rendered \
  --theme tokyo-night
```

**Windows:** skill scripts use `pathToFileURL` for `beautiful-mermaid` load (patched in user pack).

**First run:** `cd ~/.cursor/skills/pretty-mermaid && npm install` if auto-install fails.

---

## Theme guide (from upstream)

| Context | Theme |
|---------|--------|
| Light system-design report | `github-light`, `zinc-light` |
| Dark IDE / technical blog | `tokyo-night`, `github-dark` |
| High-contrast slides | `zinc-light`, `dracula` |

---

## Diagram authoring

pretty-mermaid renders **the same Mermaid source** as `mmdc`. Layout rules live in:

- [state-diagram-layout.md](state-diagram-layout.md)
- [repo-mermaid-rules.md](repo-mermaid-rules.md)
- [viewport-and-layout.md](viewport-and-layout.md)

Upstream templates: `~/.cursor/skills/pretty-mermaid/assets/example_diagrams/*.mmd`
