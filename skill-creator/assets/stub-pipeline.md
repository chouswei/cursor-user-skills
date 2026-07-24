# Stub: pipeline SKILL.md (fill placeholders)

**Hybrid / meta-orchestration** (pipeline that routes to other skills or embeds selector): use **`stub-hybrid-pipeline.md`** instead of this file.

```yaml
---
name: <skill-name>
description: >-
  <Third-person WHAT + WHEN. Triggers: ...>
metadata:
  pattern: pipeline
  version: 1.0-<slug>
  domain: <domain>
pattern: pipeline
version: 1.0-<slug>

pipeline_steps:
  1. <Step title>
     - <JSON or instruction for this step>
  2. Principles Retrieval (optional)
     - Call Tool Wrapper: <retriever-name> with query from step 1.
  3. <Core step>
  4. Self-Review & Iterate
     - Internal check; max 1 revision.
  5. Final Output
     - Strict template from assets/<output-template>.md

system_instruction: |
  Concise mode. JSON for internal steps if used. Intermediate steps ≤ 400 tokens. Final output matches assets/<output-template>.md exactly.

token_guardrails: |
  - Prefer loading references/<core-principles>.md once per run; minimal quoted excerpts.
  - response_format: json for internal steps when specified
---
```

Body: **Role**, **Execution contract**, **Resources** (links), **Step 2 — Tool** if retriever exists, **Pairing** optional.

Create `references/core-<domain>-principles.md`, `assets/<output-template>.md`, optional `tools/<name>-principles-retriever.py` with `tool_spec`.
