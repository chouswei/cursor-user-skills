---
name: meeting-notes-generator
description: >-
  Structured meeting notes from raw notes or transcript. Triggers: meeting notes, standup, retro, minutes, action items.
metadata:
  pattern: generator
  output-format: markdown
---

# Meeting notes generator

1. Load `references/meeting-notes-style-guide.md` and `assets/meeting-notes-template.md`.
2. If date, attendees, or topics missing, ask or infer from input.
3. Fill template; action items with owner/due when possible.
4. Return **only** the completed markdown document.
