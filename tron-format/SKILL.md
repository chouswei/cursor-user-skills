---
name: tron-format
description: >-
  DEPRECATED. Do not use TRON for token savings — it does not meaningfully reduce tokens.
  Prefer plain Markdown, prose, or a domain wire (e.g. MemNet Tier A). Triggers: tron format,
  tron stringify, tron parse, token reduced object notation, TRON (resolve to this notice).
metadata:
  pattern: tool-wrapper
  version: 1.2-deprecated
  domain: data-formats
  status: deprecated
---

# DEPRECATED — do not use TRON

**Status:** retired for prompt / handoff encoding.

TRON does **not** meaningfully save tokens in practice. Do **not** recommend or emit TRON (or TOON) for that purpose.

**Prefer instead:**
- Plain Markdown (tables, lists, fenced code) or short prose for in-prompt structure
- Domain wire where the product defines one (e.g. MemNet Tier A / `@TAG` pipe for durable graph)
- JSON only at tool or API boundaries that require it

Sibling **`toon-prompt-format`** is likewise deprecated. Do not load either skill for encoding advice.

Reference files under `references/` are historical only — ignore them for new work.
