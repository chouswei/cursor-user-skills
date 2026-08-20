# Agent Rules and Skills (Master)

**Audience:** models (Cursor agents), not end-user docs.
**Pack root:** `~/.cursor/skills/` ([cursor-user-skills](https://github.com/chouswei/cursor-user-skills)).

## Where facts live

| Store | Owns |
|-------|------|
| **User Rules** (Cursor Settings; draft [user-rules-PASTE-INTO-UI.txt](~/.cursor/user-rules-PASTE-INTO-UI.txt)) | Global prefs, no secrets, Terminal (Windows), prompt disciplines, sub-agent policy + model table, Workflow, MemNet goldfish loop, MemNet under Multitask Mode. **SSOT -- do not restate here.** |
| **This file** | Pack hub: skill-graph routing, token tips, MemNet examples, skill binding, cross-refs |
| **Pack `rules/*.mdc`** | Optional always-on mirrors; User Rules win when both apply |
| **Open-repo `AGENTS.md`** (`modelbasedPrj-*`) | SysML / PCBA / part layout for that system |

Prefer ASCII in skill/hub durable text (pack rule R16 in [LLM.md](LLM.md)). Never write `state.vscdb`.

---

## 1. Token Efficiency (MUST)

| Do | Why |
|----|-----|
| **Trigger-first routing** | Match phrase -> [SKILL-GRAPH.md](SKILL-GRAPH.md); never browse skill folders |
| **Max 2 trigger passes** | Then ask user or open-repo `AGENTS.md` |
| **One specialist per turn** | Default; SysML stack per User Rules Workflow |
| **Lazy-load references/assets** | Open only when a step needs them |
| **MCP over bulk file reads** | Cheaper than reading entire trees |
| **No normative paste** | Cite paths; do not paste huge specs |

Sub-agents / MemNet handoff: follow **User Rules** (sub-agent policy; MemNet goldfish loop; MemNet under Multitask Mode when Multitask / Task workers are active).

---

## 2. Skill Discovery by Trigger

1. Extract keywords from the user request
2. Scan [SKILL-GRAPH.md](SKILL-GRAPH.md) trigger table (max 2 passes); [LLM.md](LLM.md) secondary
3. Open matched `<id>/SKILL.md` and follow steps
4. If still unclear -> ask the user, or open-repo `AGENTS.md` / domain checklist

### Trigger examples (membership = `skill-graph-seed.wire` `@SKL`)

| Task | Triggers | Skill |
|------|----------|-------|
| Code review | code review, smell audit, refactor feedback | `code-reviewer` |
| Premortem | premortem, blind spots, failure modes | `risk-assessor` |
| Project plan | plan a project, I want to build, roadmap | `project-planner` |
| Decision analysis | multi-criteria, weighted scoring, MCDM | `mcdm-decider` |
| Academic report | thesis, lab report, IMRaD, lit review | `academic-report-generator` |
| Tech spec | RFC, design proposal, tech spec draft | `rfc-generator` |
| Generate Mermaid | create/edit Mermaid, fix diagram syntax | `mermaid` (then `mmdc` / `pretty-mermaid` / `mermaid-doc-readability` per its router) |
| Markdown to HTML | markdown to html, mdtohtml, render html | `mdtohtml` |
| DigiKey search | digikey, MPN search, digikey pricing | `mcp-digikey` |
| Inventree stock | inventree, IPN, inventree part | `mcp-inventree` |
| File to Markdown | markitdown, pdf to md, docx to markdown | `mcp-markitdown` |
| Cursor rules | create rule, .mdc, alwaysApply, AGENTS.md, user/team rules | `rule-writer` |
| SysML + MemNet GQL | sysml gql, modeling pin_map, TSK_model GQL | `sysml-gql` |
| Use MemNet | use memnet, how to use memnet, memnet goldfish | `memnet-use` |

**See:** [SKILL-GRAPH.md](SKILL-GRAPH.md) -> `skill-graph-seed.wire`. Route steps: User Rules **Workflow**.

---

## 3. MemNet examples (pack-owned)

Normative loop and tiers: **User Rules** (Workflow + MemNet goldfish loop). Store grammar: [memnet-format](memnet-format/SKILL.md). Tools: [mcp-memnet](mcp-memnet/SKILL.md). Do not use TOON/TRON stubs.

**SysML modeling:** [sysml-memnet-pipeline](sysml-memnet-documentation/references/sysml-memnet-pipeline.md) -- `s1:`...`s6:` step codes; do not log pipeline only in chat when MemNet is up.

### Example: Router output (openCypher-shaped mutate -- MemNet up)

```cypher
CREATE (t:TSK {goal: 'Relay harness edit', phase: 'route', status: 'settled', recycle: 'delete_on_settle'})
CREATE (c1:CLM {type: 'decision', code: 'pick:sysml-modeling-workflow', recycle: 'delete_on_settle'})
CREATE (c2:CLM {type: 'decision', code: 'pick:sysml-memnet-documentation', recycle: 'delete_on_settle'})
CREATE (t)-[:LED_TO_SUCCESS {note: 'pass', recycle: 'persistent'}]->(:SKL {id: 'sysml-modeling-workflow'})
```

### Example: Router output (Markdown -- MemNet down)

| skill_id | domain | reason |
|----------|--------|--------|
| sysml-connections | sysml | User asks about rewiring parts |
| sysml-traceability | sysml | May need to verify satisfaction |
| ask-user | meta | If still unclear, ask or use repo AGENTS |

User-facing output stays Markdown. At tool boundaries, use JSON as required by the tool.

Lessons: user corrections -> `tasks/lessons.md`. Touch only what the task needs.

---

## 4. Skill Binding & Maintenance

| Rule | Detail |
|------|--------|
| **Entry file** | `<pack-root>/<id>/SKILL.md` -- follow frontmatter + numbered steps |
| **Pick by trigger** | SKILL-GRAPH.md (max 2 passes) |
| **Unclear route** | Ask user, or open-repo `AGENTS.md`; optional [reasoning-strategy-selector](reasoning-strategy-selector/SKILL.md) only for explicit multi-match |
| **New/audit skills** | [skill-creator](skill-creator/SKILL.md), [skill-reviewer](skill-reviewer/SKILL.md); **skillfish** (registry) |
| **Cursor rules** | [rule-writer](rule-writer/SKILL.md) -- Project/Team/AGENTS.md writable; User Rules = draft for user paste (Customize -> Rules); never `state.vscdb` / pack != Settings |

**Version rule:** bump `metadata.version` in skill frontmatter before pushing pack changes to GitHub (skillfish consumers).

### ADK Compliance

- Canonical **patterns**: generator, reviewer, inversion, pipeline, tool-wrapper
- Hybrid skills declare **`metadata.secondary`**
- Folder structure matches skill ids in **`related_skills.txt`**

---

## 5. Cross-References

| Resource | Purpose |
|----------|---------|
| [SKILL-GRAPH.md](SKILL-GRAPH.md) | Wire hub -> `skill-graph-seed.wire` |
| [LLM.md](LLM.md) | Detailed skill discovery / pack rules |
| [user-rules-PASTE-INTO-UI.txt](~/.cursor/user-rules-PASTE-INTO-UI.txt) | User Rules SSOT draft (prefs, secrets, terminal, sub-agent, workflow, goldfish, multitask MemNet) |
| [reasoning-strategy-selector](reasoning-strategy-selector/SKILL.md) | Optional graph router (explicit multi-match only) |
| [memnet-format](memnet-format/SKILL.md) | MemNet GQL wire / shaped pin_map |
| [mcp-memnet](mcp-memnet/SKILL.md) | MemNet MCP tools / pin map |
| [sysml-gql](sysml-gql/SKILL.md) | Thin SysML x MemNet GQL turn loop |
| [sysml-memnet-pipeline](sysml-memnet-documentation/references/sysml-memnet-pipeline.md) | Pipeline step atoms |
| [sysml-memnet-read-policy](sysml-memnet-documentation/references/sysml-memnet-read-policy.md) | Pin map vs narrow `.sysml` |
| Open-repo **AGENTS.md** (`modelbasedPrj-*`) | SysML / PCBA when that system repo is open |

---

## Key Rule: Limited Iteration

Do not walk skill folders or `related_skills.txt` as a checklist. Match triggers (<=2 passes), open one skill, execute. Ask when routing stays ambiguous.
