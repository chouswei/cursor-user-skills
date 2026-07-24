---
name: commit-message-generator
description: >-
  Conventional commits from diff, staged changes, or description. Pipeline: clarify JSON, load style guide, draft
  message, rubric self-review, then plain-text output only. Triggers: commit message, conventional commit,
  changelog-style git message.
metadata:
  pattern: pipeline
  version: 2.0-commit-message
  domain: developer-tools

pipeline_steps:
  1. Clarify (JSON)
     - Emit: change_summary (string), breaking_change (bool), scope_guess (string or empty).
  2. Load references
     - Read references/commit-style-guide.md; apply types and length rules when drafting.
  3. Draft
     - Produce candidate `type(scope): subject` plus optional body per guide.
  4. Self-review
     - Apply references/commit-message-rubric.md; emit JSON: pass (bool), violations (string[]), revision_note (string). Max 1 revision of steps 3-4.
  5. Final output
     - **Plain text only** per assets/commit-output-contract.md: subject line, optional blank line and body. No markdown fences, no commentary.

system_instruction: |
  JSON for steps 1 and 4 only. Step 5 must be only the commit message text. Each JSON emit <= 400 tokens.

token_guardrails: |
  - response_format: json steps 1,4; step 5 = plain text message only per commit-output-contract.
---

# Commit message generator

**Role:** Conventional commits with a short quality gate.

Run **pipeline_steps**; step 4 before final.

**Resources:** [references/commit-style-guide.md](references/commit-style-guide.md) · [references/commit-message-rubric.md](references/commit-message-rubric.md) · [assets/commit-template.md](assets/commit-template.md) · [assets/commit-output-contract.md](assets/commit-output-contract.md)

**Pairing:** [code-reviewer](../code-reviewer/SKILL.md) for large change sets when scope unclear.
