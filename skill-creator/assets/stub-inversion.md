# Stub: inversion SKILL.md (fill placeholders)

```yaml
---
name: <skill-name>
description: >-
  <Third-person. Use when user wants <outcome> but context must be gathered first. Triggers: ...>
metadata:
  pattern: inversion
  interaction: multi-turn
---
```

Body template:

- **DO NOT** synthesize final output until all phases complete.

**Phase 1 —** (ask one question at a time; list ordered questions)

**Phase 2 —** (only after Phase 1 complete; constraints / technical)

**Phase 3 — Synthesis** (only after all answers)

1. Load `assets/<plan-or-output-template>.md`
2. Fill every section from gathered answers
3. Present and iterate until user confirms

Create `assets/<template>.md` with required sections.
