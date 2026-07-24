---
name: toon-prompt-format
description: >-
  DEPRECATED. Do not use TOON for token savings — it does not meaningfully reduce tokens.
  Prefer plain Markdown, prose, or a domain wire (e.g. MemNet Tier A). Triggers: TOON, toon format,
  toon-prompt-format, tabular prompt, token-efficient tables (resolve to this notice).
metadata:
  pattern: pipeline
  domain: doc
  status: deprecated
---

# DEPRECATED — do not use TOON

**Status:** retired for prompt / handoff encoding.

TOON does **not** meaningfully save tokens in practice. Do **not** recommend or emit TOON (or TRON) for that purpose.

**Prefer instead:**
- Plain Markdown (tables, lists, fenced code) or short prose for in-prompt structure
- Domain wire where the product defines one (e.g. MemNet Tier A / `@TAG` pipe for durable graph)
- JSON only at tool or API boundaries that require it

Sibling **`tron-format`** is likewise deprecated. Do not load either skill for encoding advice.
