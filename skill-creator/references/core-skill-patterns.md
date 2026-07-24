# Core skill patterns (token-optimized)

## First principles (core doctrine)

- **Truth over Convention:** Start from what a skill must be to be useful and loadable in Google ADK, not from copying existing files.
- **Progressive Disclosure:** L1 = `description` (discovery); L2 = `SKILL.md` body; L3 = `references/` and `assets/`. Never dump L3 into L2.
- **Specificity Beats Generality:** `description` is the routing index — third person, concrete triggers. Vague descriptions fail.
- **Separation of Concerns:** Orchestration in `SKILL.md`; knowledge, checklists, templates in `references/` and `assets/`.
- **Self-Consistency:** A generated skill should be able to follow the same principles as skill-creator.
- **Feedback & Validation:** Run a quality checklist before delivering generated output.
- **Composition over Monoliths:** Pick one primary pattern; note secondary patterns in one line when mixed.

## Pattern: tool-wrapper

- Use when the agent needs expert conventions for one library, API, or tool.
- Mechanism: triggers in description, then load `references/` conventions, then apply when writing or reviewing.
- Typical dirs: `references/` (or minimal inline); optional `tools/*-principles-retriever.py` for token-efficient retrieval.

## Pattern: generator

- Use when output must match a fixed structure every time.
- Mechanism: `assets/` = template; `references/` = style/quality; gather inputs, fill, return one artifact.

## Pattern: reviewer

- Use when scoring or critiquing against a checklist with severity levels.
- Mechanism: load checklist from `references/`; apply protocol; output summary, findings, score, recommendations.

## Pattern: inversion

- Use when the agent must gather context before synthesis (interview first).
- Mechanism: phased questions with gates; only then load `assets/*-template.md` and fill.

## Pattern: pipeline

- Use when ordered steps with gates are required; skipping a step breaks correctness.
- Mechanism: `pipeline_steps` in frontmatter or body; optional principles retrieval step; `system_instruction` / `token_guardrails` for discipline.

## Pattern: hybrid pipeline (pipeline-in-pipeline / meta-orchestration)

- Use when the skill is still **primarily ordered steps** (`metadata.pattern: pipeline`) but **embeds** another pattern or **calls out** to other skills.
- Examples: (1) pipeline whose middle step says "run **reasoning-strategy-selector** then invoke returned `order`"; (2) pipeline ending with a **reviewer** pass; (3) pipeline that wraps a **generator** after a gated **inversion** intake.
- Mechanism: keep **one primary** `metadata.pattern` = `pipeline`; add **one line** in YAML or body, e.g. `secondary: "hybrid: routes via reasoning-strategy-selector; final reviewer step"` or document sub-steps in `pipeline_steps` explicitly.
- Scaffold: use **`assets/stub-hybrid-pipeline.md`** (not plain `stub-pipeline.md`) when the user asks for nested pipeline, meta-skill, orchestration across skills, or "pipeline that uses the selector."
- Anti-pattern: duplicating full `SKILL.md` bodies of other skills inside this skill — link paths and names only.

## Choosing the right pattern

- Fixed document structure every time -> **generator**
- Evaluate against a rubric or checklist -> **reviewer**
- Must ask questions before building -> **inversion**
- Strict multi-step workflow with checkpoints -> **pipeline**
- Ordered workflow that **routes to or chains other skills** -> **pipeline** + **stub-hybrid-pipeline** (hybrid / meta-orchestration)
- Library or API conventions only -> **tool-wrapper**
- Unsure or hybrid -> primary = strongest fit; note composition in one line (e.g. pipeline with final reviewer step; hybrid pipeline with selector step).

## Anti-patterns

- Wall of text in `SKILL.md` instead of `references/` or `assets/`.
- Generic description ("helps with docs") with no triggers.
- Duplicate repo-wide rules — link to project rules instead.
- Missing gates on inversion or pipeline steps.
- Mismatched `tool_spec["name"]` and SKILL text for retriever tools.
- Claiming two primary patterns in `metadata.pattern` instead of one primary + one-line secondary note.

## Retrieval seeds

skill, create skill, scaffold, SKILL.md, tool wrapper, generator, reviewer, inversion, pipeline, hybrid pipeline, nested pipeline, meta pipeline, orchestration, reasoning-strategy-selector, sub-skill, chain skills, ADK, SkillToolset, references, assets, progressive disclosure, pattern, checklist, template, conventions, skill.fish, skillfish, agentskills, publish skill, skillfish.json, team sync
