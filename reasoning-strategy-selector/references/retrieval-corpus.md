# Retrieval corpus (strategy-retriever only)

Machine-ranked bullets for `tools/strategy-retriever.py`. Do not paste this file into the model; call the tool or CLI instead.

The retriever **skips** trailing keyword-seed lines (e.g. `Core method: …`, `Docs: …`) so short queries rank **skill-routing** bullets, not synonym lists.

## Bullets

- Use **mcdm-decider** when many criteria must be weighted, scored, or ranked.
- Use **optimization-planner** when maximizing/minimizing under explicit constraints.
- Use **control-theory-planner** for feedback, stability, regulation of dynamic systems.
- Use **none** when the task is trivial, fully specified, or purely mechanical.
- Use **scientific-method-first-principles** when you need the **full** scientific method (question → background → hypothesis → experiment → analyze → conclude → iterate) fused with **hard invariants** (SLOs, physics, safety) into one engineering design or decision.
- Use **empirical-paradox-synthesis** when **both poles of a tension are evidence- or constraint-backed** and you need a **checkable** both/and mechanism (phasing, scope, guardrails) in one pass.
- Use **security-reviewer** for security and compliance of code, design, or config.
- Use **risk-assessor** for risk lists, premortem, blind spots before a decision (general).
- Use **launch-readiness-assessor** for go-live / production readiness specifically.
- Use **pr-reviewer** for **pull request** process: standards, breaking changes, team norms.
- Use **code-reviewer** for **implementation** review: readability, smells, security in code (artifact-focused; not the same as PR workflow).
- Use **architecture-reviewer** for system design, diagrams, scalability and maintainability at architecture level.
- Use **tech-report-reviewer** for critiquing **technical reports** (structure, evidence, clarity, audience fit) - not code review or PR process.
- Use **decision-inverter** for structured premortem on a **named decision** (decision-inverter skill).
- Use **incentive-alignment-reviewer** for incentives, principal–agent, alignment problems.
- Use **academic-report-generator** for scholarly reports, IMRaD, thesis/lab sections, lit reviews.
- Use **adr-generator** for Architecture Decision Records.
- Use **rfc-generator** for RFCs and technical design proposals.
- Use **tech-report-generator** for technical / engineering reports: status, investigation summaries, evaluations, architecture snapshots, handoff docs (not RFC or academic paper).
- Use **commit-message-generator** for conventional commits from diffs or descriptions.
- Use **meeting-notes-generator** for minutes and structured meeting output.
- Use **project-planner** for roadmaps, milestones, work breakdown.
- Use **pandas-expert** for pandas-heavy data manipulation and vectorization.
- Use **engineering-practices-learner** to **capture, classify, label, relate** tried practices (taxonomy_path, tags, typed **relations** between ids, 1-hop retrieval expansion) in **JSON** internal steps.
- Use **skill-creator** to scaffold **new** skills, tool wrappers, pipelines, or hybrid meta-skills.
- Use **skillfish** for **skill.fish** / **skillfish** CLI workflows: `npx skillfish add`, registry search, `submit`, team **`skillfish.json`** (`bundle` / `install`). Not for drafting SKILL bodies - that is **skill-creator**.
- Use **skill-reviewer** to **audit** an Agent Skill folder (`SKILL.md`, refs, tools): discovery, safety, **skill.fish** readiness. Not **code-reviewer** (application code) or **pr-reviewer** (PR process).
- Use **`order: ["sysml-refactorer"]`** when ambiguity is **how to run a cross-file SysML refactor** (rename symbols, de facto port migration, `SharedConnections` + deploy + common lib together). Not for obvious single-deploy **connection** edits (**sysml-connections**) or a **single** generator task (**sysml-requirements-generator**, …).
- Use **`order: []`** when the user's question is **only** which **sysml-*** specialist **other than refactor orchestration**, **mcp-*** wrapper, **mermaid**, or **mmdc** — use **Next action:** **[SKILL-GRAPH.md](../SKILL-GRAPH.md)** and **[LLM.md](../LLM.md)**; do **not** place `mcp-*` / `sysml-*` / `mermaid` / `mmdc` in `order` **except** **`sysml-refactorer`**.
- Correct routing needs **small** context: one retrieval pass, short `order`, concise template.
- Prefer `tools/strategy-retriever.py` over loading this whole file into the model.
- Query: objective + a few keywords; do not paste the full user message.
- `rationale`: ≤ 4 terse bullets. Final template: phrases only; no user-query echo.
- Scan assumptions, polarities, and failure/blind-spot signals before choosing.
- High stakes or fragile plan → consider **decision-inverter** or **risk-assessor** early.
- **empirical-paradox-synthesis** after **scientific-method-first-principles** if evidenced tension remains after fusion.
- **Meta / hybrid authoring:** `order: ["skill-creator"]`; in **Next action**, tell the main agent to re-match SKILL-GRAPH triggers when sub-skills to embed are unclear. Do **not** put `reasoning-strategy-selector` inside `order` (no self-loop).
- Core method: hypothesis, experiment, falsify, SLO, invariant, measured, evidence, mechanism.
- Inversion / risk: premortem, failure, blind, rollout, safety, disaster, second-order.
- Docs: report, RFC, ADR, IMRaD, minutes, commit.
- Review: code review, PR, architecture, security, incentives.
- Meta: skill.md, skillfish, scaffold skill.
- SysML refactor: rename, SharedConnections, cross-file.
