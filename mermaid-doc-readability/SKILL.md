---
name: mermaid-doc-readability
description: >-
  Improve Mermaid readability: shorten labels, reduce density, tune layout and
  fontSize via init config, then validate with mmdc. Use when diagrams are too
  small, cluttered, or hard to scan. Not for: creating new diagrams (mermaid),
  mmdc CLI reference (mmdc), or themed/ASCII export (pretty-mermaid).
metadata:
  pattern: pipeline
  version: "1.1"
  domain: documentation
  pairs_with: [mermaid, mmdc, markdown-viewer-user-pack]
---

# Mermaid Doc Readability

Specialist pass after a diagram exists. Authoring entry: [mermaid](../mermaid/SKILL.md).

## Pipeline

1. Shorten labels and merge low-value nodes.
2. Prefer `flowchart TB` for long chains.
3. Increase legibility with Mermaid init config:

```mermaid
%%{init: {'themeVariables': {'fontSize': '20px'}, 'flowchart': {'nodeSpacing': 60, 'rankSpacing': 80}} }%%
flowchart TB
  A[Input] --> B[Process] --> C[Output]
```

4. Validate:

```bash
mmdc -i <diagram.mmd>
mmdc -i <doc.md>
```

5. Remove temporary `*.svg` validation artefacts.

## Companion

- Preview / zoom: [markdown-viewer-user-pack](../markdown-viewer-user-pack/SKILL.md)
- Parser-safe labels: [mermaid](../mermaid/SKILL.md) prohibited-characters table
- Themed export after cleanup: [pretty-mermaid](../pretty-mermaid/SKILL.md)
