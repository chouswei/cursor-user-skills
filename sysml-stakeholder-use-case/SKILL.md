---
name: sysml-stakeholder-use-case
description: >-
  Scaffold lightweight stakeholder / goal / use-case style modeling in SysML v2 textual: stakeholder or actor
  part defs, goal or concern requirements, use case part defs with doc; link to system context in deploy.
  Triggers: stakeholder, actor, use case, user goal, mission objective, context diagram narrative in sysml.
metadata:
  pattern: generator
  output-format: sysml
  secondary: ask-first
  pairs_with: [mcp-sysml-v2, sysml-requirements-generator, sysml-view-doc-sync]
token_guardrails: |
  - Follow OMG SysML v2 textual syntax for any use case / objective constructs; validate with MCP.
  - Prefer project package; extend only if pattern repeats across projects.
  - Keep stubs minimal; user may map to full Requirements 2025 library later.
---

# SysML stakeholder & use case (textual)

**When:** Capture **who** cares, **what** they need, and **use cases** as explicit model elements (not only prose in **`doc`** on the system part).

## Pipeline

1. **Ask first** — Stakeholder names, primary **goals** (short), **use case** titles and actors (which stakeholder or external system).

2. **Package** — Usually **`deploy-<project>.sysml`** or dedicated **`requirements-`** / **`context-`** file; align with **`root-*.sysml`** imports (**sysml-root-config**).

3. **Generate** — Minimal patterns (adjust to validator):
   - **`part def`** or **`attribute def`** for stakeholder / actor roles with **`doc /* concern */`**
   - **`requirement def`** for goals if normative (**sysml-requirements-generator**)
   - **`part def <UseCaseName>`** with **`doc /* pre/post, actor, main success */`** for each use case
   - Optional **`part`** usages under a **system context** composite referencing stakeholders and use cases

4. **Trace** — **`doc`** cross-references or future **`satisfy`** when design implements a use case (**sysml-traceability**).

5. **Verify** — **SysML v2 MCP validate**; fix syntax per project KerML/SysML version.

6. **Docs** — Sync **`outputs/*.md`** context / use-case section (**sysml-view-doc-sync**).

**Note:** Exact **`use case`** keywords depend on SysML v2 library imports; if tooling rejects `use case def`, model as **`part def`** + **`requirement def`** until standard profile is wired.
