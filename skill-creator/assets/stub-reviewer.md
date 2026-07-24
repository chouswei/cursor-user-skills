# Stub: reviewer SKILL.md (fill placeholders)

```yaml
---
name: <skill-name>
description: >-
  <Third-person. Use when reviewing <subject> for <criteria>. Triggers: ...>
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---
```

Body template:

1. Load `references/<review-checklist>.md` for criteria.
2. Understand the artifact before critiquing.
3. Apply each rule; for each issue: location, severity (error/warning/info), why, suggested fix.
4. Output: **Summary**, **Findings** by severity, **Score** (1–10), **Recommendations**.

Create `references/<review-checklist>.md` with checkable items by category.
