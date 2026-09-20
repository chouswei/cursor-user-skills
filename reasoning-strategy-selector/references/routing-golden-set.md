# routing-golden-set — labelled intents for score_routing.py

Fields: `id`, `intent`, `expected_order`, `acceptable_alternatives` (slash-separated skill ids).

| id | intent | expected_order | acceptable_alternatives |
|----|--------|----------------|-------------------------|
| sysml_refactor | cross-file SysML refactor rename parts ports | sysml-refactorer | sysml-modeling-workflow / sysml-refactorer |
| sysml_new | scaffold new SysML v2 project folder config | sysml-new-project | sysml-new-project / sysml-modeling-workflow |
| sysmledge_loop | sysmledge STALE sysml propose gql_read rev_status | sysmledge-workflow | sysmledge-workflow / sysml-modeling-workflow |
| sysmledge_multitask | sysmledge cursor multitask tip!=face product MCP sysmledge | sysmledge-cursor-multitask | sysmledge-cursor-multitask / sysmledge-workflow / memnet-multitask |
| oosem_cycle | OOSEM object-oriented systems engineering scenario-driven MBSE | oosem-workflow | oosem-workflow / sysml-modeling-workflow |
| nested_parts | nested parts hierarchical structure modeling | sysml-nested-structure-modeling | sysml-nested-structure-modeling / sysml-modeling-workflow |
| stakeholder_uc | stakeholder use case mission objective | sysml-stakeholder-use-case | sysml-stakeholder-use-case / oosem-workflow |
| sysml_req_audit | audit requirements satisfy links traceability | sysml-requirements-audit | sysml-requirements-audit / sysml-traceability |
| reasoning_ambiguous | scientific method hypothesis experiment for design decision | scientific-method-first-principles | scientific-method-first-principles / empirical-paradox-synthesis / mcdm-decider |
| premortem | what would fail blind spots decision risks | decision-inverter | decision-inverter / risk-assessor / launch-readiness-assessor |
| code_review | review this code for quality smells | code-reviewer | code-reviewer / architecture-reviewer |
| pr_review | PR review merge readiness breaking change | pr-reviewer | pr-reviewer / code-reviewer |
| pcba_netlist | parse Eagle netlist extract signals | pcba-netlist-reader | pcba-netlist-reader / sysml-pcba-de-facto-alignment |
| mermaid_block | architecture block diagram from deploy model | mermaid | mermaid / sysml-view-doc-sync |
| report_gen | technical report white paper design doc | tech-report-generator | tech-report-generator / project-output-article |
| rfc_vs_adr | RFC design proposal tech spec | rfc-generator | rfc-generator / adr-generator |
| mcp_validate | validate sysml parse diagnostics | mcp-sysml-v2 | mcp-sysml-v2 |
| skill_creator | create new skill write SKILL.md | skill-creator | skill-creator / skill-reviewer |
| skill_graph_bind | skill graph repo seed relative skills | skill-graph-workflow | skill-graph-workflow / skill-creator |
| memnet_warm | memnet query warm goldfish loop design memory | sysml-memnet-documentation | sysml-memnet-documentation / mcp-memnet / memnet-format |
| pcba_review | PCBA design review power ground thermal | pcba-design-reviewer | pcba-design-reviewer / hardware-custom-pcba-workflow (deprecated stub -> pack hub) |
| mermaid_placement | interconnection mermaid placement memnet graph first | sysml-interconnection-mermaid | sysml-interconnection-mermaid / mermaid / sysml-memnet-documentation / sysml-view-doc-sync |
