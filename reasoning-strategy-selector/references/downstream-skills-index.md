# Downstream skills index (L3)

**Graph routing:** full corpus in [`skill-graph-seed.wire`](skill-graph-seed.wire). Schema: [`skill-graph.md`](skill-graph.md).

**Router subset:** `metadata.related_skills` in [`../SKILL.md`](../SKILL.md) — disambiguation among method/doc/meta skills. SysML/MCP/Mermaid skills routable via graph even when outside `related_skills`.

| id | Use when (short) |
|----|------------------|
| academic-report-generator | Academic / IMRaD / thesis / lit review drafts |
| adr-generator | Architecture Decision Records |
| architecture-reviewer | System design, diagrams, scalability / maintainability |
| code-reviewer | Implementation code quality (not PR process only) |
| commit-message-generator | Conventional commits from diff / description |
| control-theory-planner | Feedback loops, stability, regulation |
| decision-inverter | Structured premortem on a decision |
| scientific-method-first-principles | Full scientific method + bedrock invariants fused |
| empirical-paradox-synthesis | Evidenced poles; both/and with checkable mechanism |
| engineering-practices-learner | Practices + taxonomy/labels + typed relations; JSON pipeline |
| incentive-alignment-reviewer | Incentives, principal-agent, alignment |
| launch-readiness-assessor | Go-live readiness, pre-launch risk |
| mcdm-decider | Multi-criteria ranking / tradeoffs |
| meeting-notes-generator | Minutes, structured meeting output |
| optimization-planner | Constrained optimization, objectives |
| pandas-expert | Pandas / vectorized data work |
| pr-reviewer | PR standards, breaking changes, process |
| project-planner | Roadmap, milestones, WBS |
| risk-assessor | Risk assessment, premortem (non-launch) |
| rfc-generator | RFC / design proposal docs |
| security-reviewer | Security, compliance review |
| tech-report-generator | Tech / engineering reports, status, investigations, handoffs |
| tech-report-reviewer | Review / critique technical reports before distribution |
| skill-creator | Scaffold new skills / hybrid pipelines |
| skillfish | skill.fish registry: install, search, submit, bundle/install manifest |
| skill-reviewer | Audit SKILL.md packages; structure, safety, publish readiness |
| sysml-new-project | Scaffold new SysML v2 project |
| sysml-refactorer | Cross-file SysML v2 refactors: renames, lib + deploy + `SharedConnections` |

Audit view (not routing): [core-strategy-principles.md](core-strategy-principles.md) (generated from seed).

**Fast-path:** [SKILL-GRAPH.md](../../SKILL-GRAPH.md) trigger table (generated). **Benchmark:** `python tools/score_routing.py`.
