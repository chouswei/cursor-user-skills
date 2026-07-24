---
name: security-reviewer
description: >-
  Security and compliance review for code, design, or config. Triggers: security audit, vulnerability,
  OWASP, compliance check, threat review.
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

# Security reviewer

1. Load `references/security-review-checklist.md`.
2. Understand artifact context before judging.
3. For each issue: location; severity error|warning|info; why it matters; remediation.
4. Output: **Summary** (posture, risk) · **Findings** (by severity) · **Score** (1-10) · **Recommendations**.
