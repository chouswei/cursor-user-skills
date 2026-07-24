# Agent Rules and Skills (Master)

**Audience:** This pack is read **by models** (Cursor agents), not as end-user documentation. **Tiered handoffs:** MemNet **shared dialect** (Write = display; **memnet-llm 0.3.1** -- pin map bare present; mutate `+`/`~`/`-`; `NEW` for creates) when MemNet is up; **plain Markdown** tables or short prose when MemNet is down -- [memnet-format](memnet-format/SKILL.md), [mcp-memnet](mcp-memnet/SKILL.md), [sysml-memnet-pipeline](sysml-memnet-documentation/references/sysml-memnet-pipeline.md). Do not use TOON/TRON. Prefer ASCII in skill/hub durable text (pack rule R16 in [LLM.md](LLM.md)).

**Single source of truth for general routing, workflow, token efficiency, and skill discovery.** For SysML / PCBA in the **system-models-and-architecture** workspace, use that repository's root **`AGENTS.md`** when that project is open (not a path under this pack).

---

## 1. Token Efficiency (MUST)

| Do | Why |
|----|-----|
| **Trigger-first routing** (primary) | Match user phrase to skill triggers in SKILL-GRAPH.md -- 3x faster than browsing |
| **Limited trigger table iteration** (max 2 passes) | Scan SKILL-GRAPH.md trigger table twice; never iterate `related_skills.txt` as checklist |
| **One specialist per turn** (default) | Cuts redundant context loading |
| **Lazy-load references/assets** | Open only when a step needs them; obey `token_guardrails` |
| **MCP tools over file reads** | sysml-v2-lsp-mcp, sysmledgraph-mcp cheaper than reading entire files |
| **Use MemNet shared dialect for durable steps** | When MemNet is up: pin map + mutate ([memnet-format](memnet-format/SKILL.md)); plain Markdown when down |
| **Plain Markdown when MemNet down** | Ephemeral in-prompt handoff (tables / short lists); JSON only at tool boundaries |
| **Subagents for exploration** | Broad repo search in parallel; short summaries. Normative: [sub-agent-policy](~/.cursor/rules/sub-agent-policy.mdc) (skill-routed; role->Grok/Gemini/Composer; no Composer FAST) |
| **No normative paste** | Cite resource paths, don't paste huge specs |

---

## 2. Skill Discovery by Trigger

### Primary Method: Trigger Matching

1. **Extract keywords** from user request (e.g., "add requirement" -> triggers: "requirement", "R1", "SHALL")
2. **Scan [SKILL-GRAPH.md](SKILL-GRAPH.md)** trigger table (max 2 passes)
3. **Open matched `<id>/SKILL.md`** and follow steps
4. **If still unclear** -> ask the user, or follow the open repo's `AGENTS.md` / domain checklist (do not default to the optional graph router)

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

**See:** [SKILL-GRAPH.md](SKILL-GRAPH.md) -> `skill-graph-seed.wire` for ids/triggers; [user-pack-skills-catalog.mdc](~/.cursor/rules/user-pack-skills-catalog.mdc) for routing MUST/MUSTNOT only.

---

## 3. General Workflow

### Plan
For 3+ steps, new project, or architecture decisions: write brief plan first. Include scope confirmation.

### Route by Trigger
1. Match user phrase to triggers in SKILL-GRAPH.md
2. **Limited iteration allowed**: max 2 scans of trigger table
3. Open matched skill's `SKILL.md`
4. **Never** iterate `related_skills.txt` as a checklist

### Execute
- One skill per turn (default)
- Follow skill's numbered steps
- **MemNet up:** **shared dialect** between steps -- [memnet-format](memnet-format/SKILL.md); SysML step codes in [sysml-memnet-pipeline](../sysml-memnet-documentation/references/sysml-memnet-pipeline.md)
- **MemNet down:** plain Markdown tables or short prose for in-prompt handoffs only

### Verify
- Run scripts or MCP tools
- Inspect outputs (code, docs, diagrams)
- **Proof** = commands executed + sane results

### Lessons
User corrections -> `tasks/lessons.md`. Skim when relevant to current task.

### Minimal Impact
- Touch only what the task needs
- Root cause fixes, not band-aids
- Prefer clear structure over hacks

---

## 4. MemNet shared dialect / Markdown for internal communication

### Tiered handoff

| Priority | When | Format |
|----------|------|--------|
| 1 | MemNet up; multi-step or durable | **Shared dialect** via `add`/`update` -- [memnet-format](memnet-format/SKILL.md) |
| 2 | MemNet down; same-turn scratch | **Plain Markdown** tables or short prose |
| 3 | Tool / MCP boundary | JSON envelope only |

Do **not** use TOON or TRON (deprecated stubs only: [toon-prompt-format](toon-prompt-format/SKILL.md), [tron-format](tron-format/SKILL.md)).

**SysML modeling:** [sysml-memnet-pipeline](../sysml-memnet-documentation/references/sysml-memnet-pipeline.md) -- `s1:`...`s6:` step codes; do not log pipeline only in chat when MemNet is up.

### When to use Markdown (MemNet down or ephemeral)

- **Same-turn scratch** when MemNet unavailable
- **Internal tables** in skills -- BOM rows, pin maps (may also mutate to the graph when MemNet returns)
- **Plan passing** to subagent when MemNet down

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

### Conversion Rule

User-facing output stays Markdown. At tool boundaries (CLI, API, file I/O), use JSON as required by the tool.

---

## 5. Skill Binding & Maintenance

### How to Use Skills

| Rule | Detail |
|------|--------|
| **Entry file** | `<pack-root>/<id>/SKILL.md` -- follow frontmatter + numbered steps |
| **Pick by trigger** | Match user phrase to triggers in SKILL-GRAPH.md (max 2 passes) |
| **Unclear route** | Ask user, or open-repo `AGENTS.md` / domain checklist; optional [reasoning-strategy-selector](reasoning-strategy-selector/SKILL.md) only for explicit multi-match routing |
| **New/audit skills** | [skill-creator](skill-creator/SKILL.md), [skill-reviewer](skill-reviewer/SKILL.md) (user pack), **skillfish** (registry) |

**Version rule for user pack:** always bump `metadata.version` in a skill's frontmatter if you will push changes to the GitHub repo that distributes the pack (ensures skillfish consumers detect updates).


### ADK Compliance

- All skills use canonical **patterns**: generator, reviewer, inversion, pipeline, tool-wrapper
- Hybrid skills declare **`metadata.secondary`** (e.g., `pattern: pipeline`, `secondary: router`)
- Folder structure matches skill ids in **`related_skills.txt`**

---

## 6. Cross-References

| Resource | Purpose |
|----------|---------|
| [SKILL-GRAPH.md](SKILL-GRAPH.md) | Wire hub -> `skill-graph-seed.wire` (canonical skill graph) |
| [LLM.md](LLM.md) | Detailed skill discovery procedure |
| [reasoning-strategy-selector](reasoning-strategy-selector/SKILL.md) | Optional graph router (explicit multi-match only) |
| [memnet-format](memnet-format/SKILL.md) | Shared dialect |
| [mcp-memnet](mcp-memnet/SKILL.md) | MemNet MCP tools / pin map |
| [toon-prompt-format](toon-prompt-format/SKILL.md) | Deprecated notice only -- do not use for encoding |
| [tron-format](tron-format/SKILL.md) | Deprecated notice only -- do not use for encoding |
| [sysml-memnet-pipeline](sysml-memnet-documentation/references/sysml-memnet-pipeline.md) | Pipeline step atoms (`s1:`...`s6:`, G/M, route) |
| [sysml-memnet-read-policy](sysml-memnet-documentation/references/sysml-memnet-read-policy.md) | When to read pin map vs narrow `.sysml` |
| `.cursor/rules/` | Always-on: workflow, goldfish, slim catalog, confirm-build, no-secrets, prompt-quality. On-demand: terminal-windows |
| Repo **AGENTS.md** (system-models-and-architecture root) | SysML / PCBA workflow when that repo is open |

---

## Key Rule: Limited Iteration

Do not exhaustively walk skill folders or `related_skills.txt`. Match triggers (<=2 passes), open one skill, execute. Ask the user when routing stays ambiguous.
