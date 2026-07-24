# Stub: tool-wrapper SKILL.md (fill placeholders)

```yaml
---
name: <skill-name>
description: >-
  <Third-person WHAT + WHEN. Concrete triggers: product names, verbs, file types.>
metadata:
  pattern: tool-wrapper
  domain: <domain>
---
```

Body template (keep short; detail in references):

- You are an expert in `<domain>`. Apply conventions from the user's task.
- Load `references/<conventions-or-core-principles>.md` for full rules.
- **When reviewing:** load reference, check each rule, cite rule + fix.
- **When writing:** load reference, follow every convention.

Optional: add `tools/<name>-principles-retriever.py` and a "Step — Principles retrieval" that calls Tool Wrapper + ADK `tool_spec` name `<name>-principles-retriever`.

Also create `references/<file>.md` with bullet conventions + **Retrieval seeds** line at end.
