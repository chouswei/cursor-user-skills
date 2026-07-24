# Stub: generator SKILL.md (fill placeholders)

```yaml
---
name: <skill-name>
description: >-
  <Third-person. Use when user asks to create/draft/generate <artifact>. Triggers: ...>
metadata:
  pattern: generator
  output-format: markdown
---
```

Body template:

1. Load `references/<style-guide>.md` for tone and rules.
2. Load `assets/<output-template>.md` for required structure.
3. Gather missing variables from user (list what you need).
4. Fill template; every section must appear in output.
5. Return only the completed artifact unless user asked for commentary.

Create matching `references/*.md` and `assets/*-template.md`.
