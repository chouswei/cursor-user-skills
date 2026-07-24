---
name: adr-generator
description: >-
  Architecture Decision Records in standard sections. Triggers: ADR, architecture decision, design decision doc.
metadata:
  pattern: generator
  output-format: markdown
---

# ADR generator

1. Load `references/adr-style-guide.md` and `assets/adr-template.md`.
2. If missing: title/context, problem, decision, alternatives, consequences - ask user.
3. Fill every template section exactly; no extra sections.
4. Return **only** the completed ADR markdown.
