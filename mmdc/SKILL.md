---
name: mmdc
description: >-
  Expert reference for mermaid-cli (mmdc): validate and render Mermaid via CLI
  (SVG/PNG/PDF), install, and troubleshoot mmdc errors. Use when the user asks
  about mmdc options, mermaid-cli install, or CLI export. Not for: authoring
  diagrams (mermaid), themed/ASCII export (pretty-mermaid), or declutter-only
  rewrites (mermaid-doc-readability).
metadata:
  pattern: tool-wrapper
  domain: documentation
  version: "1.3"
  specialization: library-guide
  pairs_with: [mermaid, pretty-mermaid]
---

# mmdc (mermaid-cli)

CLI specialist for **validate** and **render**. Pair with [mermaid](../mermaid/SKILL.md) for authoring.

| Goal | Do |
|------|-----|
| Validate | Load [references/commands.md](references/commands.md); run `mmdc -i file.mmd`; fix and re-validate |
| Render SVG/PNG/PDF | Same reference; correct `-i` / `-o`; themes `-t neutral` / `-t dark`, `-b #ffffff` when asked |
| Themed / ASCII export | After `mmdc` passes, defer to [pretty-mermaid](../pretty-mermaid/SKILL.md) or [pretty-mermaid-bridge](../mermaid/references/pretty-mermaid-bridge.md) |
| Parse / label errors | [mermaid](../mermaid/SKILL.md) Error Handling + prohibited-characters table |
| Cluttered chart | [mermaid-doc-readability](../mermaid-doc-readability/SKILL.md) |

**Install:** `npm install -g @mermaid-js/mermaid-cli` or `npx @mermaid-js/mermaid-cli`
