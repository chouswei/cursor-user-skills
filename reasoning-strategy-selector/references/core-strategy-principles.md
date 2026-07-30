# Core strategy principles (generated fallback + audit view)

<!-- GENERATED: do not hand-edit; run bootstrap_skill_graph.py --regenerate-views -->

**Source:** [`skill-graph-seed.wire`](skill-graph-seed.wire). Regenerate: `python tools/bootstrap_skill_graph.py --regenerate-views`.

**Purpose:** Human audit view of `@SKL` node metadata from the skill graph. **Not used for routing.**

| Skill | Direction | Domain | Complexity | Stakes | Evidence | Tension |
|-------|-----------|--------|------------|--------|----------|---------|
| academic-report-generator | G | doc | medium | low | structural | low |
| adr-generator | G | doc | low | low | structural | low |
| api-client-pattern | G | user | medium | medium | structural | low |
| architecture-reviewer | R | user | high | high | structural | medium |
| code-reviewer | R | user | medium | medium | structural | low |
| commit-message-generator | G | doc | low | low | structural | low |
| control-theory-planner | P | user | high | high | conceptual | low |
| decision-inverter | R | user | high | high | conceptual | high |
| empirical-paradox-synthesis | P | user | high | high | measured | high |
| engineering-practices-learner | P | user | high | low | structural | low |
| file-operations | P | user | medium | medium | structural | low |
| fusion-electronics-fetch | T | pcba | medium | medium | structural | low |
| incentive-alignment-reviewer | R | user | high | high | conceptual | high |
| launch-readiness-assessor | R | user | medium | high | structural | low |
| llm-model-suggester | P | meta | medium | low | structural | low |
| markdown-preview-enhanced | G | user | medium | medium | structural | low |
| markdown-viewer-user-pack | T | user | medium | medium | structural | low |
| mcdm-decider | P | user | high | high | measured | medium |
| mcp-chrome-devtools | T | meta | medium | medium | structural | low |
| mcp-digikey | T | meta | medium | medium | structural | low |
| mcp-inventree | T | meta | medium | medium | structural | low |
| mcp-latex | T | meta | medium | medium | structural | low |
| mcp-markitdown | T | meta | medium | medium | structural | low |
| mcp-memnet | T | meta | medium | medium | structural | low |
| mcp-novel-writer | T | meta | medium | medium | structural | low |
| mcp-sysml-v2 | T | sysml-tool | medium | low | structural | low |
| mcp-sysmledgraph | T | sysml-tool | high | low | structural | low |
| md-to-tex | P | doc | medium | low | structural | low |
| mdtohtml | T | doc | low | low | structural | low |
| meeting-notes-generator | G | doc | low | low | structural | low |
| memnet-codebase-snap | P | user | medium | medium | structural | low |
| memnet-format | T | meta | medium | medium | structural | low |
| mermaid | G | doc | medium | low | structural | low |
| mermaid-doc-readability | P | user | medium | medium | structural | low |
| mmdc | T | doc | low | low | structural | low |
| optimization-planner | P | user | high | high | measured | low |
| pandas-expert | T | user | medium | low | structural | low |
| pcba-design-reviewer | R | pcba | high | high | structural | low |
| pcba-netlist-reader | T | pcba | medium | low | structural | low |
| polarfire-soc-setup | T | user | medium | medium | structural | low |
| pr-reviewer | R | user | medium | medium | structural | low |
| pretty-mermaid | T | user | medium | medium | structural | low |
| project-output-article | P | user | medium | medium | structural | low |
| project-planner | G | user | medium | high | structural | low |
| prompt-writing-discipline | P | doc | medium | medium | structural | low |
| rfc-generator | G | doc | medium | low | structural | low |
| risk-assessor | R | user | medium | high | measured | low |
| rule-writer | G | meta | medium | medium | structural | low |
| scientific-method-first-principles | P | user | high | high | measured | medium |
| security-reviewer | R | user | high | high | structural | low |
| skill-creator | G | meta | high | low | structural | low |
| skill-reviewer | R | meta | high | low | structural | low |
| skillfish | T | meta | low | low | structural | low |
| sysml-allocate-generator | G | sysml | medium | medium | structural | low |
| sysml-behaviour-generator | G | sysml | medium | medium | structural | low |
| sysml-common-file-scale | P | sysml | medium | medium | structural | low |
| sysml-common-lib-contribution | P | sysml | medium | medium | structural | low |
| sysml-common-library-naming | T | sysml | medium | medium | structural | low |
| sysml-connections | P | sysml | medium | medium | structural | low |
| sysml-eagle-netlist-bridge | G | sysml | medium | medium | structural | low |
| sysml-eagle-netlist-parser-tool | T | sysml | medium | medium | structural | low |
| sysml-hardware-part-generator | G | sysml | medium | medium | structural | low |
| sysml-import-order-helper | P | sysml | medium | medium | structural | low |
| sysml-interconnection-mermaid | P | sysml | medium | medium | structural | low |
| sysml-item-generator | G | sysml | medium | medium | structural | low |
| sysml-memnet-cache | T | sysml | medium | medium | structural | low |
| sysml-memnet-documentation | P | sysml | high | medium | structural | low |
| sysml-modeling-session-checklist | P | sysml | medium | medium | structural | low |
| sysml-modeling-workflow | P | sysml | high | medium | structural | low |
| sysml-nested-structure-modeling | P | sysml | medium | medium | structural | low |
| sysml-new-project | G | sysml | medium | medium | structural | low |
| sysml-part-reviewer | R | sysml | medium | medium | structural | low |
| sysml-pcba-de-facto-alignment | R | sysml | medium | medium | structural | low |
| sysml-physical-port-generator | G | sysml | medium | medium | structural | low |
| sysml-refactorer | P | sysml | high | high | structural | low |
| sysml-requirements-audit | P | sysml | medium | medium | structural | low |
| sysml-requirements-generator | G | sysml | medium | medium | structural | low |
| sysml-root-config | G | sysml | medium | medium | structural | low |
| sysml-signal-processing-pipeline | P | sysml | medium | medium | structural | low |
| sysml-software-part-generator | G | sysml | medium | medium | structural | low |
| sysml-software-port-generator | G | sysml | medium | medium | structural | low |
| sysml-stakeholder-use-case | G | sysml | medium | medium | structural | low |
| sysml-traceability | P | sysml | medium | medium | structural | low |
| sysml-v2-release-how-to-use | P | sysml | medium | medium | structural | low |
| sysml-v2-syntax-reference | T | sysml | medium | medium | structural | low |
| sysml-view-doc-sync | R | sysml | medium | medium | structural | low |
| system-design-report-generator | P | doc | medium | medium | structural | low |
| tech-report-generator | G | doc | medium | low | structural | low |
| tech-report-reviewer | R | doc | medium | low | structural | low |
| toon-prompt-format | T | doc | medium | low | structural | low |
| traceability-footprint-to-sysml | P | user | medium | medium | structural | low |
| tron-format | T | doc | medium | low | structural | low |
| vibe-repo-init | P | user | medium | medium | structural | low |
---

## Routing

Skill selection is **graph-only** (triggers + typed edges). See [`skill-graph.md`](skill-graph.md) and `route_graph()` in `tools/skill_graph_lib.py`.
