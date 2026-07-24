---
name: pr-reviewer
description: >-
  Pull request review: standards, breaking changes, migration, docs - **process/workflow**, not deep code
  smell audit alone. Triggers: PR review, merge readiness, breaking change, team standards.
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

# PR reviewer

1. Load `references/pr-review-checklist.md`.
2. Read PR description, diff, linked issues; understand scope.
3. For each issue: file/line; severity error|warning|info; why; fix.
4. Output: **Summary** · **Findings** (by severity) · **Score** (1-10) · **Recommendations** before merge.
