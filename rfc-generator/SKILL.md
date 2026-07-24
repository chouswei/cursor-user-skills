---
name: rfc-generator
description: >-
  RFC / technical design proposal in standard sections. Triggers: RFC, design proposal, tech spec draft.
metadata:
  pattern: generator
  output-format: markdown
---

# RFC generator

1. Load `references/rfc-style-guide.md` and `assets/rfc-template.md`.
2. If missing: title, motivation, proposed solution, alternatives, implementation notes - ask user.
3. Fill every template section exactly; no extra sections.
4. Return **only** the completed RFC markdown.
