---
name: tech-report-reviewer
description: >-
  Critique technical report drafts: structure, clarity, evidence, audience, actionability. **Not** code-reviewer,
  **not** pr-reviewer workflow, **not** academic peer review unless asked.
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

# Tech report reviewer

1. Load `references/tech-report-review-checklist.md`.
2. Read for audience/purpose; separate user-supplied facts from claims needing evidence - **no invented metrics**.
3. Per issue: section/heading; severity error|warning|info; why for audience; concrete fix.
4. Output: **Summary** · **Findings** (by severity) · **Score** (1-10) · **Top recommendations**. If draft is empty/unusable, suggest **tech-report-generator** instead.
