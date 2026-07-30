# Agent Rules and Skills (Master)

**Audience:** models (Cursor agents), not end-user docs.

**SSOT pointers (do not restate):**
- Procedure / routing: [workflow.mdc](~/.cursor/rules/workflow.mdc) (SKILL-GRAPH.md triggers; seed.wire `@SKL`)
- MemNet loop / serve-down Markdown / no TOON/TRON: [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc)
- Sub-agents / models: [sub-agent-policy.mdc](~/.cursor/rules/sub-agent-policy.mdc)
- Prompt authoring: [prompt-quality.mdc](~/.cursor/rules/prompt-quality.mdc)
- No secrets: [no-secrets.mdc](~/.cursor/rules/no-secrets.mdc)
- Store grammar: [memnet-format](memnet-format/SKILL.md) · tools: [mcp-memnet](mcp-memnet/SKILL.md)
- Open **`modelbasedPrj-*`**: use that repo's root `AGENTS.md` for SysML / PCBA

Prefer ASCII in skill/hub durable text (pack rule R16 in [LLM.md](LLM.md)).

---

## 1. Token Efficiency (MUST)

| Do | Why |
|----|-----|
| **Trigger-first routing** | Match phrase -> SKILL-GRAPH.md triggers; never browse skill folders |
| **Max 2 trigger passes** | Then ask user or open-repo `AGENTS.md` |
| **One specialist per turn** | Default; SysML stack per workflow |
| **Lazy-load references/assets** | Open only when a step needs them |
| **MCP over bulk file reads** | Cheaper than reading entire trees |
| **MemNet / Markdown handoff** | See memnet-goldfish-loop.mdc |
| **Subagents for exploration** | See sub-agent-policy.mdc |
| **No normative paste** | Cite paths; don't paste huge specs |


---

## 2. Skill Discovery by Trigger

### Primary Method: Trigger Matching

1. **Extract keywords** from user request
2. **Scan [SKILL-GRAPH.md](SKILL-GRAPH.md)** trigger table (max 2 passes)
3. **Open matched `<id>/SKILL.md`** and follow steps
4. **If still unclear** -> ask the user, or open-repo `AGENTS.md` / domain checklist

### Trigger Examples (User Pack; membership = skill-graph-seed.wire `@SKL`)

| Task | Triggers | Skill |
|------|----------|-------|
| Code review | code review, smell audit, refactor feedback | `code-reviewer` |
| Premortem | premortem, blind spots, failure modes | `risk-assessor` |
| Project plan | plan a project, I want to build, roadmap | `project-planner` |
| Decision analysis | multi-criteria, weighted scoring, MCDM | `mcdm-decider` |
| Academic report | thesis, lab report, IMRaD, lit review | `academic-report-generator` |
| Tech spec | RFC, design proposal, tech spec draft | `rfc-generator` |
| Generate Mermaid | create/edit Mermaid, fix diagram syntax | `mermaid` (then `mmdc` / `pretty-mermaid` / `mermaid-doc-readability` per its router table) |
| Markdown to HTML | markdown to html, mdtohtml, render html | `mdtohtml` |
| DigiKey search | digikey, MPN search, digikey pricing | `mcp-digikey` |
| Inventree stock | inventree, IPN, inventree part | `mcp-inventree` |
| File to Markdown | markitdown, pdf to md, docx to markdown | `mcp-markitdown` |
| Cursor rules | create rule, .mdc, alwaysApply, AGENTS.md, user/team rules | `rule-writer` |

**See:** [SKILL-GRAPH.md](SKILL-GRAPH.md) -> `skill-graph-seed.wire`. Normative route steps: [workflow.mdc](~/.cursor/rules/workflow.mdc).

---

## 3. General Workflow

Normative: [workflow.mdc](~/.cursor/rules/workflow.mdc). Memory: [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc).

Lessons: user corrections -> `tasks/lessons.md`. Touch only what the task needs.

---

## 4. MemNet / Markdown handoff (examples hub)

Normative tiers and loop: [workflow.mdc](~/.cursor/rules/workflow.mdc) §3 + [memnet-goldfish-loop.mdc](~/.cursor/rules/memnet-goldfish-loop.mdc). Store grammar: [memnet-format](memnet-format/SKILL.md). Do not use TOON/TRON stubs.

**SysML modeling:** [sysml-memnet-pipeline](sysml-memnet-documentation/references/sysml-memnet-pipeline.md) -- `s1:`...`s6:` step codes; do not log pipeline only in chat when MemNet is up.

### Example: Router output (shared dialect -- MemNet up)

```text
## Nodes
+ TSK [NEW] ; goal=Relay harness edit ; phase=route ; status=settled ; recycle=delete_on_settle
+ CLM [NEW] ; type=decision ; code=pick:sysml-modeling-workflow ; recycle=delete_on_settle
+ CLM [NEW] ; type=decision ; code=pick:sysml-memnet-documentation ; recycle=delete_on_settle

## Edges
+ E01 [NEW] --(led_to_success)--> [sysml-modeling-workflow] ; note=pass ; recycle=persistent
```

### Example: Router output (Markdown -- MemNet down)

| skill_id | domain | reason |
|----------|--------|--------|
| sysml-connections | sysml | User asks about rewiring parts |
| sysml-traceability | sysml | May need to verify satisfaction |
| ask-user | meta | If still unclear, ask or use repo AGENTS |

User-facing output stays Markdown. At tool boundaries, use JSON as required by the tool.

---

## 5. Skill Binding & Maintenance

| Rule | Detail |
|------|--------|
| **Entry file** | `<pack-root>/<id>/SKILL.md` -- follow frontmatter + numbered steps |
| **Pick by trigger** | SKILL-GRAPH.md (max 2 passes) |
| **Unclear route** | Ask user, or open-repo `AGENTS.md`; optional [reasoning-strategy-selector](reasoning-strategy-selector/SKILL.md) only for explicit multi-match |
| **New/audit skills** | [skill-creator](skill-creator/SKILL.md), [skill-reviewer](skill-reviewer/SKILL.md); **skillfish** (registry) |
| **Cursor rules** | [rule-writer](rule-writer/SKILL.md) -- Project/Team/AGENTS.md writable; User Rules = draft for user paste (Customize -> Rules); never `state.vscdb` / pack≠Settings |

**Version rule:** bump `metadata.version` in skill frontmatter before pushing pack changes to GitHub (skillfish consumers).

### ADK Compliance

- Canonical **patterns**: generator, reviewer, inversion, pipeline, tool-wrapper
- Hybrid skills declare **`metadata.secondary`**
- Folder structure matches skill ids in **`related_skills.txt`**

---

## 6. Cross-References

| Resource | Purpose |
|----------|---------|
| [SKILL-GRAPH.md](SKILL-GRAPH.md) | Wire hub -> `skill-graph-seed.wire` |
| [LLM.md](LLM.md) | Detailed skill discovery procedure |
| [reasoning-strategy-selector](reasoning-strategy-selector/SKILL.md) | Optional graph router (explicit multi-match only) |
| [memnet-format](memnet-format/SKILL.md) | Shared dialect |
| [mcp-memnet](mcp-memnet/SKILL.md) | MemNet MCP tools / pin map |
| [sysml-memnet-pipeline](sysml-memnet-documentation/references/sysml-memnet-pipeline.md) | Pipeline step atoms |
| [sysml-memnet-read-policy](sysml-memnet-documentation/references/sysml-memnet-read-policy.md) | Pin map vs narrow `.sysml` |
| `~/.cursor/rules/` (pack copies in `rules/`) | Always-on required: workflow, goldfish, sub-agent, prompt-quality, no-secrets |
| Open-repo **AGENTS.md** (`modelbasedPrj-*`) | SysML / PCBA when that system repo is open |

---

## Key Rule: Limited Iteration

Do not walk skill folders or `related_skills.txt` as a checklist. Match triggers (<=2 passes), open one skill, execute. Ask when routing stays ambiguous.
