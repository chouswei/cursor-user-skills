# Stub: generic / fallback SKILL.md

Use when no single pattern fits cleanly. Prefer `metadata.pattern: tool-wrapper` with a thin SKILL that defers detail to `references/README.md` or `references/overview.md`.

```yaml
---
name: <skill-name>
description: >-
  <Third-person WHAT + WHEN — be as specific as possible.>
metadata:
  pattern: tool-wrapper
  domain: general
---
```

Body: Short role statement; load `references/overview.md` for full behavior; one or two steps only.

Create `references/overview.md` with real structure the agent should follow.
