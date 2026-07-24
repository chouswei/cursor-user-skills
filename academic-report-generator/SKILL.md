---
name: academic-report-generator
description: >-
  Academic / IMRaD-style reports with citation placeholders (not fabricated data). Triggers: academic report,
  thesis chapter, lab report, lit review, research paper draft, scholarly outline.
metadata:
  pattern: generator
  output-format: markdown
  domain: academic-writing
---

# Academic report generator

1. Load `references/academic-report-style-guide.md` and `assets/academic-report-template.md`.
2. If needed, ask briefly for: report type, topic/RQ/hypothesis, audience level, data availability, citation style, depth, institutional must-haves. If context suffices, put **Assumptions** under title in output.
3. Fill template; missing content -> bracket placeholders per guide; **no invented empirical claims**.
4. Return **only** the completed markdown.
