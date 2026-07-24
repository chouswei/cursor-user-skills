---
name: code-reviewer
description: >-
  Code quality, security, readability, maintainability, performance, and token-efficient
  context use on the **artifact** (not PR process). Triggers: code review, refactor feedback,
  smell audit, implementation review, verbose code, prompt bloat, redundant duplication.
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

# Code reviewer

1. Load `references/review-checklist.md` (dimensions: correctness, edge cases, style, performance, **token efficiency**; plus security, readability, testing).
2. Understand intent before critiquing.
3. For each issue: line/location; severity error|warning|info; **why** it matters; fix or **alternative** with snippet if useful. Follow checklist **How to provide feedback** (specific, explain why, suggest alternatives).
4. Output: **Summary** · **Findings** (by severity) · **Score** (1-10) · **Top 3 recommendations**.
